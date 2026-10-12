ACTA DE FALLO C4a Y CONGELACION DEL CRUDO

# ACTA DE FALLO C4a Y CONGELACION DEL CRUDO — plasma-ade · 2026-10-12

UNIVERSO DECLARADO: el repositorio plasma-ade en su commit 3ed9618 (semilla vacia de esta acta), sobre
la historia 5f671ed · 0283604 · 6d7c8f4 · 96c295b · 3ed9618. Objetos medidos en este acto: el crudo
nominal congelado (solver_plasma_cw_crudo_1649.txt), su repeticion (replay_solver_plasma_cw_1715.txt),
los dos crudos de sonda (probe_esponja_crudo_1654.txt y probe_rizado_crudo_1655.txt), el archivo del
solver y el archivo del pre-registro.
MOTOR: python3 -B · numpy 2.4.6 · git · shasum -a 256 · diff · grep -cE.
UNIDAD: linea (wc -l) · byte (wc -c) · campo JSON · ocurrencia-linea (grep -c cuenta LINEAS, no
ocurrencias).
VENTANA: T_UTC = 2026-10-12T17:22:38Z (ventana del gate A2.1 que autoriza esta escritura).
AUTORIDAD: orden del dueno del 2026-10-12, punto 3: emitir el acta de fallo de la corrida actual bajo
A2.1, congelando el estado en solver_plasma_cw_crudo_1649.txt, antes de preparar cualquier
modificacion al solver.

## 1. VEREDICTO CENTRAL

Criterios sellados: 6. Cumplidos: 5. Fallados: 1 (C4a).
C4a exige |m_med menos m_exacto| dividido entre 12.3900 menor o igual a 0.02.
Medido: m_med = −13.27434113131028 · m_exacto = −12.39 · m_exacto_maquina = −12.389989917479564 ·
m_teor = −12.3125 · err_rel = 0.07137539397177393, esto es 7.1375 por ciento.
EL FALLO SE ACEPTA COMO RESULTADO METROLOGICO LEGITIMO. Queda prohibido alterar los criterios del
pre-registro congelado para forzar un pase espurio.

## 2. LO QUE SI CIERRA (y por que no rescata a C4a)

C4b: T(omega1, d_tilde = 1.00) = 2.1863499317e−06 · umbral 5.0e−06 · margen 2.29 — VERDE.
C5: minimo T(omega2) = 9.7879196910e−01 · umbral 0.97 — VERDE.
C4c: T_medido mayor que 10 T_piso — VERDE, pero DEGENERADO (ver seccion 4).
Sellos de aritmetica del pre-registro: 27 filas · 27 verdes · 0 rojas.
Ratios de corte (T_medido entre T_exacto), d_tilde 0.25 · 0.50 · 0.75 · 1.00:
1.805806 · 0.517835 · 0.673769 · 0.791603.
Ratios de banda pasante en el mismo orden: 0.998749 · 1.000281 · 0.997893 · 0.998686.
Lectura honesta: el regimen pasante reproduce la transmitancia exacta a nivel de 1e−3 y el regimen de
corte no. El fallo es de NIVEL y de PENDIENTE en corte, no de signo ni de mecanismo ausente.

## 3. CAUSA DEL FALLO: MEDIDA, NO CONJETURADA

Sonda 1 (malla temporal y amplitud de la esponja), crudo probe_esponja_crudo_1654.txt ·
l = 36 · B = 2521 · sha16 = 89628ea19d4bdb7c:
  (N_t = 4000,  sigma_max = 10): m = −13.274341131 · err = 0.071375394 · residuo en vacio = 9.26e−03
  (N_t = 4000,  sigma_max = 30): m = −11.790010343 · err = 0.048425315 · residuo = 1.47e−02
  (N_t = 4000,  sigma_max = 60): m = −13.849978793 · err = 0.117835254 · residuo = 1.43e−02
  (N_t = 12000, sigma_max = 10): m = −14.109735782 · err = 0.138800305 · residuo = 7.70e−05
  (N_t = 12000, sigma_max = 30): m = −13.548820115 · err = 0.093528661 · residuo = 2.96e−04
  (N_t = 12000, sigma_max = 60): m = −13.326990617 · err = 0.075624747 · residuo = 5.42e−04
  (N_t = 20000, sigma_max = 60): m = −13.281321515 · err = 0.071938783 · residuo = 1.93e−05
Los residuos colapsan por un factor 523 (6.79e−02 a 1.28e−04) al pasar de la ventana corta a la
larga: N_t = 4000 NO es regimen estacionario. Y el nivel medido depende fuerte de sigma_max:
T(d_tilde = 0.25) vale 4.4658e−02 · 2.1019e−02 · 1.3092e−02 para sigma_max 10 · 30 · 60 con
N_t = 12000 (factor 3.4), y se estabiliza en el tiempo para sigma_max = 60 (1.309181e−02 contra
1.318732e−02). El control pasante en las dos ventanas largas con sigma_max = 60 da
min T = 9.7855782993e−01 y 9.7855799896e−01: el pasante es robusto, el corte no.
Sonda 2 (rizado espacial del monitor en la corrida vacia), crudo probe_rizado_crudo_1655.txt ·
l = 52 · B = 2521 · sha16 = b7aa486fbc05a8d6 (el mismo numero de bytes que la sonda 1 es coincidencia
de tamano, no de contenido: los sha16 difieren):
  Barrido de la celda del monitor 640 a 740 paso 10, sigma_max = 60: V entre 3.615677196e−02 y
  1.458610269e−01 con V_medio = 9.979651897e−02 · RIZADO = (maximo menos minimo) entre V_medio =
  1.099279, de donde el instrumento de la sonda lee |r_esponja| = RIZADO entre 2 = 0.549640.
  El mismo barrido con sigma_max = 10: V_medio = 7.293071485e−02 · RIZADO = 0.929645 ·
  |r_esponja| = 0.464823.
  Perfil de la esponja hacia el muro (sigma_max = 60): 1.229434951e−01 en la celda 735 ·
  9.361937369e−02 en 745 · 5.797754866e−02 en 755 · 2.461790863e−02 en 765 ·
  4.672401986e−03 en 775 · 3.151073792e−07 en 790 · 4.457653524e−14 en 799.
Consecuencia declarada: la esponja SI absorbe (decaimiento monotono de once ordenes), pero el dominio
NO es libre de reflexion, y el monitor de una sola celda cae sobre una estructura de onda estacionaria
(lee 1.0098 y 1.2981 mientras sus vecinos recorren 0.45 a 1.38). V de referencia y V del monitor son
muestras de onda estacionaria, no amplitudes de onda progresiva. De ahi el deficit de nivel y el error
de pendiente; no de ahi la discretizacion del medio.
Exoneraciones medidas:
  Discretizacion del medio: sinh cuadrado de alpha dx entre 2 = 0.0059203 da alpha_discreta = 0.978713
  contra alpha_exacta = 0.979796, desvio −0.11 por ciento a favor — exonerada.
  Desfase de media celda: 2.45 por ciento y con el signo contrario — no explica el fallo.
Control de amplitud de la fuente (declarado, sin criterio asociado): J0 dx eta0 entre 2 =
7.853981634e−02 · V_ref(omega1) = 6.805388152755e−02 (ratio 0.866488931) ·
V_ref(omega2) = 7.954135099645e−02 (ratio 1.012751935).

## 4. DEGENERACIONES DECLARADAS DENTRO DEL CRUDO

(i) Corrida 2 (omega_p = 0) es bit-identica a la Corrida 1: con omega_p cuadrado por dt igual a cero el
vector J es identicamente nulo y ambos sistemas son el mismo. El criterio C2 (|T menos 1| menor o igual
a 1e−4) se satisface por construccion: no es medicion independiente.
(ii) Corrida 3 (PEC) da V_piso = 0.0 exacto y por tanto T_piso = 0. Es testigo topologico, no piso
numerico: el factor 10 en C4c degenera a la exigencia de que T sea mayor que cero.

## 5. CONTROL DE RESPUESTA (seccion G, esponja apagada)

V = 7.026928390e−04 · T = 1.066167044e−04 · residuo_rel = 2.980e+00. El estimador SI puede diferir de
1: se etiqueta como control de respuesta del instrumento, no como criterio de aceptacion.

## 6. CONGELACION DEL CRUDO NOMINAL

Objeto congelado: solver_plasma_cw_crudo_1649.txt.
  l = 249 · B = 11862 · sha16 = d16eb91a1ac15e66 ·
  sha256 = d16eb91a1ac15e66a2e737c97473a51e5c75c1dd462f6efa834efb643261f80e ·
  mtime = 2026-10-12T16:49:57Z · signo de dollar = 0 · backslash = 2 · cercas triples = 0 ·
  bytes no ASCII = 45 · primer byte = LF · ultimo byte = LF.
Reconstruccion: el crudo se reproduce desde el solver congelado.
  Solver: sim/solver_plasma_cw.py · l = 381 · B = 17151 · sha16 = 390ea737d890821a ·
  blob = c55d85a35c0f3dd21f9fb80f1a0bd4aa8b08bcb9 · commit 96c295baac18d864e4acf08344822db981a0acbe.
Prueba de reproducibilidad ejecutada en este acto, a las 2026-10-12T17:15:51Z:
  repeticion = replay_solver_plasma_cw_1715.txt · RC 0 · l = 249 · B = 11862 ·
  sha16 = 4f17b5e66a973445.
  diff contra el crudo congelado: 8 lineas marcadas, esto es 4 pares, TODAS de reloj: linea 10
  (cabecera de ventana), lineas 237 y 238 (t_utc_arranque y t_utc_cierre del JSON) y linea 248
  (T_UTC de cierre).
  Comparacion campo a campo del JSON: las mismas claves, 0 faltantes, 0 sobrantes, y la unica
  diferencia son t_utc_arranque y t_utc_cierre. Todos los demas campos son identicos.
Lectura: el estado congelado NO es un objeto irrepetible. Es reproducible hasta el reloj; la unica
deriva es la marca de tiempo, que el propio solver escribe. El sha256 citado arriba es la huella de
la corrida de 16:49:57Z; cualquier otro reloj da otro sha256 con la misma fisica.
Durabilidad declarada: el crudo vive en el directorio temporal del sistema y ese directorio no es
almacenamiento permanente. Lo que hace la congelacion durable es el par (identidad citada arriba) mas
(commit 96c295b mas la prueba de reproducibilidad): el estado se reconstruye corriendo el solver
congelado, no copiando el archivo.

## 7. CORRECCIONES DE PREMISA EN LA ORDEN (medidas, no adjudicadas)

(a) La orden describe una esponja abrupta. DIVERGE: el perfil congelado ya es un polinomio graduado de
grado 4, sigma igual a sigma_max por (d entre 60) elevado a 4, maximo en el muro y practicamente nulo
en el borde interno. Lo que falta no es el graduado: es el acoplamiento de impedancia. La medicion de
la sonda 2 lo confirma: perfil monotono y sin salto, y aun asi |r| = 0.465.
(b) La orden cifra la reflectancia parasita en |r| de aproximadamente 0.50. COINCIDE EN ESCALA y
DIVERGE en el segundo decimal para la instrumentacion congelada: medido 0.464823 con sigma_max = 10
(el valor que usa la corrida nominal) y 0.549640 con sigma_max = 60. El 0.50 de la orden cae entre los
dos y esta mas cerca del primero.
(c) La orden propone un monitor de onda progresiva. El instrumento congelado NO tiene ese monitor:
mide una sola celda (I_MON = 700) y ajusta amplitud por minimos cuadrados sobre coseno y seno. Se
declara ademas una diferencia de rotulacion: el token literal H_y aparece en 0 lineas del solver,
porque el campo magnetico vive ahi como la variable de nombre hy. Es rotulacion, no objeto.

## 8. REMEDIOS AUTORIZADOS: PENDIENTES, NINGUNO INICIADO

1. Frontera absorbente de radiacion de primer orden (Mur 1D, con la razon entre c dt menos dx y
   c dt mas dx) o perfil adiabatico polinomial de impedancia adaptada, hasta abatir |r| por debajo de
   1e−3.
2. Monitor de onda progresiva desacoplada, V mas igual a (E_z mas eta0 H_y) entre 2, para cancelar la
   contribucion de la onda reflejada.
3. Extension de la ventana temporal hasta residuo estricto en la losa por debajo de 1e−4. La sonda 1
   ya mide ese orden solo a partir de N_t = 12000 a 20000.
Contrato de destino: los tres remedios tocan parametros sellados del pre-registro congelado
(pre-registro de l = 233 · B = 16556 · sha16 = 2f4a74b2be2878ff ·
blob = 8543d9b3994001b608a910bc4128af6c5811a636, cuyo apendice es la seccion 11 con 84 lineas).
Ninguno puede alterar el umbral de C4a ni ningun otro criterio, ni editar la seccion 11. Todo cambio
de N_t, de sigma_max o de la celda del monitor exige un apendice NUEVO en ese archivo, con su propio
gate A2.1 en RC 0 y su propia identificacion de bloque previo. Este acto no modifica el solver ni el
pre-registro.

## 9. TRAZABILIDAD

Historia del repositorio en el momento del acto: 5f671ed (pre-registro sellado) · 0283604 (apendice 11
de adjudicacion) · 6d7c8f4 (semilla vacia del solver) · 96c295b (solver con las 5 corridas y el fallo
de C4a declarado) · 3ed9618 (semilla vacia de esta acta).
Estado del arbol antes del bootstrap de esta acta: limpio, sucios = 0.
Gate A2.1 de esta escritura: RC 0, con destino esta acta, bloque previo
e69de29bb2d1d6434b8b29ae775ad8c2e48c5391 y lineas previas 0.

## 10. TRAMPAS DECLARADAS EN ESTE ACTO

(a) Un chequeo de pertenencia que pregunta por la huella de esta acta respondera ya presente en el
destino: es la colision esperada del gate posterior, no un defecto del objeto.
(b) La colision de etiquetas entre la forma con prefijo de seccion y la forma sin prefijo ya fue
declarada en el apendice 11 del pre-registro; aqui se usa una sola forma en todo el documento.
(c) grep -c cuenta lineas y no ocurrencias. Toda cifra de este acto viaja con esa unidad declarada, y
toda cifra de conteo caduca al escribirse: su hora es parte de la cifra.
(d) El token H_y no existe como literal en el solver por estar el campo magnetico rotulado hy; buscar
una forma no certifica la ausencia de las otras, por lo que la ausencia se declara solo para el
literal que se midio.
(e) El comentario de codigo con la cerca tipografica triple no se usa en este documento a proposito:
la cerca queda declarada como ausente por medicion (0).
(f) Los dos crudos de sonda miden el mismo numero de bytes con contenidos distintos. El tamano no es
identidad: la identidad es el sha16.

## 11. CIERRE

Este acto NO repara, NO re-ejecuta criterios y NO altera umbrales. Congela por identidad un fallo que
se acepta, deja medido el porque, y deja los tres remedios como pendientes con su contrato de destino.
T_UTC de la ventana del gate que autoriza esta escritura: 2026-10-12T17:22:38Z.
