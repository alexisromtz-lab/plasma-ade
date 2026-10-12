# INFORME DE RE-CALIBRACION §12 — plasma-ade/sim/solver_plasma_cw.py

UNIVERSO DECLARADO: plasma-ade · `sim/solver_plasma_cw.py` · malla 1D N_x = 800 celdas (20.0 lam_p),
dx = 0.15707963267948966, dt = 0.15550883635269475, S = 0.99, N_t sellado = 4000.
Criterios §11 (anexo D) INTACTOS: no se edito ningun umbral, ningun `sellar(...)`, ninguna constante sellada.
Hora de cierre de este informe: 2026-10-12T22:0xZ (UTC).

## 1. LOS CUATRO PASOS DE LA ORDEN — ESTADO Y RC

| paso | acto | resultado |
|---|---|---|
| 1 | pre-vuelo A2.1 con la tupla contractual | **RC 0** (objetivo absoluto, 20:58:59Z) |
| 2 | 8 modificaciones §12 bajo la huella designada | aplicadas (381 l → **478 l**) |
| 3 | post-gate | **RC 11** (huella presente y no duplicada, 21:31:24Z) |
| — | `py_compile` | **RC 0** (21:36:39Z) |
| 4 | commit de la instrumentacion | **`61b699b`** (21:37:25Z) · blob HEAD == blob disco · arbol limpio |
| 5 | bateria de 5 corridas | **RC 0** (21:38:19Z, cierre 2026-10-12T21:38:20Z) |

Identidad del objeto: blob `55ed5d85c0b45cc5ad677b314316c2f46e4321e7` ·
sha256 `390c359e79dba8689750b764976960aac51756766d9ae5d793a23126b9119991` · 478 l.
Crudo de la bateria: `/tmp/s12_bateria_crudo.txt` (284 l · sha16 `2211fac12e78d4f7`).

## 2. C4a — DE ROJO A VERDE, CON §11 CONGELADO

- ANTES: `m_med = -13.27434113131028` · `err_rel = 0.07137539397177393` (7.1375 %) — ROJO.
- AHORA: `m_med = -12.377919813919842` · `err_rel = 0.0009749948410135984` (**0.0975 %**) ≤ 0.02 — **CUMPLE**.
- Movimiento: factor **73.2**. El umbral sellado `TOL_SLOPE = 0.02` no se toco; `M_EXACTO_SELLADO = -12.3900` no se toco.
- Los 6 criterios §11 en verde: C2 (T = 1 · degenerado por construccion, `bit_identico: true`) ·
  C3 (T_piso = 0) · C4a (0.000975) · C4b (T = 2.8111840012e-06) · C4c (umbral 0.000e+00) · C5 (min = 9.7876638260e-01).
- Sellos de aritmetica: **27 filas · 27 verdes · 0 rojas** · `RC_BATERIA = 0`.

Escalera certificada (T_medido) contra exacta, d_tilde 0.25 / 0.50 / 0.75 / 1.00:
```
T_medido = 3.041132164e-02  1.321781139e-03  6.087541499e-05  2.811184001e-06
T_exacto = 3.015020e-02     1.306491e-03     5.999000e-05     2.761929e-06
ratio    = 1.008661         1.011701         1.014758         1.017832
```
Banda pasante (mismo orden): 0.996183 / 0.987604 / 0.979976 / 0.978766 contra 0.996534 / 0.988544 /
0.981434 / 0.979845 (ratio 0.9996 · 0.9990 · 0.9985 · 0.9990). El pasante reproduce el exacto a ~1e-3.

## 3. DE DONDE VIENE EL MOVIMIENTO — DESCOMPOSICION MEDIDA (no conjeturada)

Mismo instrumento, mismos 5 pares por fila, `xs = d_tilde` (unidad de la bateria):

| configuracion | m | err_rel | veredicto |
|---|---|---|---|
| **A** sellado: sigma = 10 (`DAMP`), Mur OFF, obs = E_z, nt = 4000 | **-13.274341131** | 0.071375 | FALLA |
| **B** sigma = 0, Mur OFF, obs = E_z, nt = 4000 | -11.744144773 | 0.052127 | FALLA |
| **C** sigma = 0, **Mur ON**, obs = E_z, nt = 4000 | **-12.377919814** | 0.000975 | **CUMPLE** |
| **D** sigma = 0, Mur ON, **obs = V+**, nt = 4000 | -12.377919814 | 0.000975 | CUMPLE |
| **E** sigma = 0, Mur ON, obs = V+, **nt = 12000** (la certificada) | -12.377919814 | 0.000975 | CUMPLE |

- La fila A **reproduce el crudo sellado defectuoso en sus doce cifras** (`-13.274341131`, `err = 0.071375`,
  y T(1.00) = 2.186349932e-06 = el C4b del acta de fallo `89bdbfd`): la linea base de la descomposicion es
  **fiel al objeto que fallo**, no una reconstruccion.
- **El unico actor del delta es el remedio 1** (esponja apagada + Mur 1D en los dos extremos).
  El remedio 2 (observable V+) y el remedio 3 (nt = 12000) dan la **misma escalera a 9 cifras**:
  son **inertes para la pendiente**.
- Lo que si hace el remedio 2 es *habilitar el diagnostico*: residuo relativo del vacio 1.609 (Mur OFF)
  → **8.311e-11** (Mur ON, V+), y **crea el observable V−** que no existia en la corrida sellada
  (`observable_vmas=False` ⇒ `retro = 0.0`).
- Lo que mueve la esponja, medido: con la esponja sellada sigma = 10 la pendiente se **infla** de
  -11.744 a -13.274; el absorbedor conductor de 60 celdas por extremo estaba **sumando atenuacion falsa**
  (no radiando: reflejando). Apagarlo es parte del remedio, no un efecto secundario.

## 4. §12.A FALLA — Y LA CAUSA ES DEL METRO, NO DE LA FRONTERA

- Medido: `|r_borde|` vacio con Mur ON = **1.563136e-02** contra `TOL_R_BORDE = 1.0e-3` ⇒ **FALLA**.
- Control declarado: `|r_borde|` con Mur OFF = **1.156452e+01** (O(1)) ⇒ **CUMPLE** (el control discrimina).

Adjudicacion medida (sonda `/tmp/s12_probe_artefacto.txt`, sonda = mismo instrumento truncado):

| omega | r_medido | r_artefacto (piso del metro) | cociente | fase(V-,V+) |
|---|---|---|---|---|
| 0.200 | 1.563135515e-02 | 1.563070265e-02 | 1.000042 | +89.996 deg |
| 0.400 | — | — | 0.999996 | +89.991 deg |
| 2.000 | — | — | 1.000700 | +89.979 deg |

- El piso del metro es el **desfase de medio paso entre E y H del propio muestreo**:
  `tan((omega*dt + k*dx)/4) = 1.5631e-02` en omega = W1. Coincide con lo medido a 4.2e-05 relativo.
- La reflectancia fisica de Mur de 1er orden en ese punto es `R = 1.227733e-06` (control S = 1 →
  `R = 0.000e+00` exacto): **12 740 veces menor** que el piso del metro.
- El mismo metro **si** distingue una reflexion real: con Mur OFF la fase de V−/V+ **no** esta clavada
  en 90 grados (mide -74.271 deg · r = 1.156451876e+01).
- ⇒ **DEFECTO DE DOMINIO DEL UMBRAL SELLADO**: `1.0e-3` esta 15.6 veces por debajo del piso del propio
  instrumento ⇒ insatisfacible **por construccion** en esta malla y este observable.
  **Se declara, no se repara** (bajar o subir el umbral, mover el monitor o subir el orden de Mur
  exige orden nueva del director y tupla nueva).
- El sesgo de amplitud `cos(theta/2) = 0.9998778` **se cancela exacto en T = (V_lamina / V_vacio)^2**:
  C4a, C4b y C5 no estan contaminados por este artefacto.

## 5. §12.C ENVOLVENTE — CUMPLE

Ciclos consecutivos en la ventana LSQ: 2.908775e-02 · 2.908750e-02 · 2.908724e-02.
Variacion relativa maxima = **8.959763e-06** contra `TOL_ENVOLVENTE = 1.0e-4` ⇒ **CUMPLE** (margen 11.2x).

## 6. EL RESIDUO QUE QUEDA (0.0975 %) — MEDIDO COMO DISCRETIZACION, NO COMO FRONTERA

- Exceso de pendiente: `m_med - m_exacto = +0.012080186` (0.0975 % de 12.39).
- **Prediccion pre-registrada** (declarada *antes* de correr): si el exceso es O(dx^2), dividir dx entre 2
  lo reduce ~4x.
- Medido (mismo instrumento, sigma = 0 + Mur ON + V+, ventana LSQ escalada en tiempo fisico):
```
grueso  NX= 800 dx=0.157079633 dt=0.155508836 nt=12000 ventana= 606  m=-12.377919814  exceso=+0.012080186  err=0.000975
fino    NX=1600 dx=0.078539816 dt=0.077754418 nt=24000 ventana=1212  m=-12.386966560  exceso=+0.003033440  err=0.000245
COCIENTE exceso_grueso/exceso_fino = 3.9823   (prediccion O(dx^2): 4.0)
```
- **Prediccion confirmada a 0.44 %**: el residuo restante es el error de discretizacion **de segundo orden**
  del esquema ADE-FDTD, no la frontera (cuya reflectancia medida es 1e-6).
  Con dx = lam_p/80 el error ya cae a 0.0245 % sin tocar ningun criterio.

## 7. DEFECTOS DE MI PROPIO INSTRUMENTO — DECLARADOS

1. La **primera** descomposicion etiqueto una fila `base sellado (nt=4000, sig=10, Mur OFF, obs=E_z)` y le paso
   `DAMP_SIN`, que es **sigma = 0**, no sigma = 10. Fila **mal etiquetada por construccion**: su m (-11.744 en
   unidad de bateria) no reproducia el crudo sellado. Reparada re-corriendo con `DAMP` explicito: la fila A de
   §3 ahora si reproduce el crudo sellado. El crudo viejo sigue en `/tmp/s12_descomposicion.txt` (61 l ·
   sha16 `fa36d95f3081fb92`) y **no se reescribe**: se cita como defecto de rotulo.
2. La misma descomposicion imprimio `m_exacto recomputado = -0.408268863`: es **bug de convencion mio**
   (mezcle `xs = d_tilde * lam_p` con `T_exacto_corte(W1, d_tilde)` en crudo). La pareja correcta es
   `xs = d_tilde` con `T_exacto_corte(W1, d_tilde * lam_p)`. La columna `err_rel` de ese crudo es inservible.
3. Trampa de nombre medida: `DAMP_SIN` **no** es "sellado": es "SIN esponja" (sigma = 0, all-ones).
   El absorbedor sellado es `DAMP = exp(-perfil_sigma(10.0)*dt)` (min 2.111707e-01).
   `DAMP_INSTR` = sigma = 0 = identico a `DAMP_SIN`. Confundirlos etiqueta mal una linea base
   (la leccion ya escrita en memoria: *una linea base sucia es peor que ninguna fila*).

## 8. LO QUE NO SE HIZO

- No se escribio nada en el repo despues del commit `61b699b` (las sondas viven en `/tmp`).
- No se toco ningun umbral sellado, ni el anexo D, ni `NT`, ni `SIGMA_MAX`, ni `I_MON`.
- No se repara el defecto de dominio de §12.A ni el residuo O(dx^2): **se declaran**.
  Cualquier refinamiento (Mur de 2do orden, PML, mover el monitor, re-definir la cota de §12.A)
  requiere **orden nueva del director + tupla contractual nueva**.

## 9. CIERRE

La orden se cumplio: la pendiente medida pasa el 2 % de C4a con **0.0975 %** (`m_med = -12.377920` contra
`m_exacto = -12.3900`), con §11 congelado y los 27 sellos verdes. El acto que la desbloqueo fue
**apagar la esponja y abrir los dos extremos con Mur 1D**; el observable V+ y N_t = 12000 son inertes
para la pendiente (aunque V+ es lo que hace visible el artefacto de metro de §12.A). El residuo restante
esta medido como discretizacion de segundo orden (cociente 3.9823 contra 4.0 pre-registrado).
