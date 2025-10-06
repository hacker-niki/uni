import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import scipy.stats as stats
from scipy.integrate import quad # <--- ДОБАВЛЕНО: для численного интегрирования
from matplotlib import cm

# --- НОВАЯ Логика для непрерывной случайной величины (Метод 1: Отбор в 2D) ---

def generate_continuous_samples_rejection(n):
    """
    Генерирует выборку для f(x, y) = (1/63π) * (9 - sqrt(x^2+y^2)) на круге x^2+y^2 <= 9.
    Используется метод отбора (Rejection Sampling) в 2D декартовых координатах.
    """
    samples = []
    
    # M - это максимальное значение функции f(x, y) в нашей области.
    # Максимум достигается в центре (0,0), где f(0,0) = 9/(63*pi) = 1/(7*pi).
    M = 1 / (7 * np.pi)

    # Мы будем генерировать точки до тех пор, пока не наберем n "удачных"
    while len(samples) < n:
        # Шаг 1: Генерируем кандидата (x, y) в квадрате, который полностью
        # вмещает наш круг (от -3 до 3 по каждой оси).
        x_candidate = np.random.uniform(-3, 3)
        y_candidate = np.random.uniform(-3, 3)

        # Шаг 2 (Правило №1): Проверяем, попал ли кандидат внутрь круга.
        # Если нет (точка в "углу" квадрата), то сразу его отбрасываем и начинаем заново.
        if x_candidate**2 + y_candidate**2 <= 9:
            
            # Шаг 3: Если точка в круге, генерируем случайную "высоту" от 0 до M.
            u_check = np.random.uniform(0, M)

            # Вычисляем значение "рельефа" (нашей функции PDF) в точке кандидата.
            pdf_value = (1 / (63 * np.pi)) * (9 - np.sqrt(x_candidate**2 + y_candidate**2))
            
            # Шаг 4 (Правило №2): Проверяем, находится ли наша случайная высота "под рельефом".
            if u_check <= pdf_value:
                # Если да - точка принимается! Добавляем ее в наш список.
                samples.append([x_candidate, y_candidate])
                
    # Когда цикл завершится, у нас будет ровно n точек.
    return np.array(samples)

def pdf_y_given_x_zero(y, fX_0):
    """Теоретическая условная плотность f(y|x=0)"""
    if abs(y) > 3 or fX_0 == 0: return 0
    joint_val = (1 / (63 * np.pi)) * (9 - abs(y))
    return joint_val / fX_0

def pdf_x_given_y_zero(x, fY_0):
    """Теоретическая условная плотность f(x|y=0)"""
    if abs(x) > 3 or fY_0 == 0: return 0
    joint_val = (1 / (63 * np.pi)) * (9 - abs(x))
    return joint_val / fY_0

def analyze_continuous_data(samples):
    """Анализирует непрерывную выборку, строит графики и возвращает текстовый отчет."""
    x = samples[:, 0]
    y = samples[:, 1]
    n = len(x)

    alpha = 0.05 # Уровень значимости для 95% ДИ
    
    # Определяем совместную плотность как функцию от y и x для удобства интегрирования
    def joint_pdf_for_integration(y, x):
        if x**2 + y**2 > 9:
            return 0
        return (1 / (63 * np.pi)) * (9 - np.sqrt(x**2 + y**2))

    # Создаем массив точек x, для которых будем считать теоретическую плотность
    x_theory = np.linspace(-2.99, 2.99, 150)
    pdf_x_theory = []

    fX_at_zero, _ = quad(joint_pdf_for_integration, -3, 3, args=(0,))
    fY_at_zero = fX_at_zero
    
    # Для каждого x численно интегрируем совместную плотность по y
    for x_val in x_theory:
        y_limit = np.sqrt(9 - x_val**2) # Пределы интегрирования для y
        integral_val, _ = quad(joint_pdf_for_integration, -y_limit, y_limit, args=(x_val,))
        pdf_x_theory.append(integral_val)
    
    # pdf_y_theory будет таким же из-за симметрии, поэтому переиспользуем pdf_x_theory  

    # --- Создание графиков ---
    fig = plt.figure(figsize=(15, 12)) # Увеличение размера фигуры

    # 1. Гистограмма X (Маргинальная)
    ax1 = fig.add_subplot(3, 2, 1)
    ax1.hist(x, bins=30, density=True, alpha=0.7, color='skyblue', label='Эмпирическая')
    ax1.plot(x_theory, pdf_x_theory, 'r-', lw=2, label='Теоретическая')
    ax1.set_title("1. Маргинальное распределение X")
    ax1.grid(alpha=0.3)
    ax1.legend()

    # 2. Гистограмма Y (Маргинальная)
    ax2 = fig.add_subplot(3, 2, 2)
    ax2.hist(y, bins=30, density=True, alpha=0.7, color='lightgreen', label='Эмпирическая')
    ax2.plot(x_theory, pdf_x_theory, 'r-', lw=2, label='Теоретическая')
    ax2.set_title("2. Маргинальное распределение Y")
    ax2.grid(alpha=0.3)
    ax2.legend()

    # 3. 3D гистограмма (эмпирическая)
    ax3 = fig.add_subplot(3, 2, 3, projection='3d')
    hist, xedges, yedges = np.histogram2d(x, y, bins=20, range=[[-3, 3], [-3, 3]], density=True)
    X_h, Y_h = np.meshgrid(xedges[:-1] + 0.075, yedges[:-1] + 0.075)
    ax3.plot_surface(X_h, Y_h, hist.T, cmap='viridis')
    ax3.set_title("3. Эмпирическая 2D плотность")
    ax3.set_zlim(0, None)

    # 4. 3D теоретическая плотность
    ax4 = fig.add_subplot(3, 2, 4, projection='3d')
    X_g = np.linspace(-3, 3, 100)
    Y_g = np.linspace(-3, 3, 100)
    X_g, Y_g = np.meshgrid(X_g, Y_g)
    R = np.sqrt(X_g**2 + Y_g**2)
    Z = (1 / (63 * np.pi)) * (9 - R)
    Z[R > 3] = np.nan
    ax4.plot_surface(X_g, Y_g, Z, cmap=cm.plasma, alpha=0.9)
    ax4.set_title("4. Теоретическая 2D плотность")
    ax4.set_zlim(0, None)
    
    # 5. Условная плотность Y|X=0
    TOLERANCE = 0.1
    y_cond = y[np.abs(x) < TOLERANCE]
    y_cond_theory = np.linspace(-2.99, 2.99, 100)
    pdf_y_cond_theory = [pdf_y_given_x_zero(val, fX_at_zero) for val in y_cond_theory]

    ax5 = fig.add_subplot(3, 2, 5)
    ax5.hist(y_cond, bins=30, density=True, alpha=0.7, color='purple', label=f'Эмпирическая (|X| < {TOLERANCE})')
    ax5.plot(y_cond_theory, pdf_y_cond_theory, 'r-', lw=2, label='Теоретическая')
    ax5.set_title(f"5. Условное распределение Y | X ≈ 0")
    ax5.grid(alpha=0.3)
    ax5.legend()

    # 6. Условная плотность X|Y=0
    x_cond = x[np.abs(y) < TOLERANCE]

    ax6 = fig.add_subplot(3, 2, 6)
    ax6.hist(x_cond, bins=30, density=True, alpha=0.7, color='brown', label=f'Эмпирическая (|Y| < {TOLERANCE})')
    ax6.plot(y_cond_theory, pdf_y_cond_theory, 'r-', lw=2, label='Теоретическая')
    ax6.set_title(f"6. Условное распределение X | Y ≈ 0")
    ax6.grid(alpha=0.3)
    ax6.legend()


    fig.tight_layout()

    # --- Статистический анализ ---
    E_X, E_Y, Cov_XY, Cor_XY = 0.0, 0.0, 0.0, 0.0
    Var_X = Var_Y = 297/140

    mean_x, mean_y = np.mean(x), np.mean(y)
    var_x, var_y = np.var(x, ddof=1), np.var(y, ddof=1) # Используем ddof=1 для несмещенной оценки
    cov_xy = np.cov(x, y)[0, 1]
    corr_xy = np.corrcoef(x, y)[0, 1]

    # --- Интервальные оценки (95% CI) ---

    # CI для Мат. ожидания (Mean) - t-распределение
    std_x = np.sqrt(var_x)
    t_crit = stats.t.ppf(1 - alpha/2, df=n - 1)
    ci_mean_x_lower = mean_x - t_crit * std_x / np.sqrt(n)
    ci_mean_x_upper = mean_x + t_crit * std_x / np.sqrt(n)

    # CI для Дисперсии (Variance) - Chi-squared распределение
    chi2_lower = stats.chi2.ppf(alpha/2, df=n - 1)
    chi2_upper = stats.chi2.ppf(1 - alpha/2, df=n - 1)
    ci_var_x_lower = (n - 1) * var_x / chi2_upper
    ci_var_x_upper = (n - 1) * var_x / chi2_lower

    # CI для Корреляции (Correlation) - Z-преобразование Фишера
    if n > 3 and abs(corr_xy) < 1:
        z_r = 0.5 * np.log((1 + corr_xy) / (1 - corr_xy))
        z_crit = stats.norm.ppf(1 - alpha/2)
        se_z = 1 / np.sqrt(n - 3)
        ci_z_lower = z_r - z_crit * se_z
        ci_z_upper = z_r + z_crit * se_z
        ci_corr_xy_lower = np.tanh(ci_z_lower)
        ci_corr_xy_upper = np.tanh(ci_z_upper)
    else:
        ci_corr_xy_lower, ci_corr_xy_upper = np.nan, np.nan

    # Проверка гипотез (p-value)
    t_x = (mean_x - E_X) / (np.std(x, ddof=1) / np.sqrt(n))
    p_mean_x = 2 * (1 - stats.t.cdf(abs(t_x), df=n - 1))
    chi2_x = (n - 1) * var_x / Var_X
    p_var_x = 2 * min(stats.chi2.cdf(chi2_x, df=n - 1), 1 - stats.chi2.cdf(chi2_x, df=n - 1))
    t_corr = corr_xy * np.sqrt((n - 2) / (1 - corr_xy**2)) if (1 - corr_xy**2) > 0 else np.inf
    p_corr = 2 * (1 - stats.t.cdf(abs(t_corr), df=n - 2))


    # --- Формирование отчета ---
    output = ["=== Теоретические характеристики ===", f"  E[X] = {E_X:.4f}, E[Y] = {E_Y:.4f}", f"  Var[X] = {Var_X:.4f}, Var[Y] = {Var_Y:.4f}",
              f"  Cov(X, Y) = {Cov_XY:.4f}", f"  Corr(X, Y) = {Cor_XY:.4f}\n", "=== Эмпирические характеристики (Точечные и 95% ДИ) ===",
              f"  Mean X = {mean_x:.4f} \t (ДИ: [{ci_mean_x_lower:.4f}, {ci_mean_x_upper:.4f}])",
              f"  Var X = {var_x:.4f} \t (ДИ: [{ci_var_x_lower:.4f}, {ci_var_x_upper:.4f}])",
              f"  Corr(X, Y) = {corr_xy:.4f} \t (ДИ: [{ci_corr_xy_lower:.4f}, {ci_corr_xy_upper:.4f}])\n",
              "=== Проверка гипотез (p-value) ===",
              f"  H0: E[X] = {E_X:.4f}  => p-value = {p_mean_x:.4f} ({'не отвергается' if p_mean_x > 0.05 else 'отвергается'})",
              f"  H0: Var[X] = {Var_X:.4f} => p-value = {p_var_x:.4f} ({'не отвергается' if p_var_x > 0.05 else 'отвергается'})",
              f"  H0: Corr(X, Y) = 0 => p-value = {p_corr:.4f} ({'не отвергается' if p_corr > 0.05 else 'отвергается'})"]

    return fig, "\n".join(output)

# --- Логика для дискретной случайной величины (без изменений) ---
def generate_discrete_samples(n, P):
    values = [(i, j) for i in range(P.shape[0]) for j in range(P.shape[1])]
    probs = P.flatten()
    indices = np.random.choice(len(values), size=n, p=probs)
    return np.array([values[i] for i in indices])

def analyze_discrete_data(samples, P):
    x, y = samples[:, 0], samples[:, 1]
    n = len(x)
    m, k = P.shape
    fig = plt.figure(figsize=(10, 8))
    ax1 = fig.add_subplot(2, 2, 1)
    marginal_x_th = np.sum(P, axis=1)
    ax1.hist(x, bins=np.arange(-0.5, m + 0.5, 1), density=True, alpha=0.7, rwidth=0.8, color='skyblue', label='Эмпирическая')
    ax1.plot(range(m), marginal_x_th, 'ro-', label='Теоретическая')
    ax1.set_title("Маргинальное распределение X")
    ax1.set_xticks(range(m))
    ax1.legend()
    ax2 = fig.add_subplot(2, 2, 2)
    marginal_y_th = np.sum(P, axis=0)
    ax2.hist(y, bins=np.arange(-0.5, k + 0.5, 1), density=True, alpha=0.7, rwidth=0.8, color='lightgreen', label='Эмпирическая')
    ax2.plot(range(k), marginal_y_th, 'ro-', label='Теоретическая')
    ax2.set_title("Маргинальное распределение Y")
    ax2.set_xticks(range(k))
    ax2.legend()
    ax3 = fig.add_subplot(2, 2, 3, projection='3d')
    hist, _, _ = np.histogram2d(x, y, bins=(m, k), range=[[-0.5, m-0.5], [-0.5, k-0.5]], density=True)
    X_h, Y_h = np.meshgrid(range(m), range(k))
    ax3.bar3d(X_h.flatten(), Y_h.flatten(), 0, 0.8, 0.8, hist.flatten(), shade=True)
    ax3.set_title("Эмпирическое 2D распределение")
    ax4 = fig.add_subplot(2, 2, 4, projection='3d')
    X_g, Y_g = np.meshgrid(range(m), range(k))
    ax4.bar3d(X_g.flatten(), Y_g.flatten(), 0, 0.8, 0.8, P.flatten(), shade=True, color='orange')
    ax4.set_title("Теоретическое 2D распределение")
    fig.tight_layout()
    ix, iy = np.arange(m), np.arange(k)
    E_X, E_Y = np.sum(ix * marginal_x_th), np.sum(iy * marginal_y_th)
    Var_X, Var_Y = np.sum((ix**2) * marginal_x_th) - E_X**2, np.sum((iy**2) * marginal_y_th) - E_Y**2
    E_XY = sum(i * j * P[i, j] for i in range(m) for j in range(k))
    Cov_XY = E_XY - E_X * E_Y
    Cor_XY = Cov_XY / np.sqrt(Var_X * Var_Y) if Var_X > 0 and Var_Y > 0 else 0
    mean_x, mean_y, var_x, var_y = np.mean(x), np.mean(y), np.var(x), np.var(y)
    cov_xy, corr_xy = np.cov(x, y)[0, 1], np.corrcoef(x, y)[0, 1]
    obs_table = np.zeros_like(P)
    for i, j in samples: obs_table[i, j] += 1
    chi2_stat, p_indep, _, _ = stats.chi2_contingency(obs_table)
    output = [
        "=== Теоретические характеристики ===",
        f"  E[X] = {E_X:.4f}, E[Y] = {E_Y:.4f}",
        f"  Var[X] = {Var_X:.4f}, Var[Y] = {Var_Y:.4f}",
        f"  Cov(X, Y) = {Cov_XY:.4f}, Corr(X, Y) = {Cor_XY:.4f}\n",
        "=== Эмпирические характеристики ===",
        f"  Mean X = {mean_x:.4f}, Mean Y = {mean_y:.4f}",
        f"  Var X = {var_x:.4f}, Var Y = {var_y:.4f}",
        f"  Cov(X, Y) = {cov_xy:.4f}, Corr(X, Y) = {corr_xy:.4f}\n",
        "=== Проверка гипотезы о независимости (Хи-квадрат) ===",
        f"  Статистика χ² = {chi2_stat:.4f}",
        f"  p-value = {p_indep:.4f} ({'Гипотеза о независимости не отвергается' if p_indep > 0.05 else 'Гипотеза о независимости отвергается'})"
    ]
    return fig, "\n".join(output)

# --- Интерфейс Streamlit ---
st.set_page_config(layout="wide")
st.title("Моделирование и анализ двумерных случайных величин")

tab1, tab2 = st.tabs(["Непрерывная СВ", "Дискретная СВ"])

# --- ВКЛАДКА: НЕПРЕРЫВНАЯ СВ ---
with tab1:
    st.header("Симулятор непрерывной двумерной СВ")
    st.markdown(r"""
    Моделируется система `(X, Y)` с совместной плотностью распределения:
    $f(x, y) = \frac{1}{63\pi}(9 - \sqrt{x^2 + y^2})$, где $x^2 + y^2 \le 9$
    """)

    n_continuous = st.number_input("Размер выборки", min_value=100, value=1000, step=100, key="n_cont")
    
    if st.button("Сгенерировать и проанализировать", key="btn_cont"):
        with st.spinner("Идет генерация и анализ... (Этот метод может быть медленнее)"):
            # ВЫЗЫВАЕМ НОВУЮ ФУНКЦИЮ ГЕНЕРАЦИИ
            samples = generate_continuous_samples_rejection(n_continuous)
            fig, results = analyze_continuous_data(samples)
            st.session_state['cont_fig'] = fig
            st.session_state['cont_results'] = results

    if 'cont_fig' in st.session_state and 'cont_results' in st.session_state:
        st.pyplot(st.session_state['cont_fig'])
        st.text_area("Результаты анализа", st.session_state['cont_results'], height=300)
    else:
        st.info("Нажмите кнопку для запуска симуляции.")

# --- ВКЛАДКА: ДИСКРЕТНАЯ СВ ---
with tab2:
    st.header("Симулятор дискретной двумерной СВ")
    # ... (код без изменений)
    if 'prob_matrix' not in st.session_state:
        st.session_state['prob_matrix'] = pd.DataFrame([[0.1, 0.05, 0.05], [0.1, 0.3, 0.1], [0.05, 0.05, 0.2]])
    col1, col2 = st.columns([1, 2])
    with col1:
        n_discrete = st.number_input("Размер выборки", min_value=100, value=1000, step=100, key="n_disc")
        st.subheader("Матрица совместных вероятностей P(X=i, Y=j)")
        edited_df = st.data_editor(st.session_state['prob_matrix'], key="df_editor")
    st.session_state['prob_matrix'] = edited_df
    if st.button("Сгенерировать и проанализировать", key="btn_disc"):
        P_matrix = edited_df.to_numpy(dtype=float)
        if not np.isclose(P_matrix.sum(), 1.0):
            st.warning(f"Сумма вероятностей ({P_matrix.sum():.4f}) не равна 1. Матрица нормализована.")
            if P_matrix.sum() > 0: P_matrix = P_matrix / P_matrix.sum()
            else: st.error("Ошибка: сумма вероятностей равна нулю."); P_matrix = None
        if P_matrix is not None:
            with st.spinner("Идет генерация и анализ..."):
                samples = generate_discrete_samples(n_discrete, P_matrix)
                fig, results = analyze_discrete_data(samples, P_matrix)
                st.session_state['disc_fig'] = fig
                st.session_state['disc_results'] = results
    if 'disc_fig' in st.session_state and 'disc_results' in st.session_state:
        with col2:
             st.pyplot(st.session_state['disc_fig'])
        st.text_area("Результаты анализа", st.session_state['disc_results'], height=280)
    else:
        st.info("Отредактируйте матрицу (если нужно) и нажмите кнопку для запуска симуляции.")




