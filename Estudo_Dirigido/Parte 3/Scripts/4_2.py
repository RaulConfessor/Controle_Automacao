import numpy as np
import matplotlib.pyplot as plt
from scipy import signal

# Planta: G(s) = 10 / (s^2 + 3s + 2)
num_G = [10]
den_G = [1, 3, 2]

# Ganhos proporcionais a testar
Kp_valores = [0.1, 0.5, 1.0, 2.0, 5.0]
t = np.linspace(0, 10, 3000)

plt.figure(figsize=(10, 5))
for Kp in Kp_valores:
    # Malha fechada: T(s) = C(s)*G(s) / (1 + C(s)*G(s))
    # Com C(s) = Kp: T(s) = Kp*10 / (s^2 + 3s + 2 + 10*Kp)
    num_mf = [10 * Kp]
    den_mf = [1, 3, 2 + 10 * Kp]
    sys_mf = signal.TransferFunction(num_mf, den_mf)
    t_out, y_out = signal.step(sys_mf, T=t)
    plt.plot(t_out, y_out, label=f'Kp = {Kp}', lw=2)

plt.axhline(1, color='gray', ls='--', lw=1, label='Referência')
plt.xlabel('Tempo (s)'); plt.ylabel('Saída y(t)')
plt.title('Efeito da Ação Proporcional na Resposta ao Degrau')
plt.legend(); plt.grid(True); plt.show()