"""
Questao 2 - Mapa de polos no plano-s: malha aberta x malha fechada (PI).
Mostra a realocacao do polo real lento para um par complexo bem amortecido.
"""
import os, numpy as np
import matplotlib.pyplot as plt
from _comum import K, tau, Kp, Ki, RES

polo_ma = np.roots([tau, 1])                       # -1/tau
den_mf  = [tau, 1 + K*Kp, K*Ki]                    # tau s^2 + (1+K Kp) s + K Ki
polos_mf = np.roots(den_mf)
wn = np.sqrt(K*Ki/tau); zeta = (1 + K*Kp)/(2*tau*wn)
print(f"Polo malha aberta: {polo_ma}")
print(f"Polos malha fechada (PI): {polos_mf}")
print(f"wn = {wn:.3f} rad/s | zeta = {zeta:.3f}")

plt.figure(figsize=(6.4, 4.6)); ax = plt.gca()
ax.axvspan(-0.2, 0, color='#d6efd6', alpha=0.6)
ax.axvspan(0, 0.05, color='#f6d6d6', alpha=0.6)
ax.axhline(0, color='k', lw=0.8); ax.axvline(0, color='k', lw=1.2)
ax.plot(polo_ma.real, polo_ma.imag, 'X', color='#b03030', ms=13, label='Polo malha aberta (-0,010)')
ax.plot(polos_mf.real, polos_mf.imag, 'X', color='#1f7a1f', ms=13, label='Polos malha fechada (PI)')
ax.set_xlim(-0.14, 0.03); ax.set_ylim(-0.085, 0.085)
ax.set_xlabel('Parte Real  σ'); ax.set_ylabel('Parte Imaginária  jω')
ax.set_title('Mapa de Polos no Plano-s'); ax.grid(True)
ax.text(-0.13, 0.072, 'SEMIPLANO\nESTÁVEL', color='#2e7d32', fontsize=9, va='top')
ax.text(0.004, 0.072, 'INSTÁVEL', color='#b03030', fontsize=9, va='top')
ax.legend(loc='lower left', fontsize=8)
plt.tight_layout(); plt.savefig(os.path.join(RES, "02_mapa_polos.png"), dpi=150)
print("Figura salva em resultados/02_mapa_polos.png")
