# Estudo Dirigido Parte IV – Controle e Automação
**IFPB – Campus Campina Grande | 2026**
**Autor:** Raul Confessor Oliveira Silva

---

## Estrutura do Repositório

```
codigos/
├── 5_linguagens_CLP/
│   └── structured_text_exemplos.st   ← Seção 5.2 do relatório
└── 7_sistema_nivel/
    └── pid_controle_nivel.st         ← Seção 7.3 do relatório
```

---

## 5_linguagens_CLP / structured_text_exemplos.st

Corresponde à **Seção 5.2 – Linguagem Structured Text (ST)** do relatório.

Contém 5 exemplos progressivos em ST (IEC 61131-3):

| Exemplo | Descrição |
|---------|-----------|
| `PRG_Motor_Partida` | Partida direta com auto-retenção (selo), equivalente ao Ladder da Seção 5.1 |
| `PRG_Temporizador_Valvula` | Uso do bloco TON para acionar válvula após 5 s |
| `PRG_Contador_Pecas` | Contador CTU com reset automático ao atingir lote de 10 peças |
| `PRG_Controle_Temperatura` | Controle on/off com histerese e alarme de segurança |
| `PRG_Sequenciador_Ciclo` | Máquina de estados (CASE/OF) para ciclo automático de cilindro |

---

## 7_sistema_nivel / pid_controle_nivel.st

Corresponde à **Seção 7.3 – Programa ST: Malha PID de Nível** do relatório.

### Componentes implementados

**`FB_Escala`** – Function Block de escalonamento de sinal
- Converte valor bruto do ADC (0–27648 counts, padrão Siemens S7) para unidade de engenharia (0–100 %)
- Equação linear com saturação nos limites

**`FB_PID_Nivel`** – Function Block do controlador PID
- Algoritmo PID posicional com termos P, I e D separados
- Anti-windup por congelamento do integrador em saturação
- Chaveamento bumpless entre modo Manual e Automático
- Reset do integrador por sinal externo
- Parâmetros: Kp, Ti (s), Td (s), Ts (s), OUT_MIN, OUT_MAX

**`PRG_Controle_Nivel`** – Programa principal
- Lê sensor ultrassônico via módulo AI (4–20 mA)
- Escala sinal para 0–100 %
- Executa lógica de segurança (emergência, nível crítico)
- Chama controlador PID
- Converte saída Hz → counts para módulo AO (inversor de frequência)

### Parâmetros PID iniciais (ajustáveis via SCADA/IHM)

| Parâmetro | Valor | Descrição |
|-----------|-------|-----------|
| Kp | 1.2 | Ganho proporcional |
| Ti | 30.0 s | Tempo integral |
| Td | 5.0 s | Tempo derivativo |
| Ts | 0.1 s | Período de amostragem (ciclo de scan = 100 ms) |
| SP padrão | 70.0 % | Setpoint de nível |

### Hardware alvo
Compatível com qualquer CLP que suporte IEC 61131-3 ST (Siemens S7-1200/1500, Schneider Modicon, Beckhoff TwinCAT, OpenPLC Runtime).

---

## Como abrir no CODESYS / OpenPLC Editor
1. Criar novo projeto Standard Project
2. Criar `FUNCTION_BLOCK FB_Escala` e colar o código correspondente
3. Criar `FUNCTION_BLOCK FB_PID_Nivel` e colar o código correspondente
4. Criar `PROGRAM PRG_Controle_Nivel` e colar o código principal
5. Mapear variáveis `AI_NIVEL_BRUTO` e `AO_FREQ_INVERSOR` aos módulos físicos de I/O

---

## Referências
- IEC 61131-3 – Programmable Controllers: Programming Languages (2013)
- FRANCHI & CAMARGO – Controladores Lógicos Programáveis (Érica, 2008)
- OGATA, K. – Engenharia de Controle Moderno (Pearson, 2010)
