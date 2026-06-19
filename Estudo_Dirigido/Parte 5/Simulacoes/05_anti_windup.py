"""
Questao 5 - Efeito do anti-wind-up: setpoint alto (0,9 m) satura a bomba na partida.
Compara a resposta COM e SEM anti-wind-up (back-calculation).
"""
import os, numpy as np
import matplotlib.pyplot as plt
from _comum import Qmax, Kp, Ki, Kd, Tf, Tsamp, simula, RES

href = lambda t: 0.9
sem_dist = lambda t: 0.0
ta,ha,ua,_,_ = simula(Kp,Ki,Kd,Tf,Tsamp, 400, href, sem_dist, anti_windup=True)
tb,hb,ub,_,_ = simula(Kp,Ki,Kd,Tf,Tsamp, 400, href, sem_dist, anti_windup=False)
print(f"Mp com anti-windup = {(ha.max()-0.9)/0.9*100:.1f}%")
print(f"Mp sem anti-windup = {(hb.max()-0.9)/0.9*100:.1f}%")

fig, ax = plt.subplots(2,1, figsize=(7.2,5.2), sharex=True)
ax[0].plot(ta,ha,color='#1f7a1f',lw=2,label='Com anti-windup')
ax[0].plot(tb,hb,color='#b03030',lw=2,label='Sem anti-windup')
ax[0].axhline(0.9,ls='--',color='gray',label='Referência (0,9 m)')
ax[0].set_ylabel('Nível (m)'); ax[0].legend(loc='lower right'); ax[0].grid(True)
ax[0].set_title('Efeito do Anti-Wind-Up (referência satura a bomba)')
ax[1].plot(ta,ua*1000,color='#1f7a1f',lw=1.6,label='u(t) com anti-windup')
ax[1].plot(tb,ub*1000,color='#b03030',lw=1.6,label='u(t) sem anti-windup')
ax[1].axhline(Qmax*1000,ls=':',color='k',label='Saturação')
ax[1].set_xlabel('Tempo (s)'); ax[1].set_ylabel('Vazão (L/s)')
ax[1].legend(loc='upper right'); ax[1].grid(True)
plt.tight_layout(); plt.savefig(os.path.join(RES, "05_anti_windup.png"), dpi=150)
print("Figura salva em resultados/05_anti_windup.png")
