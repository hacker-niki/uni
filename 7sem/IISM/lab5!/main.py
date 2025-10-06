import streamlit as st
import json
from collections import Counter, deque
import io # Для работы с загруженным файлом

# --- Функции логики Петри-сети (Оставлены почти без изменений) ---

def load_petri(uploaded_file):
    """
    Загружает и парсит данные Петри-сети из загруженного файла.
    Принимает объект file-like (результат st.file_uploader).
    """
    if uploaded_file is None:
        return None, None, None, None, None

    # Чтение содержимого файла и декодирование в строку
    string_data = uploaded_file.read().decode("utf-8")
    data = json.loads(string_data)

    places = []
    init_marking = {}
    for p in data["places"]:
        parts = p.split(",")
        name = parts[0]
        # Безопасное чтение токенов, если их нет, по умолчанию 0
        try:
            tokens = int(parts[3])
        except (IndexError, ValueError):
            tokens = 0
            
        places.append(name)
        init_marking[name] = tokens

    transitions = []
    for t in data["trans"]:
        name = t.split(",")[0]
        transitions.append(name)

    pre = {t: {} for t in transitions}
    post = {t: {} for t in transitions}
    for arc in data["arcs"]:
        s, d = arc.split(",")
        # Предполагаем вес дуги = 1, так как в исходном формате его нет
        if s in places and d in transitions:
            pre[d][s] = pre[d].get(s, 0) + 1
        elif s in transitions and d in places:
            post[s][d] = post[s].get(d, 0) + 1

    return places, transitions, pre, post, init_marking


def enabled(t, marking, pre):
    for p, w in pre[t].items():
        if marking.get(p, 0) < w:
            return False
    return True


def fire(t, marking, pre, post):
    new = Counter(marking)
    for p, w in pre[t].items():
        new[p] -= w
    for p, w in post[t].items():
        new[p] += w
    return dict(new)


def build_diagram(places, transitions, pre, post, init):
    start = tuple(init.get(p, 0) for p in places)
    q = deque([start])
    seen = {start: None}
    edges = []

    # Устанавливаем разумный предел для предотвращения бесконечного цикла
    max_markings = 1000 
    
    while q and len(seen) < max_markings:
        mtuple = q.popleft()
        marking = {p: mtuple[i] for i, p in enumerate(places)}
        for t in transitions:
            if enabled(t, marking, pre):
                new_mark = fire(t, marking, pre, post)
                m2 = tuple(new_mark.get(p, 0) for p in places)
                edges.append((mtuple, t, m2))
                if m2 not in seen:
                    seen[m2] = (mtuple, t)
                    q.append(m2)
    
    if len(seen) >= max_markings:
        st.warning(f"Построение графа достижимости остановлено, достигнут предел в {max_markings} маркировок.")

    return list(seen.keys()), edges


def export_to_dot(places, markings, edges):
    """
    Генерирует строку в формате DOT для визуализации графа.
    """
    def fmt(mtuple):
        # Преобразование кортежа обратно в читаемую строку маркировки
        return "[" + ",".join(f"{mtuple[i]}" for i, p in enumerate(places)) + "]"

    dot_content = "digraph Diagram {\n"
    dot_content += "rankdir=TB;\n"
    
    # Определение меток узлов
    for i, m in enumerate(markings):
        # Используем индекс i как уникальный идентификатор узла в DOT
        # а m (кортеж маркировки) как метку
        dot_content += f"  m{i} [label=\"{fmt(m)}\"];\n"

    # Создание словаря для быстрого поиска индекса (ID узла) по кортежу маркировки
    marking_to_id = {m: f"m{i}" for i, m in enumerate(markings)}
    
    # Определение ребер
    for m1, t, m2 in edges:
        id1 = marking_to_id.get(m1, str(m1))
        id2 = marking_to_id.get(m2, str(m2))
        dot_content += f"  {id1} -> {id2} [label=\"{t}\"];\n"
        
    dot_content += "}\n"
    
    return dot_content


# --- Streamlit UI ---

def main():
    st.title("Анализатор сетей Петри (Streamlit)")

    # Инициализация состояния сессии
    if 'places' not in st.session_state:
        st.session_state.places = []
        st.session_state.markings = []
        st.session_state.dot_content = ""

    # Справка по классам сетей Петри (скрыта в Expander)
    intro_text = """
        **Классы сетей Петри:**
        - **Автоматные сети** — сети, в которых переход имеет не более одного входа и не более одного выхода.
        - **Маркированные сети** — сети, в которых каждая позиция имеет не более одного входа и не более одного выхода.
        - **Сети свободного выбора** — сети, в которых каждая дуга, выходящая из позиции, является либо единственным выходом из нее, либо единственным входом в переход.
        - **Простые сети** — сети, в которых каждый переход может иметь не более одной общей позиции с другими переходами.

        **Пример (из исходного Tkinter кода):**
        * **Первая сеть:** Срабатывание нескольких переходов возможно (Например a, b).
          * **Классификация по динамическим ограничениям:** безопасная (1-ограниченная), 1-консарвативная (кол-во маркеров постоянно), живая, неустойчивая.
          * **Классификация по статическим ограничениям:** Сеть свободного выбора.
        * **Вторая сеть:** Срабатывание нескольких переходов возможно (Например t2, t3).
          * **Классификация по динамическим ограничениям:** ограниченная (2-ограниченная), консарвативная (кол-во маркеров никогда не превышает 4), живая, устойчивая.
          * **Классификация по статическим ограничениям:** Маркированная сеть.
    """
    with st.expander("Справка по классам сетей Петри"):
        st.markdown(intro_text)

    # --- Ввод данных и построение ---
    st.header("1. Загрузка и анализ")

    uploaded_file = st.file_uploader(
        "Загрузите файл с описанием сети (.json)",
        type=["json", "txt"],
        help="Ожидается JSON-файл с полями 'places', 'trans', 'arcs', как в исходном коде."
    )

    col1, col2 = st.columns(2)

    with col1:
        # Кнопка для запуска построения
        if st.button("Построить диаграмму достижимости"):
            if uploaded_file is None:
                st.error("Пожалуйста, загрузите файл.")
            else:
                try:
                    # 1. Загрузка
                    places, transitions, pre, post, init = load_petri(uploaded_file)
                    st.session_state.places = places
                    
                    # 2. Построение
                    with st.spinner('Строю граф достижимости...'):
                        markings, edges = build_diagram(places, transitions, pre, post, init)
                        st.session_state.markings = markings
                        
                    # 3. Экспорт в DOT
                    dot_content = export_to_dot(places, markings, edges)
                    st.session_state.dot_content = dot_content
                    
                    st.success("Диаграмма достижимости успешно построена.")
                    st.info(f"Найдено маркировок: {len(markings)}. Переходов: {len(edges)}.")

                except Exception as e:
                    st.error(f"Ошибка при обработке файла: {e}")
                    st.session_state.places = []
                    st.session_state.markings = []
                    st.session_state.dot_content = ""

    # --- Скачивание DOT файла ---
    with col2:
        if st.session_state.dot_content:
            st.download_button(
                label="Скачать DOT-файл",
                data=st.session_state.dot_content,
                file_name="diagram.dot",
                mime="text/plain",
                help="Файл в формате Graphviz DOT для просмотра в онлайн-сервисах (например, GraphvizOnline)"
            )
            
    # --- Проверка достижимости ---
    st.header("2. Проверка достижимости")
    
    if st.session_state.places:
        place_names = ", ".join(st.session_state.places)
        st.caption(f"Позиции в сети: {place_names}")
        
        marking_placeholder = "Пример: " + ",".join(['0'] * len(st.session_state.places))
        text = st.text_input(
            "Введите маркировку для проверки (через запятую):", 
            key="marking_input",
            placeholder=marking_placeholder
        )

        if st.button("Проверить достижимость"):
            if not st.session_state.markings:
                st.warning("Сначала постройте диаграмму.")
                return

            try:
                # Преобразование введенной строки в кортеж чисел
                mtuple = tuple(int(x.strip()) for x in text.split(","))
                
                if len(mtuple) != len(st.session_state.places):
                    st.error(f"Количество значений в маркировке ({len(mtuple)}) не соответствует количеству позиций ({len(st.session_state.places)}).")
                elif mtuple in st.session_state.markings:
                    st.success(f"Маркировка **{mtuple}** достижима.")
                else:
                    st.info(f"Маркировка **{mtuple}** недостижима.")
            except ValueError:
                st.error("Введите маркировку через запятую, используя только целые числа (например, 0,1,0).")
                
    else:
        st.info("Пожалуйста, загрузите файл и постройте диаграмму, чтобы проверить достижимость.")


    # --- Визуализация ---
    st.header("3. Визуализация графа (Graphviz)")
    
    if st.session_state.dot_content:
        # Streamlit имеет встроенную поддержку Graphviz,
        # что позволяет отобразить граф прямо в приложении.
        try:
            st.graphviz_chart(st.session_state.dot_content)
        except Exception as e:
            st.warning(f"Не удалось отобразить граф (слишком большой или ошибка в синтаксисе DOT). Скачайте DOT-файл для просмотра. Ошибка: {e}")
    else:
        st.info("Граф будет отображен здесь после успешного построения.")

if __name__ == "__main__":
    main()
