"""
Parametros e funcoes comuns ao Projeto Final Integrado (controle de nivel de tanque).
Importado pelos scripts de cada questao. Tambem define a pasta de resultados.
"""
import os
import numpy as np

# ---- pasta de resultados (irma de 'simulacao') ----
HERE = os.path.dirname(os.path.abspath(__file__))
RES  = os.path.join(HERE, "..", "resultados")
os.makedirs(RES, exist_ok=True)

# ---- parametros fisicos do tanque ----
A    = 1.0      # area da secao transversal [m^2]  (tanque 1 m^2 x 1 m = 1000 L)
C    = 0.01     # condutancia da valvula de saida [m^2/s]   qout = C*h
Hmax = 1.0      # altura maxima [m]  (1000 L)
Qmax = 0.020    # vazao maxima da bomba [m^3/s]  (20 L/s @ 60 Hz)

tau = A / C            # constante de tempo [s]   = 100 s
K   = 1.0 / C          # ganho DC [s/m^2]         = 100

# ---- ganhos do controlador PID ----
Kp = 0.15
Ki = 0.010
Kd = 2.0
Tf = 4.0          # constante do filtro derivativo [s]
Tsamp = 0.5       # periodo de amostragem [s]


def simula(Kp, Ki, Kd, Tf, Tsamp, tfinal, href, d_func,
           anti_windup=True, deriv_filter=True, h0=0.0):
    """Integra o tanque (Euler, passo fino) com PID digital amostrado a Tsamp.
    Derivada sobre a medicao (evita 'derivative kick' no degrau de referencia)."""
    dt = 0.05
    n  = int(tfinal / dt)
    h  = h0
    h_prev = h0
    I = 0.0
    d_filt_prev = 0.0
    u = 0.0
    t_arr, h_arr, u_arr, e_arr, r_arr = [], [], [], [], []
    last_sample = -1e9
    Kaw = 1.0 / max(Tf, 1.0)          # ganho de back-calculation do anti-windup
    first = True
    for k in range(n):
        tk = k * dt
        r  = href(tk)
        # ---- amostragem do PID ----
        if tk - last_sample >= Tsamp - 1e-9:
            last_sample = tk
            e = r - h
            P = Kp * e                                   # proporcional
            I += Ki * Tsamp * e                          # integral (Euler progressivo)
            dmeas = 0.0 if first else -(h - h_prev) / Tsamp   # derivada sobre a medicao
            if deriv_filter:
                alpha = Tsamp / (Tf + Tsamp)
                d_filt = d_filt_prev + alpha * (Kd * dmeas - d_filt_prev)
            else:
                d_filt = Kd * dmeas
            u_unsat = P + I + d_filt
            u_sat = min(max(u_unsat, 0.0), Qmax)         # saturacao do atuador
            if anti_windup:
                I += Kaw * Tsamp * (u_sat - u_unsat)     # anti-wind-up
            u = u_sat
            h_prev = h
            d_filt_prev = d_filt
            first = False
        # ---- dinamica do tanque ----
        d = d_func(tk)                                   # perturbacao na vazao de saida
        qout = C * h + d
        h += (u - qout) / A * dt
        h = max(h, 0.0)
        t_arr.append(tk); h_arr.append(h); u_arr.append(u)
        e_arr.append(r - h); r_arr.append(r)
    return (np.array(t_arr), np.array(h_arr), np.array(u_arr),
            np.array(e_arr), np.array(r_arr))
