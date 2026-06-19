"""
Questao 4 - Rejeicao de perturbacao: a valvula de saida abre mais em t = 120 s.
A acao integral compensa o disturbio e restaura o setpoint sem erro residual.
"""
import os, numpy as np
import matplotlib.pyplot as plt
from _comum import Kp, Ki, Kd, Tf, Tsamp, simula, RES

href = lambda t: 0.6
dist = lambda t: 0.003 if t >= 120 else 0.0       # +3 L/s saindo
t,h,u,e,r = simula(Kp,Ki,Kd,Tf,Tsamp, 300, href, dist)
print(f"Desvio maximo apos perturbacao = {np.max(np.abs(h[t>=120]-0.6)):.4f} m")

fig, ax = plt.subplots(2,1, figsize=(7.2,5.2), sharex=True)
ax[0].plot(t,h,color='#1f5fb0',lw=2,label='Nível h(t)')
ax[0].plot(t,r,ls='--',color='gray',label='Referência')
ax[0].axvline(120,ls=':',color='#d08000',label='Perturbação (válvula abre)')
ax[0].set_ylabel('Nível (m)'); ax[0].legend(loc='lower right'); ax[0].grid(True)
ax[0].set_title('Rejeição de Perturbação (abertura da válvula de saída)')
ax[1].plot(t,u*1000,color='#b03030',lw=1.6,label='Vazão da bomba u(t)')
ax[1].axvline(120,ls=':',color='#d08000')
ax[1].set_xlabel('Tempo (s)'); ax[1].set_ylabel('Vazão (L/s)')
ax[1].legend(loc='upper right'); ax[1].grid(True)
plt.tight_layout(); plt.savefig(os.path.join(RES, "04_rejeicao_perturbacao.png"), dpi=150)
print("Figura salva em resultados/04_rejeicao_perturbacao.png")
