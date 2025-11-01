import streamlit as st
import random
import time

# --- Интерфейс Streamlit ---

st.set_page_config(layout="wide")
st.title("Аналитический калькулятор и симулятор СМО M/M/1")
st.markdown("##### На примере задачи о билетной кассе")

st.markdown("""
Система массового обслуживания — билетная касса с **одним окошком (n=1)** и **неограниченной очередью**. 
В кассе продаются билеты в пункты А и В. Потоки пассажиров — простейшие (пуассоновские), 
время обслуживания — показательное.
""")

# --- Ввод данных ---
st.header("Параметры системы")
col1, col2 = st.columns(2)

with col1:
    st.subheader("Входящий поток (λ)")
    passengers_a = st.number_input("Пассажиров в пункт А", min_value=0, value=3, step=1)
    passengers_b = st.number_input("Пассажиров в пункт В", min_value=0, value=2, step=1)
    time_arrival = st.number_input("За время (минут)", min_value=1, value=20, step=1)

with col2:
    st.subheader("Обслуживание (μ)")
    served_passengers = st.number_input("Обслужено пассажиров", min_value=0, value=3, step=1)
    time_service = st.number_input("За время (минут)", min_value=1, value=10, step=1)

# --- Расчеты ---
st.header("Аналитический расчет (по формулам)")
if st.button("Рассчитать характеристики СМО"):

    # 1. Расчет интенсивностей
    lambda_total = (passengers_a + passengers_b) / time_arrival
    mu = served_passengers / time_service

    st.header("Результаты анализа")
    
    col_res1, col_res2 = st.columns(2)
    
    with col_res1:
        st.subheader("Базовые интенсивности")
        st.markdown(f"**Общая интенсивность потока (λ):** `{lambda_total:.4f}` пасс/мин")
        st.markdown(f"**Интенсивность обслуживания (μ):** `{mu:.4f}` пасс/мин")

        # 2. Проверка существования финальных вероятностей
        st.subheader("Проверка стабильности системы")
        is_stable = lambda_total < mu
        
        if is_stable:
            rho = lambda_total / mu
            st.success("Система стабильна (λ < μ). Финальные вероятности существуют.")
            st.markdown(f"**Коэффициент загрузки (ρ = λ/μ):** `{rho:.4f}`")
        else:
            rho = lambda_total / mu
            st.error("Система НЕстабильна (λ ≥ μ). Очередь будет расти бесконечно.")
            st.warning("Дальнейшие расчеты характеристик не имеют смысла для нестабильной системы.")
            st.markdown(f"**Коэффициент загрузки (ρ = λ/μ):** `{rho:.4f}`")
    
    # 3. Расчет характеристик (только если система стабильна)
    if is_stable:
        with col_res2:
            st.subheader("Финальные вероятности состояний")
            p0 = 1 - rho
            p1 = p0 * rho
            p2 = p0 * rho**2
            st.markdown(f"**p₀** (касса свободна): `{p0:.4f}` ({p0:.2%})")
            st.markdown(f"**p₁** (1 чел. в кассе): `{p1:.4f}` ({p1:.2%})")
            st.markdown(f"**p₂** (2 чел. в кассе): `{p2:.4f}` ({p2:.2%})")

        st.subheader("Характеристики эффективности СМО")
        L = rho / (1 - rho)
        Lq = rho**2 / (1 - rho)
        W = L / lambda_total
        Wq = Lq / lambda_total
        
        results_col1, results_col2 = st.columns(2)
        
        with results_col1:
            st.metric(label="Среднее число пассажиров в системе (L)", value=f"{L:.3f} чел.")
            st.metric(label="Среднее число пассажиров в очереди (Lq)", value=f"{Lq:.3f} чел.")
        
        with results_col2:
            st.metric(label="Среднее время в системе (W)", value=f"{W:.3f} мин.")
            st.metric(label="Среднее время в очереди (Wq)", value=f"{Wq:.3f} мин.")
else:
    st.info("Нажмите кнопку для выполнения аналитических расчетов.")


# --- СИМУЛЯЦИЯ ---
st.markdown("---")
st.header("Визуализация симуляции в реальном времени")

sim_col1, sim_col2 = st.columns([1, 2])
with sim_col1:
    simulation_time = 10000
    simulation_speed = 0.1

if st.button("🚀 Запустить визуализацию"):
    lambda_total = (passengers_a + passengers_b) / time_arrival
    mu = served_passengers / time_service

    if lambda_total == 0 or mu == 0:
        st.error("Интенсивность потока и обслуживания должны быть больше нуля для симуляции.")
    else:
        # --- Инициализация симуляции ---
        current_time = 0
        queue = 0
        server_busy = False
        
        # События: (время, тип_события)
        # Типы: 0 - прибытие, 1 - уход (окончание обслуживания)
        events = []
        
        # Генерируем первое прибытие
        next_arrival_time = random.expovariate(lambda_total)
        events.append((next_arrival_time, 0))

        # --- Создаем плейсхолдеры для обновления "в реальном времени" ---
        st.subheader("Панель мониторинга")
        kpi_col1, kpi_col2, kpi_col3 = st.columns(3)
        time_placeholder = kpi_col1.empty()
        queue_placeholder = kpi_col2.empty()
        status_placeholder = kpi_col3.empty()

        st.subheader("Процесс")
        viz_placeholder = st.empty()
        log_placeholder = st.empty()
        log_text = ""

        while current_time < simulation_time:
            if not events:
                break # Если событий нет, выходим

            # Получаем ближайшее событие
            events.sort()
            event_time, event_type = events.pop(0)
            current_time = event_time

            # --- Обработка событий ---
            if event_type == 0: # Прибытие
                log_text += f"{current_time:.2f} мин: 🚶 Прибыл новый пассажир.\n"
                if not server_busy:
                    # Сразу начинаем обслуживание
                    server_busy = True
                    log_text += f"{current_time:.2f} мин: ✅ Пассажир начал обслуживание.\n"
                    # Генерируем время ухода
                    service_duration = random.expovariate(mu)
                    next_departure_time = current_time + service_duration
                    events.append((next_departure_time, 1))
                else:
                    # Встаем в очередь
                    queue += 1
                
                # Генерируем следующее прибытие
                next_arrival_time = current_time + random.expovariate(lambda_total)
                events.append((next_arrival_time, 0))

            elif event_type == 1: # Уход
                log_text += f"{current_time:.2f} мин: 🏁 Пассажир обслужен и ушел.\n"
                if queue > 0:
                    # Берем следующего из очереди
                    queue -= 1
                    log_text += f"{current_time:.2f} мин: ✅ Следующий из очереди начал обслуживание.\n"
                    # Генерируем время ухода для него
                    service_duration = random.expovariate(mu)
                    next_departure_time = current_time + service_duration
                    events.append((next_departure_time, 1))
                else:
                    # Очереди нет, касса свободна
                    server_busy = False

            # --- Обновление визуализации ---
            time_placeholder.metric("Симулированное время", f"{current_time:.2f} мин.")
            queue_placeholder.metric("Длина очереди", f"{queue} чел.")
            
            if server_busy:
                status_placeholder.metric("Статус кассы", "Занята 🟨")
                server_viz = "[👨‍💻]"
            else:
                status_placeholder.metric("Статус кассы", "Свободна 🟩")
                server_viz = "[   ]"

            queue_viz = "🚶" * queue
            viz_placeholder.markdown(f"**Касса:** {server_viz} <br> **Очередь:** {queue_viz}", unsafe_allow_html=True)
            
            # Обрезаем лог, чтобы он не стал слишком длинным
            log_lines = log_text.strip().split('\n')
            if len(log_lines) > 10:
                log_text = '\n'.join(log_lines[-10:]) + '\n'

            log_placeholder.text_area("Журнал событий (последние 10)", log_text, height=200)

            # Пауза для эффекта "реального времени"
            time.sleep(simulation_speed)
            
        st.success(f"Симуляция завершена на времени {current_time:.2f} минут.")
