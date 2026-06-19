"""
Questao 3 - Malha fechada com PID: seguimento de referencia (setpoint 0,6 m).
Mostra nivel h(t) e o comando de vazao u(t) (com saturacao da bomba).
"""
import os, numpy as np
import matplotlib.pyplot as plt
from _comum import Qmax, Kp, Ki, Kd, Tf, Tsamp, simula, RES

href = lambda t: 0.6
sem_dist = lambda t: 0.0
t,h,u,e,r = simula(Kp,Ki,Kd,Tf,Tsamp, 250, href, sem_dist)

hf = r[-1]
mp = (h.max()-hf)/hf*100 if h.max() > hf else 0.0
band = 0.02*hf; ts = None
for i in np.where(np.abs(h-hf) <= band)[0]:
    if np.all(np.abs(h[i:]-hf) <= band): ts = t[i]; break
print(f"Mp = {mp:.1f}%  |  ts(2%) = {ts:.1f} s  |  ess = {abs(hf-h[-1]):.4f} m")

fig, ax = plt.subplots(2,1, figsize=(7.2,5.2), sharex=True)
ax[0].plot(t,h,color='#1f5fb0',lw=2,label='Nível h(t)')
ax[0].plot(t,r,ls='--',color='gray',label='Referência (0,6 m)')
ax[0].set_ylabel('Nível (m)'); ax[0].legend(loc='lower right'); ax[0].grid(True)
ax[0].set_title('Malha Fechada com PID - Seguimento de Referência')
ax[1].plot(t,u*1000,color='#b03030',lw=1.6,label='Vazão da bomba u(t)')
ax[1].axhline(Qmax*1000,ls=':',color='k',label='Saturação (20 L/s)')
ax[1].set_xlabel('Tempo (s)'); ax[1].set_ylabel('Vazão (L/s)')
ax[1].legend(loc='upper right'); ax[1].grid(True)
plt.tight_layout(); plt.savefig(os.path.join(RES, "03_malha_fechada_pid.png"), dpi=150)
print("Figura salva em resultados/03_malha_fechada_pid.png")
