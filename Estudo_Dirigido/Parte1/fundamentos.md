# Controle e Automação I — Etapa 1: Fundamentos Teóricos

## 1. Resumo Teórico

Um sistema dinâmico linear e invariante no tempo (LIT) pode ser descrito por uma equação diferencial ordinária com coeficientes constantes.

Aplicando a Transformada de Laplace com condições iniciais nulas, essa EDO se converte em uma equação algébrica.

A relação entre saída e entrada no domínio da frequência complexa define a função de transferência:

```math
G(s) = \frac{Y(s)}{U(s)}
```

Onde:

- `Y(s)` = transformada da saída
- `U(s)` = transformada da entrada

---

## 1.2 Polos e Zeros

### Zeros

São os valores de `s` que anulam o numerador de `G(s)`.

Eles afetam a distribuição de amplitude entre os modos do sistema.

### Polos

São os valores de `s` que anulam o denominador de `G(s)`.

Eles determinam os modos naturais do sistema.

A posição dos polos no plano complexo determina o comportamento dinâmico do sistema LIT.

---

## 1.3 Estabilidade

Um sistema LIT é BIBO estável se todos os polos possuem parte real negativa.

| Localização dos polos | Comportamento |
|---|---|
| Re(p) < 0 | Sistema estável |
| Re(p) = 0 | Marginalmente estável |
| Re(p) > 0 | Sistema instável |

### Critério de Routh-Hurwitz

Permite verificar estabilidade sem calcular explicitamente os polos.

Condições:

- coeficientes positivos
- primeira coluna da tabela de Routh positiva

---

## 1.4 Resposta Temporal

A resposta temporal é composta por:

```math
y(t) = natural(t) + forçada(t)
```

### Resposta natural

Depende:

- dos polos
- das condições iniciais

### Resposta forçada

Depende da entrada aplicada.

---

# 2. Formalização Matemática

## 2.1 Transformada de Laplace

| f(t) | F(s) |
|---|---|
| δ(t) | 1 |
| u(t) | 1/s |
| e^(-at) | 1/(s+a) |
| sen(ωt) | ω/(s²+ω²) |
| cos(ωt) | s/(s²+ω²) |
| te^(-at) | 1/(s+a)² |

---

## 2.2 Sistema de Primeira Ordem

Equação diferencial:

```math
\tau \dot y(t) + y(t) = K u(t)
```

Função de transferência:

```math
G(s) = \frac{K}{\tau s + 1}
```

Polo:

```math
p = -\frac{1}{\tau}
```

Resposta ao degrau:

```math
y(t) = K(1 - e^{-t/\tau})u(t)
```

Em:

```math
t = 5\tau
```

considera-se regime permanente atingido.

---

## 2.3 Sistemas de Segunda Ordem

Forma canônica:

```math
\frac{\omega_n^2}{s^2 + 2\zeta\omega_n s + \omega_n^2}
```

| ζ | Regime | Polos |
|---|---|---|
| ζ > 1 | Superamortecido | Dois reais negativos |
| ζ = 1 | Criticamente amortecido | Polo duplo |
| 0 < ζ < 1 | Subamortecido | Complexos conjugados |
| ζ = 0 | Não amortecido | Imaginários puros |
| ζ < 0 | Instável | Parte real positiva |

---

## 2.4 Parâmetros de Desempenho

| Parâmetro | Fórmula |
|---|---|
| Tempo de pico | \( t_p = \frac{\pi}{\omega_d} \) |
| Sobressinal | \( M_p = e^{-\pi \zeta / \sqrt{1-\zeta^2}} \times 100\% \) |
| Tempo de assentamento | \( t_s \approx \frac{4}{\zeta \omega_n} \) |
| Tempo de subida | \( t_r \approx \frac{\pi - \arccos(\zeta)}{\omega_d} \) |

---

# 3. Diagramas e Ilustrações

## Diagrama em malha aberta

Adicionar imagem:

```plaintext
U(s) → [G(s)] → Y(s)
```

## Plano de estabilidade

Adicionar imagem do plano complexo.

## Diagramas polo-zero

Adicionar imagens dos casos:

- polo real negativo
- polo real positivo
- polos complexos
- etc.

---

# 4. Análise dos Resultados

## Polos reais negativos

Produzem respostas exponenciais sem oscilação.

O polo dominante é o mais próximo da origem.

---

## Pares complexos conjugados

A frequência de oscilação é:

```math
\omega_d = \omega_n \sqrt{1-\zeta^2}
```

Envelope:

```math
e^{-\sigma t}
```

onde:

```math
\sigma = \zeta \omega_n
```

---

## Sobressinal

Para:

- ζ = 0.5 → Mp ≈ 16.3%
- ζ = 0.3 → Mp ≈ 37.2%

---

# 5. Aplicações Práticas

## 5.1 Sistemas de Primeira Ordem

### Circuito RC

```math
G(s) = \frac{1}{RCs + 1}
```

### Sistema térmico

Resposta gradual da temperatura.

### Tanque hidráulico

```math
\tau = \frac{A}{C}
```

---

## 5.2 Sistemas de Segunda Ordem

### Massa-mola-amortecedor

```math
\omega_n = \sqrt{\frac{k}{m}}
```

```math
\zeta = \frac{b}{2\sqrt{km}}
```

### Circuito RLC

```math
\omega_n = \frac{1}{\sqrt{LC}}
```

```math
\zeta = \frac{R}{2\sqrt{L/C}}
```

### Motor DC

Modelado como sistema de segunda ordem com polos reais negativos.