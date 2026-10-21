#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Testigo del claims.json de plasma-ade: el contrato deja de ser prosa.

HUELLA-PLASMA-ADE-CLAIMS-WITNESS-20261020

Hasta este acto el claims.json declaraba `clase C · SIN_DATO_MECANIZABLE` con el
motivo "0 artefactos .json y 0 .txt rastreados". El motivo era cierto el dia que
se escribio (2026-10-20, antes de que existieran requirements.txt y el testigo de
las cifras), pero ya es falso: el crudo del que se derivan las cifras es el JSON
que los dos solvers imprimen entre `JSON_BEGIN` y `JSON_END`. Ese crudo existe,
se puede ejecutar y se mide en cada push.

Que exige este testigo por claim (los mismos tres eslabones que rf):

  1. PORTADOR — el `dato` existe como archivo Y esta declarado como solver en
     `tests/test_cifras_selladas.py`. Un dato sin portador es DATO_SIN_PORTADOR.
  2. DERIVA — `deriva` nombra `parser:<ruta>::<funcion>`; la funcion existe y su
     codigo LEE ese solver (nombra su clave y llama a un lector de crudo). Si no,
     PARSER_AUSENTE (no existe) o DERIVACION_CIEGA (existe y no lo lee).
  3. VALOR — `ruta` resuelve dentro del crudo y el valor que da el solver aparece
     en `afirma`. La afirmacion puede portar historia ("Filas: 190 -> 189"): la
     ley es que el valor VIGENTE este en la afirmacion, no que todo numero de la
     afirmacion sea vigente.
  4. PROSA — `afirma` aparece literal en `prosa`. Si no, README_DESALINEADO.

Divergencia declarada: `deriva` NO apunta a este archivo. Apuntar al testigo que
verifica el claim seria que el testigo se verifique a si mismo — el D13 en su
forma pura. Apunta al parser independiente `tests/test_cifras_selladas.py`, que
ya ejecuta los solvers y pinea los veredictos desde antes de que existiera el
claims mecanizable. Este modulo solo cruza el contrato; el valor lo mide aquel.
"""

import importlib.util
import inspect
import json
import re
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
CLAIMS = RAIZ / ".github" / "claims.json"
PARSER_REL = "tests/test_cifras_selladas.py"
PARSER = RAIZ / PARSER_REL

DERIVA = re.compile(r"^parser:(?P<ruta>[^:]+)::(?P<funcion>[A-Za-z_][A-Za-z0-9_]*)$")
SEGMENTO = re.compile(
    r"^(?P<clave>[A-Za-z_][A-Za-z0-9_]*)(?:\[(?P<campo>[A-Za-z_][A-Za-z0-9_]*)=(?P<valor>[^\]]+)\])?$"
)
LECTORES = ("crudo(", "res(", "ids_criterios(", "fallados(")
CAMPOS_CLAIM = ("id", "afirma", "dato", "ruta", "deriva", "polaridad", "prosa")
POLARIDADES = ("exacto",)


def parser_modulo():
    """El modulo que mide: el mismo objeto que pytest ya importo, sin recargarlo."""
    mod = sys.modules.get("test_cifras_selladas")
    if mod is not None:
        return mod
    if not PARSER.is_file():
        raise FileNotFoundError("PARSER_AUSENTE: no existe %s" % PARSER_REL)
    spec = importlib.util.spec_from_file_location("test_cifras_selladas", PARSER)
    mod = importlib.util.module_from_spec(spec)
    sys.modules["test_cifras_selladas"] = mod
    spec.loader.exec_module(mod)
    return mod


def _literal(txt):
    t = txt.strip()
    if t.lower() == "true":
        return True
    if t.lower() == "false":
        return False
    for cast in (int, float):
        try:
            return cast(t)
        except ValueError:
            pass
    return t.strip("'\"")


def resolver(obj, ruta, raiz=None, solvers=()):
    """Resuelve 'a.b[campo=false].c'; una lista al final vale su longitud.

    HUELLA-PLASMA-WITNESS-SELECTOR-DE-SOLVER-20261021: si la ruta EMPIEZA por el
    nombre de un solver, ese primer segmento es el SELECTOR — asi lo lee el
    verificador de portafolio (sim/verify_claims.py, dialecto `parser:`) — y se
    exige que sea el solver del `dato`. Nombrar otro solver no es una tolerancia:
    es RUTA_DE_OTRO_SOLVER, porque el valor saldria de un crudo que el claim no
    declara.
    """
    segmentos = ruta.split(".")
    if segmentos and solvers and segmentos[0] in solvers:
        if segmentos[0] != raiz:
            raise ValueError(
                "RUTA_DE_OTRO_SOLVER: %r selecciona %r y el dato es %r"
                % (ruta, segmentos[0], raiz)
            )
        segmentos = segmentos[1:]
    if not segmentos:
        raise ValueError("RUTA_INVALIDA: %r no resuelve nada bajo el selector" % ruta)
    actual = obj
    for segmento in segmentos:
        m = SEGMENTO.match(segmento)
        if not m:
            raise ValueError("RUTA_INVALIDA: %r no es un segmento valido" % ruta)
        clave = m.group("clave")
        if not isinstance(actual, dict) or clave not in actual:
            raise ValueError("RUTA_AUSENTE: %r no existe en el crudo" % ruta)
        actual = actual[clave]
        campo = m.group("campo")
        if campo:
            if not isinstance(actual, list):
                raise ValueError("RUTA_INVALIDA: %r filtra sobre algo que no es lista" % ruta)
            esperado = _literal(m.group("valor"))
            actual = [i for i in actual if isinstance(i, dict) and i.get(campo) == esperado]
    return len(actual) if isinstance(actual, list) else actual


def porta_valor(valor, afirma):
    """El valor vigente tiene que estar en la afirmacion, como token entero."""
    return re.search(r"(?<!\d)%s(?!\d)" % re.escape(str(valor)), afirma) is not None


def cargar_claims(ruta=CLAIMS):
    """Lee el claims.json; si falta o no parsea, falla cerrado."""
    if not ruta.is_file():
        raise FileNotFoundError("CLAIMS_INVALIDO: falta %s" % ruta.name)
    try:
        return json.loads(ruta.read_text(encoding="utf-8"))
    except ValueError as exc:
        raise ValueError("CLAIMS_INVALIDO: %s no parsea (%s)" % (ruta.name, exc))


def _solver_de(mod, dato):
    """Clave del solver cuyo archivo es `dato`, o None si no esta declarado."""
    for clave, ruta in mod.SOLVERS.items():
        p = Path(ruta)
        try:
            rel = p.resolve().relative_to(RAIZ.resolve())
        except ValueError:
            rel = p
        if rel.as_posix() == dato:
            return clave
    return None


def inconsistencias_claims(obj, mod=None):
    """Devuelve las mentiras medibles del claims.json (vacio = contrato cumplido)."""
    fallos = []
    if not isinstance(obj, dict):
        return ["CLAIMS_INVALIDO: la raiz no es un objeto"]
    if obj.get("clase") != "A":
        fallos.append("CLAIMS_INVALIDO: clase %r no es mecanizable" % (obj.get("clase"),))
    lista = obj.get("claims")
    if not isinstance(lista, list) or not lista:
        return fallos + ["CLAIMS_VACIO: un claims.json sin claims no declara nada"]
    if mod is None:
        mod = parser_modulo()

    for i, c in enumerate(lista):
        faltan = [k for k in CAMPOS_CLAIM if not isinstance(c, dict) or not c.get(k)]
        if faltan:
            fallos.append("CLAIMS_INVALIDO: claim %d sin %s" % (i, ",".join(faltan)))
            continue
        nombre = c["id"]

        if c["polaridad"] not in POLARIDADES:
            fallos.append(
                "POLARIDAD_INVENTADA: %s polaridad %r fuera de %r"
                % (nombre, c["polaridad"], list(POLARIDADES))
            )

        clave = _solver_de(mod, c["dato"])
        if not (RAIZ / c["dato"]).is_file() or clave is None:
            fallos.append(
                "DATO_SIN_PORTADOR: %s declara %s y no hay solver declarado que lo produzca"
                % (nombre, c["dato"])
            )

        m = DERIVA.match(c["deriva"])
        funcion = mod.__dict__.get(m.group("funcion")) if m else None
        if not m or m.group("ruta") != PARSER_REL or not callable(funcion):
            fallos.append(
                "PARSER_AUSENTE: %s deriva %r no nombra una funcion de %s"
                % (nombre, c["deriva"], PARSER_REL)
            )
        elif clave is not None:
            fuente = inspect.getsource(funcion)
            if '"%s"' % clave not in fuente or not any(lec in fuente for lec in LECTORES):
                fallos.append(
                    "DERIVACION_CIEGA: %s deriva en %s, que no lee el crudo de %s"
                    % (nombre, funcion.__name__, clave)
                )

        if clave is not None:
            try:
                valor = resolver(
                    mod.res(clave), c["ruta"], raiz=clave, solvers=tuple(mod.SOLVERS)
                )
            except ValueError as exc:
                causa = str(exc)
                codigo = causa.split(":", 1)[0]
                fallos.append("%s: %s · %s" % (codigo, nombre, causa))
            else:
                if not porta_valor(valor, c["afirma"]):
                    fallos.append(
                        "VALOR_NO_ES_EL_CRUDO: %s afirma %r y el crudo de %s da %s en %s"
                        % (nombre, c["afirma"], clave, valor, c["ruta"])
                    )

        prosa = RAIZ / c["prosa"]
        if not prosa.is_file():
            fallos.append("PROSA_AUSENTE: %s cita %s" % (nombre, c["prosa"]))
        elif c["afirma"] not in prosa.read_text(encoding="utf-8").replace("\u2212", "-"):
            fallos.append(
                "README_DESALINEADO: %s afirma %r y %s no lo dice"
                % (nombre, c["afirma"], c["prosa"])
            )
    return fallos


def test_el_claims_declara_solo_lo_que_el_solver_mide():
    """Portador real, derivacion que lo lee, valor vigente y prosa que lo cita."""
    fallos = inconsistencias_claims(cargar_claims())
    assert not fallos, "; ".join(fallos)


def test_el_testigo_de_claims_sabe_fallar():
    """Falsificador del testigo: cada mentira del claims.json tiene que ser cazada."""
    sano = cargar_claims()
    assert not inconsistencias_claims(sano), "EL_CLAIMS_SANO_YA_FALLA"

    def mutar(indice, campo, valor):
        copia = json.loads(json.dumps(sano))
        copia["claims"][indice][campo] = valor
        return copia

    mutaciones = {
        "DATO_SIN_PORTADOR": mutar(0, "dato", "sim/solver_que_no_existe.py"),
        "PARSER_AUSENTE": mutar(
            0, "deriva", "parser:tests/test_cifras_selladas.py::test_que_no_existe"
        ),
        "DERIVACION_CIEGA": mutar(0, "dato", "sim/solver_plasma_pulso.py"),
        "RUTA_AUSENTE": mutar(0, "ruta", "sellos.no_existe"),
        "RUTA_DE_OTRO_SOLVER": mutar(0, "ruta", "pulso.sellos.filas"),
        "VALOR_NO_ES_EL_CRUDO": mutar(0, "ruta", "sellos.rojas"),
        "POLARIDAD_INVENTADA": mutar(0, "polaridad", "creciente"),
        "README_DESALINEADO": mutar(0, "afirma", "27 sellos rotos"),
        "CLAIMS_VACIO": {"clase": "A", "claims": []},
        "CLAIMS_INVALIDO": {"clase": "C"},
    }
    for esperado, roto in mutaciones.items():
        cazado = inconsistencias_claims(roto)
        assert any(f.startswith(esperado + ":") for f in cazado), (
            "MUTACION_NO_CAZADA: %s — el testigo no discrimina (%r)" % (esperado, cazado)
        )

    roto = Path("/tmp/plasma_claims_roto.json")
    roto.write_text("{ esto no es json", encoding="utf-8")
    try:
        try:
            cargar_claims(roto)
        except ValueError as exc:
            assert "CLAIMS_INVALIDO" in str(exc), "CLAIMS_INVALIDO_SIN_CAUSA"
        else:
            raise AssertionError("CLAIMS_ROTO_PARSEA")
    finally:
        roto.unlink(missing_ok=True)
