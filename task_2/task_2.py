# Два кубика — сумма = s (расширение)

# Описание: бросаем два кубика, смотрим событие сумма = 7 (или = 2, 12 и т.д.).
# Теория: классическая вероятностная масса (прим. 6/36 для 7).
# Моделирование: генерация пар 1..6.

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

N = 10000          # число бросков
rng = np.random.default_rng(42)

# ТЕОРЕТИЧЕСКИЕ ВЕРОЯТНОСТИ
theoretical_probs = {
    2: 1/36, 3: 2/36, 4: 3/36, 5: 4/36, 6: 5/36,
    7: 6/36, 8: 5/36, 9: 4/36, 10: 3/36, 11: 2/36, 12: 1/36
}


# МОДЕЛИРОВАНИЕ БРОСКОВ
die1 = rng.integers(1, 7, size=N)
die2 = rng.integers(1, 7, size=N)
sums = die1 + die2


#ВИЗУАЛИЗАЦИЯ
sums_to_track = [5]
freqs = {s: np.zeros(N) for s in sums_to_track}
counts = {s: 0 for s in sums_to_track}

for i, s_val in enumerate(sums):
    for s in sums_to_track:
        if s_val == s:
            counts[s] += 1
        freqs[s][i] = counts[s] / (i + 1)

# СРАВНЕНИЕ С ТЕОРИЕЙ
empirical_probs = {s: np.sum(sums == s) / N for s in range(2, 13)}

df = pd.DataFrame({
    "Сумма": list(range(2, 13)),
    "Частотная вероятность": [empirical_probs[s] for s in range(2, 13)],
    "Теоретическая вероятность": [theoretical_probs[s] for s in range(2, 13)]
}).round(5)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6), gridspec_kw={'width_ratios': [2, 1]})

for s in sums_to_track:
    ax1.plot(freqs[s], color='r', label=f"Частотная вероятность (сумма = {s})")
    ax1.hlines(theoretical_probs[s], 0, N, linestyles='dashed', color='g', label=f"Теоретическая вероятность (сумма = {s})")

ax1.set_xlabel(f"Число бросков ({N})")
ax1.set_ylabel("Оценка вероятности")
ax1.set_title("Сходимость частотных вероятностей\nсумм двух кубиков к классическим")
ax1.set_xscale("log")
ax1.grid(alpha=0.3)
ax1.legend()



ax2.axis("off")
table_data = df.values
columns = df.columns
table = ax2.table(cellText=table_data, colLabels=columns, loc='center')
table.auto_set_font_size(False)
table.set_fontsize(10)
table.scale(2, 2)



plt.tight_layout()
plt.show()



