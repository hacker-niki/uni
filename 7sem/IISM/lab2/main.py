import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats

# --- Логика для непрерывных случайных величин ---

def _chi2_test_continuous(samples, theoretical_dist, n_bins):
    """Вспомогательная функция для теста хи-квадрат для непрерывных данных."""
    n = len(samples)
    counts, edges = np.histogram(samples, bins=n_bins)
    exp_counts = np.array([n * (theoretical_dist.cdf(edges[i + 1]) - theoretical_dist.cdf(edges[i]))
                           for i in range(len(counts))])

    obs = counts.astype(float)
    exp = exp_counts.astype(float)

    # Объединение бинов с низкой ожидаемой частотой
    min_exp = 5
    while np.any(exp < min_exp) and len(exp) > 2:
        idx = np.argmin(exp)
        if idx == 0:
            exp[1] += exp[0]
            obs[1] += obs[0]
        else:
            exp[idx - 1] += exp[idx]
            obs[idx - 1] += obs[idx]
        exp = np.delete(exp, idx)
        obs = np.delete(obs, idx)

    if len(exp) <= 2:
        return -1, -1

    # Нормализация для обеспечения равенства сумм
    if exp.sum() > 0:
        exp *= obs.sum() / exp.sum()

    # Избегание деления на ноль, если exp содержит нули
    if np.any(exp == 0):
        return float('nan'), float('nan')
        
    chi2_stat, p = stats.chisquare(obs, exp)
    return chi2_stat, p


def analyze_continuous_samples(samples, theoretical_dist, name):
    """Анализирует выборку непрерывной СВ, генерирует график и текстовый отчет."""
    samples = np.asarray(samples)
    fig, ax = plt.subplots(figsize=(8, 5))
    n = len(samples)
    n_bins = max(10, min(100, n // 50))
    ax.hist(samples, bins=n_bins, density=True, alpha=0.7, label='Эмпирическая плотность')
    x = np.linspace(np.min(samples), np.max(samples), 1000)

    ax.plot(x, theoretical_dist.pdf(x), 'r-', lw=2, label='Теоретическая плотность')
    ax.set_title(f'Гистограмма и теоретическая плотность ({name})')
    ax.set_xlabel('Значение')
    ax.set_ylabel('Плотность')
    ax.legend()
    ax.grid(True, alpha=0.5)
    fig.tight_layout()

    mean = float(np.mean(samples))
    std = float(np.std(samples))
    median = float(np.median(samples))
    se = std / np.sqrt(n)
    t = stats.t.ppf(0.975, n - 1)
    ci_mean = (mean - t * se, mean + t * se)
    sample_var = std ** 2
    chi2_l = stats.chi2.ppf(0.025, n - 1)
    chi2_u = stats.chi2.ppf(0.975, n - 1)
    ci_var = ((n - 1) * sample_var / chi2_u, (n - 1) * sample_var / chi2_l)
    ci_std = (np.sqrt(ci_var[0]), np.sqrt(ci_var[1]))

    ks_stat, ks_p = stats.kstest(samples, theoretical_dist.cdf)
    chi2_stat, chi2_p = _chi2_test_continuous(samples, theoretical_dist, n_bins=n_bins)

    out = []
    out.append(f"СТАТИСТИЧЕСКИЙ АНАЛИЗ ({name})")
    out.append("=" * 70)
    out.append(f"Количество samples: {n:,}")
    out.append("\nТОЧЕЧНЫЕ ОЦЕНКИ:")
    out.append(f"  Среднее: {mean:.6f}")
    out.append(f"  Стандартное отклонение: {std:.6f}")
    out.append(f"  Медиана: {median:.6f}")
    out.append("\nИНТЕРВАЛЬНЫЕ ОЦЕНКИ (95%):")
    out.append(f"  Среднее: ({ci_mean[0]:.6f}, {ci_mean[1]:.6f})")
    out.append(f"  Дисперсия: ({ci_var[0]:.6f}, {ci_var[1]:.6f})")
    out.append(f"  Стандартное отклонение: ({ci_std[0]:.6f}, {ci_std[1]:.6f})")
    out.append("\nПРОВЕРКА СООТВЕТСТВИЯ:")
    out.append("  Тест Колмогорова-Смирнова:")
    out.append(f"    Статистика: {ks_stat:.6f}")
    out.append(f"    p-value: {ks_p:.6f}")
    out.append(f"    Вывод: {'Гипотеза не отвергается' if ks_p > 0.05 else 'Гипотеза отвергается'}")
    out.append("\n  Тест хи-квадрат (по бинам):")
    out.append(f"    Статистика: {chi2_stat:.6f}")
    out.append(f"    p-value: {chi2_p:.6f}")
    out.append(f"    Вывод: {'Гипотеза не отвергается' if chi2_p > 0.05 else 'Гипотеза отвергается'}")

    return fig, "\n".join(out)


# --- Логика для дискретных случайных величин ---

def _chi2_test_discrete(values, obs_counts, exp_probs, n):
    """Вспомогательная функция для теста хи-квадрат для дискретных данных."""
    obs = obs_counts.astype(float).copy()
    exp = (np.array(exp_probs) * n).astype(float)
    
    # Объединение категорий с низкой ожидаемой частотой
    min_exp = 5
    while True:
        if len(exp) <= 1: return float('nan'), float('nan')
        min_idx = np.argmin(exp)
        if exp[min_idx] >= min_exp: break
        if min_idx == 0:
            exp[1] += exp[0]
            obs[1] += obs[0]
        else:
            exp[min_idx - 1] += exp[min_idx]
            obs[min_idx - 1] += obs[min_idx]
        exp = np.delete(exp, min_idx)
        obs = np.delete(obs, min_idx)
    
    if exp.sum() > 0:
        exp *= obs.sum() / exp.sum()
    else:
        return float('nan'), float('nan')

    if np.any(exp == 0):
        return float('nan'), float('nan')
    
    chi2_stat, p = stats.chisquare(obs, exp)
    return chi2_stat, p

def analyze_discrete_samples(samples, theoretical_dist, name):
    """Анализирует выборку дискретной СВ, генерирует график и текстовый отчет."""
    samples = np.asarray(samples)
    fig, ax = plt.subplots(figsize=(8, 5))

    unique, counts = np.unique(samples, return_counts=True)
    n = len(samples)
    
    min_val = int(np.min(unique))
    max_val = int(np.max(unique))
    
    values = np.arange(min_val, max_val + 2) # +2 для наглядности графика
    theoretical_probs = theoretical_dist.pmf(values)
    
    empirical_probs_map = {u: c / n for u, c in zip(unique, counts)}
    empirical_probs = np.array([empirical_probs_map.get(v, 0.0) for v in values])

    x = np.arange(len(values))
    width = 0.35
    ax.bar(x - width / 2, theoretical_probs, width, label='Теоретические вероятности', alpha=0.8)
    ax.bar(x + width / 2, empirical_probs, width, label='Эмпирические частоты', alpha=0.8)
    ax.set_xlabel('Значения')
    ax.set_ylabel('Вероятность / Частота')
    ax.set_title(f'Сравнение теоретического и эмпирического распределения ({name})')
    ax.set_xticks(x)
    ax.set_xticklabels([str(int(v)) for v in values])
    ax.legend()
    ax.grid(True, axis='y', alpha=0.3)
    fig.tight_layout()

    mean = float(np.mean(samples))
    std = float(np.std(samples))
    median = float(np.median(samples))
    se = std / np.sqrt(n)
    t = stats.t.ppf(0.975, n - 1)
    ci_mean = (mean - t * se, mean + t * se)
    sample_var = std ** 2
    chi2_l = stats.chi2.ppf(0.025, n - 1)
    chi2_u = stats.chi2.ppf(0.975, n - 1)
    ci_var = ((n - 1) * sample_var / chi2_u, (n - 1) * sample_var / chi2_l)
    ci_std = (np.sqrt(ci_var[0]), np.sqrt(ci_var[1]))

    obs_values = np.arange(int(np.min(unique)), int(np.max(unique)) + 1)
    obs_counts = np.array([empirical_probs_map.get(v, 0) * n for v in obs_values])
    exp_probs = theoretical_dist.pmf(obs_values)

    chi2_stat, chi2_p = _chi2_test_discrete(obs_values, obs_counts, exp_probs, n)
    ks_stat, ks_p = stats.kstest(samples, theoretical_dist.cdf)

    out = []
    out.append(f"СТАТИСТИЧЕСКИЙ АНАЛИЗ ({name})")
    out.append("=" * 70)
    out.append(f"Количество samples: {n:,}")
    out.append("\nТОЧЕЧНЫЕ ОЦЕНКИ:")
    out.append(f"  Среднее: {mean:.6f}")
    out.append(f"  Стандартное отклонение: {std:.6f}")
    out.append(f"  Медиана: {median:.6f}")
    out.append("\nИНТЕРВАЛЬНЫЕ ОЦЕНКИ (95%):")
    out.append(f"  Среднее: ({ci_mean[0]:.6f}, {ci_mean[1]:.6f})")
    out.append(f"  Дисперсия: ({ci_var[0]:.6f}, {ci_var[1]:.6f})")
    out.append(f"  Стандартное отклонение: ({ci_std[0]:.6f}, {ci_std[1]:.6f})")
    out.append("\nПРОВЕРКА СООТВЕТСТВИЯ:")
    out.append("  Тест хи-квадрат:")
    if np.isnan(chi2_stat):
        out.append("    Недостаточно данных для проведения теста хи-квадрат.")
    else:
        out.append(f"    Статистика: {chi2_stat:.6f}")
        out.append(f"    p-value: {chi2_p:.6f}")
        out.append(f"    Вывод: {'Гипотеза не отвергается' if chi2_p > 0.05 else 'Гипотеза отвергается'}")
    out.append("\n  Тест Колмогорова-Смирнова (с осторожностью для дискретных СВ):")
    out.append(f"    Статистика: {ks_stat:.6f}")
    out.append(f"    p-value: {ks_p:.6f}")
    out.append(f"    Вывод: {'Гипотеза не отвергается' if ks_p > 0.05 else 'Гипотеза отвергается'}")

    return fig, "\n".join(out)


# --- Интерфейс Streamlit ---

st.set_page_config(layout="wide")
st.title("Моделирование и анализ случайных величин")

# --- Боковая панель для настроек ---
st.sidebar.header("Параметры симуляции")
sim_type = st.sidebar.radio("Выберите тип величины", ["Непрерывные", "Дискретные"])

if sim_type == "Непрерывные":
    dist_name = st.sidebar.selectbox(
        "Выберите распределение:",
        ["Экспоненциальное", "Нормальное", "Равномерное", "Логнормальное"]
    )
    if dist_name == "Экспоненциальное":
        lam = st.sidebar.number_input("Параметр λ (интенсивность)", value=1.0, min_value=0.01, format="%.2f")
    elif dist_name == "Нормальное":
        mu = st.sidebar.number_input("μ (мат. ожидание)", value=0.0, format="%.2f")
        sigma = st.sidebar.number_input("σ (станд. отклонение)", value=1.0, min_value=0.01, format="%.2f")
    elif dist_name == "Равномерное":
        a = st.sidebar.number_input("a (нижняя граница)", value=0.0, format="%.2f")
        b = st.sidebar.number_input("b (верхняя граница)", value=1.0, format="%.2f")
    elif dist_name == "Логнормальное":
        mu = st.sidebar.number_input("μ (мат. ожидание логарифма)", value=0.0, format="%.2f")
        sigma = st.sidebar.number_input("σ (станд. отклонение логарифма)", value=1.0, min_value=0.01, format="%.2f")

else: # Дискретные
    dist_name = st.sidebar.selectbox(
        "Выберите распределение:",
        ["Биномиальное", "Пуассона", "Геометрическое"]
    )
    if dist_name == "Биномиальное":
        trials = st.sidebar.number_input("n (количество испытаний)", value=10, min_value=1, step=1)
        p_binom = st.sidebar.slider("p (вероятность успеха)", 0.0, 1.0, 0.5)
    elif dist_name == "Пуассона":
        lam_poisson = st.sidebar.number_input("λ (интенсивность)", value=3.0, min_value=0.1, format="%.2f")
    elif dist_name == "Геометрическое":
        p_geom = st.sidebar.slider("p (вероятность успеха)", 0.0, 1.0, 0.3)

n_samples = st.sidebar.number_input("Количество samples", value=10000, min_value=10, step=100)

run_button = st.sidebar.button("Запустить симуляцию")


# --- Основное окно для вывода результатов ---
if run_button:
    try:
        u = np.random.random(n_samples) # Базовая случайная величина

        if sim_type == "Непрерывные":
            if dist_name == "Экспоненциальное":
                if lam <= 0: raise ValueError("λ должен быть > 0")
                samples = -np.log(1 - u) / lam
                theoretical = stats.expon(scale=1.0 / lam)
            elif dist_name == "Нормальное":
                if sigma <= 0: raise ValueError("σ должен быть > 0")
                samples = stats.norm.ppf(u, loc=mu, scale=sigma)
                theoretical = stats.norm(loc=mu, scale=sigma)
            elif dist_name == "Равномерное":
                if a >= b: raise ValueError("a должно быть < b")
                samples = a + (b - a) * u
                theoretical = stats.uniform(loc=a, scale=b - a)
            elif dist_name == "Логнормальное":
                if sigma <= 0: raise ValueError("σ должен быть > 0")
                z = stats.norm.ppf(u)
                samples = np.exp(mu + sigma * z)
                theoretical = stats.lognorm(s=sigma, scale=np.exp(mu))
            
            fig, results_text = analyze_continuous_samples(samples, theoretical, dist_name)

        else: # Дискретные
            if dist_name == "Биномиальное":
                if not (0 <= p_binom <= 1): raise ValueError("p должен быть в [0,1]")
                samples = stats.binom.ppf(u, n=trials, p=p_binom).astype(int)
                theoretical = stats.binom(n=trials, p=p_binom)
            elif dist_name == "Пуассона":
                if lam_poisson <= 0: raise ValueError("λ должен быть > 0")
                samples = stats.poisson.ppf(u, mu=lam_poisson).astype(int)
                theoretical = stats.poisson(mu=lam_poisson)
            elif dist_name == "Геометрическое":
                if not (0 < p_geom <= 1): raise ValueError("p должен быть в (0,1]")
                samples = stats.geom.ppf(u, p=p_geom).astype(int)
                theoretical = stats.geom(p=p_geom)

            fig, results_text = analyze_discrete_samples(samples, theoretical, dist_name)

        # Вывод результатов
        tab1, tab2 = st.tabs(["📊 График", "📄 Результаты анализа"])
        with tab1:
            st.pyplot(fig)
        with tab2:
            st.text(results_text)
            
    except Exception as e:
        st.error(f"Произошла ошибка: {e}")

else:
    st.info("Настройте параметры на боковой панели и нажмите 'Запустить симуляцию'.")
