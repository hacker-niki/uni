import os
import json
import requests
from django.http import JsonResponse
from django.shortcuts import render
from django.conf import settings
from .forms import TextFileUploadForm
from .models import TextEntry, Question, Answer, TextChunk

import json

def split_text_into_chunks(text, chunk_size=1000):
    return [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]

def upload_file_and_display_questions(request):
    if request.method == 'POST':
        form = TextFileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            # Сохраните загруженный файл
            file = request.FILES['text_file']
            file_path = os.path.join(settings.MEDIA_ROOT, file.name)

            # Создайте директорию, если она не существует
            os.makedirs(settings.MEDIA_ROOT, exist_ok=True)

            with open(file_path, 'wb+') as destination:
                for chunk in file.chunks():
                    destination.write(chunk)

            # Чтение содержимого файла
            with open(file_path, 'r') as f:
                file_content = f.read()
            
            text_entry = TextEntry.objects.create(text=file_content)

            chunks = split_text_into_chunks(file_content)
            for index, chunk_text in enumerate(chunks):
                TextChunk.objects.create(
                    text_entry=text_entry,
                    chunk_text=chunk_text,
                    order=index
                )

            print('start processing...')
            for index, chunk in enumerate(text_entry.chunks.all().order_by('order')):
                print('chunk ', index)
                # Отправка содержимого файла в нейронную сеть
                ollama_url = os.environ.get('OLLAMA_URL', 'http://ollama:11434')
                ollama_response = requests.post(
                    f'{ollama_url}/api/generate',
                    json={
                        'model': 'question_processor',
                        'prompt': chunk.chunk_text,
                        'stream': False
                    }
                )

                print(json.loads(ollama_response.json().get('response')).get('questions', []))

                # Получение вопросов и ответов из ответа
                questions_data = json.loads(ollama_response.json().get('response')).get('questions', [])

                for question_data in questions_data:
                    question_text = question_data['question']
                    question = Question.objects.create(text_chunk=chunk, question_text=question_text)

                    # Сохранение ответов
                    for answer_data in question_data['answers']:
                        answer_text = answer_data['text']
                        is_correct = answer_data['is_correct']
                        Answer.objects.create(question=question, answer_text=answer_text, is_correct=is_correct)

    else:
        form = TextFileUploadForm()

    text_entries = TextEntry.objects.all() 

    return render(request, 'questions.html', {
        'form': form,
        'text_entries': text_entries
    })