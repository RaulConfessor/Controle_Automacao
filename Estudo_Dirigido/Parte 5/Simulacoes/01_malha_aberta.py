"""
Questao 1 - Resposta ao degrau em MALHA ABERTA do tanque.
Modelo: G(s) = K/(tau*s + 1), com K = 1/C e tau = A/C.
"""
import os, numpy as np
from scipy import signal
import matplotlib.pyplot as plt
from _comum import A, C, K, tau, RES

# Funcao de transferencia da planta
qin_step = 0.005                       # degrau de vazao [m^3/s] -> h_final = K*qin = 0,5 m
num = [K * qin_step]
den = [tau, 1]
polo = np.roots([tau, 1])
print(f"tau = {tau:.1f} s | K = {K:.1f} | polo malha aberta = {polo[0]:.4f} rad/s")

t = np.linspace(0, 600, 4000)
_, y = signal.step(signal.TransferFunction(num, den), T=t)

plt.figure(figsize=(7.2, 3.6))
plt.plot(t, y, color='#1f5fb0', lw=2, label='Nível h(t)')
plt.axhline(K*qin_step, ls='--', color='gray', label='Valor final (0,5 m)')
plt.axhline(K*qin_step*0.632, ls=':', color='orange', label='63,2% (t = τ)')
plt.axvline(tau, ls=':', color='orange')
plt.xlabel('Tempo (s)'); plt.ylabel('Nível (m)'); plt.grid(True)
plt.title('Tanque - Resposta ao Degrau em Malha Aberta')
plt.legend(loc='lower right'); plt.tight_layout()
plt.savefig(os.path.join(RES, "01_resposta_malha_aberta.png"), dpi=150)
print("Figura salva em resultados/01_resposta_malha_aberta.png")
