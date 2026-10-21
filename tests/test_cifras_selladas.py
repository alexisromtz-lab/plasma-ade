#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Testigo de las cifras selladas de plasma-ade.

HUELLA-PLASMA-ADE-CIFRAS-SELLADAS-20261020

Quien mide: los dos solvers del repositorio, ejecutados enteros. Hasta este acto
ningun CI los corria — 1336 lineas de instrumento, 27 + 189 sellos y ni un job
que los mirara.

Que se pinea: VEREDICTOS, no digitos.

  · El denominador autoritativo es el JSON del solver (`sellos.filas`,
    `sellos.rojas`), no la linea `filas = N` impresa al humano: en el pulso el
    JSON dice 189 y la linea impresa 184 porque cuentan cosas distintas (acta de
    custodia §4, nota de denominador). Un testigo que lea la prosa hereda la
    confusion.
  · Los ultimos digitos de T viajan con el BLAS y no pueden firmar veredicto
    (medido: numpy 2.4.6 y 2.5.4 dan los mismos veredictos, el mismo numero de
    sellos y el mismo RC). El veredicto CUMPLE/FALLA, el denominador y el RC si.
  · El README conserva el acta de fallo de C4a como historia congelada; el
    estado VIGENTE de §12 lo declara la recalibracion, y este testigo exige que
    el README lo declare en la misma seccion (si no, README_DESALINEADO).
"""

import json
import re
import subprocess
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]

SOLVERS = {
    "cw": RAIZ / "sim" / "solver_plasma_cw.py",
    "pulso": RAIZ / "sim" / "solver_plasma_pulso.py",
}

# Umbrales que el README publica y que el solver aplica: dos portadores, un dato.
UMBRALES_PUBLICADOS = {"C4a": "0.02", "C4b": "5.0e-06", "C5": "0.97"}

_CRUDO = {}


def crudo(nombre):
    """Corre el solver entero y devuelve (rc, stdout, JSON del bloque declarado)."""
    if nombre in _CRUDO:
        return _CRUDO[nombre]
    ruta = SOLVERS[nombre]
    if not ruta.is_file():
        raise AssertionError(
            "INSTRUMENTO_AUSENTE: %s no existe" % ruta.relative_to(RAIZ)
        )
    r = subprocess.run(
        [sys.executable, "-B", str(ruta)],
        cwd=str(RAIZ),
        capture_output=True,
        text=True,
        timeout=900,
    )
    bloque = re.search(r"^JSON_BEGIN$(.*?)^JSON_END$", r.stdout, re.M | re.S)
    if not bloque:
        raise AssertionError(
            "SIN_CRUDO: %s no imprimio JSON_BEGIN/JSON_END (rc=%d) · stderr=%s"
            % (nombre, r.returncode, r.stderr.strip()[-500:])
        )
    fila = (r.returncode, r.stdout, json.loads(bloque.group(1)))
    _CRUDO[nombre] = fila
    return fila


def res(nombre):
    return crudo(nombre)[2]


def ids_criterios(nombre):
    return [c["nombre"].split()[0] for c in res(nombre)["criterios"]]


def fallados(nombre):
    return [c["nombre"].split()[0] for c in res(nombre)["criterios"] if not c["cumple"]]


def readme():
    ruta = RAIZ / "README.md"
    if not ruta.is_file():
        raise AssertionError("README_AUSENTE: no hay portador que cruzar")
    # El README escribe el signo menos tipografico (U+2212); el solver, ASCII.
    return ruta.read_text(encoding="utf-8").replace("\u2212", "-")


def seccion(titulo):
    texto = readme()
    i = texto.find(titulo)
    if i < 0:
        raise AssertionError("README_DESALINEADO: falta la seccion %r" % titulo)
    resto = texto[i + len(titulo) :]
    j = resto.find("### §")
    return resto if j < 0 else resto[:j]


# --------------------------------------------------------------------------- #
#  §12 · CW — 27 sellos, 6 criterios
# --------------------------------------------------------------------------- #
def test_cw_sellos_cierran():
    rc, _, dato = crudo("cw")
    filas = dato["sellos"]["filas"]
    rojas = dato["sellos"]["rojas"]
    assert filas > 0, "VACUIDAD: 0 sellos emitidos en cw (%r)" % (filas,)
    assert rojas == [], "SELLOS_ROJOS: cw %r" % (rojas,)
    assert rc == 0, (
        "RC_NO_CERO: cw rc=%d (0 = los sellos cuadran; 2 = alguna cifra sellada no cuadra)"
        % rc
    )
    assert filas == 27, (
        "DENOMINADOR_MOVIDO: cw filas=%r; el acto declara 27 (recalibracion §2)" % (filas,)
    )


def test_cw_veredicto_publicado():
    ids = ids_criterios("cw")
    assert ids == ["C2", "C3", "C4a", "C4b", "C4c", "C5"], (
        "CRITERIOS_DESALINEADOS: cw %r" % (ids,)
    )
    rojos = fallados("cw")
    assert rojos == [], (
        "VEREDICTO_DESALINEADO: cw fallados=%r; la recalibracion §12 "
        "(s12_informe_recalibracion.md, blob 55ed5d85) declara los 6 en CUMPLE" % (rojos,)
    )


def test_cw_negativo_del_borde_sigue_declarado():
    inst = res("cw")["instrumentacion_s12"]
    assert inst["mur"] is True, "MUR_APAGADO: el universo §12 declara Mur 1D activo"
    r_borde = abs(inst["r_borde"])
    tope = inst["tol_r_borde"]
    assert r_borde > tope, (
        "NEGATIVO_DECLARADO_CAMBIO: |r_borde|=%.6e <= %.1e; el informe §12 lo declara "
        "FALLA — un cambio exige acta nueva, no un test verde" % (r_borde, tope)
    )
    assert abs(inst["r_borde_control"]) > 1.0, (
        "CONTROL_NO_DISCRIMINA: el control con Mur OFF debe ser O(1), medido %.6e"
        % abs(inst["r_borde_control"])
    )


# --------------------------------------------------------------------------- #
#  §13 · pulsos — 189 sellos, 9 criterios (6 cumplen, 3 fallan y se declaran)
# --------------------------------------------------------------------------- #
def test_pulso_sellos_cierran():
    rc, _, dato = crudo("pulso")
    filas = dato["sellos"]["filas"]
    rojas = dato["sellos"]["rojas"]
    assert filas > 0, "VACUIDAD: 0 sellos emitidos en pulso (%r)" % (filas,)
    assert rojas == [], "SELLOS_ROJOS: pulso %r" % (rojas,)
    assert rc == 0, (
        "RC_NO_CERO: pulso rc=%d (0 = los sellos cuadran; 2 = alguna cifra sellada no cuadra)"
        % rc
    )
    assert filas == 189, (
        "DENOMINADOR_MOVIDO: pulso filas=%r; el acta §13 declara 190 -> 189 "
        "(la fila retirada esta declarada en §5.1)" % (filas,)
    )


def test_pulso_veredicto_publicado():
    ids = ids_criterios("pulso")
    assert ids == ["P1", "P2a", "P2b", "P2c", "P3", "P4", "P5", "P6", "P7"], (
        "CRITERIOS_DESALINEADOS: pulso %r" % (ids,)
    )
    rojos = fallados("pulso")
    assert rojos == ["P1", "P2a", "P4"], (
        "VEREDICTO_DESALINEADO: pulso fallados=%r; el acta §13 declara P1, P2a y P4 "
        "fallados — el fallo se publica, no se re-optimiza" % (rojos,)
    )


# --------------------------------------------------------------------------- #
#  El portador: el README no puede decir lo contrario que el instrumento
# --------------------------------------------------------------------------- #
def test_readme_porta_los_umbrales_del_solver():
    texto = readme()
    nombres = {c["nombre"].split()[0]: c["nombre"] for c in res("cw")["criterios"]}
    faltan = ["%s=%s" % (k, v) for k, v in UMBRALES_PUBLICADOS.items() if v not in texto]
    assert not faltan, (
        "README_DESALINEADO: umbrales que el solver aplica y el README no porta: %r" % (faltan,)
    )
    discrepan = [
        "%s: el solver dice %r" % (k, nombres[k])
        for k, v in UMBRALES_PUBLICADOS.items()
        if v not in nombres[k]
    ]
    assert not discrepan, "UMBRAL_NO_ES_EL_DEL_SOLVER: %r" % (discrepan,)


def test_readme_declara_el_estado_vigente_de_s12():
    s12 = seccion("### §12")
    assert re.search(r"recalibraci", s12, re.I), (
        "README_DESALINEADO: §12 no declara la recalibracion que dejo C4a en CUMPLE "
        "(el acta de fallo se conserva como historia, pero el estado vigente se declara)"
    )
    limpio = s12.replace("*", "").replace("`", "")
    cumplidos = sum(1 for c in res("cw")["criterios"] if c["cumple"])
    total = len(res("cw")["criterios"])
    assert re.search(r"cumplidos\s*[:=]\s*%d\b" % cumplidos, limpio), (
        "README_DESALINEADO: §12 no declara 'cumplidos: %d' (el solver mide %d/%d)"
        % (cumplidos, cumplidos, total)
    )
    assert re.search(r"fallados\s*[:=]\s*%d\b" % len(fallados("cw")), limpio), (
        "README_DESALINEADO: §12 no declara 'fallados: %d' (el solver mide %r)"
        % (len(fallados("cw")), fallados("cw"))
    )


def test_readme_declara_el_veredicto_de_s13():
    s13 = seccion("### §13")
    limpio = s13.replace("*", "").replace("`", "")
    rojos = fallados("pulso")
    cumplidos = len(res("pulso")["criterios"]) - len(rojos)
    assert re.search(r"cumplidos\s*[:=]?\s*%d\b" % cumplidos, limpio), (
        "README_DESALINEADO: §13 no declara 'cumplidos %d'" % cumplidos
    )
    assert re.search(r"fallados\s*[:=]?\s*%d\b" % len(rojos), limpio), (
        "README_DESALINEADO: §13 no declara 'fallados %d'" % len(rojos)
    )
    sin_portar = [p for p in rojos if p not in limpio]
    assert not sin_portar, (
        "README_DESALINEADO: §13 no nombra los criterios fallados %r" % (sin_portar,)
    )
