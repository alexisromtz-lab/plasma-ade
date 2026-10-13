# PROPAGACION DE PULSOS DE BANDA ANCHA EN PLASMA FRIO

UNIVERSO DECLARADO: /Users/marlene/plasma-ade, commit 0bbec33, arbol git limpio (SUCIOS=0), medido 2026-10-13. Semilla de este archivo: blob vacio e69de29bb2d1d6434b8b29ae775ad8c2e48c5391, 0 lineas, 0 bytes. Gate A2.1 corrido sobre esa semilla: PRE-VUELO OK, RC_GATE_PRE=0.

Este documento es el PRE-REGISTRO del ciclo §13. Una vez escrito NO se edita: todo resultado posterior entra como apendice numerado o acta de custodia.

## §13.0. Contrato del archivo, respaldos y orden de fases

ALCANCE: pasar de excitacion CW armonica (§12) a propagacion de pulsos temporales de banda ancha (paquetes de onda gaussiana modulados). Tres fenomenos declarados: velocidad de grupo frente a velocidad de fase cerca de la frecuencia de corte, ensanchamiento dispersivo del pulso, y precursores opticos (pulsos de Sommerfeld y Brillouin en medios ADE).

COUPLING DECLARADO CON §12: la escalera de corte d_tilde validada en §12 sirve como cota asintotica de absorcion/reflexion para CADA componente espectral de Fourier del pulso. La forma cerrada se usa VERBATIM la sellada (T_exacto_corte / T_exacto_pasante del solver sellado, lineas 116 y 122). Una forma re-derivada en este ciclo NO sustituye a la sellada (trampa M1, §13.5.g).

### §13.0.a. Contrato de forma

- Cero signos monetarios en todo el archivo: el signo seguido de acento grave re-inyecta texto previo en las herramientas de reemplazo.
- Exactamente 1 encabezado H1, que es la huella literal de este pre-registro.
- Encabezados contados por PREFIJO, no leidos.
- Ninguna linea no vacia se repite dentro del archivo. Los bloques verbatim se escriben por INDENTACION de 4 espacios y sin cercas de codigo: una cerca repetida violaria este mismo contrato.
- Sin retorno de carro embebido.
- Identidad por hash de objeto de git (git hash-object), nunca por el tamano.

### §13.0.b. Respaldos aritmeticos

Cada cifra de §13.5 cita aqui su archivo, su rango de lineas y su sha16. Estos crudos se midieron en este mismo ciclo, antes de escribir este documento.

    ar3   /tmp/ar3.txt    34 l    2197 b    564b67a2f82f67f2
    ar4   /tmp/ar4.txt    23 l    1471 b    ec480e9b36bc5f08
    ar5   /tmp/ar5.txt    34 l    2613 b    bd38067da854de68
    ar6   /tmp/ar6.txt    20 l    1691 b    63894828c298f8c4
    ar7   /tmp/ar7.txt    58 l    3648 b    94e28afc4f02ffe5
    ar8   /tmp/ar8.txt    35 l    2121 b    7a8a902916343a85
    ar9   /tmp/ar9.txt    56 l    3599 b    682952f9b7c3182c
    ar10  /tmp/ar10.txt   27 l    1870 b    2e3bce8c82751ab0

DECLARADO: ar9 y ar10 tienen generador nombrado en disco (/tmp/gen_ar9.py y /tmp/gen_ar10.py; ambos importan /tmp/mod_probe.py, que son las lineas 1-274 del solver sellado extraidas con awk). ar3 a ar8 se produjeron con instrumentos ad-hoc de este mismo ciclo que NO quedaron como archivo nombrado: ese crudo intermedio es irrepetible tal cual. Se declara, no se adjudica. Por eso §13.5 reproduce cada cifra verbatim: si /tmp se pierde, el documento sobrevive y la cifra sigue siendo citable con su linea.

### §13.0.c. Orden de fases

1. Escritura de este pre-registro mas commit mas post-verificacion contando encabezados.
2. Gate A2.1 sobre sim/solver_plasma_pulso.py con su blob fresco, escritura del solver, commit y py_compile.
3. Corrida de la bateria R1 a R24 mas el control R25, con captura del crudo y sello UTC.
4. Verificacion: sellos, codigo de retorno, limpieza del arbol, hashes de blob. Commit.
5. Acta de custodia e informe.

NINGUNA cifra de resultado de este ciclo se entrega en el chat: el entregable corto es la ruta del archivo, y el largo es el archivo.

## §13.1. Regimen congelado heredado de §11 y §12

UNIVERSO DECLARADO: solver sellado §12 (sim/solver_plasma_cw.py, 478 l, 23073 b, blob 55ed5d85c0b45cc5ad677b314316c2f46e4321e7, commit 61b699b) leido en modo probe. Estas constantes se heredan sin cambio.

    dx=0.157079632679 dt=0.155508836353 S=dt/dx=0.990000000000 1/S=1.010101
    dt*wp=0.155508836353 w_p=1.000000 lam_p=2pi=6.283185307180 w_nyq=20.202020202
    C_MUR=(dt-dx)/(dt+dx)=-5.025125628141e-03
    NX=800 N_ABS=60 SIGMA_MAX=10.0 I_SRC=100 I_MON=700 NT_sellado=4000 NT_instrumentado=12000

RESPALDO: /tmp/ar9.txt l.4-l.7.

§13.1.a. Instrumento sellado (§12) que se reusa literal: esponja APAGADA (SIGMA_ESPOJA_INSTR=0.0) mas contorno de Mur de primer orden 1D en AMBOS extremos con C_MUR; V+ y V- medidos en I_MON=700; ventana de minimos cuadrados = ultimos 606 pasos. TRAMPA DECLARADA: DAMP_SIN es sigma=0 (todos unos) y NO es el absorbedor sellado (sigma=10). Confundirlos es el error que se cobro como control fallido en §12.

§13.1.b. TOL_R_BORDE SE HEREDA COMO DECLARACION, NO SE RE-IMPONE. §12 midio que el piso del instrumento E/H a medio paso vale tan((w*dt+k*dx)/4)=1.563070265e-02 y el |r_borde| medido vale 1.563136e-02: razon 1.000042, fase V-/V+ de +89.996 grados, contra una reflectancia fisica de Mur de 1.227733e-06, que es 12740 veces menor. TOL_R_BORDE=1.0e-3 queda por eso declarado INSATISFACIBLE (15.6 veces por debajo del piso del instrumento) y NO se vuelve a exigir en §13. RESPALDO: s12_informe_recalibracion.md l.68, l.75, l.81, l.90 (sha256 4f08219fefa767f4d681966deaca3f68a6f6a32fee8f2985f8ab9b7e2b45709b, commit fbbe011).

§13.1.c. El sesgo de amplitud cos(theta/2)=0.9998778 se cancela EXACTO en T=(V_lamina/V_vacio)^2, que es la forma en que §13 mide transmitancia por bin. Por eso ni C4a ni C4b ni C5 ni la transmitancia por bin de §13 quedan contaminados por ese sesgo. RESPALDO: s12_informe_recalibracion.md l.90.

§13.1.d. §12 queda CONGELADO. Commit fbbe011. Nada de §12 se re-abre en este ciclo.

## §13.2. Excitaciones declaradas

UNIVERSO DECLARADO: fuentes de corriente J_s(t) sobre la malla congelada de §13.1, tau=16.0, t0=6*tau=96.0, w0 en {1.05, 1.25, 2.00, 4.00}.

§13.2.a. Fuente E-A (paquete gaussiano modulado): J_s(t) = exp(-(t-t0)^2/(2*tau^2)) * sin(w0*t).

§13.2.b. Fuente E-B (escalon con subida suave): sin^2(pi*t/(2*t_rise))*sin(w0*t) para t menor que t_rise, y sin(w0*t) despues. Aqui t_rise = 1 paso.

PROXY DECLARADO: el espectro que §13.5.t usa para la atenuacion agregada es el espectro de J_s, NO el del campo. Es un proxy declarado, no el objeto.

VENTANA DECLARADA: NFFT=8192, NI0=420, N_ventana=8192 pasos a partir de NI0, d_w_fft=2*pi/(NFFT*dt)=4.932134e-03. sigma_w=1/tau=0.062500, lo que da 12.6720 bins dentro de mas menos 1 sigma por lado. La BANDA DECLARADA del pulso es la de 4/tau=0.250000 por lado, que son 50.6880 bins (101 bins contados). La cola izquierda en NI0 vale exp(-(NI0*dt-t0)^2/(2*tau^2))=0.158951, es decir -15.97 dB: se declara, no se corrige.

RESPALDO: /tmp/ar9.txt l.10-l.14.

BANDAS POR PORTADOR, sobre la misma retícula:

    w0=1.05  1sigma=[0.987500,1.112500]  4/tau=[0.800000,1.300000]  bins=101
    w0=1.25  1sigma=[1.187500,1.312500]  4/tau=[1.000000,1.500000]  bins=101
    w0=2.00  1sigma=[1.937500,2.062500]  4/tau=[1.750000,2.250000]  bins=101
    w0=4.00  1sigma=[3.937500,4.062500]  4/tau=[3.750000,4.250000]  bins=101

RESPALDO: /tmp/ar9.txt l.17-l.20.

§13.2.c. Validacion del medidor de ancho de envolvente. El medidor pre-registrado mide la corrida CONTIGUA alrededor del pico que cubre el 1/e del maximo. Contra la identidad analitica 2*sqrt(2)*tau:

    ancho_analitico=2sqrt2*tau=45.254834   ancho_medido(pre-registrado)=45.253071   dif_rel=3.895707e-05
    muestras_analitico=291.0113            muestras_medido=291.0000                 dif=0.0113 paso(s)

RESPALDO: /tmp/ar10.txt l.4-l.5. El medidor queda VALIDADO contra su propia identidad a 3.895707e-05, que es 0.0113 paso de 291.

CONTROL DE IDENTIDAD DEL ANCHO DE ENTRADA, medido aparte:

    ancho_in(2sqrt2*tau)=45.254834   ancho_in/DT=291.0113   tau*sqrt(8)=45.254834

RESPALDO: /tmp/ar9.txt l.56. DEFECTO CERRADO EN ESTE CICLO: un ancho_in de 85.529860 medido antes era artefacto de tomar la envolvente de entrada de la gaussiana REAL en vez de la ANALITICA; con la analitica el valor es 45.253071 y coincide.

§13.2.d. Energia fuera de banda. Fraccion de la energia espectral que cae FUERA de la banda declarada, medida sobre la ventana declarada:

    w0=1.05  fuera_4tau=1.159317e-03 (-29.36 dB)  fuera_1sigma=1.822297e-01 (-7.39 dB)
    w0=1.25  fuera_4tau=1.052691e-03 (-29.78 dB)  fuera_1sigma=1.638631e-01 (-7.86 dB)
    w0=2.00  fuera_4tau=1.085244e-03 (-29.64 dB)  fuera_1sigma=1.637616e-01 (-7.86 dB)
    w0=4.00  fuera_4tau=1.058335e-03 (-29.75 dB)  fuera_1sigma=1.805993e-01 (-7.43 dB)

RESPALDO: /tmp/ar10.txt l.8-l.11. CONSECUENCIA DECLARADA: fuera de la banda de 4/tau queda solo entre -29.36 y -29.78 dB, mientras que fuera de 1 sigma queda entre -7.39 y -7.86 dB. Por eso la banda declarada de este pre-registro es la de 4/tau y NO la de 1 sigma. No se baja ningun umbral: se declara cual es la banda.

§13.2.e. Retícula espectral efectiva:

    bins_positivos=rfft(8192)=4097   w_max=w_nyq=pi/dt=20.202020   d_w=4.932134e-03
    bins_con_w menor que 1.0 (bajo corte)=203   bins_con_w mayor o igual a 1.0=3894

RESPALDO: /tmp/ar10.txt l.14-l.15.

## §13.3. Geometrias, banco de monitores y matriz de corridas

UNIVERSO DECLARADO: 25 corridas sobre NX=800, N_ABS=60, I_SRC=100, NT=12000 (instrumentado), instrumento sellado de §13.1.a.

§13.3.a. G-ref: vacio, sin lamina. Monitores 300, 500 y 700. Portadores {1.05, 1.25, 2.00, 4.00} con fuente E-A, y 1.25 con fuente E-B.

§13.3.b. G-escalera: escalera de corte de §12 con d_tilde en {0.25, 0.50, 0.75, 1.00} lam_p, que son 10, 20, 30 y 40 celdas. Portadores {1.25, 2.00, 4.00} con fuente E-A.

§13.3.c. G-medio: lamina gruesa d=4*lam_p=160 celdas, colocada en las celdas 320 a 480. Banco de monitores 300, 380, 383, 470, 500 y 700. El par intra-lamina 380 y 383 (separacion de 3 celdas) es SECUNDARIO: se declara contaminado por onda estacionaria dentro de la lamina, y con el solo NO se adjudica nada. El par 380 y 385 se RECHAZA en este pre-registro.

§13.3.d. Matriz de corridas:

    R1   G-ref     E-A  w0=1.05
    R2   G-ref     E-A  w0=1.25
    R3   G-ref     E-A  w0=2.00
    R4   G-ref     E-A  w0=4.00
    R5   G-ref     E-B  t_rise=1  w0=1.25   (control de velocidad de frente)
    R6   G-medio   E-A  w0=1.05
    R7   G-medio   E-A  w0=1.25
    R8   G-medio   E-A  w0=2.00
    R9   G-medio   E-A  w0=4.00
    R10  G-medio   E-B  t_rise=1  w0=1.05
    R11  G-medio   E-B  t_rise=1  w0=1.25
    R12  G-medio   E-B  t_rise=1  w0=2.00
    R13  G-escalera d_tilde=0.25  E-A  w0=1.25
    R14  G-escalera d_tilde=0.25  E-A  w0=2.00
    R15  G-escalera d_tilde=0.25  E-A  w0=4.00
    R16  G-escalera d_tilde=0.50  E-A  w0=1.25
    R17  G-escalera d_tilde=0.50  E-A  w0=2.00
    R18  G-escalera d_tilde=0.50  E-A  w0=4.00
    R19  G-escalera d_tilde=0.75  E-A  w0=1.25
    R20  G-escalera d_tilde=0.75  E-A  w0=2.00
    R21  G-escalera d_tilde=0.75  E-A  w0=4.00
    R22  G-escalera d_tilde=1.00  E-A  w0=1.25
    R23  G-escalera d_tilde=1.00  E-A  w0=2.00
    R24  G-escalera d_tilde=1.00  E-A  w0=4.00
    R25  G-medio   E-A  w0=1.25  con INSTRUMENTO DEFECTUOSO (control must-fail)

R25 es el control must-fail: misma geometria y mismo portador que R7 pero con el instrumento defectuoso (esponja SIGMA=10 ENCENDIDA y contorno de Mur APAGADO). Debe FALLAR P1 mientras el instrumento sellado lo pasa. Sin R25, P1 no discrimina: un criterio que el instrumento defectuoso tambien pasaria no mide nada.

## §13.4. Observables

O1. Transmitancia por bin: |T(w)|^2 = |E_lamina(w)|^2 / |E_vacio(w)|^2, bin a bin de la ventana declarada, comparando la corrida con lamina contra su corrida de referencia sin lamina, en el MISMO monitor. Es libre de convencion por construccion.

O2. Pendiente de fase por bin: derivada numerica de la fase desenvuelta de la transferencia entre monitores, sin ramas, con la correccion de interfaz declarada aparte. De aqui sale v_g.

O3. Ancho de envolvente por corrida contigua al 1/e, en entrada y en salida. De aqui sale B.

O4. Arribo del frente: primer paso en que la traza cruza un umbral de amplitud declarado, corriendo la geometria con plasma y la geometria de vacio al MISMO monitor.

O5. Frecuencia instantanea a lo largo de la escalera de silla de Sommerfeld w_s(ct/z), para el chirp.

O6. Identidad v_ph * v_g. NO se usa como evidencia por si misma: es una identidad del continuo, y una identidad no es evidencia. Lo que se pre-registra es la FIRMA NUMERICA de la malla, que si puede diferir.

## §13.5. Tablas de prediccion pre-registradas

Cada bloque cita su archivo de respaldo con rango de lineas y sha16. Estas tablas se fijan ANTES de correr la bateria.

### §13.5.a. T1, dispersion exacta del continuo

    w0=1.05  n=0.30491068 k=0.32015621 beta2=-30.472929 v_ph=3.27964900 v_g=0.30491068 lam/dx=124.9390
    w0=1.25  n=0.60000000 k=0.75000000 beta2=-2.370370 v_ph=1.66666667 v_g=0.60000000 lam/dx=53.3333
    w0=2.00  n=0.86602540 k=1.73205081 beta2=-0.192450 v_ph=1.15470054 v_g=0.86602540 lam/dx=23.0940
    w0=4.00  n=0.96824584 k=3.87298335 beta2=-0.017213 v_ph=1.03279556 v_g=0.96824584 lam/dx=10.3280

RESPALDO: /tmp/ar7.txt l.3-l.7 (58 l, 3648 b, 94e28afc4f02ffe5), bloque T1.

### §13.5.b. T2, dispersion numerica de la malla

    w0=1.05  k_num=0.31634351 v_ph_num=3.31917666 v_g_num=0.30249796 err_k=-1.19089% err_vph=+1.20524% err_vg=-0.79129% vph*vg=1.00404417
    w0=1.25  k_num=0.74714563 v_ph_num=1.67303394 v_g_num=0.60011752 err_k=-0.38058% err_vph=+0.38204% err_vg=+0.01959% vph*vg=1.00401698
    w0=2.00  k_num=1.72804799 v_ph_num=1.15737527 v_g_num=0.86736900 err_k=-0.23110% err_vph=+0.23164% err_vg=+0.15515% vph*vg=1.00387143
    w0=4.00  k_num=3.86578654 v_ph_num=1.03471828 v_g_num=0.96945816 err_k=-0.18582% err_vph=+0.18617% err_vg=+0.12521% vph*vg=1.00311608

RESPALDO: /tmp/ar7.txt l.9-l.13, bloque T2.

### §13.5.c. T3, control de coherencia contra la forma cerrada SELLADA, d=4 lam_p

    w=0.90  |T|^2=7.5140272663e-10 sellada=7.5140272663e-10 err=4.128e-16
    w=0.95  |T|^2=2.1485712945e-07 sellada=2.1485712945e-07 err=3.696e-15
    w=0.99  |T|^2=2.6022588088e-04 sellada=2.6022588088e-04 err=1.479e-14
    w=1.05  |T|^2=3.1934991130e-01 sellada=3.1934991130e-01 err=0.000e+00
    w=1.25  |T|^2=1.0000000000e+00 sellada=1.0000000000e+00 err=0.000e+00
    w=2.00  |T|^2=9.9605588506e-01 sellada=9.9605588506e-01 err=1.115e-16
    w=4.00  |T|^2=9.9999732639e-01 sellada=9.9999732639e-01 err=1.110e-16

RESPALDO: /tmp/ar8.txt l.2-l.9 (35 l, 2121 b, 7a8a902916343a85), bloque T3. La forma cerrada es exacta en LOS DOS LADOS del corte, incluido el evanescente. En /tmp/ar7.txt l.15-l.21 el mismo bloque T3 sale contaminado porque usa una forma RE-DERIVADA: por eso T3 se cita de ar8 y NO de ar7 (ver §13.5.g).

### §13.5.d. T4, escalera de corte SELLADA, d_tilde en 0.25 / 0.50 / 0.75 / 1.00 lam_p

    w=0.20  3.015020e-02 1.306491e-03 5.999000e-05 2.761929e-06
    w=0.60  2.612118e-01 2.392228e-02 1.957537e-03 1.586962e-04
    w=0.90  5.295931e-01 1.539471e-01 4.016058e-02 1.027167e-02
    w=0.95  5.746833e-01 2.113492e-01 7.638707e-02 2.814538e-02
    w=0.99  6.098515e-01 2.712458e-01 1.324590e-01 7.143189e-02

RESPALDO: /tmp/ar8.txt l.10-l.15, bloque T4. ESTA es la escalera que §13 usa como cota. En /tmp/ar7.txt l.23-l.28 la escalera de corte sale con otros valores (w=0.60 da 2.880325e-02 en vez de 2.612118e-01): esa tabla es la forma re-derivada y NO se usa.

### §13.5.e. T5, escalera pasante SELLADA, mismas cuatro d_tilde

    w=1.05  0.66054738 0.38788490 0.31213444 0.35593077
    w=1.25  0.80464213 0.87548638 0.96000990 0.77854671
    w=1.50  0.92092216 0.98846218 0.93975263 0.96102204
    w=2.00  0.99653425 0.98854382 0.98143390 0.97984510
    w=3.00  0.99678430 0.99908603 0.99834688 0.99731209
    w=4.00  0.99995908 0.99984278 0.99966941 0.99946625

RESPALDO: /tmp/ar8.txt l.16-l.22, bloque T5. /tmp/ar7.txt l.30-l.36 reproduce los mismos valores: aqui los dos crudos COINCIDEN.

### §13.5.f. T6, lamina gruesa d=4 lam_p=25.132741 (160 celdas), SELLADA

    w=0.90  7.5140272663e-10 n=nan k=nan
    w=0.95  2.1485712945e-07 n=nan k=nan
    w=0.99  2.6022588088e-04 n=nan k=nan
    w=1.05  3.1934991130e-01 n=0.30491068 k=0.32015621
    w=1.25  1.0000000000e+00 n=0.60000000 k=0.75000000
    w=2.00  9.9605588506e-01 n=0.86602540 k=1.73205081
    w=4.00  9.9999732639e-01 n=0.96824584 k=3.87298335

RESPALDO: /tmp/ar8.txt l.23-l.30, bloque T6. Bajo el corte la sellada imprime nan porque n es imaginario puro: se declara como tal, no se reemplaza por cero.

### §13.5.g. M1, trampa medida: una forma cerrada re-derivada HOY no es la de §12

    w=0.20  mia=1.633237e-23 sellada=2.508913e-22 razon=15.3616
    w=0.60  mia=1.221491e-18 sellada=1.266441e-17 razon=10.3680
    w=0.90  mia=2.090228e-10 sellada=7.514027e-10 razon=3.5948
    w=0.99  mia=3.536967e-04 sellada=2.602259e-04 razon=0.7357

RESPALDO: /tmp/ar8.txt l.31-l.35, bloque M1. DECLARACION: la escalera de §13 usa la funcion sellada VERBATIM; la variante re-derivada se cita solo como TRAMPA. Las razones 15.3616, 10.3680, 3.5948 y 0.7357 muestran que ni siquiera el orden de magnitud se conserva.

### §13.5.h. CINCO, signo del retardo (fase total contra referencia de vacio a igual distancia)

    w0=1.05  pico_vac=33.123382  pico_medio=1857.397541  d_t_medido=+1824.274159  dt_g_exacto=57.293828  d_t/dt_g=31.840675
    w0=1.25  pico_vac=33.123382  pico_medio=15.861901   d_t_medido=-17.261481    dt_g_exacto=16.755161  d_t/dt_g=-1.030219
    w0=2.00  pico_vac=33.123382  pico_medio=29.235661   d_t_medido=-3.887721     dt_g_exacto=3.888049   d_t/dt_g=-0.999916
    w0=4.00  pico_vac=33.123382  pico_medio=32.345838   d_t_medido=-0.777544     dt_g_exacto=0.824242   d_t/dt_g=-0.943344

RESPALDO: /tmp/ar3.txt l.3-l.9 (34 l, 2197 b, 564b67a2f82f67f2), bloque CINCO. DEFECTO DECLARADO Y CERRADO: d_t_medido sale NEGATIVO porque los brazos del instrumento usaban exp(+i*w*L), que bajo la convencion e^(+i*w*t) de numpy es un ADELANTO. Convencion declarada: con numpy, ifft usa e^(+i*w*t), luego el retardo es e^(-i*w*tau). El observable que se pre-registra por eso es LIBRE DE CONVENCION: la diferencia de pico de envolvente entre la corrida con lamina y la corrida de vacio en el MISMO monitor.

### §13.5.i. SEIS, pendiente de fase de la transferencia entre los monitores 300 y 500

    w0=1.05  dph/dw_num=55.536330  dph/dw_exacto=30.400714  dph/dw_exceso=57.293828  dt_g=57.293828  incremento_por_bin=0.186991
    w0=1.25  dph/dw_num=45.731421  dph/dw_exacto=20.613568  dph/dw_exceso=16.755161  dt_g=16.755161  incremento_por_bin=0.153978
    w0=2.00  dph/dw_num=29.085596  dph/dw_exacto=3.950010   dph/dw_exceso=3.888049   dt_g=3.888049   incremento_por_bin=0.097931
    w0=4.00  dph/dw_num=25.958941  dph/dw_exacto=0.826414   dph/dw_exceso=0.824242   dt_g=0.824242   incremento_por_bin=0.087404

RESPALDO: /tmp/ar3.txt l.10-l.16, bloque SEIS.

### §13.5.j. SIETE, B medido con la transferencia exacta y entrada gaussiana ANALITICA (tercer medidor)

    w0=1.05  ancho_in=45.253071  ancho_out=85.529860  B_medido=1.890034  B_analytic=3.154379  err_rel=0.4008
    w0=1.25  ancho_in=45.253071  ancho_out=46.963669  B_medido=1.037801  B_analytic=1.026720  err_rel=0.0108
    w0=2.00  ancho_in=45.253071  ancho_out=45.253071  B_medido=1.000000  B_analytic=1.000178  err_rel=0.0002
    w0=4.00  ancho_in=45.253071  ancho_out=45.253071  B_medido=1.000000  B_analytic=1.000001  err_rel=0.0000

RESPALDO: /tmp/ar3.txt l.17-l.22, bloque SIETE. Este es un medidor DISTINTO del pre-registrado (§13.5.s): se cita como tercer medidor y cada cifra viaja con su archivo.

### §13.5.k. OCHO, espectro de la fuente E-B de escalon (t_rise=8), relativo a w=1.25

    w=1.25   1.000000e+00  +0.00
    w=1.50   4.627487e-03  -46.69
    w=2.00   1.036164e-03  -59.69
    w=3.00   4.724795e-04  -66.51
    w=4.00   3.336800e-04  -69.53
    w=6.00   2.139370e-04  -73.39
    w=10.00  1.334254e-04  -77.50
    w=20.20  9.272156e-05  -80.66

RESPALDO: /tmp/ar3.txt l.23-l.32, bloque OCHO.

### §13.5.l. NUEVE, ausencia de silla de Brillouin en Drude sin perdidas

    cambios_de_signo=0   dv/dw(1.0001)=61.043128   dv/dw(50)=8.001660e-06   monotono=True

RESPALDO: /tmp/ar3.txt l.33-l.34, bloque NUEVE. Se barrio w de 1.000001 a 50 con 200001 muestras y v_g=sqrt(w^2-1)/w. Recuento de cambios de signo de dv_g/dw en (1,50] = 0. Los dos extremos declarados del barrido descienden: dv/dw(1.0001)=61.043128 y dv/dw(50)=8.001660e-06 (el crudo no imprime una prueba de monotonía global; imprime el recuento de cambios de signo y dos extremos, y eso es lo que aquí se cita). CONSECUENCIA PRE-REGISTRADA: en un Drude sin perdidas NO hay precursor de Brillouin; la AUSENCIA se pre-registra como predicado falsable, y un precursor de Brillouin genuino exige medio resonante (Lorentz), que se difiere al ciclo §13-B con eps(w)=1-w_p^2/(w^2-w_r^2+i*gamma*w).

### §13.5.m. T8, retardo total predicho y su descomposicion

    w0=1.05  d/v_g=82.426570  interfaz=-34.420111  dt_total=48.006459  v_g_exacto=0.304911  v_g_desde_dt_total=0.523528
    w0=1.25  d/v_g=41.887902  interfaz=+5.585054   dt_total=47.472956  v_g_exacto=0.600000  v_g_desde_dt_total=0.529412
    w0=2.00  d/v_g=29.020790  interfaz=+0.194495   dt_total=29.215285  v_g_exacto=0.866025  v_g_desde_dt_total=0.860260
    w0=4.00  d/v_g=25.956984  interfaz=+0.013474   dt_total=25.970457  v_g_exacto=0.968246  v_g_desde_dt_total=0.967744

RESPALDO: /tmp/ar4.txt l.3-l.8 (23 l, 1471 b, ec480e9b36bc5f08), bloque T8. DECLARACION DURA: el termino de interfaz Fabry-Perot NO es despreciable cerca del corte. En w0=1.05 vale -34.420111 frente a d/v_g=82.426570, o sea el 42 por ciento. Sacar v_g del retardo total da 0.529412 en vez de 0.600000 en w0=1.25, un 12 por ciento de error. Por eso, en §13, v_g es ASISTIDA POR TEORIA y no una medicion independiente.

### §13.5.n. T8b, incremento de fase por bin sobre [1.01, 4.00]

    max|dph/dw|=228.475573  bin_max=1.126872 rad  (menor que pi: True)
    min|dph/dw|=25.966141   bin_min=0.128068 rad
    w=1.01  192.688681  (0.950366 rad/bin)
    w=1.05  48.006459   (0.236774 rad/bin)
    w=1.25  47.472956   (0.234143 rad/bin)
    w=2.00  29.215285   (0.144094 rad/bin)
    w=4.00  25.970457   (0.128090 rad/bin)

RESPALDO: /tmp/ar4.txt l.10-l.18, bloque T8b.

### §13.5.o. T10, niveles de excitacion de la fuente E-B por t_rise, relativos a w0=1.25

    t_rise=1.0  dB(2.00)=-57.13  dB(4.00)=-65.99  dB(10.0)=-77.67  dB(20.2)=-80.83
    t_rise=2.0  dB(2.00)=-55.67  dB(4.00)=-69.06  dB(10.0)=-77.52  dB(20.2)=-80.69
    t_rise=4.0  dB(2.00)=-55.82  dB(4.00)=-69.33  dB(10.0)=-77.48  dB(20.2)=-80.67
    t_rise=8.0  dB(2.00)=-59.69  dB(4.00)=-69.53  dB(10.0)=-77.50  dB(20.2)=-80.66

RESPALDO: /tmp/ar4.txt l.19-l.23, bloque T10.

### §13.5.p. T10 bis, niveles medidos sobre la VENTANA DECLARADA, relativos al pico en w0

    w0=1.25  t_rise en {1,2,4,8}: dB(2.00)=-52.46 dB(4.00)=-65.62 dB(10.0)=-75.79 dB(20.2)=-79.32  (identico en los cuatro)
    w0=2.00  t_rise en {1,2,4,8}: dB(2.00)=+0.00 dB(4.00)=-55.69 dB(10.0)=-65.04 dB(20.2)=-68.35  (identico en los cuatro)

RESPALDO: /tmp/ar5.txt l.3-l.12 (34 l, 2613 b, bd38067da854de68), bloque T10. LIMITACION DECLARADA: la fuente de escalon casi no aporta ancho de banda, y el resultado es IDENTICO para t_rise en {1,2,4,8}: esta dominado por la fuga de la ventana, no por la rampa. La amplitud del precursor esta entre 10^-3 y 10^-4 del portador, es decir por debajo de -52 dB: el caso E-B es un ensayo de RANGO DINAMICO, no un ensayo de amplitud.

### §13.5.q. T9, frente fisico contra frente de malla

    z=94.247780  t_fisico=z/c=94.247780 (606.0606 pasos)  t_malla=z*S=93.305302 (600.0000 pasos)
    separacion=0.942478 (6.0606 pasos)  velocidad_malla=1/S=1.010101  exceso_rel=0.010101

RESPALDO: /tmp/ar9.txt l.23-l.24 y, con la misma cifra, /tmp/ar5.txt l.13-l.16. DECLARACION: el frente fisico de Sommerfeld queda 6.0606 pasos DETRAS del frente numerico de la malla; a esta resolucion NO es resoluble. La prediccion medible es por eso la COINCIDENCIA de arribo entre la corrida con plasma y la corrida de vacio, que es independiente de la amplitud y por lo tanto inmune al problema de -52 dB.

### §13.5.r. T9b, silla de Sommerfeld: version DEFECTUOSA (trampa) y version CORREGIDA

Version defectuosa, /tmp/ar5.txt l.17-l.29, para todo ct/z en {1.0010, 1.0050, 1.0100, 1.0200, 1.0500, 1.1000, 1.3000, 1.6000, 2.2000, 4.0000}:

    w_s=60.000000  v_g=0.999861  v_ph=1.000139  exceso_t=0.012962
    cruce en Nyquist: ct/z=1.001227  w_nyq=20.202020

TRAMPA MEDIDA: esa version devuelve w_s=60.000000 para TODAS las razones porque 1/v_g(w)=w/sqrt(w^2-1) DECRECE con w y la biseccion estaba escrita al reves. Version corregida, /tmp/ar6.txt l.3-l.13 (20 l, 1691 b, 63894828c298f8c4), con la biseccion `si mid/sqrt(mid^2-1) es menor que r entonces hi=mid si no lo=mid`, soporte [1.0000001, 1.0e6] y 300 iteraciones:

    ct/z=1.0010  w_s=22.377447  v_g=0.999001  v_ph=1.001000  exceso=0.094248   (0.6061 pasos)
    ct/z=1.0050  w_s=10.037461  v_g=0.995025  v_ph=1.005000  exceso=0.471239   (3.0303 pasos)
    ct/z=1.0100  w_s=7.123991   v_g=0.990099  v_ph=1.010000  exceso=0.942478   (6.0606 pasos)
    ct/z=1.0200  w_s=5.074690   v_g=0.980392  v_ph=1.020000  exceso=1.884956   (12.1212 pasos)
    ct/z=1.0500  w_s=3.279649   v_g=0.952381  v_ph=1.050000  exceso=4.712389   (30.3030 pasos)
    ct/z=1.1000  w_s=2.400397   v_g=0.909091  v_ph=1.100000  exceso=9.424778   (60.6061 pasos)
    ct/z=1.3000  w_s=1.565016   v_g=0.769231  v_ph=1.300000  exceso=28.274334  (181.8182 pasos)
    ct/z=1.6000  w_s=1.281025   v_g=0.625000  v_ph=1.600000  exceso=56.548668  (363.6364 pasos)
    ct/z=2.2000  w_s=1.122683   v_g=0.454545  v_ph=2.200000  exceso=113.097336 (727.2727 pasos)
    ct/z=4.0000  w_s=1.032796   v_g=0.250000  v_ph=4.000000  exceso=282.743339 (1818.1818 pasos)
    cruce en Nyquist: ct/z=1.001227 (w_nyq=20.202020)

La version corregida reproduce EXACTA la tabla que se habia perdido. Las tablas de §13.5.r se citan SIEMPRE de ar6; la de ar5 se cita solo como la trampa.

### §13.5.s. B pre-registrado (corrida contigua al 1/e) y B de segundo momento declarado TRAMPA

Medidor PRE-REGISTRADO, corrida contigua al 1/e, /tmp/ar6.txt l.16-l.20:

    w0=1.05  ancho_in=45.253071(291)  ancho_out=85.529860(550)  B=1.890034  B_analytic=3.154379  err_rel=0.40082
    w0=1.25  ancho_in=45.253071(291)  ancho_out=47.119177(303)  B=1.041237  B_analytic=1.026720  err_rel=0.01414
    w0=2.00  ancho_in=45.253071(291)  ancho_out=45.253071(291)  B=1.000000  B_analytic=1.000178  err_rel=0.00018
    w0=4.00  ancho_in=45.253071(291)  ancho_out=45.253071(291)  B=1.000000  B_analytic=1.000001  err_rel=0.00000

Medidor de SEGUNDO MOMENTO, /tmp/ar5.txt l.30-l.34, DECLARADO TRAMPA:

    w0=1.05  sig_in=11.313708  sig_out=113.365238  B_2mom=10.020166  B_analytic=3.154379  err_rel=2.17659
    w0=1.25  sig_in=11.313708  sig_out=13.198822   B_2mom=1.166622   B_analytic=1.026720  err_rel=0.13626
    w0=2.00  sig_in=11.313708  sig_out=11.327054   B_2mom=1.001180   B_analytic=1.000178  err_rel=0.00100
    w0=4.00  sig_in=11.313708  sig_out=11.314841   B_2mom=1.000100   B_analytic=1.000001  err_rel=0.00010

DECLARACION: el medidor de segundo momento sobreestima el ensanchamiento en w0=1.05 por un factor 3.18 sobre el analitico (217.659 por ciento de error) y en w0=1.25 por 13.626 por ciento, mientras el pre-registrado da 1.414 por ciento. B se mide con el pre-registrado, y el segundo momento NO se usa como primario.

### §13.5.t. Cota de la escalera sobre la banda del pulso, funciones selladas, d=d_tilde*lam_p

    w0=1.05 banda=[0.800000,1.300000]  d=0.25: T_min=4.375914e-01 T_max=1.000000e+00 T(w0)=6.605474e-01
    w0=1.05 banda=[0.800000,1.300000]  d=0.50: T_min=8.176435e-02 T_max=1.000000e+00 T(w0)=3.878849e-01
    w0=1.05 banda=[0.800000,1.300000]  d=0.75: T_min=1.282814e-02 T_max=1.000000e+00 T(w0)=3.121344e-01
    w0=1.05 banda=[0.800000,1.300000]  d=1.00: T_min=1.957537e-03 T_max=1.000000e+00 T(w0)=3.559308e-01
    w0=1.25 banda=[1.000000,1.500000]  d=0.25: T_min=6.185940e-01 T_max=1.000000e+00 T(w0)=8.046421e-01
    w0=1.25 banda=[1.000000,1.500000]  d=0.50: T_min=2.886206e-01 T_max=1.000000e+00 T(w0)=8.754864e-01
    w0=1.25 banda=[1.000000,1.500000]  d=0.75: T_min=1.529052e-01 T_max=1.000000e+00 T(w0)=9.600099e-01
    w0=1.25 banda=[1.000000,1.500000]  d=1.00: T_min=9.229591e-02 T_max=1.000000e+00 T(w0)=7.785467e-01
    w0=2.00 banda=[1.750000,2.250000]  d=0.25: T_min=9.768168e-01 T_max=1.000000e+00 T(w0)=9.965343e-01
    w0=2.00 banda=[1.750000,2.250000]  d=0.50: T_min=9.633840e-01 T_max=1.000000e+00 T(w0)=9.885438e-01
    w0=2.00 banda=[1.750000,2.250000]  d=0.75: T_min=9.755790e-01 T_max=1.000000e+00 T(w0)=9.814339e-01
    w0=2.00 banda=[1.750000,2.250000]  d=1.00: T_min=9.798006e-01 T_max=1.000000e+00 T(w0)=9.798451e-01
    w0=4.00 banda=[3.750000,4.250000]  d=0.25: T_min=9.995587e-01 T_max=1.000000e+00 T(w0)=9.999591e-01
    w0=4.00 banda=[3.750000,4.250000]  d=0.50: T_min=9.988083e-01 T_max=1.000000e+00 T(w0)=9.998428e-01
    w0=4.00 banda=[3.750000,4.250000]  d=0.75: T_min=9.986981e-01 T_max=1.000000e+00 T(w0)=9.996694e-01
    w0=4.00 banda=[3.750000,4.250000]  d=1.00: T_min=9.988132e-01 T_max=1.000000e+00 T(w0)=9.994663e-01

RESPALDO: /tmp/ar9.txt l.27-l.46, bloque cota. Esta es exactamente la forma en que la escalera de §12 sirve de cota para cada componente espectral del pulso.

### §13.5.u. Atenuacion espectral agregada, d=4 lam_p, fuente E-A, sobre la ventana declarada

    w0=1.05  fraccion=4.760875e-01  dB=-3.22  suma(|Js|^2)=3.721197e+05
    w0=1.25  fraccion=8.771758e-01  dB=-0.57  suma(|Js|^2)=3.722366e+05
    w0=2.00  fraccion=9.897341e-01  dB=-0.04  suma(|Js|^2)=3.722396e+05
    w0=4.00  fraccion=9.994627e-01  dB=-0.00  suma(|Js|^2)=3.722774e+05

RESPALDO: /tmp/ar9.txt l.50-l.53, bloque atenuacion. La fraccion es suma(|Js|^2*T^2)/suma(|Js|^2) sobre los 8192 bins de la ventana. Recordar el PROXY DECLARADO de §13.2.b: ese espectro es el de J_s, no el del campo.

### §13.5.v. Escalera sellada cerca del corte, dos grosores

    w=1.000001  T_pasante(d=0.25*lam_p)=6.184873e-01  T_pasante(d=1.00*lam_p)=9.200203e-02
    w=1.010000  T_pasante(d=0.25*lam_p)=6.270516e-01  T_pasante(d=1.00*lam_p)=1.194465e-01
    w=1.050000  T_pasante(d=0.25*lam_p)=6.605474e-01  T_pasante(d=1.00*lam_p)=3.559308e-01
    w=1.100000  T_pasante(d=0.25*lam_p)=7.004733e-01  T_pasante(d=1.00*lam_p)=9.379624e-01

RESPALDO: /tmp/ar10.txt l.24-l.27, bloque escalera borde.

### §13.5.w. Identidad v_ph * v_g del continuo

    w0 en {1.05, 1.25, 2.00}:  v_ph*v_g_exacto=1.000000000000  desvio_continuo=0.000e+00
    w0=4.00:                    v_ph*v_g_exacto=1.000000000000  desvio_continuo=1.110e-16

RESPALDO: /tmp/ar10.txt l.18-l.21. DECLARACION: esta tabla NO es evidencia; es una identidad del continuo y se satisface por construccion. Lo que si es medible es su FIRMA NUMERICA en la malla, que esta en §13.5.b: vph*vg = 1.00404417, 1.00401698, 1.00387143 y 1.00311608.

### §13.5.x. T7 y T7b, arribos y ensanchamiento por la transferencia exacta

d=4*lam_p=25.132741, tau=16.0, /tmp/ar7.txt l.48-l.52:

    w0=1.05  q=-2.99167282  B=3.15437891  dt_g=57.29382840  t_principal=216.125681
    w0=1.25  q=-0.23271057  B=1.02672012  dt_g=16.75516082  t_principal=175.587014
    w0=2.00  q=-0.01889374  B=1.00017847  dt_g=3.88804860   t_principal=162.719902
    w0=4.00  q=-0.00168991  B=1.00000143  dt_g=0.82424230   t_principal=159.656095

d=2*lam_p=12.566371, /tmp/ar7.txt l.54-l.58:

    w0=1.05  q=-1.49583641  B=1.79931281  dt_g=28.64691420
    w0=1.25  q=-0.11635528  B=1.00674652  dt_g=8.37758041
    w0=2.00  q=-0.00944687  B=1.00004462  dt_g=1.94402430
    w0=4.00  q=-0.00084495  B=1.00000036  dt_g=0.41212115

RESPALDO: /tmp/ar7.txt l.48-l.58, bloques T7 y T7b. NO SE CITA t_frente: en el crudo aparece sin formula impresa, y una cifra sin comando no se publica.

## §13.6. Criterios de aceptacion

Tolerancias declaradas ANTES de correr. Ninguna se baja despues; si alguna resulta inaplicable, se declara el defecto de dominio y no se adjudica.

P1. Transmitancia por bin: |T|^2 medido contra la forma sellada de §13.5.c y §13.5.f, error relativo menor o igual a 5 por ciento, evaluado sobre los bins con |E_ref| mayor o igual a 1e-3 del maximo de |E_ref| en la ventana declarada. El umbral de 1e-3 se declara de una vez y por una razon medida: fuera de la banda de 4/tau la energia cae a -29.4 a -29.8 dB (§13.2.d), de modo que los bins bajo ese umbral son ruido de ventana y no senal.

P2. Velocidad de grupo:
- P2a: v_g obtenida de la pendiente de fase sin ramas, con la correccion de interfaz declarada, debe reproducir la v_g numerica de §13.5.b dentro del 3 por ciento en todo w perteneciente a [1.01, 4.00].
- P2b (criterio duro): el incremento de fase por bin debe quedar por debajo de pi en toda la banda, es decir sin aliasing; la prediccion es max 1.126872 rad en w=1.126872 y min 0.128068 rad en w=4.00 (§13.5.n). Se DESCARTA el umbral de 0.15 rad que figuraba en el borrador de plan: la propia teoria lo muestra inaplicable en w0=1.05, donde el incremento por bin es 0.236774 rad ANTES de correr. Se declara la correccion; no se baja el umbral.
- P2c: la FIRMA NUMERICA de la identidad, es decir el producto vph*vg de la malla, debe reproducir las cuatro cifras pre-registradas de §13.5.b dentro del 2 por ciento relativo.

P3. Ensanchamiento: B medido con el medidor PRE-REGISTRADO de §13.5.s debe reproducir B_analytic dentro del 15 por ciento, y SOLO para w0 perteneciente a {1.25, 2.00, 4.00}. w0=1.05 queda DECLARADO DEGENERADO para este observable: por el medidor pre-registrado el error es 40.082 por ciento y por el medidor de segundo momento 217.659 por ciento, o sea el caso esta fuera del dominio del medidor, no fuera del objeto. El control de vacio debe dar B = 1 mas menos 2 por ciento.

P4. Arribo del frente: coincidencia del paso de arribo entre la corrida con plasma y su corrida de vacio control, en el MISMO monitor, con tolerancia de 1 paso, ambas alrededor de 600 pasos segun §13.5.q. Se declara que la separacion fisica de 6.0606 pasos entre el frente de Sommerfeld y el frente de malla NO es resoluble a esta resolucion.

P5. Chirp: la frecuencia instantanea medida en el monitor 700 a lo largo del tiempo debe descender siguiendo la escalera de silla w_s(ct/z) de §13.5.r dentro del 20 por ciento, en los peldaños alcanzables. Se declara que el primer peldaño es inalcanzable en esta malla: ct/z mayor que 1.001227 corresponde a w_s por encima de w_nyq=20.202020.

P6. Ausencia falsable de Brillouin: cero cambios de signo de dv_g/dw en w perteneciente a [1.000001, 50] con 200001 muestras, segun §13.5.l. Si aparece un cambio de signo, el predicado se refuta y el ciclo se detiene.

P7. Control must-fail R25: la misma geometria y portador que R7 pero con el instrumento defectuoso (esponja SIGMA=10 encendida, Mur apagado) debe FALLAR P1 mientras el instrumento sellado lo pasa. Si R25 pasa P1, P1 no discrimina y el ciclo se detiene. RESPALDO de por que: §12 midio que el control con Mur apagado da 1.156452e+01 y la fase NO queda clavada en 90 grados, sino en -74.271 grados (s12_informe_recalibracion.md l.81).

## §13.7. Degeneraciones y trampas declaradas

- TOL_R_BORDE=1.0e-3 se hereda como DECLARACION de insatisfacibilidad, no como criterio (§13.1.b).
- El termino de interfaz Fabry-Perot NO es despreciable cerca del corte: 42 por ciento de d/v_g en w0=1.05, y 12 por ciento de error en v_g si se saca del retardo total (§13.5.m). v_g es asistida por teoria.
- DAMP_SIN tiene sigma=0 y NO es el absorbedor sellado, que tiene sigma=10.
- Convencion: numpy ifft usa e^(+i*w*t), luego retardo es e^(-i*w*tau). El observable de retardo que se pre-registra es libre de convencion (§13.5.h).
- Deriva de dispersion numerica: err_k va de -1.19089 por ciento en w0=1.05 a -0.18582 por ciento en w0=4.00 (§13.5.b). No es un error del objeto: es el error declarado del metro.
- Contaminacion por onda estacionaria dentro de la lamina: el par intra-lamina 380 y 383 se declara SECUNDARIO; el par 380 y 385 se rechaza en este pre-registro.
- V+ y V- NO son validos dentro del plasma: solo se usan en el monitor 700, fuera del medio.
- w0=1.05 queda degenerado para B (§13.5.s) y para la asistencia teorica de v_g (§13.5.m).
- Los precursores de la fuente E-B quedan por debajo de -52 dB en la ventana declarada, e identicos para t_rise en {1,2,4,8}: es un ensayo de rango dinamico (§13.5.p).
- El medidor de B de segundo momento es una TRAMPA medida (§13.5.s).
- Una forma cerrada re-derivada en este ciclo NO es la de §12: las razones medidas son 15.3616, 10.3680, 3.5948 y 0.7357 (§13.5.g). La escalera se usa VERBATIM la sellada.
- Fuera de la banda de 4/tau solo queda entre -29.36 y -29.78 dB de energia: la banda declarada es la de 4/tau, no la de 1 sigma (§13.2.d).
- El instrumento que mide es parte de lo medido: el espectro de J_s es un proxy declarado del espectro del campo (§13.2.b).
- Toda cifra de conteo caduca al escribirse: su hora es parte de la cifra.
- t_frente aparece en /tmp/ar7.txt l.48 sin formula impresa: NO se cita como afirmacion fisica (§13.5.x).
- El crudo intermedio de ar3 a ar8 es irrepetible tal cual, porque su instrumento no quedo como archivo nombrado (§13.0.b).

## §13.8. Lo que NO se hara

- No se re-abre §12 ni su crudo (commit fbbe011).
- No se exige TOL_R_BORDE.
- No se usa ninguna forma cerrada re-derivada en este ciclo.
- No se importa solver_plasma_cw.py desde el solver de §13: importarlo corre la bateria entera de §12 y termina el proceso. Se usa una copia probe de sus lineas 1 a 274.
- No se altera ninguna constante sellada.
- No se usa el medidor de segundo momento como B primario.
- No se afirma precursor de Brillouin en un Drude sin perdidas.
- No se resuelve la separacion de 6.0606 pasos entre frente fisico y frente de malla.
- No se trata v_g como medicion independiente.
- No se cita t_frente.
- No se adjudica nada con el par intra-lamina 380 y 383.

## §13.9. Estado de cierre de este pre-registro

Gate A2.1 sobre PREREGISTRO_PULSOS_PLASMA_ADE_20261013.md: PRE-VUELO OK, RC 0, sobre el blob vacio e69de29bb2d1d6434b8b29ae775ad8c2e48c5391 con 0 lineas. Semilla commiteada en 0bbec33. Arbol git limpio, SUCIOS=0. Los dos objetivos de §13 (este archivo y sim/solver_plasma_pulso.py) existen vacios y commiteados. Siguiente paso: gate A2.1 sobre el solver y escritura de su cuerpo, con la huella literal SOLVER_PLASMA_PULSO.
