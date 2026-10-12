# SOLVER ADE-FDTD 1D CW: ESCALERA EXACTA Y TESTIGO PEC
# ===========================================================================
# UNIVERSO DECLARADO: malla 1D de N_x = 800 celdas; vacio + lamina de plasma
#   frio (nu = 0) de N_d celdas centrada en la celda 400; fuente de corriente
#   CW en la celda 100; monitor de E_z en la celda 700; esponja conductora de
#   60 celdas en cada extremo.  Unidades normalizadas: c = eps0 = mu0 = 1
#   (=> eta0 = 1, lam_p = 2 pi, dx = lam_p/40, dt = 0.99 dx/c).
# MOTOR: python3 -B con numpy y math (sin dependencias externas).
# UNIDAD: longitud en celdas y en lam_p; tiempo en pasos dt; T adimensional.
# VENTANA: el reloj UTC que este script imprime al arrancar y al cerrar.
# ===========================================================================
# Las cifras selladas del pre-registro (adenda 11) se re-miden aqui y se
# aseveran al cierre (RC = 2 si alguna no cuadra).  Ningun rotulo se imprime
# sin su numero al lado; ningun numero se imprime sin su sello.
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

# --- discretizacion (sellada) -----------------------------------------------
DX = LAMBDA_P / 40.0
DT = 0.99 * DX / C
NX = 800
NT = 4000
N_ABS = 60
SIGMA_MAX = 10.0
I_SRC = 100
I_SLAB = 400
I_MON = 700
N_VENTANA = 606

# --- bandas, escalera y umbrales (sellados) ---------------------------------
W1 = 0.2 * OMEGA_P
W2 = 2.0 * OMEGA_P
D_TILDE = (0.25, 0.50, 0.75, 1.00)
ND = tuple(int(round(40.0 * d)) for d in D_TILDE)
T_SELLADO_W1 = (3.015020e-02, 1.306491e-03, 5.999000e-05, 2.761929e-06)
T_SELLADO_W2 = (0.996534, 0.988544, 0.981434, 0.979845)
ALPHA_D_SELLADO = (1.5391, 3.0781, 4.6172, 6.1562)
M_EXACTO_SELLADO = -12.3900
M_TEOR = -12.3125
B_TEOR = -0.487109
PREF_SELLADO = 0.614400
KAPPA_SELLADO = 4.898979
DT_WP_SELLADO = 0.1555088
TOL_SLOPE = 0.02
TOL_T1 = 5.0e-6
TOL_T2 = 0.97
TOL_PISO_ABS = 1.0e-8
FACTOR_PISO = 10.0
TOL_VACIO = 1.0e-4


# --------------------------------------------------------------------------- #
#  A.  SELLOS: la aritmetica congelada se re-mide aqui y se asevera al cierre
# --------------------------------------------------------------------------- #
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


def pendiente(xs, ys):
    x = np.asarray(xs, dtype=float)
    y = np.asarray(ys, dtype=float)
    xm = x.mean()
    ym = y.mean()
    den = float(np.sum((x - xm) ** 2))
    num = float(np.sum((x - xm) * (y - ym)))
    return num / den


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


def n_rampa(w0):
    return int(math.floor(5.0 * (2.0 * math.pi / w0) / DT))


ALPHA = math.sqrt(OMEGA_P ** 2 - W1 ** 2)
KAPPA = math.sqrt((OMEGA_P ** 2) / (W1 ** 2) - 1.0)
PREFACTOR = 16.0 * KAPPA ** 2 / (1.0 + KAPPA ** 2) ** 2
ALPHA_D = tuple(ALPHA * LAMBDA_P * d for d in D_TILDE)
T_EXACTO_W1 = tuple(T_exacto_corte(W1, d * LAMBDA_P) for d in D_TILDE)
T_EXACTO_W2 = tuple(T_exacto_pasante(W2, d * LAMBDA_P) for d in D_TILDE)
M_EXACTO_CALC = pendiente(D_TILDE, np.log(T_EXACTO_W1))
M_EXACTO_7CIF = pendiente(D_TILDE, np.log(T_SELLADO_W1))

sellar("dx = lam_p/40", DX, LAMBDA_P / 40.0, 0.0)
sellar("dt = 0.99 dx/c", DT, 0.15550884, 1e-7)
sellar("dt * wp", DT * OMEGA_P, DT_WP_SELLADO, 1e-6)
sellar("eta0 = sqrt(mu0/eps0)", ETA0, 1.0, 1e-15)
sellar("lam_p = 2 pi", LAMBDA_P, 2.0 * math.pi, 1e-15)
sellar("kappa = sqrt((wp/w1)^2 - 1)", KAPPA, KAPPA_SELLADO, 1e-6)
sellar("kappa^2", KAPPA ** 2, 24.0, 1e-9)
sellar("prefactor 16 k^2/(1+k^2)^2", PREFACTOR, PREF_SELLADO, 1e-6)
sellar("b_teor = ln(prefactor)", math.log(PREFACTOR), B_TEOR, 1e-5)
sellar("m_teor = -2 alpha lam_p", -2.0 * ALPHA * LAMBDA_P, M_TEOR, 1e-5)
sellar("tau1 = (2 pi/w1)/dt  [pasos]", (2.0 * math.pi / W1) / DT, 202.02, 1e-4)
sellar("n_rampa(w1) = floor(5 tau1)", n_rampa(W1), 1010, 1e-9)
sellar("n_rampa(w2) = floor(5 tau2)", n_rampa(W2), 101, 1e-9)
sellar("media de N_d = 40 * d_tilde", sum(ND) / float(len(ND)), 25.0, 1e-15, "N_d = 10, 20, 30, 40")
for k, d in enumerate(D_TILDE):
    sellar("alpha*d  d_tilde=%.2f" % d, ALPHA_D[k], ALPHA_D_SELLADO[k], 1e-4)
    sellar("T_exacto corte   d_tilde=%.2f" % d, T_EXACTO_W1[k], T_SELLADO_W1[k], 1e-6)
    sellar("T_exacto pasante d_tilde=%.2f" % d, T_EXACTO_W2[k], T_SELLADO_W2[k], 1e-6)
sellar("m_exacto (regresion sobre los T de 7 cifras)", M_EXACTO_7CIF, M_EXACTO_SELLADO, 1e-5)


# --------------------------------------------------------------------------- #
#  B.  INSTRUMENTO
# --------------------------------------------------------------------------- #
def perfil_sigma(sigma_max):
    s = np.zeros(NX)
    for i in range(N_ABS):
        d = float(N_ABS - i)
        s[i] = sigma_max * (d / N_ABS) ** 4
    for i in range(NX - N_ABS, NX):
        d = float(i - (NX - N_ABS) + 1)
        s[i] = sigma_max * (d / N_ABS) ** 4
    return s


SIGMA = perfil_sigma(SIGMA_MAX)
DAMP = np.exp(-SIGMA * DT)
DAMP_SIN = np.exp(-perfil_sigma(0.0) * DT)


def fuente(t, w0):
    trampa = 5.0 * (2.0 * math.pi / w0)
    s = math.sin(math.pi * t / (2.0 * trampa)) ** 2 if t <= trampa else 1.0
    return s * math.sin(w0 * t)


def serie_fuente(w0):
    return np.array([fuente((n + 1) * DT, w0) for n in range(NT)], dtype=float)


def estimar(muestras, tiempos, w0):
    M = np.column_stack([np.cos(w0 * tiempos), np.sin(w0 * tiempos)])
    sol = np.linalg.lstsq(M, muestras, rcond=None)[0]
    A = float(sol[0])
    B = float(sol[1])
    V = math.hypot(A, B)
    r = muestras - M.dot(sol)
    return A, B, V, float(np.sqrt(float(np.mean(r * r))))


def correr(w0, n_d, modo, omega_p=OMEGA_P, damp=DAMP, esponja="encendida"):
    """modo: 'vacio' (sin lamina) | 'lar' (lamina de plasma nu = 0) | 'pec'
    (lamina con E_z = 0 forzado).  Un paso = H, J, E, fuente, absorcion, PEC."""
    ez = np.zeros(NX)
    hy = np.zeros(NX)
    jz = np.zeros(NX)
    if n_d > 0:
        i0 = I_SLAB - n_d // 2
        i1 = i0 + n_d
    else:
        i0 = I_SLAB
        i1 = I_SLAB
    acople = (omega_p ** 2) * DT
    jsrc = serie_fuente(w0)
    n0 = NT - N_VENTANA
    mues = np.empty(N_VENTANA)
    tvec = np.empty(N_VENTANA)
    for n in range(NT):
        hy[:-1] -= (DT / DX) * (ez[1:] - ez[:-1])
        if modo == "lar" and n_d > 0:
            jz[i0:i1] += acople * ez[i0:i1]
        ez[1:] -= (DT / DX) * (hy[1:] - hy[:-1]) + DT * jz[1:]
        ez[I_SRC] -= DT * jsrc[n]
        np.multiply(ez, damp, out=ez)
        if modo == "pec":
            ez[i0:i1] = 0.0
        if n >= n0:
            mues[n - n0] = ez[I_MON]
            tvec[n - n0] = (n + 1) * DT
    A, B, V, res = estimar(mues, tvec, w0)
    return dict(w0=w0, n_d=n_d, modo=modo, omega_p=omega_p, esponja=esponja,
                celda_lamina=[i0, i1], ventana=[n0, NT - 1],
                A=A, B=B, V=V, residuo=res,
                residuo_rel=(res / V if V > 0.0 else 0.0),
                pico_ventana=float(np.max(np.abs(mues))),
                suma_campo=float(np.sum(ez)),
                suma_abs_campo=float(np.sum(np.abs(ez))),
                muestra=mues)


def sec(t):
    print("")
    print("=" * 79)
    print(t)
    print("=" * 79)


sec("SOLVER ADE-FDTD 1D CW: ESCALERA EXACTA Y TESTIGO PEC")
print("UNIVERSO DECLARADO: malla 1D N_x = %d celdas (%.4f lam_p) · vacio + lamina" % (NX, NX * DX / LAMBDA_P))
print("  de plasma frio nu = 0 centrada en la celda %d · fuente CW en la celda %d ·" % (I_SLAB, I_SRC))
print("  monitor de E_z en la celda %d · esponja conductora de %d celdas por extremo." % (I_MON, N_ABS))
print("MOTOR: python3 -B · numpy %s · solo numpy y math." % np.__version__)
print("UNIDAD: longitud en celdas y en lam_p · tiempo en pasos dt · T adimensional.")
print("VENTANA: T_UTC_ARRANQUE = %s" % T_UTC_ARRANQUE)

sec("A. CIFRAS SELLADAS DEL PRE-REGISTRO (adenda 11): re-medidas con assert")
print("  %-46s %-17s %-17s %-10s %s" % ("cifra", "medido", "sellado", "rel", ""))
for nombre, valor, esperado, rel, ok, nota in FILAS_SELLO:
    print("  %-46s %-17.10g %-17.10g %-10.2e %s%s"
          % (nombre, valor, esperado, rel, "OK" if ok else "ROJO",
             ("  " + nota) if nota else ""))
print("  filas = %d · rojas = %d" % (len(FILAS_SELLO), len(FALLOS_SELLO)))
print("  m_exacto: regresion sobre los T de 7 cifras = %.6f · regresion sobre T de"
      " maquina = %.6f · m_teor = %.6f" % (M_EXACTO_7CIF, M_EXACTO_CALC, M_TEOR))

sec("B. INSTRUMENTO")
print("  dx = %.10e (lam_p/40) · dt = %.10e (0.99 dx/c) · dt*wp = %.10e · N_t = %d"
      % (DX, DT, DT * OMEGA_P, NT))
print("  esponja: sigma(x) = %.1f (d/%d)^4 · integrador exp(-sigma dt) · damper minimo = %.6e"
      % (SIGMA_MAX, N_ABS, DAMP[0]))
print("  fuente: s(t) = sin^2(pi t/(2 T_rampa)), s = 1 despues · J = s(t) sin(w0 t)")
print("    w1 = %.3f wp: T_rampa = %.6f = %d pasos · tau1 = %.4f pasos · n_rampa = %d"
      % (W1 / OMEGA_P, 5 * 2 * math.pi / W1, n_rampa(W1), (2 * math.pi / W1) / DT, n_rampa(W1)))
print("    w2 = %.3f wp: T_rampa = %.6f = %d pasos · tau2 = %.4f pasos · n_rampa = %d"
      % (W2 / OMEGA_P, 5 * 2 * math.pi / W2, n_rampa(W2), (2 * math.pi / W2) / DT, n_rampa(W2)))
print("  lamina: celdas [%d - N_d/2, %d - N_d/2 + N_d) · N_d = 40 * d_tilde => %s"
      % (I_SLAB, I_SLAB, ND))
print("    d_tilde va en unidades de lam_p: d = d_tilde * lam_p = N_d * dx")
print("  ventana LSQ: %d muestras, n en [%d, %d] = %.5f portadoras de w1"
      % (N_VENTANA, NT - N_VENTANA, NT - 1, N_VENTANA * DT / (2 * math.pi / W1)))

sec("C. CORRIDA 1 (REFERENCIA VACIA) Y CORRIDA 2 (PISO DINAMICO wp = 0)")
r1 = correr(W1, 0, "vacio")
r1b = correr(W2, 0, "vacio")
r2 = correr(W1, ND[-1], "lar", omega_p=0.0)
print("  C1 w1: V_ref = %.12e · A = %+.12e · B = %+.12e · residuo = %.3e (rel %.3e)"
      % (r1["V"], r1["A"], r1["B"], r1["residuo"], r1["residuo_rel"]))
print("  C1 w2: V_ref = %.12e · A = %+.12e · B = %+.12e · residuo = %.3e (rel %.3e)"
      % (r1b["V"], r1b["A"], r1b["B"], r1b["residuo"], r1b["residuo_rel"]))
print("  prediccion declarada (hoja de corriente 1D): J0 * dx * eta0 / 2 = %.9e" % (DX * ETA0 / 2.0))
print("    V_ref(w1)/prediccion = %.9f · V_ref(w2)/prediccion = %.9f  [declarado: sin criterio]"
      % (r1["V"] / (DX * ETA0 / 2.0), r1b["V"] / (DX * ETA0 / 2.0)))
T2 = (r2["V"] / r1["V"]) ** 2
print("  C2 (wp = 0, N_d = %d, w1): V = %.12e · T = %.17g" % (ND[-1], r2["V"], T2))
print("  identidad bit a bit C1 vs C2: ventana = %s · suma del campo = %s · suma de |campo| = %s"
      % (np.array_equal(r1["muestra"], r2["muestra"]),
         r1["suma_campo"] == r2["suma_campo"],
         r1["suma_abs_campo"] == r2["suma_abs_campo"]))
print("  DECLARACION: con wp = 0 la corriente J_z se cumple identicamente 0 => la corrida 2")
print("    reproduce la corrida 1 bit a bit.  El chequeo |T - 1| <= 1e-4 se satisface POR")
print("    CONSTRUCCION: es identidad de camino (topologia), no un piso medido.")

sec("D. CORRIDA 3 (TESTIGO PEC: E_z = 0 forzado en la lamina de N_d = %d)" % ND[-1])
r3 = correr(W1, ND[-1], "pec")
T3 = (r3["V"] / r1["V"]) ** 2
print("  V_piso = %.12e · A = %+.12e · B = %+.12e · pico de la ventana = %.3e · residuo = %.3e"
      % (r3["V"], r3["A"], r3["B"], r3["pico_ventana"], r3["residuo"]))
print("  T_piso = %.17g   [umbral: <= %.1e]" % (T3, TOL_PISO_ABS))
print("  DECLARACION: V_piso = 0 exacto.  Con E_z = 0 en la lamina el campo a la derecha queda")
print("    identicamente nulo: el testigo certifica AUSENCIA DE CAMINO PARALELO (topologia), no un")
print("    piso numerico.  El umbral relativo 10*T_piso queda vacio (0): la condicion real es T > 0.")

sec("E. CORRIDA 4 (ESCALERA DE CORTE w1 = %.3f wp)" % (W1 / OMEGA_P))
print("  %-8s %-6s %-9s %-18s %-18s %-11s %-11s"
      % ("d_tilde", "N_d", "alpha*d", "T_medido", "T_exacto", "T_med/T_ex", "resid_rel"))
T_ESC = []
for k, nd in enumerate(ND):
    r = correr(W1, nd, "lar")
    t = (r["V"] / r1["V"]) ** 2
    T_ESC.append(t)
    print("  %-8.2f %-6d %-9.4f %-18.10e %-18.10e %-11.6f %.3e"
          % (D_TILDE[k], nd, ALPHA_D[k], t, T_EXACTO_W1[k], t / T_EXACTO_W1[k], r["residuo_rel"]))
M_MED = pendiente(D_TILDE, np.log(T_ESC))
ERR_M = abs(M_MED - M_EXACTO_SELLADO) / abs(M_EXACTO_SELLADO)
print("")
print("  m_med = %.6f  (regresion de ln T vs d_tilde sobre %d puntos)" % (M_MED, len(ND)))
print("  m_exacto sellado = %.6f · m_exacto por regresion de maquina = %.6f · m_teor = %.6f"
      % (M_EXACTO_SELLADO, M_EXACTO_CALC, M_TEOR))
print("  |m_med - m_exacto| / |m_exacto| = %.6f   [umbral: <= %.4f]" % (ERR_M, TOL_SLOPE))
print("  T(w1, d_tilde = 1.00) = %.10e   [umbral: <= %.1e]" % (T_ESC[-1], TOL_T1))
print("  T_piso = %.3e · 10 * T_piso = %.3e" % (T3, FACTOR_PISO * T3))

sec("F. CORRIDA 5 (CONTROL PASANTE w2 = %.3f wp)" % (W2 / OMEGA_P))
print("  %-8s %-6s %-18s %-18s %-11s %-11s"
      % ("d_tilde", "N_d", "T_medido", "T_exacto", "T_med/T_ex", "resid_rel"))
T_PAS = []
for k, nd in enumerate(ND):
    r = correr(W2, nd, "lar")
    t = (r["V"] / r1b["V"]) ** 2
    T_PAS.append(t)
    print("  %-8.2f %-6d %-18.10e %-18.10e %-11.6f %.3e"
          % (D_TILDE[k], nd, t, T_EXACTO_W2[k], t / T_EXACTO_W2[k], r["residuo_rel"]))
print("  minimo medido = %.10e   [umbral: >= %.4f]" % (min(T_PAS), TOL_T2))

sec("G. EXTRA DECLARADO DEL INSTRUMENTO (no es criterio: existe para que el metro pueda diferir)")
r4 = correr(W1, 0, "vacio", damp=DAMP_SIN, esponja="apagada")
T4 = (r4["V"] / r1["V"]) ** 2
print("  G1 esponja apagada (sigma_max = 0, dominio cerrado): V = %.9e · T = %.9e · residuo_rel = %.3e"
      % (r4["V"], T4, r4["residuo_rel"]))
print("     => el mismo estimador SI puede dar T distinto de 1: T = 1 exacto solo ocurre cuando el")
print("        camino es identico.  Control positivo de respuesta del instrumento.")

sec("H. CRITERIOS")
CRIT = [
    ("C2  |T - 1| <= %.1e (wp = 0, N_d = %d, w1)" % (TOL_VACIO, ND[-1]),
     abs(T2 - 1.0) <= TOL_VACIO, "T = %.17g · DEGENERADO POR CONSTRUCCION" % T2),
    ("C3  T_piso <= %.1e (PEC, N_d = %d, w1)" % (TOL_PISO_ABS, ND[-1]),
     T3 <= TOL_PISO_ABS, "T_piso = %.17g" % T3),
    ("C4a |m_med - %.4f| / %.4f <= %.2f" % (M_EXACTO_SELLADO, abs(M_EXACTO_SELLADO), TOL_SLOPE),
     ERR_M <= TOL_SLOPE, "m_med = %.6f · err = %.6f" % (M_MED, ERR_M)),
    ("C4b T(w1, d_tilde = 1.00) <= %.1e" % TOL_T1,
     T_ESC[-1] <= TOL_T1, "T = %.10e" % T_ESC[-1]),
    ("C4c T(w1, d_tilde = 1.00) > %.1f * T_piso" % FACTOR_PISO,
     T_ESC[-1] > FACTOR_PISO * T3, "umbral = %.3e" % (FACTOR_PISO * T3)),
    ("C5  min T(w2) >= %.2f" % TOL_T2,
     min(T_PAS) >= TOL_T2, "min = %.10e" % min(T_PAS)),
]
for nombre, ok, det in CRIT:
    print("  %-46s %-6s %s" % (nombre, "CUMPLE" if ok else "FALLA", det))
print("  criterios = %d · cumplidos = %d · fallados = %d"
      % (len(CRIT), sum(1 for c in CRIT if c[1]), sum(1 for c in CRIT if not c[1])))

RES = dict(
    t_utc_arranque=T_UTC_ARRANQUE,
    t_utc_cierre=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    sellos=dict(filas=len(FILAS_SELLO), rojas=FALLOS_SELLO),
    instrumento=dict(NX=NX, NT=NT, dx=DX, dt=DT, dt_wp=DT * OMEGA_P, N_ABS=N_ABS,
                     sigma_max=SIGMA_MAX, I_SRC=I_SRC, I_SLAB=I_SLAB, I_MON=I_MON,
                     N_VENTANA=N_VENTANA, n_rampa_w1=n_rampa(W1), n_rampa_w2=n_rampa(W2)),
    escalera=dict(d_tilde=list(D_TILDE), N_d=list(ND), alpha_d=list(ALPHA_D),
                  T_exacto=list(T_EXACTO_W1), T_medido=list(T_ESC),
                  m_med=M_MED, m_exacto=M_EXACTO_SELLADO,
                  m_exacto_maquina=M_EXACTO_CALC, m_teor=M_TEOR, err_rel=ERR_M),
    pasante=dict(T_exacto=list(T_EXACTO_W2), T_medido=list(T_PAS), minimo=min(T_PAS)),
    piso=dict(T=T3, V=r3["V"]),
    vacio=dict(V_ref_w1=r1["V"], V_ref_w2=r1b["V"], T=T2,
               bit_identico=bool(np.array_equal(r1["muestra"], r2["muestra"]))),
    extra_esponja_apagada=dict(V=r4["V"], T=T4, residuo_rel=r4["residuo_rel"]),
    criterios=[dict(nombre=n, cumple=bool(ok), detalle=d) for n, ok, d in CRIT],
)

print("")
print("JSON_BEGIN")
print(json.dumps(RES, indent=1, sort_keys=True))
print("JSON_END")
print("")
print("T_UTC_CIERRE = %s" % time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()))
print("RC = %d  (0 = los sellos cuadran; 2 = alguna cifra sellada no cuadra)"
      % (2 if FALLOS_SELLO else 0))
sys.exit(2 if FALLOS_SELLO else 0)
