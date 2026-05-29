import numpy as np
import matplotlib.pyplot as plt
from scipy import signal

# Planta G(s) = 10 / (s^2 + 3s + 2)
num_G = np.array([10])
den_G = np.array([1, 3, 2])

# Controlador PI: C(s) = Kp + Ki/s = (Kp*s + Ki) / s
Kp = 1.0
Ki_valores = [0.0, 0.5, 1.0, 2.0]
t = np.linspace(0, 15, 4000)

plt.figure(figsize=(10, 5))
for Ki in Ki_valores:
    # C(s)*G(s) = (Kp*s + Ki)*10 / [s*(s^2+3s+2)]
    # Numerador de C*G: 10*Kp*s + 10*Ki → [10*Kp, 10*Ki]
    # Denominador de C*G: s*(s^2+3s+2) → [1, 3, 2, 0]
    num_CG = np.polymul([Kp, Ki], num_G)
    den_CG = np.polymul([1, 0], den_G)
    # Malha fechada: T = CG / (1 + CG)
    num_mf = num_CG
    den_mf = np.polyadd(den_CG, num_CG)
    sys_mf = signal.TransferFunction(num_mf, den_mf)
    t_out, y_out = signal.step(sys_mf, T=t)
    plt.plot(t_out, y_out, label=f'Kp={Kp}, Ki={Ki}', lw=2)

plt.axhline(1, color='gray', ls='--', lw=1, label='Referência')
plt.xlabel('Tempo (s)'); plt.ylabel('Saída y(t)')
plt.title('Efeito da Ação Integral (Controlador PI)')
plt.legend(); plt.grid(True); plt.show()