import streamlit as st

# --- Интерфейс Streamlit ---

st.set_page_config(layout="wide")
st.title("Аналитический калькулятор СМО M/M/1")
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
            st.error("Система НЕстабильна (λ ≥ μ). Очередь будет расти бесконечно.")
            st.warning("Дальнейшие расчеты характеристик не имеют смысла для нестабильной системы.")
    
    # 3. Расчет характеристик (только если система стабильна)
    if is_stable:
        with col_res2:
            st.subheader("Финальные вероятности состояний")
            # p_k = (1 - rho) * rho**k
            p0 = 1 - rho
            p1 = p0 * rho
            p2 = p0 * rho**2
            st.markdown(f"**p₀** (касса свободна): `{p0:.4f}` ({p0:.2%})")
            st.markdown(f"**p₁** (1 чел. в кассе): `{p1:.4f}` ({p1:.2%})")
            st.markdown(f"**p₂** (2 чел. в кассе): `{p2:.4f}` ({p2:.2%})")

        st.subheader("Характеристики эффективности СМО")
        # Среднее число заявок в системе
        L = rho / (1 - rho)
        # Среднее число заявок в очереди
        Lq = rho**2 / (1 - rho)
        # Среднее время пребывания в системе
        W = L / lambda_total
        # Среднее время пребывания в очереди
        Wq = Lq / lambda_total
        
        results_col1, results_col2 = st.columns(2)
        
        with results_col1:
            st.metric(label="Среднее число пассажиров в системе (L)", value=f"{L:.3f} чел.")
            st.metric(label="Среднее число пассажиров в очереди (Lq)", value=f"{Lq:.3f} чел.")
        
        with results_col2:
            st.metric(label="Среднее время в системе (W)", value=f"{W:.3f} мин.")
            st.metric(label="Среднее время в очереди (Wq)", value=f"{Wq:.3f} мин.")
else:
    st.info("Нажмите кнопку для выполнения расчетов.")
