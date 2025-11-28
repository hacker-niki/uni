from fastapi import FastAPI, Depends, HTTPException, UploadFile, File
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
from pydantic import BaseModel
from typing import List, Optional
import httpx
import json
import re
from database import init_db, get_session, Question

app = FastAPI(title="Dataset Generator")

# Создаем директорию для статических файлов
import os
os.makedirs("static", exist_ok=True)

app.mount("/static", StaticFiles(directory="static"), name="static")


class AnswerModel(BaseModel):
    text: str
    is_correct: bool


class QuestionModel(BaseModel):
    question: str
    answers: List[AnswerModel]


class GenerateRequest(BaseModel):
    text: str


class ApproveRequest(BaseModel):
    question_ids: List[int]


def clean_text(text: str) -> str:
    """
    Очищает текст от нестандартных символов, оставляя только:
    - буквы (латиница и кириллица)
    - цифры
    - основные знаки препинания
    - пробелы и переносы строк

    Args:
        text: Исходный текст

    Returns:
        Очищенный текст
    """
    # Оставляем только разрешенные символы:
    # - буквы любых алфавитов (Unicode \w)
    # - цифры
    # - пробелы, переносы строк, табуляцию
    # - основные знаки препинания: . , ! ? ; : - ( ) " ' « »
    cleaned = re.sub(r'[^\w\s.,!?;:\-()"\'\«\»\n\r\t]', '', text)

    # Удаляем множественные пробелы
    cleaned = re.sub(r'[ \t]+', ' ', cleaned)

    # Удаляем множественные переносы строк (больше 2 подряд)
    cleaned = re.sub(r'\n{3,}', '\n\n', cleaned)

    return cleaned.strip()


def split_text_into_chunks(text: str, paragraphs_per_chunk: int = 2, min_words: int = 100) -> List[str]:
    """
    Разбивает текст на чанки по N абзацев с минимальным количеством слов.

    Args:
        text: Исходный текст
        paragraphs_per_chunk: Количество абзацев в одном чанке (по умолчанию 2-3)
        min_words: Минимальное количество слов в чанке (по умолчанию 100)

    Returns:
        Список чанков текста
    """
    # Разбиваем текст на абзацы (по двойным переносам строки или одиночным)
    paragraphs = re.split(r'\n\s*\n|\n', text)

    # Удаляем пустые абзацы
    paragraphs = [p.strip() for p in paragraphs if p.strip()]

    if not paragraphs:
        return []

    # Группируем абзацы в чанки с проверкой минимального количества слов
    chunks = []
    i = 0
    while i < len(paragraphs):
        chunk_paragraphs = []
        word_count = 0

        # Собираем абзацы для чанка
        while i < len(paragraphs):
            paragraph = paragraphs[i]
            paragraph_words = len(paragraph.split())

            chunk_paragraphs.append(paragraph)
            word_count += paragraph_words
            i += 1

            # Проверяем условия для завершения чанка
            # 1. Достигли минимального количества слов
            if word_count >= min_words:
                # Если уже набрали нужное количество абзацев или больше, завершаем чанк
                if len(chunk_paragraphs) >= paragraphs_per_chunk:
                    break
                # Если абзацев меньше, но следующий абзац сделает чанк слишком большим, завершаем
                if i < len(paragraphs):
                    next_paragraph_words = len(paragraphs[i].split())
                    # Если следующий абзац добавит больше 100 слов, завершаем текущий чанк
                    if word_count + next_paragraph_words > min_words * 2:
                        break

            # Если это последний абзац, завершаем чанк в любом случае
            if i >= len(paragraphs):
                break

        if chunk_paragraphs:
            chunk_text = '\n\n'.join(chunk_paragraphs)
            chunks.append(chunk_text)

    return chunks


@app.on_event("startup")
async def startup():
    await init_db()


@app.get("/")
async def read_root():
    return FileResponse("static/index.html")


@app.post("/api/generate")
async def generate_questions(
    request: GenerateRequest,
    session: AsyncSession = Depends(get_session)
):
    """Генерирует вопросы через Ollama и сохраняет в БД"""
    try:
        # Очищаем текст от нестандартных символов
        cleaned_text = clean_text(request.text)

        if not cleaned_text or len(cleaned_text.strip()) < 10:
            raise HTTPException(status_code=400, detail="Text is too short or empty after cleaning")

        # Разбиваем текст на чанки по 2-3 абзаца
        chunks = split_text_into_chunks(cleaned_text, paragraphs_per_chunk=2)

        if not chunks:
            raise HTTPException(status_code=400, detail="Could not create chunks from text. Text might be too short.")

        all_saved_questions = []
        successful_chunks = 0
        failed_chunks = 0

        # Обрабатываем каждый чанк отдельно
        # Увеличенный таймаут для обработки больших чанков текста
        async with httpx.AsyncClient(timeout=800.0) as client:
            for chunk_idx, chunk in enumerate(chunks):
                try:
                    # Отправляем запрос в Ollama для каждого чанка
                    ollama_response = await client.post(
                        "http://localhost:11434/api/generate",
                        json={
                            "model": "dataset-generator",
                            "prompt": chunk,
                            "stream": False
                        }
                    )

                    if ollama_response.status_code != 200:
                        error_detail = ""
                        try:
                            error_data = ollama_response.json()
                            error_detail = error_data.get("error", "")
                        except:
                            pass

                        print(f"Чанк {chunk_idx + 1}: Ошибка Ollama (статус {ollama_response.status_code}) {error_detail}, пропускаем")
                        failed_chunks += 1
                        continue  # Пропускаем чанк если ошибка, но продолжаем обработку других

                    # Парсим ответ
                    response_data = ollama_response.json()
                    generated_text = response_data.get("response", "")

                    # Пытаемся извлечь JSON из ответа
                    # Ищем JSON между фигурными скобками
                    start_idx = generated_text.find("{")
                    end_idx = generated_text.rfind("}") + 1

                    if start_idx == -1 or end_idx == 0:
                        print(f"Чанк {chunk_idx + 1}: Невалидный JSON, пропускаем")
                        failed_chunks += 1
                        continue  # Пропускаем чанк если невалидный JSON

                    try:
                        json_str = generated_text[start_idx:end_idx]
                        questions_data = json.loads(json_str)
                    except json.JSONDecodeError as e:
                        print(f"Чанк {chunk_idx + 1}: Ошибка парсинга JSON ({str(e)}), пропускаем")
                        failed_chunks += 1
                        continue  # Пропускаем чанк если ошибка парсинга

                    # Сохраняем вопросы в БД
                    for q_data in questions_data.get("questions", []):
                        try:
                            # Находим правильный ответ
                            correct_idx = 0
                            answers_list = []
                            for idx, answer in enumerate(q_data.get("answers", [])):
                                answers_list.append(answer["text"])
                                if answer.get("is_correct", False):
                                    correct_idx = idx + 1

                            # Дополняем до 5 ответов если нужно
                            while len(answers_list) < 5:
                                answers_list.append("")

                            question = Question(
                                question_text=q_data.get("question", ""),
                                answer_1=answers_list[0],
                                answer_2=answers_list[1],
                                answer_3=answers_list[2],
                                answer_4=answers_list[3],
                                answer_5=answers_list[4],
                                correct_answer_index=correct_idx,
                                is_approved=False,
                                source_text=chunk[:500]  # Сохраняем первые 500 символов чанка
                            )
                            session.add(question)
                            await session.flush()
                            all_saved_questions.append({
                                "id": question.id,
                                "question": question.question_text,
                                "answers": [
                                    {"text": question.answer_1, "is_correct": correct_idx == 1},
                                    {"text": question.answer_2, "is_correct": correct_idx == 2},
                                    {"text": question.answer_3, "is_correct": correct_idx == 3},
                                    {"text": question.answer_4, "is_correct": correct_idx == 4},
                                    {"text": question.answer_5, "is_correct": correct_idx == 5},
                                ],
                                "chunk_index": chunk_idx
                            })
                        except Exception as e:
                            print(f"Чанк {chunk_idx + 1}: Ошибка сохранения вопроса ({str(e)}), пропускаем вопрос")
                            continue

                    # Если дошли до сюда и добавили хотя бы один вопрос, чанк успешен
                    if questions_data.get("questions"):
                        successful_chunks += 1
                    else:
                        failed_chunks += 1

                except httpx.TimeoutException:
                    print(f"Чанк {chunk_idx + 1}: Таймаут запроса, пропускаем")
                    failed_chunks += 1
                    continue
                except httpx.RequestError as e:
                    print(f"Чанк {chunk_idx + 1}: Ошибка сети ({str(e)}), пропускаем")
                    failed_chunks += 1
                    continue
                except Exception as e:
                    print(f"Чанк {chunk_idx + 1}: Неожиданная ошибка ({str(e)}), пропускаем")
                    failed_chunks += 1
                    continue

            await session.commit()

            if not all_saved_questions:
                raise HTTPException(
                    status_code=500,
                    detail=f"Failed to generate questions from {len(chunks)} chunks. Check if Ollama service is running and model is loaded."
                )

            return {
                "questions": all_saved_questions,
                "chunks_processed": len(chunks),
                "successful_chunks": successful_chunks,
                "failed_chunks": failed_chunks,
                "total_questions": len(all_saved_questions)
            }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Generation error: {str(e)}")


@app.get("/api/questions")
async def get_questions(
    approved_only: bool = False,
    session: AsyncSession = Depends(get_session)
):
    """Получает все вопросы из БД"""
    if approved_only:
        stmt = select(Question).where(Question.is_approved == True)
    else:
        stmt = select(Question).where(Question.is_approved == False)

    result = await session.execute(stmt)
    questions = result.scalars().all()

    questions_list = []
    for q in questions:
        questions_list.append({
            "id": q.id,
            "question": q.question_text,
            "answers": [
                {"text": q.answer_1, "is_correct": q.correct_answer_index == 1},
                {"text": q.answer_2, "is_correct": q.correct_answer_index == 2},
                {"text": q.answer_3, "is_correct": q.correct_answer_index == 3},
                {"text": q.answer_4, "is_correct": q.correct_answer_index == 4},
                {"text": q.answer_5, "is_correct": q.correct_answer_index == 5},
            ],
            "is_approved": q.is_approved
        })

    return {"questions": questions_list}


@app.post("/api/approve")
async def approve_questions(
    request: ApproveRequest,
    session: AsyncSession = Depends(get_session)
):
    """Аппрувит выбранные вопросы"""
    stmt = select(Question).where(Question.id.in_(request.question_ids))
    result = await session.execute(stmt)
    questions = result.scalars().all()

    for question in questions:
        question.is_approved = True

    await session.commit()

    return {"status": "success", "approved_count": len(questions)}


@app.delete("/api/questions/{question_id}")
async def delete_question(
    question_id: int,
    session: AsyncSession = Depends(get_session)
):
    """Удаляет вопрос"""
    stmt = select(Question).where(Question.id == question_id)
    result = await session.execute(stmt)
    question = result.scalar_one_or_none()

    if not question:
        raise HTTPException(status_code=404, detail="Question not found")

    await session.delete(question)
    await session.commit()

    return {"status": "success"}


@app.get("/api/export")
async def export_dataset(
    session: AsyncSession = Depends(get_session)
):
    """Экспортирует аппрувнутые вопросы в JSON формате"""
    stmt = select(Question).where(Question.is_approved == True)
    result = await session.execute(stmt)
    questions = result.scalars().all()

    dataset = []
    for q in questions:
        dataset.append({
            "question": q.question_text,
            "answers": [
                {"text": q.answer_1, "is_correct": q.correct_answer_index == 1},
                {"text": q.answer_2, "is_correct": q.correct_answer_index == 2},
                {"text": q.answer_3, "is_correct": q.correct_answer_index == 3},
                {"text": q.answer_4, "is_correct": q.correct_answer_index == 4},
                {"text": q.answer_5, "is_correct": q.correct_answer_index == 5},
            ]
        })

    return JSONResponse(
        content={"questions": dataset},
        headers={
            "Content-Disposition": "attachment; filename=dataset.json"
        }
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
