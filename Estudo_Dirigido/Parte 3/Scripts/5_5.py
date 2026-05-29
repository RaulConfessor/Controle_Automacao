#include <stdio.h>
#include <math.h>

/* ── Estrutura do controlador PID ─────────────────────────────────────────── */
typedef struct {
    float Kp, Ki, Kd;
    float T;
    float integral;
    float erro_ant;
    float u_min, u_max;
} PID_t;

/* ── Inicialização ────────────────────────────────────────────────────────── */
void PID_init(PID_t *pid, float Kp, float Ki, float Kd,
              float T, float u_min, float u_max) {
    pid->Kp       = Kp;
    pid->Ki       = Ki;
    pid->Kd       = Kd;
    pid->T        = T;
    pid->integral = 0.0f;
    pid->erro_ant = 0.0f;
    pid->u_min    = u_min;
    pid->u_max    = u_max;
}

/* ── Cálculo do PID a cada amostra ───────────────────────────────────────── */
float PID_compute(PID_t *pid, float referencia, float medicao) {
    float erro     = referencia - medicao;
    float derivada = (erro - pid->erro_ant) / pid->T;

    pid->integral += erro * pid->T;

    float u = pid->Kp * erro
            + pid->Ki * pid->integral
            + pid->Kd * derivada;

    /* Saturação do atuador */
    if (u > pid->u_max) u = pid->u_max;
    if (u < pid->u_min) u = pid->u_min;

    pid->erro_ant = erro;
    return u;
}

/* ── Parâmetros do Motor DC ──────────────────────────────────────────────── */
#define Ra   1.0f
#define La   0.01f
#define J    0.01f
#define b_m  0.1f
#define Kt   0.01f
#define Kb   0.01f

/* ── Programa principal: simulação numérica ───────────────────────────────── */
int main(void) {
    /* Parâmetros de simulação */
    float T       = 0.001f;   /* Período de amostragem: 1 ms      */
    float t_total = 2.0f;     /* Tempo total de simulação: 2 s    */
    int   N       = (int)(t_total / T);

    /* Controlador PID */
    PID_t pid;
    PID_init(&pid, 50.0f, 100.0f, 5.0f, T, -12.0f, 12.0f);

    /* Estado inicial do motor */
    float ia = 0.0f;   /* Corrente de armadura [A]         */
    float w  = 0.0f;   /* Velocidade angular   [rad/s]     */

    float referencia = 1.0f;   /* Degrau unitário */

    /* Cabeçalho do CSV de saída */
    printf("tempo_s,velocidade_rad_s,controle_V,erro\n");

    for (int k = 0; k < N; k++) {
        float t_atual = k * T;

        /* 1. Calcula ação de controle */
        float u = PID_compute(&pid, referencia, w);

        /* 2. Integra dinâmica do motor (Euler progressivo) */
        float dia_dt = (u  - Ra * ia - Kb * w) / La;
        float dw_dt  = (Kt * ia - b_m * w)     / J;

        ia += dia_dt * T;
        w  += dw_dt  * T;

        /* 3. Registra resultado a cada 10 ms para não poluir saída */
        if (k % 10 == 0) {
            float erro = referencia - w;
            printf("%.4f,%.6f,%.6f,%.6f\n",
                   t_atual, w, u, erro);
        }
    }

    return 0;
}

/*
 * ── Como compilar e executar ──────────────────────────────────────────────
 *
 * Linux / macOS:
 *   gcc -o pid_motor pid_motor.c -lm
 *   ./pid_motor
 *
 * Windows (MinGW):
 *   gcc -o pid_motor.exe pid_motor.c -lm
 *   pid_motor.exe
 *
 * Para salvar os resultados e plotar no Python:
 *   ./pid_motor > resultado.csv
 *
 * ── Plotar o CSV no Python ────────────────────────────────────────────────
 * import pandas as pd, matplotlib.pyplot as plt
 * df = pd.read_csv('resultado.csv')
 * df.plot(x='tempo_s', y=['velocidade_rad_s','controle_V','erro'])
 * plt.grid(True); plt.show()
 */