import numpy as np
import matplotlib.pyplot as plt

# ── Parâmetros do Motor DC ──────────────────────────────────────────────────
Ra = 1.0;  La = 0.01
J  = 0.01; b  = 0.1
Kt = 0.01; Kb = 0.01

# ── Parâmetros do PID ───────────────────────────────────────────────────────
Kp   = 50.0
Ki   = 100.0
Kd   = 5.0
T    = 0.001      # Período de amostragem: 1 ms
Ka   = 0.1        # Ganho anti-wind-up (back-calculation)
U_MIN, U_MAX = -12.0, 12.0

def pid_anti_windup(referencia_val, t_total, T, Kp, Ki, Kd, Ka,
                    u_min, u_max):
    N = int(t_total / T)
    t = np.linspace(0, t_total, N)

    # Variáveis de estado do motor
    ia = 0.0
    w  = 0.0

    # Variáveis internas do PID
    integral  = 0.0
    erro_ant  = 0.0
    u_raw_ant = 0.0
    u_sat_ant = 0.0

    # Vetores de resultado
    y_out = np.zeros(N)
    u_out = np.zeros(N)
    e_out = np.zeros(N)

    for k in range(N):
        referencia = referencia_val  # degrau constante

        # Erro atual
        erro = referencia - w

        # Integral com correção anti-wind-up (back-calculation)
        # Na primeira iteração não há u_ant ainda, usa só o erro
        if k == 0:
            integral += erro * T
        else:
            integral += (erro + Ka * (u_sat_ant - u_raw_ant)) * T

        # Ação derivativa
        derivada = (erro - erro_ant) / T

        # Sinal de controle (sem saturação)
        u_raw = Kp * erro + Ki * integral + Kd * derivada

        # Saturação do atuador
        u_sat = np.clip(u_raw, u_min, u_max)

        # ── Dinâmica do Motor DC (Euler progressivo) ──────────────────────
        dia_dt = (u_sat - Ra * ia - Kb * w) / La
        dw_dt  = (Kt * ia - b * w) / J
        ia += dia_dt * T
        w  += dw_dt  * T

        # Armazenar
        y_out[k]  = w
        u_out[k]  = u_sat
        e_out[k]  = erro

        # Atualizar memória
        erro_ant  = erro
        u_raw_ant = u_raw
        u_sat_ant = u_sat

    return t, y_out, u_out, e_out


# ── Executar simulação ──────────────────────────────────────────────────────
t, y, u, e = pid_anti_windup(
    referencia_val=1.0,
    t_total=2.0,
    T=T, Kp=Kp, Ki=Ki, Kd=Kd, Ka=Ka,
    u_min=U_MIN, u_max=U_MAX
)

# ── Gráficos ────────────────────────────────────────────────────────────────
fig, axes = plt.subplots(3, 1, figsize=(10, 9), sharex=True)

axes[0].plot(t, y, 'b', lw=2, label='Velocidade ω(t)')
axes[0].axhline(1.0, color='gray', ls='--', lw=1.2, label='Referência')
axes[0].set_ylabel('ω (rad/s)')
axes[0].set_title('PID Digital com Anti-Wind-Up – Motor DC (T = 1 ms)')
axes[0].legend(); axes[0].grid(True)

axes[1].plot(t, u, 'r', lw=2, label='Sinal de controle u(t)')
axes[1].axhline(U_MAX, color='k', ls=':', lw=1, label=f'Saturação (+{U_MAX}V)')
axes[1].axhline(U_MIN, color='k', ls=':', lw=1, label=f'Saturação ({U_MIN}V)')
axes[1].set_ylabel('u (V)')
axes[1].legend(); axes[1].grid(True)

axes[2].plot(t, e, 'g', lw=2, label='Erro e(t)')
axes[2].axhline(0, color='gray', ls='--', lw=1)
axes[2].set_ylabel('e(t)')
axes[2].set_xlabel('Tempo (s)')
axes[2].legend(); axes[2].grid(True)

plt.tight_layout()
plt.show()