import numpy as np
import matplotlib.pyplot as plt

# Parâmetros do Motor DC (simulação numérica)
Ra=1.0; La=0.01; J=0.01; b=0.1; Kt=0.01; Kb=0.01

# Parâmetros do PID digital
Kp=50.0; Ki=100.0; Kd=5.0
T = 0.001  # Período de amostragem: 1 ms

# Simulação por integração numérica (Euler)
t_total = 2.0
N = int(t_total / T)
t = np.linspace(0, t_total, N)

# Variáveis de estado
ia = 0.0   # Corrente de armadura
w  = 0.0   # Velocidade angular

# Variáveis do PID
erro_ant = 0.0
integral = 0.0
referencia = 1.0  # Degrau unitário

y_out = np.zeros(N)
u_out = np.zeros(N)
e_out = np.zeros(N)

for k in range(N):
    # Erro atual
    erro = referencia - w

    # Ação PID (forma posicional)
    integral += erro * T
    derivada  = (erro - erro_ant) / T
    u = Kp * erro + Ki * integral + Kd * derivada

    # Saturação do atuador (±12 V)
    u = np.clip(u, -12.0, 12.0)

    # Dinâmica do motor (Euler progressivo)
    dia_dt = (u - Ra*ia - Kb*w) / La
    dw_dt  = (Kt*ia - b*w) / J
    ia += dia_dt * T
    w  += dw_dt  * T

    # Armazenar resultados
    y_out[k] = w
    u_out[k] = u
    e_out[k] = erro
    erro_ant = erro

# Gráfico
fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(10, 9), sharex=True)

ax1.plot(t, y_out, 'b', lw=2, label='Velocidade ω(t)')
ax1.axhline(referencia, color='gray', ls='--', label='Referência')
ax1.set_ylabel('ω (rad/s)'); ax1.legend(); ax1.grid(True)
ax1.set_title('PID Digital – Motor DC (T = 1 ms)')

ax2.plot(t, u_out, 'r', lw=2, label='Sinal de Controle u(t)')
ax2.axhline(12, color='k', ls=':', lw=1, label='Saturação (+12V)')
ax2.axhline(-12, color='k', ls=':', lw=1)
ax2.set_ylabel('u (V)'); ax2.legend(); ax2.grid(True)

ax3.plot(t, e_out, 'g', lw=2, label='Erro e(t)')
ax3.axhline(0, color='gray', ls='--')
ax3.set_ylabel('e(t)'); ax3.set_xlabel('Tempo (s)')
ax3.legend(); ax3.grid(True)

plt.tight_layout(); plt.show()