import numpy as np
import matplotlib.pyplot as plt
from scipy import signal

# Planta: Motor DC simplificado
Ra=1.0; La=0.01; J=0.01; b=0.1; Kt=0.01; Kb=0.01
num_G = [Kt]
den_G = [La*J, La*b + Ra*J, Ra*b + Kb*Kt]
G = signal.TransferFunction(num_G, den_G)

# Parâmetros PID sintonizados por Ziegler-Nichols
Kp = 50.0; Ki = 100.0; Kd = 5.0
num_C = [Kd, Kp, Ki]
den_C = [1, 0]

num_CG = np.polymul(num_C, num_G)
den_CG = np.polymul(den_C, den_G)
num_mf = num_CG
den_mf = np.polyadd(den_CG, num_CG)
sys_mf = signal.TransferFunction(num_mf, den_mf)

t = np.linspace(0, 2, 5000)
t_ma, y_ma = signal.step(G, T=t)
t_mf, y_mf = signal.step(sys_mf, T=t)

fig, axes = plt.subplots(1, 2, figsize=(12, 5))

axes[0].plot(t_ma, y_ma, color='red', lw=2, label='Malha Aberta')
axes[0].set_title('Resposta em Malha Aberta'); axes[0].grid(True)
axes[0].set_xlabel('Tempo (s)'); axes[0].set_ylabel('ω(t) [rad/s]')
axes[0].legend()

axes[1].plot(t_mf, y_mf, color='blue', lw=2, label='Malha Fechada c/ PID')
axes[1].axhline(1, color='gray', ls='--', lw=1, label='Referência')
axes[1].set_title('Resposta em Malha Fechada com PID'); axes[1].grid(True)
axes[1].set_xlabel('Tempo (s)'); axes[1].set_ylabel('ω(t) [rad/s]')
axes[1].legend()

plt.suptitle('Motor DC – Malha Aberta vs. Malha Fechada com PID',
             fontweight='bold')
plt.tight_layout(); plt.show()