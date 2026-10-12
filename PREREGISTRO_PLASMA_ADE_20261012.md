# PRE-REGISTRO METROLÓGICO: ELECTRODINÁMICA ADE-FDTD 1D EN PLASMA FRÍO

UNIVERSO DECLARADO: una dimensión espacial (x); campos E_z y H_y más una corriente auxiliar J_z; dominio discreto de N_x celdas; régimen sin colisiones estricto (nu = 0); sin iones, sin temperatura, sin no linealidad.

MOTOR DECLARADO: solver ADE-FDTD 1D propio, aritmética de doble precisión (float64), esquema explícito de tipo Yee con saltos alternados de E y H. La ecuación de la corriente se integra con el mismo paso temporal que los campos (esquema ADE, sin paso interno).

UNIDAD DE MEDIDA: transmitancia de potencia adimensional T = (magnitud de la DFT de E_transmitido en el bin central) al cuadrado, dividida por (magnitud de la DFT de E_referencia en el mismo bin) al cuadrado.

VENTANA DE MEDICIÓN: reloj UTC. La aritmética de este documento fue verificada en la ventana sellada en la sección 11.

ESTADO: pre-registro congelado ANTES de la primera corrida. Ninguna cifra de este documento fue elegida después de ver una salida del solver.

## 1. Contrato de la orden

El objeto destino es este archivo. La orden de escritura viaja con la tupla TARGET, BLOB_PRE, HUELLA y LINEAS_PRE. Bruto de ejecución atómica: este alta es una PRIMERA ESCRITURA declarada como excepción, autorizada por el dueño; el gate determinista no puede emitir RC 0 sobre un objeto ausente, de modo que se registra el RC real medido antes y después.

La huella exclusiva del texto insertado es el propio título H1 de este archivo. Obligación contraída: commit inmediato tras la escritura, con el mensaje init: congelar preregistro plasma ade 1d.

## 2. Sistema físico y ecuaciones

El medio es un plasma frío no magnetizado, descrito por una permitividad de Drude sin pérdidas. Las tres ecuaciones que el solver debe integrar son, en unidades del Sistema Internacional:

∂H_y/∂t = −(1/μ₀) ∂E_z/∂x

∂E_z/∂t = −(1/ε₀) ∂H_y/∂x − (1/ε₀) J_z

∂J_z/∂t + ν J_z = ε₀ ω_p² E_z

En régimen sin colisiones (ν = 0) la relación de dispersión exacta de la onda plana es ω² = ω_p² + k² c². Por debajo de la frecuencia de plasma la onda no se propaga: k es imaginario puro y define la constante de decaimiento α.

## 3. Régimen congelado (escalas)

Frecuencia de plasma ω_p como unidad. Velocidad de la luz c. Longitud de plasma λ_p = 2πc/ω_p.

Espesor de lámina d = 2 λ_p.

Paso espacial Δx = λ_p / 40.

Paso temporal Δt = 0.99 Δx / c.

Con estas tres últimas se cumplen las dos condiciones duras del esquema explícito: el paso temporal queda por debajo del límite de Courant (0.99 de Δx/c) y, dentro de la lámina a la frecuencia pasante de la sección 5, la malla resuelve 23.09 puntos por longitud de onda del medio (medido, sección 10).

## 4. Banda de corte profundo — el nulo

Frecuencia de prueba ω₁ = 0.2 ω_p.

Constante de decaimiento α = sqrt(ω_p² − ω₁²)/c = 0.979796 ω_p/c.

Contraste de impedancia adimensional κ = α c / ω₁, de modo que κ² = 24.0000.

Prefactor de la lámina finita por la cara única: 16 κ² / (1 + κ²)² = 0.614400.

Espesor óptico de la lámina congelada: α d = 12.3125.

Transmitancia teórica: T(ω₁) = 0.614400 · e^(−2 α d) = 1.241562e−11.

Criterio del nulo: T_medido(ω₁) ≤ 1e−8. El umbral es deliberadamente tres órdenes por encima de la predicción, para que un resultado nulo no dependa del último decimal. El mismo umbral corresponde a α d = 8.9668, es decir a una lámina de d = 1.4565 λ_p: si la observación no llega al umbral, la causa no es que la lámina sea corta.

Comprobación de forma cerrada: la transmitancia del escalón de espesor finito, 1 / (1 + 0.25 (κ + 1/κ)² sinh²(κ ω₁ d / c)), coincide con el producto prefactor por exponencial dentro de la precisión doble para d = λ_p y d = 2 λ_p.

## 5. Banda pasante — el control positivo

Frecuencia de prueba ω₂ = 2.0 ω_p.

Índice del medio: n = sqrt(1 − (ω_p/ω₂)²) = sqrt(3)/2 = 0.866025.

Reflectancia por cara: R = ((n − 1)/(n + 1))² = 0.005155.

Término de Fabry-Pérot: F = 4 R / (1 − R)² = 0.020833.

Fase de ida y vuelta en la lámina: β d = 21.7656 radianes.

Transmitancia teórica: T(ω₂) pertenece al intervalo cerrado [0.97959, 1.00000]. El extremo inferior es 1/(1 + F) = 0.979592, que corresponde al peor caso de interferencia constructiva de la reflexión.

Criterio del control positivo: T_medido(ω₂) ≥ 0.97. Si el control positivo no alcanza 0.97, EL EXPERIMENTO SE ANULA: no se reporta nulo, se reporta instrumento roto.

## 6. Punto a — excitación

La fuente es una corriente de superficie en una celda, con envolvente suave de dos medias ondas sobre el pulso completo:

J_s(t) = sin(ω₀ t) · sin²(π t / T_pulso), para 0 ≤ t ≤ T_pulso, y cero fuera de ese intervalo.

Ancho espectral exigido: T_pulso ≥ 40 · (2π/ω₀), lo que acota el ensanchamiento relativo del pico a Δω/ω₀ ≤ 0.05.

La transmitancia se mide como cociente de densidades espectrales en el bin central ω₀, no como cociente de valores de pico temporal.

## 7. Punto b — caja y ventana

Celdas del dominio: N_x = 800, equivalentes a 20 λ_p.

Absorbente: capa de tipo esponja o PML de 60 celdas en cada extremo.

Posición de la fuente: celda 100 (2.5 λ_p desde el borde interior del absorbente izquierdo).

Posición de la lámina: centrada en la celda 400; desde x_inicio = 400 − N_d/2 hasta x_fin = 400 + N_d/2, con N_d = d / Δx el número de celdas de la lámina.

Posición del monitor: celda 700 (2.5 λ_p antes del absorbente derecho).

Pasos temporales: N_t = 4000.

Criterio de ventana limpia: la energía residual registrada en el monitor al final de la corrida debe ser menor que 1e−12 del valor de referencia.

## 8. Punto c — protocolo de tres corridas

Corrida 1, referencia de vacío: N_d = 0 y ω_p = 0. Produce la traza de referencia E_ref en el monitor.

Corrida 2, piso dinámico: ω_p = 0 pero con la lámina presente y con las mismas rutinas ADE que integran J_z. Si la transmitancia de esta corrida se aparta de 1.0 en más de 1e−4, hay disipación espuria introducida por el integrador y EL EXPERIMENTO SE ANULA.

Corrida 3, lámina activa: ω_p mayor que cero, con las mismas rutinas. La transmitancia reportada es T = (magnitud de DFT de E_3 en ω₀) al cuadrado dividida por (magnitud de DFT de E_1 en ω₀) al cuadrado.

Las tres corridas comparten Δx, Δt, N_x, N_t, absorbente, fuente y monitor. Cambia únicamente N_d y ω_p.

## 9. Punto d — escalera de espesores y pendiente

Serie congelada: d aprox pertenece a {0.5, 1.0, 2.0, 4.0}, en unidades de λ_p.

Ajuste lineal: ln T = m · d aprox + b.

Pendiente teórica: m_teor = −2 α λ_p = −4π sqrt(1 − 0.2²) = −12.3125 por λ_p.

Intercepto teórico: b_teor = ln(0.614400) = −0.4871.

Tolerancia de aceptación de la pendiente: |m_medido − m_teor| / |m_teor| ≤ 0.02.

Predicción escalón que la escalera debe reproducir, con la transmitancia del escalón finito: d aprox = 0.5 da 1.306e−03; d aprox = 1.0 da 2.762e−06; d aprox = 2.0 da 1.242e−11; d aprox = 4.0 da 2.509e−22.

La cifra que decide el nulo es la pendiente, no un umbral único: una sola lectura por encima del piso puede confundirse con el piso del propio instrumento, y la pendiente no.

## 10. Presupuesto numérico y observaciones declaradas

Se declaran tres tensiones medidas antes de escribir, sin adjudicarlas. Quedan abiertas para decisión del dueño.

Observación 1, presupuesto temporal contra excitación. Con Δx = λ_p/40 y Δt = 0.99 Δx/c resulta Δt = 0.155509 λ_p/c, es decir 0.155509 / ω_p. La ventana N_t = 4000 cubre 622.04 / ω_p, o sea 19.80 periodos de la portadora ω₁ (periodo 2π/ω₁ = 31.4159 / ω_p). Un pulso que cumpla T_pulso ≥ 40 · (2π/ω₀) dura 1256.64 / ω_p y exige 8081 pasos; añadiendo el tránsito de 20 λ_p, unos 808 pasos, hacen falta cerca de 8889 pasos. Conclusión declarada: N_t = 4000 y T_pulso ≥ 40 periodos de portadora son mutuamente incompatibles si la fuente es un pulso. El ancho espectral Δω/ω₀ ≈ 0.05 sólo es alcanzable con N_t = 4000 si la fuente es onda continua durante toda la ventana (unos 20 ciclos), no un pulso de 40 ciclos.

Observación 2, rango dinámico de la escalera. Los dos extremos de la escalera quedan fuera del alcance de la doble precisión: d aprox = 2.0 predice 1.24e−11 y d aprox = 4.0 predice 2.51e−22. El segundo valor está por debajo del piso relativo de float64 (≈ 1e−16) aplicado a cualquier energía de referencia normalizada. Un ajuste de cuatro puntos en esas condiciones queda dominado por dos puntos no medibles, y la pendiente que de ellos salga no mide la lámina: mide el ruido de redondeo.

Observación 3, alcance real de la corrida de piso. La corrida 2 (ω_p = 0) mide la pérdida del integrador en la zona donde T es del orden de 1. No mide la capacidad del instrumento de resolver una transmitancia de 1e−11. Para la banda de corte profundo falta un control explícito de piso en esa banda: por ejemplo el bin espectral con la fuente apagada, o una corrida sin camino de señal. Sin ese control, un valor bajo en la lámina activa no se distingue de un cero de resolución.

## 11. Gates de este propio archivo y sello

Contrato de forma exigido a este archivo: cero signos de moneda; número de líneas de título H1 igual a 1; líneas de encabezado de sección contadas por prefijo; sin líneas de contenido no vacío repetidas; sin retorno de carro incrustado; identidad sellada por hash.

Tupla de la orden de primera escritura, declarada como excepción de alta: TARGET igual a PREREGISTRO_PLASMA_ADE_20261012.md dentro del repositorio plasma-ade; BLOB_PRE igual a ausente; LINEAS_PRE igual a 0; HUELLA igual al título H1 de este archivo.

T_UTC_S de verificación aritmética: 2026-10-12T06:59:18Z.

Ventana declarada de la aritmética: constantes verificadas con python3 en doble precisión; α d = 12.3125; prefactor = 0.614400; T(ω₁) = 1.241562e−11; umbral 1e−8 equivalente a α d = 8.9668 y a d = 1.4565 λ_p; n = 0.866025; R = 0.005155; F = 0.020833; β d = 21.7656 radianes; T mínimo de la banda pasante = 0.979592.

Estado de las tres observaciones de la sección 10: declaradas, no adjudicadas. Este pre-registro no las resuelve; las expone para que la decisión quede registrada antes de la primera corrida.
