# plasma-ade — pulsos de banda ancha en el ADE de plasma frío, con el fallo congelado como resultado

> **EN —** 1D ADE (auxiliary differential equation) solver for cold-plasma dispersion. Every
> criterion was sealed before the first number; a criterion that failed is **published as a
> metrological result**, with its raw capture frozen and forbidden to be re-optimised. 9 criteria:
> 6 met, 3 failed and declared.

## La regla de esta casa

El pre-registro se sella **antes** de la primera cifra y es **APPEND-ONLY**. Si un criterio falla,
el fallo **se acepta como resultado metrológico legítimo** y queda prohibido alterar los criterios del
pre-registro congelado para forzar un pase espurio. El crudo de la corrida que falló se **congela**
con nombre propio y no se vuelve a tocar.

## Dos ciclos cerrados, con su cifra

### §12 · corrida CW — `C4a` falla y se congela

- Criterios sellados: **6** · cumplidos: **5** · fallados: **1** (`C4a`).
- `C4a` exige `|m_med − m_exacto| / 12.3900 ≤ 0.02`. **No lo cumple.** Causa **medida, no
  conjeturada** (incluye descartar explícitamente el desfase de media celda: 2.45 % y con el signo
  contrario, que no explica el fallo).
- Lo que sí cierra: `C4b` `T(ω1, d̃=1.00) = 2.1863499317e−06` contra umbral `5.0e−06` (margen 2.29)
  y `C5` `min T(ω2) = 9.7879196910e−01` contra umbral `0.97`.
- Crudo congelado: `solver_plasma_cw_crudo_1649.txt`, con su repetición `replay_solver_plasma_cw_1715.txt`.

Acta: [`ACTA_DE_FALLO_C4A_Y_CONGELACION_DEL_CRUDO_20261012.md`](ACTA_DE_FALLO_C4A_Y_CONGELACION_DEL_CRUDO_20261012.md)

### §13 · pulsos de banda ancha — cierre con veredicto

```
UNIVERSO DECLARADO: N_x = 800 celdas (20.0000 lam_p); vacio mas lamina de plasma frio nu = 0;
fuente de pulso en la celda 100; banco de monitores; esponja APAGADA sigma = 0.0
mas Mur 1D con c_mur = -0.005025125628
MOTOR: python3 -B · numpy 2.4.6 · solo numpy y math
UNIDAD: longitud en celdas y lam_p; tiempo en pasos dt; c = 1
```

- **Criterios: 9 · cumplidos 6 · fallados 3** — `P1` por dominio, `P2a` por residuo de borde
  declarado, `P4` por emparejamiento declarado.
- **Rojos de sello: 16 → 0.** **Filas: 190 → 189** (la fila retirada está declarada en §5.1).
  **RC 2 → 0.**
- Universo del cierre: instrumento de registro `sim/solver_plasma_pulso.py`
  (`a20b823`, blob `a69636003c1a5de3ec0ebcc1ec9eb233e5459c19`), pre-registro `8224d84`
  (APPEND-ONLY, intacto) y `§12` congelado (`fbbe011`).
- **Pendiente declarado, no resuelto:** los dos bins pegados al corte de `R6` (§6.3) y el peor caso
  de la rejilla de la cota a `1.25` (§9). **Se declaran; no se adjudican.**

Acta: [`ACTA_DE_CUSTODIA_E_INFORME_PULSOS_BANDA_ANCHA_20261013.md`](ACTA_DE_CUSTODIA_E_INFORME_PULSOS_BANDA_ANCHA_20261013.md)

## Mapa

```
PREREGISTRO_PLASMA_ADE_20261012.md              sello del ciclo CW (§12)
PREREGISTRO_PULSOS_PLASMA_ADE_20261013.md       sello del ciclo de pulsos (§13)
ACTA_DE_FALLO_C4A_Y_CONGELACION_DEL_CRUDO_20261012.md    el fallo + el crudo congelado
ACTA_DE_CUSTODIA_E_INFORME_PULSOS_BANDA_ANCHA_20261013.md el cierre de §13 con su veredicto
s12_informe_recalibracion.md                    recalibración de §12
sim/solver_plasma_cw.py                         motor CW
sim/solver_plasma_pulso.py                      motor de pulsos (el del cierre)
```

## Reproducir

```sh
python3 -B sim/solver_plasma_pulso.py     # corre la bateria completa: imprime el crudo JSON
                                          # y cierra con `RC = 0` (sellos cuadran) o `RC = 2`
```

El solver **no expone CLI**: es un instrumento que se ejecuta entero y termina con su `RC`. La corrida
certificada de §13 quedó registrada en el acta con su crudo POST
(`crudo13_20261013T051041Z.txt`, 1062 líneas, 49603 B, **RC 0**), que es el portador del veredicto.

Cada cifra de las actas viaja con su **comando**, su **hora UTC**, su **universo** y su **unidad**.
La identidad de cada acta **se mide fuera de ella** (`git hash-object`, `wc -l`, `wc -c` en
terminal): una pieza que declara su propio `sha` describe su versión anterior.

## Límites declarados

- `C4a` falla y **así se publica**: no hay acta posterior que lo convierta en verde.
- El residuo de borde de `P2a` vive **en el propio piso de máscara** que el criterio declara;
  restringir el `unwrap` a la banda da un resultado **idéntico** al global ⇒ no se adjudica.
- Algunas cifras citadas provienen de **sondeos ad-hoc** cuyos instrumentos no se conservaron: se
  declaran **irrepetibles**, se citan por slug completo y no se adjudican.

## Licencia y citación

MIT — ver [`LICENSE`](LICENSE). Cite el acta del ciclo que use, con su `T_UTC_ACTA` y su commit.

**Parte del archivo de instrumentos de [alexisromtz-lab](https://github.com/alexisromtz-lab).**
