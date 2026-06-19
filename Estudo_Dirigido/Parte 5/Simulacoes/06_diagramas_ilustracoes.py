"""Diagramas para o Projeto Final: malha fechada e esquema do tanque (P&ID)."""
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Circle, Rectangle, Polygon
import matplotlib
matplotlib.rcParams['font.size'] = 10
import os
HERE=os.path.dirname(os.path.abspath(__file__))
FIGDIR=os.path.join(HERE,"..","resultados")
os.makedirs(FIGDIR,exist_ok=True)

# ---------------- Diagrama de blocos malha fechada ----------------
fig, ax = plt.subplots(figsize=(8.4, 2.7))
ax.set_xlim(0, 14); ax.set_ylim(0, 4); ax.axis('off')

def box(x, y, w, h, text, fc):
    p = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.05,rounding_size=0.12",
                       fc=fc, ec='#222', lw=1.4)
    ax.add_patch(p)
    ax.text(x+w/2, y+h/2, text, ha='center', va='center', fontsize=9.5, weight='bold')

def arrow(x1, y1, x2, y2):
    ax.add_patch(FancyArrowPatch((x1, y1), (x2, y2), arrowstyle='-|>',
                 mutation_scale=14, lw=1.4, color='#222'))

# soma (comparador)
cx, cy = 2.2, 2.4
ax.add_patch(Circle((cx, cy), 0.32, fc='white', ec='#222', lw=1.4))
ax.text(cx, cy, '+', ha='center', va='center', fontsize=13, weight='bold')
ax.text(cx-0.02, cy-0.55, '-', ha='center', va='center', fontsize=15, weight='bold')

ax.text(0.2, cy+0.05, 'r(t)\nsetpoint', ha='left', va='center', fontsize=8.5)
arrow(1.15, cy, cx-0.34, cy)
ax.text(2.95, cy+0.28, 'e(t)', ha='center', fontsize=8.5)

box(3.4, 1.95, 2.5, 0.95, 'Controlador PID\nC(s)  (CLP)', '#cfe3f7')
arrow(cx+0.34, cy, 3.4, cy)

box(7.0, 1.95, 2.6, 0.95, 'Bomba + Tanque\nG(s)=K/(τs+1)', '#d6efd6')
arrow(5.9, cy, 7.0, cy)
ax.text(6.45, cy+0.28, 'u(t)', ha='center', fontsize=8.5)
ax.text(6.45, cy-0.30, 'vazão', ha='center', fontsize=7.5, color='#555')

# perturbacao
ax.text(8.3, 3.7, 'd(t) válvula', ha='center', fontsize=8, color='#b35900')
arrow(8.3, 3.5, 8.3, 2.92)

arrow(9.6, cy, 11.8, cy)
ax.text(11.95, cy+0.05, 'h(t)\nnível', ha='left', va='center', fontsize=8.5)

# sensor (realimentacao)
box(7.0, 0.35, 2.6, 0.8, 'Sensor de nível\nH(s)  (4–20 mA)', '#fde9c9')
arrow(10.7, cy, 10.7, 0.75); arrow(10.7, 0.75, 9.6, 0.75)
arrow(7.0, 0.75, cx, 0.75); arrow(cx, 0.75, cx, cy-0.34)

ax.set_title('Figura 1 – Malha de Controle de Nível em Malha Fechada', fontsize=10.5, weight='bold')
plt.tight_layout()
plt.savefig(f"{FIGDIR}/06_diagrama_blocos.png", dpi=150, bbox_inches='tight'); plt.close()

# ---------------- Esquema do tanque (P&ID simplificado) ----------------
fig, ax = plt.subplots(figsize=(7.0, 4.6))
ax.set_xlim(0, 10); ax.set_ylim(0, 10); ax.axis('off')

# tanque
ax.add_patch(Rectangle((3.2, 1.6), 3.4, 5.2, fill=False, ec='#222', lw=2.2))
# agua
ax.add_patch(Rectangle((3.25, 1.65), 3.3, 2.9, fc='#bfe0f5', ec='none'))
ax.text(4.9, 3.0, 'h(t)', ha='center', fontsize=12, weight='bold', color='#13507a')
# nivel de referencia (setpoint)
ax.plot([3.2, 6.6], [5.2, 5.2], ls='--', color='#b03030', lw=1.4)
ax.text(6.75, 5.2, 'setpoint', va='center', fontsize=8.5, color='#b03030')

# sensor ultrassonico no topo
ax.add_patch(Rectangle((4.4, 6.9), 1.0, 0.5, fc='#fde9c9', ec='#222', lw=1.4))
ax.text(4.9, 7.15, 'LT', ha='center', va='center', fontsize=9, weight='bold')
for dy in (0.0, 0.18, 0.36):
    ax.plot([4.65+0.0, 4.9], [6.9-dy*0.1, 6.55-dy], color='#1f7a1f', lw=0.8)
ax.annotate('Sensor ultrassônico\n(4–20 mA, 0–100%)', (5.5, 7.15), (7.2, 7.9),
            fontsize=8, ha='center',
            arrowprops=dict(arrowstyle='-|>', color='#444'))

# entrada (bomba + inversor)
ax.add_patch(Circle((1.4, 6.3), 0.45, fc='#d6efd6', ec='#222', lw=1.6))
ax.text(1.4, 6.3, 'M', ha='center', va='center', fontsize=11, weight='bold')
ax.add_patch(Rectangle((0.5, 7.1), 1.8, 0.55, fc='#cfe3f7', ec='#222', lw=1.4))
ax.text(1.4, 7.37, 'Inversor (VFD)', ha='center', va='center', fontsize=8)
ax.plot([1.4, 1.4], [6.75, 7.1], color='#222', lw=1.4)
# tubo de entrada
ax.plot([1.85, 3.2], [6.3, 6.3], color='#222', lw=2.2)
ax.annotate('qin (0–60 Hz)', (2.5, 6.3), (1.0, 5.3), fontsize=8, ha='center',
            arrowprops=dict(arrowstyle='-|>', color='#444'))

# saida (valvula manual = perturbacao)
ax.plot([4.9, 4.9], [1.6, 0.9], color='#222', lw=2.2)
ax.plot([4.9, 6.4], [0.9, 0.9], color='#222', lw=2.2)
# valvula
ax.add_patch(Polygon([(5.6,0.7),(5.6,1.1),(6.0,0.9)], closed=True, fc='white', ec='#222', lw=1.3))
ax.add_patch(Polygon([(6.0,0.9),(6.4,0.7),(6.4,1.1)], closed=True, fc='white', ec='#222', lw=1.3))
ax.annotate('Válvula manual\n(perturbação d)', (6.0, 0.9), (8.0, 1.4), fontsize=8, ha='center',
            arrowprops=dict(arrowstyle='-|>', color='#b35900'))
ax.text(4.6, 1.2, 'qout', ha='right', fontsize=8)

# CLP
ax.add_patch(Rectangle((7.6, 4.6), 2.0, 1.6, fc='#eeeeee', ec='#222', lw=1.6))
ax.text(8.6, 5.85, 'CLP', ha='center', fontsize=10, weight='bold')
ax.text(8.6, 5.3, 'PID + Ladder\n(IEC 61131-3)', ha='center', fontsize=7.5)
# linhas de sinal CLP<->sensor e CLP->inversor
ax.annotate('', (7.6, 5.6), (5.4, 7.15), arrowprops=dict(arrowstyle='-|>', color='#1f7a1f', ls='--'))
ax.annotate('', (2.3, 7.37), (7.6, 5.0), arrowprops=dict(arrowstyle='-|>', color='#1f5fb0', ls='--'))

ax.set_title('Figura 2 – Esquema do Sistema de Controle de Nível', fontsize=10.5, weight='bold')
plt.tight_layout()
plt.savefig(f"{FIGDIR}/07_esquema_tanque.png", dpi=150, bbox_inches='tight'); plt.close()
print("Diagramas gerados.")
