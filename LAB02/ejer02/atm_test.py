"""
test_atm.py
===========
Traducción de los escenarios Gherkin (atm.feature) a código Python
usando la librería pytest-bdd.


Arquitectura BDD aplicada
--------------------------
 atm.feature   →  especificación en lenguaje natural (Gherkin)
 test_atm.py   →  implementación de los pasos (Step Definitions)
 atm.py        →  sistema bajo prueba (SUT — System Under Test)


Ciclo BDD (análogo al ciclo TDD):
 1. Escribir el escenario Gherkin  (¿qué debe hacer el sistema?)
 2. Implementar los step defs      (¿cómo se verifica en código?)
 3. Ejecutar: los tests fallan     (RED)
 4. Implementar la lógica real     (GREEN)
 5. Refactorizar                   (REFACTOR)


Cómo ejecutar
-------------
   python -m pytest test_atm.py -v
   python -m pytest test_atm.py -v --tb=short   # traceback compacto
"""


import pytest
from pytest_bdd import given, when, then, scenario, scenarios, parsers
from atm import ATM




# =============================================================================
# Vinculación de los escenarios del archivo .feature
# =============================================================================
# 'scenarios' importa TODOS los escenarios del archivo .feature de una vez.
# Alternativamente se puede usar @scenario para vincular uno a uno.


scenarios("atm.feature")




# =============================================================================
# FIXTURES — Estado compartido entre pasos de un mismo escenario
# =============================================================================


@pytest.fixture
def contexto():
   """
   Almacén de estado compartido entre los pasos Given / When / Then
   de un mismo escenario. Equivale al 'context' de Behave.
   """
   return {}




# =============================================================================
# STEP DEFINITIONS — Dado / When / Then
# =============================================================================
# Cada función decorada con @given/@when/@then corresponde exactamente
# a una línea del archivo .feature. pytest-bdd hace el match por texto.
# =============================================================================




# ─── GIVEN (Dado que…) ────────────────────────────────────────────────────────


@given(parsers.parse("que el saldo de la cuenta es {saldo:f}"))
def dado_saldo_inicial(contexto, saldo):
   """
   GIVEN: inicializa el cajero con el saldo especificado en el escenario.
   Corresponde a: 'Given que el saldo de la cuenta es <valor>'
   """
   contexto["atm"] = ATM(saldo_inicial=saldo)
   contexto["saldo_inicial"] = saldo




# ─── WHEN (Cuando…) ───────────────────────────────────────────────────────────


@when(parsers.parse("el usuario intenta retirar {monto:f}"))
def cuando_retira(contexto, monto):
   """
   WHEN: ejecuta la operación de retiro sobre el ATM.
   Corresponde a: 'When el usuario intenta retirar <monto>'
   """
   exito, mensaje = contexto["atm"].retirar(monto)
   contexto["exito"]   = exito
   contexto["mensaje"] = mensaje




@when(parsers.parse("el usuario deposita {monto:f}"))
def cuando_deposita(contexto, monto):
   """
   WHEN: ejecuta la operación de depósito sobre el ATM.
   Corresponde a: 'When el usuario deposita <monto>'
   """
   exito, mensaje = contexto["atm"].depositar(monto)
   contexto["exito"]   = exito
   contexto["mensaje"] = mensaje




# ─── THEN (Entonces…) ─────────────────────────────────────────────────────────


@then("el sistema debe rechazar la transaccion")
def entonces_rechaza(contexto):
   """
   THEN: verifica que la transacción fue rechazada (exito == False).
   Corresponde a: 'Then el sistema debe rechazar la transaccion'
   """
   assert contexto["exito"] is False, (
       f"Se esperaba que la transacción fuera RECHAZADA, "
       f"pero fue APROBADA con mensaje: '{contexto['mensaje']}'"
   )




@then("el sistema debe aprobar la transaccion")
def entonces_aprueba(contexto):
   """
   THEN: verifica que la transacción fue aprobada (exito == True).
   Corresponde a: 'Then el sistema debe aprobar la transaccion'
   """
   assert contexto["exito"] is True, (
       f"Se esperaba que la transacción fuera APROBADA, "
       f"pero fue RECHAZADA con mensaje: '{contexto['mensaje']}'"
   )




@then(parsers.parse('el mensaje de error debe contener "{texto_esperado}"'))
def entonces_mensaje_error_contiene(contexto, texto_esperado):
   """
   THEN: verifica que el mensaje de error contiene el texto esperado.
   Corresponde a: 'And el mensaje de error debe contener "<texto>"'
   """
   assert texto_esperado in contexto["mensaje"], (
       f"Se esperaba que el mensaje contuviera '{texto_esperado}', "
       f"pero el mensaje fue: '{contexto['mensaje']}'"
   )




@then(parsers.parse('el mensaje debe contener "{texto_esperado}"'))
def entonces_mensaje_contiene(contexto, texto_esperado):
   """
   THEN: verifica que el mensaje de éxito contiene el texto esperado.
   Corresponde a: 'And el mensaje debe contener "<texto>"'
   """
   assert texto_esperado in contexto["mensaje"], (
       f"Se esperaba que el mensaje contuviera '{texto_esperado}', "
       f"pero el mensaje fue: '{contexto['mensaje']}'"
   )




@then(parsers.parse("el saldo debe permanecer en {saldo_esperado:f}"))
def entonces_saldo_es(contexto, saldo_esperado):
   """
   THEN: verifica que el saldo del ATM coincide con el valor esperado.
   Corresponde a: 'And el saldo debe permanecer en <valor>'
   """
   saldo_real = contexto["atm"].consultar_saldo()
   assert abs(saldo_real - saldo_esperado) < 0.001, (
       f"Saldo esperado: S/.{saldo_esperado:.2f}, "
       f"saldo real: S/.{saldo_real:.2f}"
   )




# ─── THEN para el Scenario Outline ───────────────────────────────────────────


@then(parsers.parse("el resultado debe ser {resultado}"))
def entonces_resultado(contexto, resultado):
   """
   THEN genérico para el Scenario Outline con tabla de ejemplos.
   Corresponde a: 'Then el resultado debe ser <aprobado|rechazado>'
   """
   if resultado == "aprobado":
       assert contexto["exito"] is True, (
           f"[Outline] Se esperaba APROBADO pero fue RECHAZADO. "
           f"Mensaje: '{contexto['mensaje']}'"
       )
   elif resultado == "rechazado":
       assert contexto["exito"] is False, (
           f"[Outline] Se esperaba RECHAZADO pero fue APROBADO. "
           f"Mensaje: '{contexto['mensaje']}'"
       )
   else:
       pytest.fail(f"Resultado desconocido en la tabla de ejemplos: '{resultado}'")




# =============================================================================
# TABLA DE TRAZABILIDAD — Escenarios vs. Reglas de Negocio
# =============================================================================
#
#  Escenario                          | Regla Myers        | Tipo de prueba
# ------------------------------------+--------------------+----------------
#  Retiro con fondos insuficientes    | Error obligatorio  | Error / Límite
#  Retiro exitoso                     | Flujo normal       | Caso válido
#  Retiro del saldo exacto            | Valor límite       | Límite
#  Retiro de monto cero               | Robustez           | Robusto
#  Retiro de monto negativo           | Robustez           | Robusto
#  Depósito exitoso                   | Flujo normal       | Caso válido
#  Depósito de monto negativo         | Robustez           | Robusto
#  Outline múltiples combinaciones    | Todos los casos    | Paramétrico
#
# =============================================================================
