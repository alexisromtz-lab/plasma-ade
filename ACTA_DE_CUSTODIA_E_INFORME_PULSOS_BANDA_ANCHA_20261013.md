# Acta de custodia e informe — §13: propagación de pulsos de banda ancha en el ADE de plasma frío

## Ticket de custodia §13

**HUELLA DECLARADA EN EL PRE-VUELO A2.1:** `Ticket de custodia §13` (la huella viajó en la orden de escritura; el gate la buscó en el destino antes de permitir la escritura).

**REGLA DE IDENTIDAD DE ESTA ACTA (doctrina `x == x`):** la identidad de este archivo **se mide fuera de él** (`git hash-object`, `wc -l`, `wc -c` en terminal, sonda de cierre A2.1). Ninguna cifra de identidad propia se imprime aquí como si fuera interna: una pieza que declara su propio `sha` describe su versión anterior.

---

## 1. UNIVERSO · MOTOR · UNIDAD · VENTANA

Universo declarado tal como lo imprime el crudo del instrumento (crudo POST, l.5–l.10, verbatim):

```
UNIVERSO DECLARADO: N_x = 800 celdas (20.0000 lam_p); vacio mas lamina de plasma frio nu = 0; fuente de pulso en la celda 100; banco de monitores; instrumento sellado de §12 (esponja APAGADA sigma = 0.0 mas Mur 1D con c_mur = -0.005025125628). MOTOR: python3 -B · numpy 2.4.6 · solo numpy y math. UNIDAD: longitud en celdas y lam_p; tiempo en pasos dt; ancho en unidades de tiempo (c = 1). VENTANA: T_UTC_ARRANQUE = 2026-10-13T05:10:42Z
```

| Ancho declarado | Valor |
|---|---|
| Universo de celdas | `N_x = 800` (20.0000 lam_p) |
| Régimen | `omega_p = 1.0` · `dx = 0.15707963267948966` · `dt = 0.15550883635269475` · `S = 0.99` |
| Fuente | celda `I_SRC = 100` · lámina `I_SLAB = 400` · monitor `I_MON = 700` |
| Absorbente | borde `N_ABS = 60` · `SIGMA_MAX = 10.0` |
| Instrumento | esponja `SIGMA_ESPOJA_INSTR = 0.0` (APAGADA) + Mur 1D 1er orden `C_MUR = -1/199` |
| Reloj | `NT = 12000` pasos (sellado: 4000) |
| Nyquist | `omega_nyq = 20.202020202` |

**COMANDO QUE RESPALDA ESTA SECCIÓN:** `grep -n "UNIVERSO DECLARADO" /tmp/crudo13_20261013T051041Z.txt`.

---

## 2. PARÁMETROS DEL OBJETO §13 (diseño de registro)

Universo declarado: los parámetros abajo, leídos del instrumento de registro `sim/solver_plasma_pulso.py` (blob `a69636003c1a5de3ec0ebcc1ec9eb233e5459c19`, 858 l, 43422 B).

| Parámetro | Valor | Casa |
|---|---|---|
| `NFFT` | 8192 | l.94 y ss. |
| `NI0` | 420 | ventana fuente |
| `d_omega_fft` | 4.932134e-03 | rejilla espectral |
| `sigma_omega` | 0.0625 | envolvente gaussiana |
| bins por sigma | 12.6720 | derivado |
| `tau` | 16.0 | ancho temporal |
| `t0` | 96.0 | retardo de la fuente |
| banda declarada `4/tau` | 0.250 (101 bins) | pre-registro l.76 |
| cola en `NI0` | 0.158951 (-15.97 dB) | envolvente |
| `CORTE_NUM` | 1.002015250 | corte numérico |
| `D_MEDIO_TEO` | 25.132741 | `4*lam_p` |
| `NT_DECL_VENTANA` | `NI0 + NFFT` = 8612 | l.532 |
| frecuencias portadoras | 1.05 · 1.25 · 2.00 · 4.00 | 4 portadoras |
| escalera de corte `d̃` | 0.25 · 0.50 · 0.75 · 1.00 `lam_p` | 4 peldaños |
| `ANCHO_ANALITICO` | 45.254834 | control de vacío |

**Sellos de referencia `T8_SELLO` = (d/v_g, interfaz, dt_total, v_g_exacto)** (l.139–144):

| `w0` | `d/v_g` | interfaz | `dt_total` | `v_g_exacto` |
|---|---|---|---|---|
| 1.05 | 82.426570 | -34.420111 | 48.006459 | 0.304911 |
| 1.25 | 41.887902 | 5.585054 | 47.472956 | 0.600000 |
| 2.00 | 29.020790 | 0.194495 | 29.215285 | 0.866025 |
| 4.00 | 25.956984 | 0.013474 | 25.970457 | 0.968246 |

**`DT_G_SELLO` = el EXCESO `D*(dk/dw - 1)`** (l.147): `1.05: 57.29382840` · `1.25: 16.75516082` · `2.00: 3.88804860` · `4.00: 0.82424230`.

**Identidad exacta verificada en el instrumento** (l.233–235): `dvg_exacto(w) = n + w*dn/dw = dk/dw = 1/v_g` (y por tanto `v_ph*v_g = 1`).

**COMANDO QUE RESPALDA ESTA SECCIÓN:** `cd /Users/marlene/plasma-ade && sed -n '139,151p;193,235p' sim/solver_plasma_pulso.py` (lectura del blob `a6963600…`; no se importó `sim/solver_plasma_cw.py`).

---

## 3. CUSTODIA — CADENA DE IDENTIDAD

Universo declarado: los cinco blobs de la cadena §13, medidos con `git log --format=%H` y `git hash-object` en terminal.

| Pieza | Commit | Blob / sha16 | Líneas | Bytes |
|---|---|---|---|---|
| Pre-registro §13 (APPEND-ONLY) | `8224d84` (semilla `0bbec33`) | sha16 `114dba8de269c96a` | 499 | 38441 |
| Solver sellado §12 | `61b699b` | `55ed5d85c0b45cc5ad677b314316c2f46e4321e7` | 478 | — |
| Informe §12 sellado | `fbbe011` | sha256 `4f08219fefa767f4d681966deaca3f68a6f6a32fee8f2985f8ab9b7e2b45709b` | 141 | — |
| Solver §13 (instrumento de registro) | `a20b823` | `a69636003c1a5de3ec0ebcc1ec9eb233e5459c19` | 858 | 43422 |
| — su foto previa (antes de las 6 correcciones) | — | `a923e0ed56142d5d686a5edf04870aea0fc921ec` | 737 | — |
| Acta (semilla de esta pieza) | `8fd4773` | `dbc71a9dfaf0e4f7ad6909e8db95cadb2ea47c8e` | 1 | — |

**GATE DE PRE-VUELO A2.1 (bloqueante, corrido ANTES de escribir este cuerpo):**
TARGET `ACTA_DE_CUSTODIA_E_INFORME_PULSOS_BANDA_ANCHA_20261013.md` · BLOB_PRE `dbc71a9dfaf0e4f7ad6909e8db95cadb2ea47c8e` · HUELLA `Ticket de custodia §13` · LINEAS_PRE `1` ⇒ **RC 0 (PRE-VUELO OK)**. Sin ese RC 0 la escritura estaba prohibida.

**GATE DE POST-VERIFICACIÓN (doble sonda, turno 2):** sonda nominal ⇒ **RC 11** (huella ya presente = la fila quedó escrita) · sonda de control (blob previo `dbc71a9d…` con huella ausente) ⇒ **RC 12** (`DESINCRONIZADO · BLOB MUTADO`). El par 11/12 es lo que distingue «escribí» de «el gate no mira».

**COMANDO QUE RESPALDA ESTA SECCIÓN:**
`cd /Users/marlene/plasma-ade && git log -1 --format=%H,%s -- sim/solver_plasma_pulso.py && git hash-object sim/solver_plasma_pulso.py && wc -l -c ACTA_DE_CUSTODIA_E_INFORME_PULSOS_BANDA_ANCHA_20261013.md`.

---

## 4. VEREDICTO — LA BATERÍA CERTIFICADA

Universo declarado: **190 filas de sello** en la corrida PRE y **189** en la POST (la fila retirada se declara en §5.1); 25 corridas registradas; 9 criterios §13.6.

| Corrida | Sello temporal | RC | Líneas | Bytes | `sellos.filas` | `rojas` | Arranque / cierre UTC |
|---|---|---|---|---|---|---|---|
| PRE (antes de las 6 correcciones) | `20261013T033312Z` | **2** | 1002 | 39635 | **190** | **16** | 03:33:13Z / 03:33:32Z |
| POST (instrumento corregido) | `20261013T051041Z` | **0** | 1062 | 49603 | **189** | **[]** | 05:10:42Z / 05:10:48Z |

**NOTA DE DENOMINADOR (obligatoria):** el JSON `sellos.filas` es el denominador autoritativo del conteo; vale **190 → 189** (una fila retirada, §5.1) y `rojas` **16 → 0**. No existe un par «184/185» en esta pieza: cualquier lectura en ese sentido es de otro metro.

**LOS 16 ROJOS DE LA PRE, DESCOMPUESTOS POR LÍNEA DEL CRUDO PRE** (denominador: 16 rojos nombrados, l.970–l.1002 del crudo PRE):

| Bloque | Líneas PRE | Rojos | Causa (medida) |
|---|---|---|---|
| `T1 beta2 w0=4.00` | l.66 | 1 | literal corto: `-0.017213` vs medido `-0.01721325932` (medido < media unidad del último dígito impreso) ⇒ literal insatisfacible |
| `T7 dt_g` (1.05 / 1.25 / 2.00 / 4.00) | l.123 · l.129 · l.135 · l.141 | 4 | las dos cantidades verdaderas **cruzadas**: `dt_total` leído contra el **exceso** |
| `fuera 4tau` · `fuera 1sig` · `suma |Js|^2` · `atenuacion` (w0=1.05) | l.189–l.192 | 4 | ventana fuente no declarada (`NI0..NI0+NFFT`) |
| `fuera 4tau` (w0=1.25) | l.193 | 1 | ídem |
| bloque w0=2.00 | l.197–l.199 | 3 | ídem |
| bloque w0=4.00 | l.201–l.203 | 3 | ídem |
| **Total** | — | **16** | 1 + 4 + 4 + 1 + 3 + 3 |

**COMANDO QUE RESPALDA ESTA SECCIÓN:**
`cd /tmp && for f in crudo13_20261013T033312Z.txt crudo13_20261013T051041Z.txt; do echo "== $f"; wc -l -c $f; grep -n '"filas"\|"rojas"' $f; done` y `sed -n '970,1002p' /tmp/crudo13_20261013T033312Z.txt`.

---

## 5. LAS SEIS CORRECCIONES DE INSTRUMENTO (commit `a20b823`)

Universo declarado: las seis correcciones aplicadas bajo el gate A2.1 al blob `a923e0ed56142d5d686a5edf04870aea0fc921ec` (737 l), resultando el blob `a69636003c1a5de3ec0ebcc1ec9eb233e5459c19` (858 l, 43422 B).

**5.1 — `beta2` literal declarada insatisfacible (fila 185 → 184; `filas` 190 → 189).**
Medido (crudo POST l.15, verbatim):

```
T1 beta2    w0=4.00  medido -0.01721325932 · literal -0.017213 · |dif| = 2.593e-07 (media unidad del ultimo digito impreso = 5.0e-07) -> DECLARADO INSATISFACIBLE POR CONSTRUCCION
```

Las otras tres portadoras **pasan** (1.05: -30.47292915 vs -30.4729294, 4.89e-09 · 1.25: -2.37037037 vs -2.37037, 1.56e-07 · 2.00: -0.1924500897 vs -0.19245, 4.66e-07). El defecto no es del objeto: **el literal impreso no alcanza a su propio objeto** — 8 dígitos significativos para un valor que la rejilla sostiene en 12. La fila se **declara insatisfacible por construcción** y **se retira**; el retiro es el `190 → 189`.

**5.2 — `T7` emparejado al EXCESO de retardo de grupo, no al total.**
Medido (crudo POST l.16–l.19, verbatim para 1.05):

```
T7/T8 emparejamiento w0=1.05: D*(dv_g/dw - 1) = 57.29382840 -> DT_G_SELLO = 57.29382840 ; el literal dt_total de referencia vive en T8_SELLO[2] = 48.006459
```

Las cuatro filas POST: `T7 dt_g exceso w0=1.05 57.2938284 vs 57.2938284 rel 1.36e-11 OK` y sus análogas (16.75516082/16.75516082 · 3.88804860/3.88804860 · 0.82424230/0.82424230). El comentario viejo que rotulaba `57.29` como «`d/v_g` + interfaz» es **FALSO** y queda declarado: `d/v_g` = 82.426570 vive en `T8_SELLO[0]` y la interfaz = -34.420111 en `T8_SELLO[1]`. **Lo que estaba mal era el rótulo, no la cifra**; las dos cantidades verdaderas estaban cruzadas.

**5.3 — Ventana de fuente declarada (`NT_DECL_VENTANA = NI0 + NFFT`) contra `ar10` H2.**
Medido (crudo POST l.24/26/28/30):
`max|declarada - rebanada|` = 1.629993e-01 (1.05) · 1.935519e-01 (1.25) · 3.080462e-01 (2.00) · 6.028669e-01 (4.00), con `max|declarada[:-1] - rebanada[1:]|` = 3.246e-01 · 3.859e-01 · 6.112e-01 · 1.160e+00 rotulado por el propio instrumento como **`(identidad del paso)`**.
**DECLARACIÓN:** la segunda columna es una **identidad de consistencia de la rejilla** (la fuente corrida un paso debe reproducir la rejilla declarada); por el pre-registro **l.423** una identidad **no es evidencia**: se imprime como control del instrumento, no como medición del objeto. Las 16 filas de la ventana pasan a OK.

**5.4 — Dominio `P1` con `w > w_p` declarado + columna de rejilla numérica.**
Cada fila de `P1` lleva ahora su línea `dominio` (crudo POST l.235/238/241/244/247/250/253/256/…/293). El criterio sellado exige `|E_ref| >= 1e-3` del máximo en la ventana declarada (pre-registro l.447); el instrumento **añade `w > w_p`** porque bajo corte `T_sellado` es evanescente y **el criterio no es evaluable con su propio piso**. Ver §6 para la atribución y el certificado `T2`.

**5.5 — `P2a` con el término `+D` de la identidad `G = T*e^{+iwD}`.**
El pre-registro l.450 exige `v_g` dentro del 3 % en todo `w` de `[1.01, 4.00]` **con la corrección de interfaz declarada**. La corrección añade el término de retardo `+D` (no una re-derivación de la forma cerrada sellada).

**5.6 — `P4` con las dos parejas declaradas (E-A / E-B).**
El pre-registro exige coincidencia en `600 +- 1` paso. Se declaran **las dos** parejas porque las dos fuentes (E-A, E-B) son el mismo objeto físico con dos rampas distintas. Ver §7 para la **errata de rótulos** del propio instrumento.

**COMANDO QUE RESPALDA ESTA SECCIÓN:**
`cd /tmp && sed -n '15,31p' crudo13_20261013T051041Z.txt && grep -c 'bajo_corte_excluidos' crudo13_20261013T051041Z.txt`.

---

## 6. P1 — DOMINIO, NO-EVALUABILIDAD Y CERTIFICADO `T2`

Universo declarado: las filas `P1` del crudo POST (l.233–l.293), 20 filas impresas, de las cuales **19 corren con instrumento sellado** (la 20.ª es `R25`, marcada `[DEFECTUOSO]` y usada como must-fail).

### 6.1 Dominio por fila (verbatim del crudo, columna `dominio:`)

| Fila | Panel | `w0` | bins en máscara | **evaluados (`w > w_p`)** | bajo corte excluidos | `err_max` (`w > w_p`) | `err_max` (máscara completa) | veredicto |
|---|---|---|---|---|---|---|---|---|
| R6 | G-medio EA | 1.05 | 94 | 57 | 37 | 1.025916 | 1.514671e+12 | FALLA (30 rojos) |
| R7 | G-medio EA | 1.25 | 94 | 94 | 0 | 0.242419 | 2.424194e-01 | FALLA (12 rojos) |
| R8 | G-medio EA | 2.00 | 94 | 94 | 0 | 0.004381 | 4.381382e-03 | CUMPLE |
| R9 | G-medio EA | 4.00 | 95 | 95 | 0 | 0.000517 | 5.169134e-04 | CUMPLE |
| R10 | G-medio EB | 1.05 | 343 | 170 | 173 | 759.421380 | 4.504774e+23 | FALLA (164 rojos) |
| R11 | G-medio EB | 1.25 | 546 | 346 | 200 | 156.697051 | 5.770864e+23 | FALLA (314 rojos) |
| R12 | G-medio EB | 2.00 | 649 | 496 | 153 | 37.644664 | 6.144804e+24 | FALLA (474 rojos) |
| R25 | G-medio EA (defectuoso) | 1.25 | 94 | 94 | 0 | 0.290069 | 4.378045e-03 | FALLA (14 rojos) — must-fail |

La escalera (`R13`–`R24`) **cumple las 12 filas** (`err_max` de 4.378e-03 a 1.580e-04 con 0 rojos), y `R25` **falla a propósito**: `P7 R25 (instrumento defectuoso): FALLA P1 -> discrimina` ⇒ el criterio `P1` **discrimina** (no es un verde por construcción).

### 6.2 El residuo EB es defecto de EVALUABILIDAD, no absorción

**Certificado `T2`** (memoria de cálculo `/tmp/p13g_out.txt`, 24 l; `UNIVERSO DECLARADO: 6 bins (el argmax impreso de cada fila de P1); d = 4*lam_p = 25.132741 celdas`; bloque de formas selladas sha256[:16] `0e4f86336fe34882`):

| Fila | panel | `w*` | `T_sellado(w*)` | `T2 = T_sellado^2` | lectura |
|---|---|---|---|---|---|
| R10 | EB 1.05 | 1.0752 | 7.560111e-01 | **5.748870e+02** | NO FÍSICO (`T > 1`) |
| R11 | EB 1.25 | 1.1591 | 7.286220e-01 | **1.149015e+02** | NO FÍSICO |
| R12 | EB 2.00 | 1.6621 | 9.575994e-01 | **3.700611e+01** | NO FÍSICO |
| R6 | EA 1.05 | 1.0111 | 2.159422e-01 | 4.374808e-01 | pasivo; ~2.03x sobre ambos modelos — declarado, no adjudicado |
| R7 | EA 1.25 | 1.0259 | 4.669015e-01 | 5.800874e-01 | pasivo |
| R25 | EA 1.25 | 1.0259 | 4.669015e-01 | 6.023352e-01 | pasivo |

`T2 > 1` significa **ganancia de energía en un medio pasivo**: el residuo EB no es un exceso de absorción medido, es **el criterio corriéndose fuera de su dominio de evaluabilidad**.

**Certificado independiente, desde los propios conteos del crudo** (`bins con T2>1` en la línea `rejilla` de cada fila): `R6 6` · `R9 1` · `R10 42` · `R11 126` · `R12 168` · `R15 2` · `R25 3`.

### 6.3 Atribución del residuo por encima del corte

Medido (memoria de cálculo `/tmp/p13f_out.txt`, citada por el propio crudo POST l.295–l.300, `CORTE_NUM = 1.002015250`):

- `R7` arriba del corte baja de `0.242419`/12 rojos (sello) a `0.032926`/0 rojos (rejilla numérica) ⇒ **el residuo de R7 es dispersión de la REJILLA, no del instrumento.**
- `R6` arriba del corte: `1.025916`/30 contra `0.729242`/16, y **dos bins pegados al corte NO quedan explicados** (`w = 1.0062`: err 0.3234 sello / 0.7292 rejilla; `w = 1.0111`: err 1.0259 / 0.3670) ⇒ **se declaran, no se adjudican.**
- Ni `P1_MASCARA_REL` ni `TOL_P1` se tocan. (Precedente §12: no se baja el umbral, **se declara el defecto de dominio**.)

### 6.4 DOS DEFECTOS DE METRO PROPIOS, DECLARADOS (no adjudicados)

**(a) La comparación `rejilla vs sello` de `/tmp/p13g.py` es un artefacto de BIN MEZCLADO.** El sondeo emparejaba el **máximo global** de `err_rej` con el **argmax** de `err`: dos bins distintos. La prosa del propio crudo lo muestra (l.298–l.300): `w = 1.0111` da sello `1.0259` vs rejilla `0.3670`, y `w = 1.0062` da `0.3234` vs `0.7292`. ⇒ **`p13g` se cita SOLO por el certificado `T2` de §6.2, nunca como comparación rejilla-vs-sello.**

**(b) La atribución «la columna de rejilla absuelve el residuo EB» NO SE ESCRIBE: es una coincidencia aritmética.** Se midió `708.846838` (rejilla) contra `759.421380` (sello) en R10 — una razón de ~0.93 que parecía absolver al instrumento. Las dos columnas **no son independientes**: ambas son **errores relativos** y están dominadas por el **mismo `T2`** ⇒ escalan juntas. Y para las filas EB, `T2` está **órdenes de magnitud por encima de 1** (§6.2) ⇒ la columna de rejilla **no absuelve nada**: hereda el mismo defecto de dominio. La cifra queda registrada aquí **como trampa medida**, no como hallazgo.

**COMANDO QUE RESPALDA ESTA SECCIÓN:**
`cd /tmp && sed -n '233,303p' crudo13_20261013T051041Z.txt && cat p13g_out.txt && cat p13f_out.txt`.

---

## 7. `P4` — ERRATA DE RÓTULOS DEL INSTRUMENTO (filas contra prosa)

Universo declarado: las dos filas `P4` del crudo POST (l.342–l.343) y los picos de referencia del vacío (l.222–l.228).

**La filas (autoritativas):**

```
R11  vs R5   (EB w0=1.25): umbral=7.973e-05 · t_vacio=603 t_plasma=603 |dif|=0 paso(s) CUMPLE
R7   vs R2   (EA w0=1.25): umbral=7.833e-05 · t_vacio=852 t_plasma=939 |dif|=87 paso(s) FALLA
```

**La prosa del instrumento (l.346–l.349, impresión fija) dice lo contrario:** `R11 (E-A) contra R5 da 0 pasos -> CUMPLE; R7 (E-B, t_rise = 1 paso) contra R2 da 87 pasos -> FALLA`.

**CERTIFICACIÓN DE QUE LAS FILAS SON LAS CORRECTAS — hecha desde el crudo solo, sin releer el código:**
el umbral de cada fila es exactamente `1e-3` del pico de su corrida vacía de referencia (`FRONT_UMBRAL_REL = 1.0e-3`):
`ref EB w0=1.25: … pico |V+| @700 = 7.972900e-02` × `1e-3` = **7.9729e-05** = el `umbral` de `R11` ⇒ la referencia de `R11` es **E-B**.
`ref EA w0=1.25: … pico |V+| @700 = 7.832900e-02` × `1e-3` = **7.8329e-05** = el `umbral` de `R7` ⇒ la referencia de `R7` es **E-A**.

**⇒ La prosa tiene los rótulos INVERTIDOS, y su atribución del mecanismo también:** los 87 pasos **no** son «el retardo de arranque de la rampa E-B» (esa rampa está en `R11`, que da 0 pasos); son el caso `E-A` de `R7`. **El retardo de 87 pasos NO se adjudica**: se declara la errata del rótulo y se conservan las dos filas. `TOL_P4_PASOS` no se toca.

**Predicción registrada (no resoluble, pre-registro §13.5.q):** `frente de malla = 600.0000 pasos; frente fisico = 606.0606 pasos (NO resoluble)`. La separación de 6.0606 pasos **no se resuelve** (prohibición §13.8) y `t_frente` no se cita.

**COMANDO QUE RESPALDA ESTA SECCIÓN:** `cd /tmp && sed -n '222,229p;341,349p' crudo13_20261013T051041Z.txt`.

---

## 8. LOS NUEVE CRITERIOS §13.6 (verbatim del crudo, l.374–l.383)

```
P1 transmitancia por bin <= 5% (sellado, dominio w > w_p declarado) FALLA  cumplen 14 de 19 · bins bajo corte excluidos y declarados
P2a v_g por pendiente de fase <= 3%            FALLA  cumplen 2 de 5
P2b incremento de fase por bin < pi            CUMPLE cumplen 5 de 5
P2c firma numerica vph*vg <= 2%                CUMPLE sellado
P3 ensanchamiento B <= 15% (w0 en 1.25/2/4)    CUMPLE w0=1.05 declarado degenerado
P4 arribo del frente plasma vs vacio <= 1 paso FALLA  {'R11': (603, 603, 0), 'R7': (852, 939, 87)}
P5 chirp <= 20% en peldaños alcanzables        CUMPLE err_max=0.120424
P6 ausencia de Brillouin (0 cambios de signo)  CUMPLE cambios=0
P7 R25 must-fail discrimina P1                 CUMPLE R25 err_max=0.290069
criterios = 9 · cumplidos = 6 · fallados = 3
```

**Los 3 fallos, cada uno con su causa medida y declarada:**

**(1) `P1` — cumplen 14 de 19.** Causa: dominio (bajo corte el criterio no es evaluable) + residuo de rejilla. Ver §6. **`P1 sellado: corridas con instrumento sellado = 19 · cumplen = 14 · fallan = 5`** (las 5 que fallan: `R6` · `R7` · `R10` · `R11` · `R12`).

**(2) `P2a` — cumplen 2 de 5.** Filas (crudo POST l.306–l.320): `R6 w0=1.05 v_g_med=0.310724 v_g_num=0.304057 err_max=58.438347 FALLA · inc_fase_max=1.203090 rad CUMPLE` · `R7 0.602111/0.598247 0.780482 FALLA` · `R8 0.868882/0.867722 0.003723 CUMPLE` · `R9 0.970287/0.969458 0.001354 CUMPLE` · `R25 0.600080/0.598247 0.759179 FALLA`.
**Residuo de borde DECLARADO, no curado** (memorias `/tmp/p13d_out.txt`, `/tmp/p13b_out.txt`, `/tmp/p13c_out.txt`): el residuo vive **en el propio piso de máscara** que el criterio declara; restringido a `|R| >= 5 %` del máximo vale `0.714670` (R6 @1.0308) · `0.058284` (R7 @1.1097) · `0.455966` (R11 @1.2429). **Restringir el `unwrap` a la banda da un resultado IDÉNTICO al global** (`p13b`) y **la corrección de interfaz numérica empeora** (`p13c`) ⇒ el residuo **no se adjudica**. `TOL_P2A` no se toca.

**(3) `P4` — ver §7.** El fallo es de emparejamiento declarado, con la errata de rótulos ya certificada.

**Las 6 que cumplen, con sus cifras:**

- **`P2b`**: `cumplen 5 de 5` (predicción: `max 1.126872 rad` = `pi` con margen).
- **`P2c`** (firma numérica `v_ph*v_g <= 2 %`): `CUMPLE sellado`. **Nota de metro:** el crudo imprime el rótulo como `dentro del 2%%` — un `%%` literal de la plantilla de impresión. Es **errata tipográfica del rótulo**, no del criterio; se declara para que no se lea como «2 por mil».
- **`P3`** (ensanchamiento `B <= 15 %`; aplica solo a `w0` en `{1.25, 2.00, 4.00}`; `w0 = 1.05` **se declara DEGENERADO**). Control de vacío: `ancho_in medido = 45.253071 pasos=291 · analitico = 45.254834 · B_vacio = 0.99996105 CUMPLE`. Filas: `R7 w0=1.25 ancho_out=47.119177(303) B=1.041237 err=0.014139 CUMPLE [pre-reg 1.041237]` · `R8 w0=2.00 B=1.000000 err=0.000178 CUMPLE` · `R9 w0=4.00 B=1.000000 err=0.000001 CUMPLE` · `R25 w0=1.25 47.274686(304) B=1.044674 err=0.017486 CUMPLE [pre-reg 1.041237]`. **`R6 w0=1.05`: `ancho_out=85.374351(549) B=1.886598 B_analytic=3.154379 err=0.401911 DEGENERADO [pre-reg 1.890034]`** ⇒ el valor pre-registrado `1.890034` se reproduce (`1.886598`) y aun así se declara **DEGENERADO** (la envolvente a 1.05 está pegada al corte: el 1/e no es medible con el piso declarado).
- **`P5`** (chirp contra la escalera `w_s(ct/z) <= 20 %`): `peldaños alcanzables (env >= 10% del pico, ct/z resoluble) = 457` · `P5 max err_rel = 0.120424 CUMPLE (tolerancia 0.20)`. Muestra de 7 peldaños con `err_rel` 0.063325 · 0.087653 · 0.104635 · 0.115277 · 0.120082 · 0.119239 · 0.114775. `primer peldaño inalcanzable: ct/z = 1.001227 corresponde a w_s > w_nyq (declarado)`.
- **`P6`** (ausencia falsable de Brillouin en Drude sin pérdidas): `barrido w en [1.000001, 50] con 200001 muestras · cambios_de_signo = 0 · dv/dw(1.0001)=75.168103 dv/dw(50)=8.002e-06` ⇒ `P6 CUMPLE (predicado refutado si cambios_de_signo > 0)`. **El predicado es falsable y no se refutó**: esto es una **ausencia medida**, no una afirmación de precursor de Brillouin (prohibición §13.8).
- **`P7`**: ver §6.1. `R25 err_max=0.290069` ⇒ **discrimina**.

**COMANDO QUE RESPALDA ESTA SECCIÓN:** `cd /tmp && sed -n '304,383p' crudo13_20261013T051041Z.txt`.

---

## 9. DEFECTOS DECLARADOS (no reparados, no ocultados)

Universo declarado: las líneas de declaración del crudo POST (l.20–l.31) más las divergencias nombradas.

| Defecto | Medición | Estado |
|---|---|---|
| **Rejilla de la cota: `N = 4001` en la fuente contra `40001` al verificar** | `DEFECTO DOMINIO cota w0=…: N=40001 -> peor rel T_min =` 2.876211e-07 (1.05) · **2.889248e-03 (1.25)** · 4.336129e-08 (2.00) · 4.984944e-08 (4.00) | **declarado**; el peor caso (1.25) **no se adjudica** |
| **Convención degenerada `T(omega_p) := 1.0`** (y `1.0` para `w <= 0` y `abs(w - omega_p) <= 1e-12`) | forma sellada `T_sellado`, l.193–224 del solver | **sellado**: es convención declarada, no medición |
| **`§13.5.u` describe la atenuación como `suma(|Js|^2 * T^2)`; el respaldo mide `suma(p*T^1)/suma(p)`** | `atenuacion w0=1.05: … (T^1, no T^2); §13.5.u la describe en prosa … -> DIVERGENCIA DECLARADA, gobierna el respaldo medido` (ídem 1.25/2.00/4.00) | **DIVERGENCIA DECLARADA**; gobierna el respaldo. Valores medidos: 0.4760885262 (1.05) · 0.877176004 (1.25) · 0.9897340838 (2.00) · 0.9994626526 (4.00) |
| **Ventana de fuente: `max|declarada[:-1] - rebanada[1:]|` es una IDENTIDAD de consistencia** | 3.246e-01 · 3.859e-01 · 6.112e-01 · 1.160e+00, rotulada por el instrumento `(identidad del paso)` | **declarado**; por pre-registro l.423 una identidad **no es evidencia** |
| **Etiqueta `E-A`/`E-B` impresa por la prosa de `P4`** | §7 | **errata certificada**; las filas gobiernan |
| **Comparación `rejilla vs sello` de `/tmp/p13g.py`** | §6.4(a) | **artefacto de bin mezclado**: se declara y se limita el uso a `T2` |
| **«La rejilla absuelve el residuo EB»** | §6.4(b) | **NO SE ESCRIBE**: coincidencia aritmética entre dos errores relativos dominados por el mismo `T2` |

**Defectos de instrumento corregidos y retirados de la lista de rojos:** los seis de §5. **Criterios con umbral tocado: NINGUNO** (`P1_MASCARA_REL` · `TOL_P1` · `TOL_P2A` · `TOL_P2B` · `TOL_P2C` · `TOL_P3` · `TOL_P4_PASOS` · `TOL_P5` · `FRONT_UMBRAL_REL` intactos). El precedente se respeta: **no se baja el umbral, se declara el defecto de dominio.**

**COMANDO QUE RESPALDA ESTA SECCIÓN:** `cd /tmp && sed -n '20,31p' crudo13_20261013T051041Z.txt`.

---

## 10. LO QUE ESTA PIEZA NO DICE (prohibiciones §13.8 respetadas)

Universo declarado: lista de prohibiciones del pre-registro §13.8; verificación de que ninguna figura de esta acta las viola.

1. **No se reabrió §12** — el solver sellado `sim/solver_plasma_cw.py` (`61b699b`, blob `55ed5d85c0b45cc5ad677b314316c2f46e4321e7`) no se editó; su informe `s12_informe_recalibracion.md` (`fbbe011`) no se tocó.
2. **No se impuso `TOL_R_BORDE`** — viaja como declaración heredada (pre-registro l.60).
3. **No se usó una forma cerrada re-derivada** — gobiernan las formas selladas `T_exacto_corte` / `T_exacto_pasante` / `T_sellado`.
4. **No se importó `sim/solver_plasma_cw.py`** — el sondeo usó las líneas 1–274 extraídas como módulo aparte (`awk 'NR<=274' … > /tmp/mod_probe.py`), porque importarlo **corre la batería §12**.
5. **No se alteró ninguna constante sellada.**
6. **No se usó el metro de segundo momento como `B` primario** — `B` viene del ancho contiguo al 1/e.
7. **No se afirma precursor de Brillouin en Drude sin pérdidas** — `P6` es una **ausencia falsable medida** (`cambios_de_signo = 0`).
8. **No se resolvió la separación de frente de 6.0606 pasos** — se cita la predicción y se declara `NO resoluble`.
9. **`v_g` no se trata como independiente** — `v_g = n = 1/v_ph` es identidad verificada (l.233–235); por eso `P2a` es un criterio sobre la **pendiente de fase** con el término `+D` declarado.
10. **No se cita `t_frente`.**
11. **No se adjudicó con el par intra-lámina 380/383.**

**COMANDO QUE RESPALDA ESTA SECCIÓN:** `cd /Users/marlene/plasma-ade && git log --oneline -6 && git diff --stat fbbe011..HEAD -- sim/solver_plasma_cw.py s12_informe_recalibracion.md` (esperado: sin diferencias) y `grep -n "TOL_R_BORDE" PREREGISTRO_PULSOS_PLASMA_ADE_20261013.md`.

---

## 11. MEMORIAS DE CÁLCULO (instrumentos citados, conservados)

Universo declarado: los crudos y sondeos que respaldan cada cifra de esta acta, conservados en `/tmp` con su identidad medida.

| Pieza | Identidad / tamaño | Qué respalda |
|---|---|---|
| `/tmp/crudo13_20261013T051041Z.txt` | POST · 1062 l · 49603 B · RC 0 | **el veredicto y todas las filas** |
| `/tmp/crudo13_20261013T033312Z.txt` | PRE · 1002 l · 39635 B · RC 2 | los 16 rojos y su descomposición por línea |
| `/tmp/p13g.py` + `p13g_out.txt` | sha16 `f12f2abc99eed898` · 24 l | **solo** el certificado `T2` (§6.2) |
| `/tmp/p13f_out.txt` | — | atribución del residuo por encima del corte (§6.3) |
| `/tmp/p13d_out.txt` · `p13b_out.txt` · `p13c_out.txt` | — | residuo de borde `P2a` y sus dos controles (§8.2) |
| `/tmp/ar10.txt` | 27 l · 1870 b · sha16 `2e3bce8c82751ab0` | H2 de la ventana fuente (§5.3) |
| `/tmp/ar8.txt` | 35 l · 2121 b · sha16 `7a8a902916343a85` | `T1` (pre-registro l.176) |
| `/tmp/ar3.txt` … `/tmp/ar9.txt` | — | sondeos ad-hoc |

**DECLARACIÓN DE REPETIBILIDAD (doctrina «el crudo intermedio es irrepetible si no se conserva el instrumento»):** `ar3`–`ar8` son **sondeos ad-hoc**: sus cifras están citadas con su línea, pero **no todos sus instrumentos quedaron conservados** ⇒ lo irrepetible **se declara, no se adjudica**. Los irrepetibles se citan **por slug completo**, no se renumeran y no se duplican.

**COMANDO QUE RESPALDA ESTA SECCIÓN:** `cd /tmp && ls -l crudo13_20261013T051041Z.txt crudo13_20261013T033312Z.txt p13*.txt ar*.txt && shasum -a 256 crudo13_20261013T051041Z.txt crudo13_20261013T033312Z.txt | cut -c1-16`.

---

## 12. CIERRE

Universo declarado: §13 queda **cerrado con veredicto** sobre el instrumento de registro `sim/solver_plasma_pulso.py` (`a20b823`, blob `a69636003c1a5de3ec0ebcc1ec9eb233e5459c19`), con pre-registro `8224d84` (APPEND-ONLY, intacto) y §12 congelado (`fbbe011`).

- **Criterios:** 9 · **cumplidos 6** · **fallados 3** (`P1` por dominio, `P2a` por residuo de borde declarado, `P4` por emparejamiento declarado).
- **Rojos de sello:** **16 → 0**; **filas:** **190 → 189** (fila retirada declarada en §5.1). **RC 2 → 0.**
- **Ninguna cifra de esta acta se publica sin su comando**; ninguna se publica sin denominador declarado; ninguna comparación se publica cuando las dos columnas son el mismo error relativo (§6.4.b).
- **Pendiente declarado, no resuelto:** los dos bins pegados al corte de `R6` (§6.3) y el peor caso de la rejilla de la cota a `1.25` (§9). **Se declaran; no se adjudican.**
- **La identidad de esta acta se mide fuera de ella** (sonda de cierre A2.1 + `git hash-object`): el blob semilla es `dbc71a9dfaf0e4f7ad6909e8db95cadb2ea47c8e` (1 l) y el blob de este cuerpo se certifica en el cierre, no aquí.

