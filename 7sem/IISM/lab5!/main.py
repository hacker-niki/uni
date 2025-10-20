import streamlit as st
import json
import graphviz
from copy import deepcopy

THEORY_TEXT = """
### Теоретическая справка по Сетям Петри

**Сеть Петри** — это математическая модель для описания и анализа распределенных систем. Она состоит из:
- **Позиций (Places)**: Изображаются кругами, представляют собой условия или ресурсы. В них могут находиться *фишки*.
- **Переходов (Transitions)**: Изображаются прямоугольниками, представляют события, которые могут произойти.
- **Дуг (Arcs)**: Соединяют позиции и переходы.
- **Маркировка (Marking)**: Распределение фишек по позициям в данный момент времени. Начальная маркировка — это исходное состояние системы.

**Правило срабатывания перехода:**
1. Переход называется **разрешенным** (enabled/fireable), если в каждой из его *входных* позиций находится как минимум одна фишка (для дуг кратностью 1).
2. **Срабатывание** (firing) перехода — это атомарный процесс:
   - Из каждой входной позиции изымается одна фишка.
   - В каждую выходную позицию добавляется одна фишка.

**Свойства Сети Петри:**
- **Ограниченность**: Количество фишек в любой позиции никогда не превысит некоторого числа `k`. Если `k=1`, сеть называется **безопасной**.
- **Живость**: Характеризует отсутствие тупиков. Живая сеть гарантирует, что любой переход может в конечном итоге сработать снова.
- **Достижимость**: Возможность перехода из одной маркировки в другую.

---

Формат загружаемых данных берется с сайта
[petry](https://petri.hp102.ru/)
"""


def parse_input_data(json_string: str):
    """Парсит входную JSON строку и создает структуру сети Петри."""
    try:
        data = json.loads(json_string)
        
        initial_marking = {}
        for p_str in data.get('places', []):
            name, _, _, tokens = p_str.split(',')
            initial_marking[name] = int(tokens)
            
        transitions = {}
        for t_str in data.get('trans', []):
            name, _, _ = t_str.split(',')
            transitions[name] = {'inputs': set(), 'outputs': set()}
            
        place_names = set(initial_marking.keys())
        transition_names = set(transitions.keys())

        for a_str in data.get('arcs', []):
            source, dest = a_str.split(',')
            if source in place_names and dest in transition_names:
                transitions[dest]['inputs'].add(source)
            elif source in transition_names and dest in place_names:
                transitions[source]['outputs'].add(dest)
            else:
                st.error(f"Неверная дуга: {a_str}. Один из элементов не определен.")
                return None, None
                
        return initial_marking, {'transitions': transitions, 'places': place_names}

    except (json.JSONDecodeError, ValueError, IndexError) as e:
        st.error(f"Ошибка при обработке входных данных: {e}")
        return None, None

def get_fireable_transitions(marking: dict, net_structure: dict) -> list:
    """Возвращает список переходов, которые могут сработать при текущей маркировке."""
    fireable = []
    if not net_structure or 'transitions' not in net_structure:
        return []
        
    for t_name, t_data in net_structure['transitions'].items():
        # Переход разрешен, если все его входные позиции имеют хотя бы одну фишку
        is_enabled = all(marking.get(p_name, 0) > 0 for p_name in t_data['inputs'])
        if is_enabled:
            fireable.append(t_name)
    return sorted(fireable)

def fire_transition(marking: dict, net_structure: dict, transition_name: str) -> dict:
    """Выполняет срабатывание перехода и возвращает новую маркировку."""
    if transition_name not in get_fireable_transitions(marking, net_structure):
        # Дополнительная проверка, если состояние изменилось
        return marking

    new_marking = marking.copy()
    transition_data = net_structure['transitions'][transition_name]
    
    # Забираем фишки из входных позиций
    for p_in in transition_data['inputs']:
        new_marking[p_in] -= 1
        
    # Добавляем фишки в выходные позиции
    for p_out in transition_data['outputs']:
        new_marking[p_out] += 1
        
    return new_marking

def generate_graphviz_dot(marking: dict, net_structure: dict, fireable_transitions: list) -> str:
    """Генерирует DOT-строку для визуализации сети с помощью Graphviz."""
    dot = graphviz.Digraph('PetriNet', comment='Petri Net Simulation')
    dot.attr(rankdir='LR', splines='true') # Расположение слева направо

    # Добавляем позиции (круги)
    for p_name in sorted(net_structure['places']):
        tokens = marking.get(p_name, 0)
        # label отображает имя и кол-во фишек
        # fillcolor меняется, если в позиции есть фишки
        dot.node(
            p_name, 
            label=f"{p_name}\\n({tokens})", 
            shape='circle', 
            style='filled', 
            fillcolor='lightyellow' if tokens > 0 else 'white'
        )

    # Добавляем переходы (прямоугольники)
    for t_name in sorted(net_structure['transitions'].keys()):
        is_fireable = t_name in fireable_transitions
        # Разрешенные переходы подсвечиваются зеленым
        dot.node(
            t_name, 
            label=t_name, 
            shape='box', 
            style='filled',
            fillcolor='lightgreen' if is_fireable else 'lightblue'
        )

    # Добавляем дуги
    for t_name, t_data in net_structure['transitions'].items():
        for p_in in t_data['inputs']:
            dot.edge(p_in, t_name)
        for p_out in t_data['outputs']:
            dot.edge(t_name, p_out)
            
    return dot

st.set_page_config(layout="wide")
st.title("Симулятор Сетей Петри")

# Разделяем интерфейс на две колонки
col1, col2 = st.columns([1, 2])

with col1:
    st.header("1. Определение Сети")
    
    # Поле для ввода данных с примером по умолчанию
    default_input = '''
{
    "places":["P1,506,126,0","P2,627,131,0","P3,658,357,1","P5,300,347,0","P6,493,354,1"],
    "trans":["T1,465,238","T2,588,247","T3,691,247","T4,403,350"],
    "arcs":["P1,T2","P2,T2","T3,P2","T1,P1","T2,P3","P3,T3","T2,P6","P6,T1","P6,T4","T4,P5"]
}
    '''
    json_input = st.text_area("Введите структуру сети в формате JSON:", value=default_input, height=250)
    
    # Кнопка для загрузки/сброса симуляции
    if st.button("Загрузить / Сбросить модель"):
        initial_marking, net_structure = parse_input_data(json_input)
        if initial_marking is not None and net_structure is not None:
            st.session_state.marking = initial_marking
            st.session_state.net_structure = net_structure
            st.session_state.history = [("Начальное состояние", initial_marking)]
            st.success("Модель успешно загружена!")
        else:
            st.error("Не удалось загрузить модель. Проверьте формат данных.")
            # Очищаем состояние, если загрузка не удалась
            st.session_state.marking = None
            st.session_state.net_structure = None
            st.session_state.history = []

    # Отображение информации только если модель загружена
    if 'marking' in st.session_state and st.session_state.marking is not None:
        st.header("2. Управление Симуляцией")
        
        current_marking = st.session_state.marking
        net_structure = st.session_state.net_structure
        
        fireable_transitions = get_fireable_transitions(current_marking, net_structure)
        
        if not fireable_transitions:
            st.warning("Нет доступных переходов для срабатывания (тупик).")
        else:
            st.write("**Доступные переходы:**")
            # Создаем кнопки для каждого доступного перехода
            for t_name in fireable_transitions:
                if st.button(f"Запустить переход {t_name}", key=f"fire_{t_name}"):
                    new_marking = fire_transition(current_marking, net_structure, t_name)
                    st.session_state.history.append((t_name, current_marking))
                    st.session_state.marking = new_marking
                    st.rerun() # Перезапускаем скрипт для обновления UI

        st.header("Текущая Маркировка")
        st.json(st.session_state.marking)

with col2:
    st.header("Визуализация Сети")

    if 'marking' in st.session_state and st.session_state.marking is not None:
        current_marking = st.session_state.marking
        net_structure = st.session_state.net_structure
        fireable = get_fireable_transitions(current_marking, net_structure)
        
        # Генерируем и отображаем граф
        dot_graph = generate_graphviz_dot(current_marking, net_structure, fireable)
        st.graphviz_chart(dot_graph)
        
        st.header("История срабатываний")
        # Отображаем историю в обратном порядке (последние события сверху)
        history_log = ""
        for i, (action, marking) in enumerate(reversed(st.session_state.history)):
            if action == "Начальное состояние":
                history_log += f"{action}"
            else:
                history_log += f"`{action}` <-"
        st.markdown(history_log)

    else:
        st.info("Загрузите модель сети, чтобы начать симуляцию.")
    
    with st.expander("теория"):
        st.markdown(THEORY_TEXT)
