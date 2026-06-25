(* ============================================================
   ESTUDO DIRIGIDO PARTE IV - Controle e Automação
   Seção 5.2 - Linguagem Structured Text (ST) - IEC 61131-3
   Autor: Raul Confessor Oliveira Silva
   IFPB - Campus Campina Grande, 2026
   ============================================================ *)


(* ----------------------------------------------------------
   EXEMPLO 1 - Partida direta de motor com intertravamento
   Equivalente ao Ladder da Seção 5.1, mas em ST.
   Variáveis: B_START (BOOL), B_STOP (BOOL), K_MOTOR (BOOL)
   ---------------------------------------------------------- *)
PROGRAM PRG_Motor_Partida
VAR
    B_START  : BOOL;   (* Botão liga (NA) *)
    B_STOP   : BOOL;   (* Botão desliga (NF) - normalmente TRUE *)
    K_MOTOR  : BOOL;   (* Bobina de saída do contator do motor *)
END_VAR

(* Lógica de selo (self-holding): liga pelo START ou pelo próprio selo,
   desliga quando STOP é acionado (lógica NF: B_STOP = FALSE ao pressionar) *)
IF (B_START OR K_MOTOR) AND B_STOP THEN
    K_MOTOR := TRUE;
ELSE
    K_MOTOR := FALSE;
END_IF;

END_PROGRAM


(* ----------------------------------------------------------
   EXEMPLO 2 - Temporizador TON e acionamento sequencial
   Aciona VALV_1 após 5 s de SENSOR_1 ativo.
   ---------------------------------------------------------- *)
PROGRAM PRG_Temporizador_Valvula
VAR
    SENSOR_1 : BOOL;            (* Sensor de entrada *)
    VALV_1   : BOOL;            (* Válvula de saída *)
    T1       : TON;             (* Bloco de função temporizador On-Delay *)
END_VAR

(* Aciona temporizador enquanto sensor estiver ativo *)
T1(IN := SENSOR_1, PT := T#5S);

(* Valvula só abre após os 5 segundos *)
VALV_1 := T1.Q;

END_PROGRAM


(* ----------------------------------------------------------
   EXEMPLO 3 - Contagem de peças e reset automático
   Conta pulsos de SENSOR_PECA até 10, então ativa SAIDA_LOTE
   e reseta o contador.
   ---------------------------------------------------------- *)
PROGRAM PRG_Contador_Pecas
VAR
    SENSOR_PECA : BOOL;    (* Sensor de presença de peça *)
    SAIDA_LOTE  : BOOL;    (* Sinaliza lote completo *)
    CTU_PECA    : CTU;     (* Contador crescente *)
    RESET_CTR   : BOOL;    (* Sinal interno de reset *)
END_VAR

(* Executa contador *)
CTU_PECA(CU := SENSOR_PECA, R := RESET_CTR, PV := 10);

(* Lote completo quando atingir 10 peças *)
SAIDA_LOTE := CTU_PECA.Q;

(* Reset automático ao completar o lote *)
IF CTU_PECA.Q THEN
    RESET_CTR := TRUE;
ELSE
    RESET_CTR := FALSE;
END_IF;

END_PROGRAM


(* ----------------------------------------------------------
   EXEMPLO 4 - Controle de temperatura com histerese
   Liga resistência quando temp < setpoint - histerese.
   Desliga quando temp > setpoint + histerese.
   ---------------------------------------------------------- *)
PROGRAM PRG_Controle_Temperatura
VAR
    TEMP_ATUAL      : REAL;    (* Temperatura lida (°C) *)
    SETPOINT        : REAL := 80.0;   (* Temperatura desejada (°C) *)
    HISTERESE       : REAL := 2.0;    (* Banda morta (°C) *)
    RESISTENCIA     : BOOL;    (* Saída: acionar resistência *)
    ALARME_ALTA     : BOOL;    (* Alarme de temperatura alta *)
    TEMP_MAX        : REAL := 95.0;   (* Limite de segurança *)
END_VAR

(* Alarme de segurança - prioridade máxima *)
IF TEMP_ATUAL >= TEMP_MAX THEN
    ALARME_ALTA  := TRUE;
    RESISTENCIA  := FALSE;   (* Desliga por segurança *)
ELSE
    ALARME_ALTA  := FALSE;

    (* Controle liga/desliga com histerese *)
    IF TEMP_ATUAL < (SETPOINT - HISTERESE) THEN
        RESISTENCIA := TRUE;     (* Temperatura baixa: liga *)
    ELSIF TEMP_ATUAL > (SETPOINT + HISTERESE) THEN
        RESISTENCIA := FALSE;    (* Temperatura alta: desliga *)
    (* Dentro da banda: mantém estado atual (histerese) *)
    END_IF;
END_IF;

END_PROGRAM


(* ----------------------------------------------------------
   EXEMPLO 5 - Sequenciador de estados (máquina de estados)
   Simula um ciclo automático: ESPERA -> AVANÇO -> RETORNO
   ---------------------------------------------------------- *)
PROGRAM PRG_Sequenciador_Ciclo
VAR
    (* Entradas *)
    BTN_CICLO   : BOOL;    (* Botão iniciar ciclo *)
    FIM_AVANCO  : BOOL;    (* Sensor fim de avanço *)
    FIM_RETORNO : BOOL;    (* Sensor fim de retorno / posição inicial *)

    (* Saídas *)
    SOL_AVANCO  : BOOL;    (* Solenóide de avanço *)
    SOL_RETORNO : BOOL;    (* Solenóide de retorno *)
    LAMP_AUTO   : BOOL;    (* Lâmpada de ciclo em andamento *)

    (* Variável de estado *)
    ESTADO      : INT := 0;
    (* 0 = ESPERA, 1 = AVANÇANDO, 2 = RETORNANDO *)
END_VAR

CASE ESTADO OF

    0: (* ESPERA - aguarda botão de ciclo com cilindro na origem *)
        SOL_AVANCO  := FALSE;
        SOL_RETORNO := FALSE;
        LAMP_AUTO   := FALSE;
        IF BTN_CICLO AND FIM_RETORNO THEN
            ESTADO := 1;
        END_IF;

    1: (* AVANÇANDO *)
        SOL_AVANCO  := TRUE;
        SOL_RETORNO := FALSE;
        LAMP_AUTO   := TRUE;
        IF FIM_AVANCO THEN
            ESTADO := 2;
        END_IF;

    2: (* RETORNANDO *)
        SOL_AVANCO  := FALSE;
        SOL_RETORNO := TRUE;
        LAMP_AUTO   := TRUE;
        IF FIM_RETORNO THEN
            ESTADO := 0;   (* Volta à espera *)
        END_IF;

    ELSE
        (* Estado inválido: reset de segurança *)
        ESTADO      := 0;
        SOL_AVANCO  := FALSE;
        SOL_RETORNO := FALSE;

END_CASE;

END_PROGRAM
