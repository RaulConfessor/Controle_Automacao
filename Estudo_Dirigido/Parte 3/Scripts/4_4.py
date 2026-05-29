import numpy as np
import matplotlib.pyplot as plt
from scipy import signal

# Planta G(s) = 10 / (s^2 + 3s + 2)
num_G = np.array([10])
den_G = np.array([1, 3, 2])

# PID com diferentes Kd (Kp e Ki fixos)
Kp = 1.0; Ki = 1.0
Kd_valores = [0.0, 0.2, 0.5, 1.0]
t = np.linspace(0, 15, 4000)

plt.figure(figsize=(10, 5))
for Kd in Kd_valores:
    # C(s) = (Kd*s^2 + Kp*s + Ki) / s
    num_C = [Kd, Kp, Ki]
    den_C = [1, 0]
    # C(s)*G(s): numerador e denominador por convolução
    num_CG = np.polymul(num_C, num_G)
    den_CG = np.polymul(den_C, den_G)
    # Malha fechada
    num_mf = num_CG
    den_mf = np.polyadd(den_CG, num_CG)
    sys_mf = signal.TransferFunction(num_mf, den_mf)
    t_out, y_out = signal.step(sys_mf, T=t)
    plt.plot(t_out, y_out, label=f'Kp={Kp}, Ki={Ki}, Kd={Kd}', lw=2)

plt.axhline(1, color='gray', ls='--', lw=1, label='Referência')
plt.xlabel('Tempo (s)'); plt.ylabel('Saída y(t)')
plt.title('Efeito da Ação Derivativa no Controlador PID')
plt.legend(); plt.grid(True); plt.show()