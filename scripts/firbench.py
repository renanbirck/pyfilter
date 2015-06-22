#!/usr/bin/env python3

import numpy as np, scipy as sp, scipy.signal as signal
import matplotlib.pyplot as plt
import timeit
# Forçar o uso de LaTeX
import matplotlib
from matplotlib import rc
##rc('font',**{'family':'sans-serif','sans-serif':['Helvetica']})
## for Palatino and other serif fonts use:
rc('font',**{'family':'serif','serif':['Palatino']})
rc('text', usetex=True)
matplotlib.rc('xtick', labelsize=20)
matplotlib.rc('ytick', labelsize=20)


def design_FIR(taps, sample_rate):
    nyquist = sample_rate/2
    return signal.firwin2(taps, [0, nyquist/2, nyquist], [1, 1, 0], nyq=nyquist)

import time
t = time.time()
b = design_FIR(32768, 1000)
#timeit.timeit("design_FIR(8192, 1000)", setup="from __main__ import design_FIR", number=1000)
elapsed = time.time() - t
print(elapsed)
len(b)

speeds = []
for num_taps in [1, 2, 4, 8, 10, 16, 30, 32, 60, 64, 120, 128, 250, 256, 500, 512, 1000, 1024, 2000, 2048, 4000, 4096, 5000, 6000, 7000, 8000, 8192, 9000, 10000, 10500, 11000, 11500, 12000, 12500, 13000, 13500, 14000, 14500, 15000, 15500, 16000, 16384, 20000, 30000, 32768, 40000, 50000, 60000, 65000, 65536]:
    print("Número de taps: ", num_taps)
    times = []
    for _ in range(1000):
        t = time.time()
        b = design_FIR(num_taps, 1000)
        elapsed = time.time() - t
        times.append(elapsed)

    speeds.append((num_taps, np.mean(times), np.min(times), np.max(times)))

import pickle
output = open('fir_result.pkl', 'wb')

pickle.dump(speeds, output)
output.close()

fig = plt.figure(1, figsize=(12, 9))
plt.plot([taps for (taps, time, _, _) in speeds], [time*1000 for (taps, time, _, _) in speeds], 'k^-', linewidth=1.5, markersize=9)
plt.plot([taps for (taps, _, min_time, _) in speeds], [min_time*1000 for (taps, _, min_time, _) in speeds], 'k--', linewidth=1.5, markersize=2)
plt.plot([taps for (taps, _, _, max_time) in speeds], [max_time*1000 for (taps, _, _, max_time) in speeds], 'ko-', linewidth=1.5, markersize=2)

plt.xlabel("N\\'umero de taps", fontsize=19)
plt.ylabel('tempo (ms)', fontsize=19)
#plt.axis([1, 66000, 0, 30])
plt.grid()
plt.title('Filtro FIR simples passa-baixa: tempo de computa\c{c}\~ao (1000 execu\c{c}\~oes)', fontsize=19)
plt.legend(["Tempo m\\'edio", "Tempo m\\'inimo", "Tempo m\\'aximo"], loc='best', fontsize=19)
plt.show()
plt.savefig('FIR_benchmark.svg')

