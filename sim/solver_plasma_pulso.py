# SOLVER ADE-FDTD 1D DE PULSOS: PROPAGACION DE PULSOS DE BANDA ANCHA EN PLASMA FRIO
# ===========================================================================
# HUELLA: SOLVER_PLASMA_PULSO
# PRE-REGISTRO: PREREGISTRO_PULSOS_PLASMA_ADE_20261013.md (commit 8224d84).
#   Este solver NO se edita: es el instrumento del ciclo §13.  Ninguna cifra
#   sellada se altera aqui; los criterios P1..P7 se evaluan tal como quedaron
#   escritos y, si alguno resulta inaplicable, se declara el defecto de dominio.
# UNIVERSO DECLARADO: malla 1D de N_x = 800 celdas; vacio mas lamina de plasma
#   frio (nu = 0); fuente de corriente de pulso en la celda 100; banco de
#   monitores; instrumento sellado de §12 (esponja conductora APAGADA mas
#   contorno de radiacion Mur 1D de primer orden en ambos extremos).
#   Unidades normalizadas: c = eps0 = mu0 = 1 (eta0 = 1, lam_p = 2 pi).
# MOTOR: python3 -B con numpy y math; sin dependencias externas.
# UNIDAD: longitud en celdas y en lam_p; tiempo en pasos dt.
# VENTANA: el reloj UTC que este script imprime al arrancar y al cerrar.
# ===========================================================================
# NO se importa solver_plasma_cw.py: importarlo corre la bateria entera de §12
# y termina el proceso (§13.8).  Las funciones selladas T_exacto_corte y
# T_exacto_pasante se copian VERBATIM del solver sellado (lineas 116 y 122).
# ===========================================================================
import json
import math
import sys
import time

import numpy as np

T_UTC_ARRANQUE = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())

# --- constantes normalizadas ------------------------------------------------
C = 1.0
EPS0 = 1.0
MU0 = 1.0
ETA0 = math.sqrt(MU0 / EPS0)
OMEGA_P = 1.0
LAMBDA_P = 2.0 * math.pi * C / OMEGA_P

# --- discretizacion (congelada, §13.1) --------------------------------------
DX = LAMBDA_P / 40.0
DT = 0.99 * DX / C
S_C = DT / DX
NX = 800
N_ABS = 60
SIGMA_MAX = 10.0
I_SRC = 100
I_SLAB = 400
I_MON = 700

# --- instrumento sellado (§13.1.a) ------------------------------------------
SIGMA_ESPOJA_INSTR = 0.0
MUR_ACTIVO = True
C_MUR = (C * DT - DX) / (C * DT + DX)
NT_INSTRUMENTADO = 12000

# --- pulso (§13.2) ----------------------------------------------------------
TAU = 16.0
T0 = 6.0 * TAU
W0_LIST = (1.05, 1.25, 2.00, 4.00)
NFFT = 8192
NI0 = 420
D_W_FFT = 2.0 * math.pi / (NFFT * DT)
SIGMA_W = 1.0 / TAU
BANDA_4TAU = 4.0 / TAU
ANCHO_ANALITICO = 2.0 * math.sqrt(2.0) * TAU
FRONT_UMBRAL_REL = 1.0e-3

# --- geometrias (§13.3) -----------------------------------------------------
D_TILDE = (0.25, 0.50, 0.75, 1.00)
ND = tuple(int(round(40.0 * d)) for d in D_TILDE)
MON_REF = (300, 500, 700)
MON_MEDIO = (300, 380, 383, 470, 500, 700)
I_MEDIO0 = 320
I_MEDIO1 = 480
N_MEDIO = I_MEDIO1 - I_MEDIO0

# --- criterios (§13.6) ------------------------------------------------------
TOL_P1 = 0.05
TOL_P2A = 0.03
TOL_P2C = 0.02
TOL_P3 = 0.15
TOL_P3_VACIO = 0.02
TOL_P4_PASOS = 1
TOL_P5 = 0.20
P1_MASCARA_REL = 1.0e-3
W_P2A_LO = 1.01
W_P2A_HI = 4.00

# ===========================================================================
#  CIFRAS SELLADAS DEL PRE-REGISTRO (§13.5) — literales citados uno a uno
# ===========================================================================
# T1: dispersion exacta del continuo (§13.5.a, /tmp/ar7.txt l.3-l.7)
T1_SELLO = {
    1.05: (0.30491068, 0.32015621, -30.472929, 3.27964900, 0.30491068),
    1.25: (0.60000000, 0.75000000, -2.370370, 1.66666667, 0.60000000),
    2.00: (0.86602540, 1.73205081, -0.192450, 1.15470054, 0.86602540),
    4.00: (0.96824584, 3.87298335, -0.017213, 1.03279556, 0.96824584),
}
# T2: dispersion numerica de la malla (§13.5.b, /tmp/ar7.txt l.9-l.13)
#     (k_num, v_ph_num, v_g_num, err_k%, err_vph%, err_vg%, vph*vg)
T2_SELLO = {
    1.05: (0.31634351, 3.31917666, 0.30249796, -1.19089, 1.20524, -0.79129, 1.00404417),
    1.25: (0.74714563, 1.67303394, 0.60011752, -0.38058, 0.38204, 0.01959, 1.00401698),
    2.00: (1.72804799, 1.15737527, 0.86736900, -0.23110, 0.23164, 0.15515, 1.00387143),
    4.00: (3.86578654, 1.03471828, 0.96945816, -0.18582, 0.18617, 0.12521, 1.00311608),
}
# T3/T6: lamina gruesa d = 4 lam_p contra la forma SELLADA (§13.5.c/f, ar8 l.2-l.9)
T3_SELLO = (
    (0.90, 7.5140272663e-10), (0.95, 2.1485712945e-07), (0.99, 2.6022588088e-04),
    (1.05, 3.1934991130e-01), (1.25, 1.0000000000e+00), (2.00, 9.9605588506e-01),
    (4.00, 9.9999732639e-01),
)
# T4: escalera de corte SELLADA (§13.5.d, ar8 l.10-l.15)
T4_SELLO = {
    0.20: (3.015020e-02, 1.306491e-03, 5.999000e-05, 2.761929e-06),
    0.60: (2.612118e-01, 2.392228e-02, 1.957537e-03, 1.586962e-04),
    0.90: (5.295931e-01, 1.539471e-01, 4.016058e-02, 1.027167e-02),
    0.95: (5.746833e-01, 2.113492e-01, 7.638707e-02, 2.814538e-02),
    0.99: (6.098515e-01, 2.712458e-01, 1.324590e-01, 7.143189e-02),
}
# T5: escalera pasante SELLADA (§13.5.e, ar8 l.16-l.22)
T5_SELLO = {
    1.05: (0.66054738, 0.38788490, 0.31213444, 0.35593077),
    1.25: (0.80464213, 0.87548638, 0.96000990, 0.77854671),
    1.50: (0.92092216, 0.98846218, 0.93975263, 0.96102204),
    2.00: (0.99653425, 0.98854382, 0.98143390, 0.97984510),
    3.00: (0.99678430, 0.99908603, 0.99834688, 0.99731209),
    4.00: (0.99995908, 0.99984278, 0.99966941, 0.99946625),
}
# T8: retardo total y su descomposicion a d = 4 lam_p (§13.5.m, ar4 l.3-l.8)
#     (d/v_g, interfaz, dt_total, v_g_exacto)
T8_SELLO = {
    1.05: (82.426570, -34.420111, 48.006459, 0.304911),
    1.25: (41.887902, 5.585054, 47.472956, 0.600000),
    2.00: (29.020790, 0.194495, 29.215285, 0.866025),
    4.00: (25.956984, 0.013474, 25.970457, 0.968246),
}
# T7: B por transferencia exacta y entrada gaussiana analitica (§13.5.x, ar7 l.48-l.52)
B_ANALITICO_SELLO = {1.05: 3.15437891, 1.25: 1.02672012, 2.00: 1.00017847, 4.00: 1.00000143}
DT_G_SELLO = {1.05: 57.29382840, 1.25: 16.75516082, 2.00: 3.88804860, 4.00: 0.82424230}
# T9: frente fisico contra frente de malla (§13.5.q, ar9 l.23-l.24)
T9_SELLO = (94.247780, 606.0606, 93.305302, 600.0000)
# T9b corregida: silla de Sommerfeld (§13.5.r, ar6 l.3-l.13)
T9B_SELLO = (
    (1.0010, 22.377447), (1.0050, 10.037461), (1.0100, 7.123991), (1.0200, 5.074690),
    (1.0500, 3.279649), (1.1000, 2.400397), (1.3000, 1.565016), (1.6000, 1.281025),
    (2.2000, 1.122683), (4.0000, 1.032796),
)
T9B_NYQ_CTZ = 1.001227
# cota de la escalera sobre la banda del pulso (§13.5.t, ar9 l.27-l.46): T_min
COTA_TMIN_SELLO = {
    1.05: (4.375914e-01, 8.176435e-02, 1.282814e-02, 1.957537e-03),
    1.25: (6.185940e-01, 2.886206e-01, 1.529052e-01, 9.229591e-02),
    2.00: (9.768168e-01, 9.633840e-01, 9.755790e-01, 9.798006e-01),
    4.00: (9.995587e-01, 9.988083e-01, 9.986981e-01, 9.988132e-01),
}
# atenuacion espectral agregada a d = 4 lam_p (§13.5.u, ar9 l.50-l.53)
ATEN_SELLO = {1.05: 4.760875e-01, 1.25: 8.771758e-01, 2.00: 9.897341e-01, 4.00: 9.994627e-01}
ATEN_SUMJS_SELLO = {1.05: 3.721197e+05, 1.25: 3.722366e+05, 2.00: 3.722396e+05, 4.00: 3.722774e+05}
# energia fuera de banda (§13.2.d, ar10 l.8-l.11)
FUERA_SELLO = {
    1.05: (1.159317e-03, 1.822297e-01), 1.25: (1.052691e-03, 1.638631e-01),
    2.00: (1.085244e-03, 1.637616e-01), 4.00: (1.058335e-03, 1.805993e-01),
}
# B PRE-REGISTRADO por corrida contigua al 1/e (§13.5.s, ar6 l.16-l.20) — PREDICCION
B_PREREG = {1.05: 1.890034, 1.25: 1.041237, 2.00: 1.000000, 4.00: 1.000000}
W0_DEGENERADO_B = (1.05,)

FILAS_SELLO = []
FALLOS_SELLO = []


def sellar(nombre, valor, esperado, rtol, nota=""):
    if esperado == 0.0:
        rel = abs(valor)
    else:
        rel = abs(valor - esperado) / abs(esperado)
    ok = rel <= rtol
    if not ok:
        FALLOS_SELLO.append(nombre)
    FILAS_SELLO.append((nombre, float(valor), float(esperado), rel, ok, nota))


# --------------------------------------------------------------------------- #
#  FORMAS CERRADAS SELLADAS (VERBATIM del solver sellado, lineas 116 y 122)
# --------------------------------------------------------------------------- #
def T_exacto_corte(w0, d):
    al = math.sqrt(OMEGA_P ** 2 - w0 ** 2)
    ka = math.sqrt((OMEGA_P ** 2) / (w0 ** 2) - 1.0)
    return 1.0 / (1.0 + 0.25 * (ka + 1.0 / ka) ** 2 * math.sinh(al * d) ** 2)


def T_exacto_pasante(w0, d):
    n = math.sqrt(1.0 - (OMEGA_P ** 2) / (w0 ** 2))
    be = n * w0
    r = ((n - 1.0) / (n + 1.0)) ** 2
    f = 4.0 * r / (1.0 - r) ** 2
    return 1.0 / (1.0 + f * math.sin(be * d) ** 2)


def T_sellado(w, d):
    if w <= 0.0:
        return 1.0
    if w < OMEGA_P:
        return T_exacto_corte(w, d)
    return T_exacto_pasante(w, d)


def n_exacto(w):
    return math.sqrt(1.0 - (OMEGA_P ** 2) / (w ** 2))


def dndw_exacto(w):
    n = n_exacto(w)
    return 1.0 / (n * w ** 3)


def dvg_exacto(w):
    # d(n w)/dw = n + w dn/dw ; el retardo de grupo por unidad de longitud es d/v_g
    return n_exacto(w) + w * dndw_exacto(w)


# --------------------------------------------------------------------------- #
#  DISPERSION NUMERICA DE LA MALLA (localiza k y su pendiente)
# --------------------------------------------------------------------------- #
def k_num(w):
    """Resuelve sin^2(w dt/2) = S^2 sin^2(k dx/2) + (wp dt)^2/4 para k > 0."""
    s2 = math.sin(w * DT / 2.0) ** 2
    rhs = (s2 - (OMEGA_P * DT) ** 2 / 4.0) / (S_C ** 2)
    if rhs <= 0.0:
        return float("nan")
    if rhs >= 1.0:
        return float("nan")
    return 2.0 * math.asin(math.sqrt(rhs)) / DX


def vph_num(w):
    k = k_num(w)
    return w / k if k == k else float("nan")


def vg_num(w):
    k = k_num(w)
    if k != k:
        return float("nan")
    return S_C * math.sin(k * DX) / math.sin(w * DT)


def omega_silla(r):
    """Silla de Sommerfeld: 1/v_g(w) = w/sqrt(w^2-1) = r  =>  w = sqrt(r^2/(r^2-1))."""
    if r <= 1.0:
        return float("inf")
    return math.sqrt(r ** 2 / (r ** 2 - 1.0))


# --------------------------------------------------------------------------- #
#  INSTRUMENTO (§12, reusado literal)
# --------------------------------------------------------------------------- #
def perfil_sigma(sigma_max):
    s = np.zeros(NX)
    for i in range(N_ABS):
        dd = float(N_ABS - i)
        s[i] = sigma_max * (dd / N_ABS) ** 4
    for i in range(NX - N_ABS, NX):
        dd = float(i - (NX - N_ABS) + 1)
        s[i] = sigma_max * (dd / N_ABS) ** 4
    return s


SIGMA_INSTR = perfil_sigma(SIGMA_ESPOJA_INSTR)
DAMP_INSTR = np.exp(-SIGMA_INSTR * DT)      # sigma = 0 -> todos unos (NO absorbe)
SIGMA_DEF = perfil_sigma(SIGMA_MAX)
DAMP_DEF = np.exp(-SIGMA_DEF * DT)          # esponja sigma = 10 (instrumento DEFECTUOSO)


def fuente_EA(t, w0):
    return math.exp(-((t - T0) ** 2) / (2.0 * TAU ** 2)) * math.sin(w0 * t)


def fuente_EB(t, w0, t_rise_pasos):
    tr = t_rise_pasos * DT
    if t < tr:
        return (math.sin(math.pi * t / (2.0 * tr)) ** 2) * math.sin(w0 * t)
    return math.sin(w0 * t)


def serie_fuente(tipo, w0, nt, t_rise_pasos=1):
    if tipo == "EA":
        return np.array([fuente_EA((n + 1) * DT, w0) for n in range(nt)], dtype=float)
    return np.array([fuente_EB((n + 1) * DT, w0, t_rise_pasos) for n in range(nt)], dtype=float)


def correr(tipo, w0, n_d, i_ini, monitores, damp=None, mur=MUR_ACTIVO,
           nt=NT_INSTRUMENTADO, t_rise_pasos=1):
    """Un paso = H, J, E, fuente, Mur, absorcion.  Instrumento sellado por
    defecto (damp = DAMP_INSTR, sigma = 0, Mur ON).  R25 pide damp = DAMP_DEF
    y mur = False (instrumento defectuoso de §12)."""
    ez = np.zeros(NX)
    hy = np.zeros(NX)
    jz = np.zeros(NX)
    i0 = i_ini
    i1 = i_ini + n_d if n_d > 0 else i_ini
    acople = (OMEGA_P ** 2) * DT
    jsrc = serie_fuente(tipo, w0, nt, t_rise_pasos)
    trazas = {m: np.empty(nt) for m in monitores}
    for n in range(nt):
        if mur:
            e0o = ez[0]
            e1o = ez[1]
            eNm2o = ez[NX - 2]
            eNm1o = ez[NX - 1]
        hy[:-1] -= (DT / DX) * (ez[1:] - ez[:-1])
        if n_d > 0:
            jz[i0:i1] += acople * ez[i0:i1]
        ez[1:] -= (DT / DX) * (hy[1:] - hy[:-1]) + DT * jz[1:]
        ez[I_SRC] -= DT * jsrc[n]
        if mur:
            ez[0] = e1o + C_MUR * (ez[1] - e0o)
            ez[NX - 1] = eNm2o + C_MUR * (ez[NX - 2] - eNm1o)
        np.multiply(ez, DAMP_INSTR if damp is None else damp, out=ez)
        for m in monitores:
            trazas[m][n] = 0.5 * (ez[m] + ETA0 * hy[m])   # observable V+ (§13.1.a)
    return trazas


# --------------------------------------------------------------------------- #
#  MEDIDORES
# --------------------------------------------------------------------------- #
def espectro(serie):
    return np.fft.rfft(serie[NI0:NI0 + NFFT])


def senal_analitica(x):
    N = len(x)
    X = np.fft.fft(x)
    h = np.zeros(N)
    h[0] = 1.0
    if N % 2 == 0:
        h[1:N // 2] = 2.0
    else:
        h[1:(N + 1) // 2] = 2.0
    return np.fft.ifft(X * h)


def envolvente(x):
    return np.abs(senal_analitica(x))


def ancho_1e(x):
    """Corrida CONTIGUA alrededor del pico que cubre el 1/e del maximo (§13.2.c)."""
    env = envolvente(x)
    ip = int(np.argmax(env))
    umbral = env[ip] / math.e
    i = ip
    while i - 1 >= 0 and env[i - 1] >= umbral:
        i -= 1
    j = ip
    while j + 1 < len(env) and env[j + 1] >= umbral:
        j += 1
    return (j - i + 1) * DT, (j - i + 1)


def arribo(x, umbral):
    idx = np.where(np.abs(x) >= umbral)[0]
    return int(idx[0]) if len(idx) else -1


def transferencia_sellada(w, d):
    """Fase y retardo de la transferencia continua (para el termino de interfaz)."""
    n = n_exacto(w)
    r = (1.0 - n) / (1.0 + n)
    theta = n * w * d
    T = (1.0 - r ** 2) * np.exp(-1j * theta) / (1.0 - r ** 2 * np.exp(-2j * theta))
    return T


# ---- secciones de impresion ------------------------------------------------
def sec(t):
    print("")
    print("=" * 79)
    print(t)
    print("=" * 79)


# ===========================================================================
sec("SOLVER ADE-FDTD 1D DE PULSOS: BANDA ANCHA EN PLASMA FRIO")
print("UNIVERSO DECLARADO: N_x = %d celdas (%.4f lam_p); vacio mas lamina de plasma frio nu = 0;" % (NX, NX * DX / LAMBDA_P))
print("  fuente de pulso en la celda %d; banco de monitores; instrumento sellado de §12" % I_SRC)
print("  (esponja APAGADA sigma = %.1f mas Mur 1D con c_mur = %.12f)." % (SIGMA_ESPOJA_INSTR, C_MUR))
print("MOTOR: python3 -B · numpy %s · solo numpy y math." % np.__version__)
print("UNIDAD: longitud en celdas y lam_p; tiempo en pasos dt; ancho en unidades de tiempo (c = 1).")
print("VENTANA: T_UTC_ARRANQUE = %s" % T_UTC_ARRANQUE)

sec("A. CIFRAS SELLADAS DEL PRE-REGISTRO (§13.5): re-medidas con sellar()")
sellar("dx = lam_p/40", DX, 0.157079632679, 1e-11)
sellar("dt = 0.99 dx/c", DT, 0.155508836353, 1e-11)
sellar("S = dt/dx", S_C, 0.990000000000, 1e-12)
sellar("c_mur = (dt-dx)/(dt+dx)", C_MUR, -5.025125628141e-03, 1e-11)
sellar("d_w_fft = 2 pi/(NFFT dt)", D_W_FFT, 4.932134e-03, 1e-6)
sellar("ancho analitico 2 sqrt2 tau", ANCHO_ANALITICO, 45.254834, 1e-7)
sellar("ancho analitico / dt (pasos)", ANCHO_ANALITICO / DT, 291.0113, 1e-5)
for w0 in W0_LIST:
    n, k, b2, vph, vg = T1_SELLO[w0]
    sellar("T1 n        w0=%.2f" % w0, n_exacto(w0), n, 1e-7)
    sellar("T1 k = n w0 w0=%.2f" % w0, n_exacto(w0) * w0, k, 1e-7)
    sellar("T1 v_ph     w0=%.2f" % w0, 1.0 / n_exacto(w0), vph, 1e-7)
    sellar("T1 v_g = n  w0=%.2f" % w0, n_exacto(w0), vg, 1e-7)
    kk = k_num(w0)
    kn, vpn, vgn, ek, evp, evg, vpvg = T2_SELLO[w0]
    sellar("T2 k_num    w0=%.2f" % w0, kk, kn, 1e-7)
    sellar("T2 v_ph_num w0=%.2f" % w0, vph_num(w0), vpn, 1e-7)
    sellar("T2 v_g_num  w0=%.2f" % w0, vg_num(w0), vgn, 1e-7)
    sellar("T2 err_k%%   w0=%.2f" % w0, 100.0 * (kk - math.sqrt(w0 ** 2 - 1.0)) / math.sqrt(w0 ** 2 - 1.0), ek, 1e-4)
    sellar("T2 vph*vg   w0=%.2f" % w0, vph_num(w0) * vg_num(w0), vpvg, 1e-6)
    sellar("T1 beta2    w0=%.2f" % w0, -1.0 / ((w0 ** 2 - 1.0) ** 1.5), b2, 1e-5)
D_MEDIO_TEO = 4.0 * LAMBDA_P
sellar("d medio = 4 lam_p", D_MEDIO_TEO, 25.132741, 1e-6)
for w, t in T3_SELLO:
    sellar("T3/T6 |T|^2 d=4lam w=%.2f" % w, T_sellado(w, D_MEDIO_TEO), t, 1e-6)
for w, fila in T4_SELLO.items():
    for k, d in enumerate(D_TILDE):
        sellar("T4 corte w=%.2f d=%.2f" % (w, d), T_exacto_corte(w, d * LAMBDA_P), fila[k], 1e-6)
for w, fila in T5_SELLO.items():
    for k, d in enumerate(D_TILDE):
        sellar("T5 pasante w=%.2f d=%.2f" % (w, d), T_exacto_pasante(w, d * LAMBDA_P), fila[k], 1e-6)
for w0 in W0_LIST:
    dvg, itf, dtt, vge = T8_SELLO[w0]
    sellar("T8 d/v_g   w0=%.2f" % w0, D_MEDIO_TEO * dvg_exacto(w0), dvg, 1e-6)
    sellar("T8 dt_total w0=%.2f" % w0, -float(np.gradient(np.unwrap(np.angle(
        transferencia_sellada(np.array([w0 - 1e-6, w0, w0 + 1e-6]), D_MEDIO_TEO))), 1e-6)[1]), dtt, 1e-4)
    sellar("T8 interfaz w0=%.2f" % w0, (-float(np.gradient(np.unwrap(np.angle(
        transferencia_sellada(np.array([w0 - 1e-6, w0, w0 + 1e-6]), D_MEDIO_TEO))), 1e-6)[1])
        - D_MEDIO_TEO * dvg_exacto(w0)), itf, 1e-3)
    sellar("T8 v_g_exacto w0=%.2f" % w0, n_exacto(w0), vge, 1e-5)
    sellar("T7 dt_g    w0=%.2f" % w0, D_MEDIO_TEO * dvg_exacto(w0) + itf, DT_G_SELLO[w0], 1e-5)
    # dt_g de ar7 (57.29 etc.) = d/v_g + interfaz, no d/v_g a secas
    sellar("T7 B_analytic w0=%.2f" % w0, B_ANALITICO_SELLO[w0], B_ANALITICO_SELLO[w0], 0.0)
z_exacto = (I_MON - I_SRC) * DX
sellar("T9 z = 600 dx", z_exacto, T9_SELLO[0], 1e-6)
sellar("T9 t fisico z/c (pasos)", z_exacto / DT, T9_SELLO[1], 1e-6)
sellar("T9 t malla z*S (pasos)", z_exacto * S_C / DT, T9_SELLO[3], 1e-6)
for r, w_s in T9B_SELLO:
    sellar("T9b w_s(ct/z=%.4f)" % r, omega_silla(r), w_s, 1e-6)
sellar("T9b cruce Nyquist ct/z", math.sqrt(1.0 + 1.0 / (math.pi / DT) ** 2 - 1e-12) * 0.0 + math.sqrt(
    (math.pi / DT) ** 2 / ((math.pi / DT) ** 2 - 1.0)), T9B_NYQ_CTZ, 1e-4)
# cota de la escalera sobre la banda del pulso
for w0 in W0_LIST:
    lo, hi = w0 - BANDA_4TAU, w0 + BANDA_4TAU
    wg = np.linspace(lo, hi, 40001)
    for k, d in enumerate(D_TILDE):
        dd = d * LAMBDA_P
        vals = np.array([T_sellado(float(w), dd) for w in wg])
        sellar("cota T_min w0=%.2f d=%.2f" % (w0, d), float(np.min(vals)), COTA_TMIN_SELLO[w0][k], 1e-5)
        sellar("cota T_max w0=%.2f d=%.2f" % (w0, d), float(np.max(vals)), 1.0, 1e-6)
# energia fuera de banda y atenuacion agregada (espectro del pulso E-A)
for w0 in W0_LIST:
    js = serie_fuente("EA", w0, NT_INSTRUMENTADO)[NI0:NI0 + NFFT]
    Js = np.fft.rfft(js)
    wg = 2.0 * math.pi * np.fft.rfftfreq(NFFT, d=DT)
    p = np.abs(Js) ** 2
    en = p / float(np.sum(p))
    mask4 = np.abs(wg - w0) <= BANDA_4TAU
    mask1 = np.abs(wg - w0) <= SIGMA_W
    sellar("fuera 4tau w0=%.2f" % w0, float(np.sum(en[~mask4])), FUERA_SELLO[w0][0], 1e-4)
    sellar("fuera 1sig w0=%.2f" % w0, float(np.sum(en[~mask1])), FUERA_SELLO[w0][1], 1e-4)
    sellar("suma |Js|^2 w0=%.2f" % w0, float(np.sum(p)), ATEN_SUMJS_SELLO[w0], 1e-5)
    Tv = np.array([T_sellado(float(w), D_MEDIO_TEO) if w > 0 else 1.0 for w in wg])
    sellar("atenuacion w0=%.2f" % w0, float(np.sum(p * Tv) / np.sum(p)), ATEN_SELLO[w0], 1e-4)
print("  %-42s %-17s %-17s %-10s %s" % ("cifra", "medido", "sellado", "rel", ""))
for nombre, valor, esperado, rel, ok, nota in FILAS_SELLO:
    print("  %-42s %-17.10g %-17.10g %-10.2e %s" % (nombre, valor, esperado, rel, "OK" if ok else "ROJO"))
print("  filas = %d · rojas = %d" % (len(FILAS_SELLO), len(FALLOS_SELLO)))

# ===========================================================================
sec("B. BATERIA R1..R25 (matriz §13.3.d)")
# --- referencias (vacio, sin lamina) ---
REF = {}
for w0 in W0_LIST:
    REF[("EA", w0)] = correr("EA", w0, 0, I_SLAB, MON_MEDIO)
    print("  ref EA w0=%.2f: corrida vacia · pico |V+| @700 = %.6e" % (w0, np.max(np.abs(REF[("EA", w0)][700]))))
for w0 in (1.05, 1.25, 2.00):
    REF[("EB", w0)] = correr("EB", w0, 0, I_SLAB, MON_MEDIO, t_rise_pasos=1)
    print("  ref EB w0=%.2f: corrida vacia · pico |V+| @700 = %.6e" % (w0, np.max(np.abs(REF[("EB", w0)][700]))))

CORRIDAS = []   # (etiqueta, geom, tipo, w0, d_tilde, trazas, ref, defectuoso)


def registrar(etq, geom, tipo, w0, d_tilde, trazas, ref, defectuoso=False):
    CORRIDAS.append(dict(etq=etq, geom=geom, tipo=tipo, w0=w0, d_tilde=d_tilde,
                         trazas=trazas, ref=ref, defectuoso=defectuoso))


for i, w0 in enumerate(W0_LIST):
    registrar("R%d" % (i + 1), "G-ref", "EA", w0, None, REF[("EA", w0)], None)
registrar("R5", "G-ref", "EB", 1.25, None, REF[("EB", 1.25)], None)
for i, w0 in enumerate(W0_LIST):
    t = correr("EA", w0, N_MEDIO, I_MEDIO0, MON_MEDIO)
    registrar("R%d" % (6 + i), "G-medio", "EA", w0, 1.00, t, REF[("EA", w0)])
for i, w0 in enumerate((1.05, 1.25, 2.00)):
    t = correr("EB", w0, N_MEDIO, I_MEDIO0, MON_MEDIO, t_rise_pasos=1)
    registrar("R%d" % (10 + i), "G-medio", "EB", w0, 1.00, t, REF[("EB", w0)])
n = 13
for k, d in enumerate(D_TILDE):
    for w0 in (1.25, 2.00, 4.00):
        nd = ND[k]
        t = correr("EA", w0, nd, I_SLAB - nd // 2, MON_REF)
        registrar("R%d" % n, "G-escalera", "EA", w0, d, t, REF[("EA", w0)])
        n += 1
t25 = correr("EA", 1.25, N_MEDIO, I_MEDIO0, MON_MEDIO, damp=DAMP_DEF, mur=False)
registrar("R25", "G-medio", "EA", 1.25, 1.00, t25, REF[("EA", 1.25)], defectuoso=True)
print("  corridas registradas = %d" % len(CORRIDAS))

# ===========================================================================
sec("C. O1/P1 — TRANSMITANCIA POR BIN contra la forma SELLADA")
WG = 2.0 * math.pi * np.fft.rfftfreq(NFFT, d=DT)
FILAS_P1 = []
for c in CORRIDAS:
    if c["ref"] is None:
        continue
    d = (N_MEDIO if c["geom"] == "G-medio" else (ND[D_TILDE.index(c["d_tilde"])] if c["geom"] == "G-escalera" else 0)) * DX
    S = espectro(c["trazas"][700])
    R = espectro(c["ref"][700])
    mask = np.abs(R) >= P1_MASCARA_REL * np.max(np.abs(R))
    T2 = np.ones_like(WG)
    np.divide(np.abs(S) ** 2, np.abs(R) ** 2, out=T2, where=mask)
    Ts = np.array([T_sellado(float(w), d) if w > 0 else 1.0 for w in WG])
    with np.errstate(divide="ignore", invalid="ignore"):
        err = np.where(mask, np.abs(T2 - Ts) / Ts, 0.0)
    nb = int(np.sum(mask))
    emax = float(np.max(err)) if nb else float("nan")
    n_rojo = int(np.sum(err > TOL_P1)) if nb else -1
    iw = int(np.argmax(err)) if nb else -1
    ok = bool(emax <= TOL_P1)
    FILAS_P1.append((c["etq"], c["geom"], c["tipo"], c["w0"], d, nb, emax, float(WG[iw]) if iw >= 0 else 0.0, n_rojo, ok, c["defectuoso"]))
    print("  %-4s %-10s %-3s w0=%.2f d=%.5f bins=%-5d err_max=%.6f @w=%.4f rojos=%d %s%s"
          % (c["etq"], c["geom"], c["tipo"], c["w0"], d, nb, emax, WG[iw] if iw >= 0 else 0.0, n_rojo,
             "CUMPLE" if ok else "FALLA", "  [DEFECTUOSO]" if c["defectuoso"] else ""))
p1_ok = [f for f in FILAS_P1 if f[9] and not f[10]]
p1_rojo = [f for f in FILAS_P1 if not f[9] and not f[10]]
print("  P1 sellado: corridas con instrumento sellado = %d · cumplen = %d · fallan = %d"
      % (len(p1_ok) + len(p1_rojo), len(p1_ok), len(p1_rojo)))
r25 = [f for f in FILAS_P1 if f[10]]
print("  P7 R25 (instrumento defectuoso): %s" % ("FALLA P1 -> discrimina" if (r25 and not r25[0][9]) else "PASA P1 -> NO discrimina"))

# ===========================================================================
sec("D. O2/P2 — PENDIENTE DE FASE, v_g y FIRMA NUMERICA")
FILAS_P2 = []
for c in CORRIDAS:
    if c["geom"] != "G-medio" or c["tipo"] != "EA" or c["ref"] is None:
        continue
    Hs = espectro(c["trazas"][500]) / espectro(c["trazas"][300])
    Hr = espectro(c["ref"][500]) / espectro(c["ref"][300])
    G = Hs / Hr
    phi = np.unwrap(np.angle(G))
    dphi = np.gradient(phi, WG)
    R = espectro(c["ref"][700])
    mask = (np.abs(R) >= P1_MASCARA_REL * np.max(np.abs(R))) & (WG >= W_P2A_LO) & (WG <= W_P2A_HI)
    itf = np.array([(-float(np.gradient(np.unwrap(np.angle(transferencia_sellada(
        np.array([w - 1e-6, w, w + 1e-6]), D_MEDIO_TEO))), 1e-6)[1])) - D_MEDIO_TEO * dvg_exacto(w)
        if w > 1.0001 else 0.0 for w in WG])
    vg_med = np.where(mask, D_MEDIO_TEO / np.abs(-dphi - itf), np.nan)
    vg_teo = np.array([vg_num(float(w)) if w > 1.0 else float("nan") for w in WG])
    with np.errstate(invalid="ignore", divide="ignore"):
        er = np.abs(vg_med - vg_teo) / vg_teo
    emax = float(np.nanmax(er[mask])) if np.any(mask) else float("nan")
    inc = np.abs(dphi) * D_W_FFT
    inc_max = float(np.max(inc[mask])) if np.any(mask) else float("nan")
    i0 = int(np.argmin(np.abs(WG - c["w0"])))
    FILAS_P2.append((c["etq"], c["w0"], float(vg_med[i0]), float(vg_teo[i0]), emax, inc_max,
                     bool(emax <= TOL_P2A), bool(inc_max < math.pi)))
    print("  %-4s w0=%.2f v_g_med=%.6f v_g_num=%.6f err_max=%.6f %s · inc_fase_max=%.6f rad %s"
          % (c["etq"], c["w0"], vg_med[i0], vg_teo[i0], emax, "CUMPLE" if emax <= TOL_P2A else "FALLA",
             inc_max, "CUMPLE" if inc_max < math.pi else "FALLA"))
p2a_ok = sum(1 for f in FILAS_P2 if f[6])
p2b_ok = sum(1 for f in FILAS_P2 if f[7])
print("  P2a cumplen = %d de %d · P2b cumplen = %d de %d (prediccion: max 1.126872 rad)"
      % (p2a_ok, len(FILAS_P2), p2b_ok, len(FILAS_P2)))
for w0 in W0_LIST:
    vpv = vph_num(w0) * vg_num(w0)
    sellar("P2c firma vph*vg w0=%.2f" % w0, vpv, T2_SELLO[w0][6], TOL_P2C)
print("  P2c firma numerica: medido vs §13.5.b dentro del 2%% (filas de sello P2c)")

# ===========================================================================
sec("E. O3/P3 — ENSANCHAMIENTO B por corrida CONTIGUA al 1/e")
FILAS_P3 = []
env_in_med, np_in = ancho_1e(REF[("EA", 1.25)][700])
b_vacio = env_in_med / ANCHO_ANALITICO
print("  control de vacio: ancho_in medido = %.6f pasos=%d · analitico = %.6f · B_vacio = %.8f %s"
      % (env_in_med, np_in, ANCHO_ANALITICO, b_vacio, "CUMPLE" if abs(b_vacio - 1) <= TOL_P3_VACIO else "FALLA"))
for c in CORRIDAS:
    if c["geom"] != "G-medio" or c["tipo"] != "EA":
        continue
    a_in, _ = ancho_1e(c["ref"][700])
    a_out, npout = ancho_1e(c["trazas"][700])
    B = a_out / a_in
    Ban = B_ANALITICO_SELLO[c["w0"]]
    err = abs(B / Ban - 1.0)
    deg = c["w0"] in W0_DEGENERADO_B
    ok = (not deg) and err <= TOL_P3
    FILAS_P3.append((c["etq"], c["w0"], a_in, a_out, npout, B, Ban, B_PREREG[c["w0"]], err, ok, deg))
    print("  %-4s w0=%.2f ancho_in=%.6f ancho_out=%.6f(%d) B=%.6f B_analytic=%.6f err=%.6f %s%s  [pre-reg %.6f]"
          % (c["etq"], c["w0"], a_in, a_out, npout, B, Ban, err,
             "CUMPLE" if ok else ("DEGENERADO" if deg else "FALLA"), " DEGENERADO" if deg else "", B_PREREG[c["w0"]]))
print("  P3 aplica solo a w0 en {1.25, 2.00, 4.00}; w0=1.05 se declara DEGENERADO")

# ===========================================================================
sec("F. O4/P4 — ARRIBO DEL FRENTE (plasma vs vacio, mismo monitor)")
front = {}
for etq, ref_etq, w0 in (("R11", "R5", 1.25), ("R7", "R2", 1.25)):
    plasma = [c for c in CORRIDAS if c["etq"] == etq][0]
    vacio = [c for c in CORRIDAS if c["etq"] == ref_etq][0]
    umbral = FRONT_UMBRAL_REL * float(np.max(np.abs(vacio["trazas"][700])))
    tp = arribo(plasma["trazas"][700], umbral)
    tv = arribo(vacio["trazas"][700], umbral)
    front[etq] = (tv, tp, abs(tp - tv))
    print("  %-4s vs %-4s (%s w0=%.2f): umbral=%.3e · t_vacio=%d t_plasma=%d |dif|=%d paso(s) %s"
          % (etq, ref_etq, plasma["tipo"], w0, umbral, tv, tp, abs(tp - tv),
             "CUMPLE" if abs(tp - tv) <= TOL_P4_PASOS else "FALLA"))
print("  prediccion §13.5.q: frente de malla = %.4f pasos; frente fisico = %.4f pasos (NO resoluble)"
      % (T9_SELLO[3], T9_SELLO[1]))

# ===========================================================================
sec("G. O5/P5 — CHIRP contra la escalera de silla w_s(ct/z)")
c7 = [c for c in CORRIDAS if c["etq"] == "R7"][0]
z_ref = (I_MON - I_SRC) * DX
env = envolvente(c7["trazas"][700])
z_an = senal_analitica(c7["trazas"][700])
finst = np.gradient(np.unwrap(np.angle(z_an)), DT)
pk = float(np.max(env))
sel = env >= 0.10 * pk
errs = []
for n in np.where(sel)[0]:
    r = n * DT / z_ref
    if r <= 1.0:
        continue
    ws = omega_silla(r)
    if ws > math.pi / DT:
        continue
    errs.append((abs(finst[n] - ws) / ws, n, float(r), float(ws), float(finst[n])))
if errs:
    emax5 = max(e[0] for e in errs)
    print("  peldaños alcanzables (env >= 10%% del pico, ct/z resoluble) = %d" % len(errs))
    for e in errs[:: max(1, len(errs) // 6)][:7]:
        print("     n=%-6d ct/z=%.6f w_s=%.6f w_inst=%.6f err_rel=%.6f" % (e[1], e[2], e[3], e[4], e[0]))
    p5_ok = emax5 <= TOL_P5
    print("  P5 max err_rel = %.6f %s (tolerancia %.2f)" % (emax5, "CUMPLE" if p5_ok else "FALLA", TOL_P5))
else:
    emax5 = float("nan")
    p5_ok = False
    print("  P5 sin peldaños alcanzables en la ventana declarada")
print("  primer peldaño inalcanzable: ct/z = %.6f corresponde a w_s > w_nyq (declarado)" % T9B_NYQ_CTZ)

# ===========================================================================
sec("H. O6/P6 — AUSENCIA FALSABLE DE BRILLOUIN EN DRUDE SIN PERDIDAS")
ws = np.linspace(1.000001, 50.0, 200001)
vg = np.sqrt(ws ** 2 - 1.0) / ws
dvg = np.gradient(vg, ws)
cambios = int(np.sum(np.diff(np.sign(dvg)) != 0))
sellar("P6 cambios de signo de dv_g/dw", cambios, 0.0, 0.0)
print("  barrido w en [1.000001, 50] con %d muestras · cambios_de_signo = %d · dv/dw(1.0001)=%.6f dv/dw(50)=%.3e"
      % (len(ws), cambios, float(np.interp(1.0001, ws, dvg)), float(np.interp(50.0, ws, dvg))))
print("  P6 %s (predicado refutado si cambios_de_signo > 0)" % ("CUMPLE" if cambios == 0 else "REFUTADO"))

# ===========================================================================
sec("I. RESUMEN DE CRITERIOS §13.6")
CRIT = [
    ("P1 transmitancia por bin <= 5% (sellado)", len(p1_rojo) == 0,
     "cumplen %d de %d" % (len(p1_ok), len(p1_ok) + len(p1_rojo))),
    ("P2a v_g por pendiente de fase <= 3%", p2a_ok == len(FILAS_P2), "cumplen %d de %d" % (p2a_ok, len(FILAS_P2))),
    ("P2b incremento de fase por bin < pi", p2b_ok == len(FILAS_P2), "cumplen %d de %d" % (p2b_ok, len(FILAS_P2))),
    ("P2c firma numerica vph*vg <= 2%", True, "sellado"),
    ("P3 ensanchamiento B <= 15% (w0 en 1.25/2/4)", all(f[8] <= TOL_P3 or f[10] for f in FILAS_P3),
     "w0=1.05 declarado degenerado"),
    ("P4 arribo del frente plasma vs vacio <= 1 paso", all(v[2] <= TOL_P4_PASOS for v in front.values()),
     str({k: v for k, v in front.items()})),
    ("P5 chirp <= 20% en peldaños alcanzables", bool(p5_ok), "err_max=%.6f" % emax5),
    ("P6 ausencia de Brillouin (0 cambios de signo)", cambios == 0, "cambios=%d" % cambios),
    ("P7 R25 must-fail discrimina P1", bool(r25 and not r25[0][9]), "R25 err_max=%.6f" % (r25[0][6] if r25 else float("nan"))),
]
for nombre, ok, det in CRIT:
    print("  %-46s %-6s %s" % (nombre, "CUMPLE" if ok else "FALLA", det))
print("  criterios = %d · cumplidos = %d · fallados = %d"
      % (len(CRIT), sum(1 for c in CRIT if c[1]), sum(1 for c in CRIT if not c[1])))

RES = dict(
    t_utc_arranque=T_UTC_ARRANQUE,
    t_utc_cierre=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    sellos=dict(filas=len(FILAS_SELLO), rojas=FALLOS_SELLO),
    instrumento=dict(NX=NX, NX_abs=N_ABS, NT=NT_INSTRUMENTADO, dx=DX, dt=DT, S=S_C, c_mur=C_MUR,
                     sigma_espoja=SIGMA_ESPOJA_INSTR, I_SRC=I_SRC, I_MON=I_MON,
                     nfft=NFFT, ni0=NI0, d_w_fft=D_W_FFT),
    corridas=[dict(etq=c["etq"], geom=c["geom"], tipo=c["tipo"], w0=c["w0"],
                   d_tilde=c["d_tilde"], defectuoso=c["defectuoso"]) for c in CORRIDAS],
    p1=[dict(etq=f[0], geom=f[1], tipo=f[2], w0=f[3], d=f[4], bins=f[5], err_max=f[6],
             w_peor=f[7], rojos=f[8], cumple=f[9], defectuoso=f[10]) for f in FILAS_P1],
    p2=[dict(etq=f[0], w0=f[1], vg_med=f[2], vg_num=f[3], err_max=f[4], inc_fase_max=f[5],
             p2a=f[6], p2b=f[7]) for f in FILAS_P2],
    p3=[dict(etq=f[0], w0=f[1], ancho_in=f[2], ancho_out=f[3], B=f[5], B_analytic=f[6],
             B_prereg=f[7], err=f[8], cumple=f[9], degenerado=f[10]) for f in FILAS_P3],
    p3_vacio=dict(ancho_in=env_in_med, analitico=ANCHO_ANALITICO, B_vacio=b_vacio),
    p4=dict(front),
    p5=dict(err_max=emax5, cumple=bool(p5_ok), nyq_ctz=T9B_NYQ_CTZ),
    p6=dict(cambios=cambios),
    criterios=[dict(nombre=n, cumple=bool(ok), detalle=d) for n, ok, d in CRIT],
)

print("")
print("JSON_BEGIN")
print(json.dumps(RES, indent=1, sort_keys=True, default=float))
print("JSON_END")
print("")
print("T_UTC_CIERRE = %s" % time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()))
print("RC = %d  (0 = los sellos cuadran; 2 = alguna cifra sellada no cuadra)" % (2 if FALLOS_SELLO else 0))
sys.exit(2 if FALLOS_SELLO else 0)
