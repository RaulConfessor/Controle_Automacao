(* ============================================================
   ESTUDO DIRIGIDO PARTE IV - Controle e Automação
   Seção 7.3 - Programa ST – Malha PID de Nível
   Sistema: Controle de nível de tanque (1000 litros)
   Sensor: Ultrassônico 4–20 mA (0–100%)
   Atuador: Bomba centrífuga via inversor de frequência (0–60 Hz)
   Autor: Raul Confessor Oliveira Silva
   IFPB - Campus Campina Grande, 2026
   ============================================================ *)

(* ----------------------------------------------------------
   BLOCO DE FUNÇÃO: FB_PID_Nivel
   Implementação manual do algoritmo PID na forma posicional,
   com anti-windup por saturação e modo manual/automático.
   ---------------------------------------------------------- *)
FUNCTION_BLOCK FB_PID_Nivel
VAR_INPUT
    PV          : REAL;     (* Process Variable: nível atual (0.0–100.0 %) *)
    SP          : REAL;     (* Setpoint: nível desejado  (0.0–100.0 %) *)
    Kp          : REAL;     (* Ganho proporcional *)
    Ti          : REAL;     (* Tempo integral (s) — 0 desativa *)
    Td          : REAL;     (* Tempo derivativo (s) — 0 desativa *)
    Ts          : REAL;     (* Período de amostragem (s) *)
    OUT_MIN     : REAL;     (* Saída mínima (ex.: 0.0 Hz) *)
    OUT_MAX     : REAL;     (* Saída máxima (ex.: 60.0 Hz) *)
    MODO_AUTO   : BOOL;     (* TRUE = automático, FALSE = manual *)
    SAIDA_MAN   : REAL;     (* Saída em modo manual *)
    RESET       : BOOL;     (* Reset do integrador *)
END_VAR

VAR_OUTPUT
    OUT         : REAL;     (* Saída do controlador (frequência do inversor) *)
    ERRO        : REAL;     (* Erro atual: SP – PV *)
    SATURADO    : BOOL;     (* TRUE quando saída está saturada (anti-windup) *)
END_VAR

VAR
    erro_ant    : REAL;     (* Erro no ciclo anterior (derivativo) *)
    integ       : REAL;     (* Acumulador integral *)
    P_term      : REAL;
    I_term      : REAL;
    D_term      : REAL;
    saida_raw   : REAL;     (* Saída antes da saturação *)
END_VAR

(* ---------- Cálculo do erro ---------- *)
ERRO := SP - PV;

IF NOT MODO_AUTO THEN
    (* Modo manual: bypass do PID, apenas limita a saída *)
    OUT       := LIMIT(OUT_MIN, SAIDA_MAN, OUT_MAX);
    integ     := OUT / Kp;   (* Bumpless transfer: pre-carrega integrador *)
    erro_ant  := ERRO;
    SATURADO  := FALSE;
    RETURN;
END_IF;

IF RESET THEN
    integ    := 0.0;
    erro_ant := 0.0;
END_IF;

(* ---------- Termo Proporcional ---------- *)
P_term := Kp * ERRO;

(* ---------- Termo Integral (com anti-windup por back-calculation) ---------- *)
IF Ti > 0.0 AND NOT SATURADO THEN
    integ := integ + (Kp * Ts / Ti) * ERRO;
ELSE
    (* Congela integrador quando saturado (anti-windup) *)
END_IF;
I_term := integ;

(* ---------- Termo Derivativo (derivada da PV, evita kick) ---------- *)
IF Td > 0.0 AND Ts > 0.0 THEN
    D_term := Kp * (Td / Ts) * (ERRO - erro_ant);
ELSE
    D_term := 0.0;
END_IF;

(* ---------- Soma PID e saturação ---------- *)
saida_raw := P_term + I_term + D_term;

IF saida_raw > OUT_MAX THEN
    OUT      := OUT_MAX;
    SATURADO := TRUE;
ELSIF saida_raw < OUT_MIN THEN
    OUT      := OUT_MIN;
    SATURADO := TRUE;
ELSE
    OUT      := saida_raw;
    SATURADO := FALSE;
END_IF;

(* ---------- Atualiza estado para próximo ciclo ---------- *)
erro_ant := ERRO;

END_FUNCTION_BLOCK


(* ----------------------------------------------------------
   BLOCO DE FUNÇÃO: FB_Escala
   Converte valor bruto (ex.: 0–27648 ADC) para engenharia (%).
   Fórmula: y = (x - x_min) / (x_max - x_min) * (y_max - y_min) + y_min
   ---------------------------------------------------------- *)
FUNCTION_BLOCK FB_Escala
VAR_INPUT
    VALOR_BRUTO : REAL;
    BRUTO_MIN   : REAL;    (* Ex.: 0 para 0 V / 6400 para 4 mA em S7 *)
    BRUTO_MAX   : REAL;    (* Ex.: 27648 para 20 mA em S7 *)
    ENG_MIN     : REAL;    (* Ex.: 0.0 % *)
    ENG_MAX     : REAL;    (* Ex.: 100.0 % *)
END_VAR
VAR_OUTPUT
    VALOR_ENG   : REAL;
END_VAR

IF (BRUTO_MAX - BRUTO_MIN) <> 0.0 THEN
    VALOR_ENG := (VALOR_BRUTO - BRUTO_MIN) / (BRUTO_MAX - BRUTO_MIN)
                 * (ENG_MAX - ENG_MIN) + ENG_MIN;
    VALOR_ENG := LIMIT(ENG_MIN, VALOR_ENG, ENG_MAX);
ELSE
    VALOR_ENG := ENG_MIN;
END_IF;

END_FUNCTION_BLOCK


(* ----------------------------------------------------------
   PROGRAMA PRINCIPAL: PRG_Controle_Nivel
   Integra leitura do sensor, escala, PID e envio ao inversor.
   Ciclo de scan configurado para Ts = 100 ms no CLP.
   ---------------------------------------------------------- *)
PROGRAM PRG_Controle_Nivel
VAR
    (* --- Entradas físicas --- *)
    AI_NIVEL_BRUTO  : REAL;    (* Módulo AI: 0–27648 (representa 4–20 mA) *)
    DI_AUTO_MAN     : BOOL;    (* Chave auto/manual no painel *)
    DI_EMERG        : BOOL;    (* Botão de emergência (NF) *)
    DI_NIVEL_CRITICO: BOOL;    (* Sensor de bóia de nível crítico alto *)

    (* --- Saídas físicas --- *)
    AO_FREQ_INVERSOR: REAL;    (* Módulo AO: 0–27648 → 0–60 Hz no inversor *)
    DO_BOMBA_CMD    : BOOL;    (* Contator/permissão de partida da bomba *)
    DO_ALARME_NIVEL : BOOL;    (* Sirene/lâmpada de alarme *)

    (* --- Variáveis de processo (IHM / SCADA) --- *)
    NIVEL_PERCENT   : REAL;    (* Nível em % (0.0–100.0) *)
    SP_NIVEL        : REAL := 70.0;  (* Setpoint padrão: 70% *)
    FREQ_BOMBA_HZ   : REAL;    (* Frequência enviada ao inversor (Hz) *)
    SAIDA_MANUAL_HZ : REAL := 30.0; (* Valor manual via IHM *)

    (* --- Parâmetros PID (ajustáveis via SCADA) --- *)
    PID_Kp  : REAL := 1.2;    (* Ganho proporcional *)
    PID_Ti  : REAL := 30.0;   (* Tempo integral (s) *)
    PID_Td  : REAL := 5.0;    (* Tempo derivativo (s) *)
    PID_Ts  : REAL := 0.1;    (* Período de amostragem: 100 ms *)

    (* --- Instâncias dos blocos de função --- *)
    ESCALA_NIVEL : FB_Escala;
    CTRL_PID     : FB_PID_Nivel;

    (* --- Auxiliares internos --- *)
    FALHA_INV    : BOOL;       (* Falha do inversor de frequência *)
    RESET_PID    : BOOL;
END_VAR

(* ====================================================
   BLOCO 1 – ESCALONAMENTO DO SINAL DO SENSOR
   Converte 0–27648 (ADC Siemens S7) para 0.0–100.0 %
   (4 mA = 6400 counts; 20 mA = 27648 counts em S7)
   ==================================================== *)
ESCALA_NIVEL(
    VALOR_BRUTO := AI_NIVEL_BRUTO,
    BRUTO_MIN   := 6400.0,     (* 4 mA *)
    BRUTO_MAX   := 27648.0,    (* 20 mA *)
    ENG_MIN     := 0.0,
    ENG_MAX     := 100.0
);
NIVEL_PERCENT := ESCALA_NIVEL.VALOR_ENG;


(* ====================================================
   BLOCO 2 – LÓGICA DE SEGURANÇA E PERMISSÕES
   ==================================================== *)

(* Alarme de nível crítico alto (sensor de bóia) *)
DO_ALARME_NIVEL := DI_NIVEL_CRITICO OR (NIVEL_PERCENT >= 95.0);

(* Emergência ou nível crítico: desliga bomba e zera saída *)
IF NOT DI_EMERG OR DO_ALARME_NIVEL THEN
    DO_BOMBA_CMD    := FALSE;
    AO_FREQ_INVERSOR:= 0.0;
    RESET_PID       := TRUE;
    RETURN;   (* Sai do ciclo sem executar PID *)
ELSE
    RESET_PID := FALSE;
END_IF;

(* Permissão de operação normal *)
DO_BOMBA_CMD := TRUE;


(* ====================================================
   BLOCO 3 – CONTROLADOR PID DE NÍVEL
   ==================================================== *)
CTRL_PID(
    PV        := NIVEL_PERCENT,
    SP        := SP_NIVEL,
    Kp        := PID_Kp,
    Ti        := PID_Ti,
    Td        := PID_Td,
    Ts        := PID_Ts,
    OUT_MIN   := 0.0,      (* 0 Hz – bomba parada *)
    OUT_MAX   := 60.0,     (* 60 Hz – velocidade máxima *)
    MODO_AUTO := DI_AUTO_MAN,
    SAIDA_MAN := SAIDA_MANUAL_HZ,
    RESET     := RESET_PID
);

FREQ_BOMBA_HZ := CTRL_PID.OUT;


(* ====================================================
   BLOCO 4 – CONVERSÃO DA SAÍDA PARA O MÓDULO AO
   Transforma Hz (0–60) em counts (0–27648) para o DAC
   ==================================================== *)
AO_FREQ_INVERSOR := (FREQ_BOMBA_HZ / 60.0) * 27648.0;


END_PROGRAM
