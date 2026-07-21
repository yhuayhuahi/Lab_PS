Feature: Operaciones del Cajero Automático (ATM)
  Como usuario del cajero automático
  Quiero realizar operaciones de retiro y depósito de forma segura
  Para que el sistema proteja mi dinero y me informe claramente de cualquier error

  Scenario: Retiro con fondos insuficientes
    Given que el saldo de la cuenta es 100.00
    When el usuario intenta retirar 150.00
    Then el sistema debe rechazar la transaccion
    And el mensaje de error debe contener "Fondos insuficientes"
    And el saldo debe permanecer en 100.00

  Scenario: Retiro exitoso con saldo suficiente
    Given que el saldo de la cuenta es 500.00
    When el usuario intenta retirar 200.00
    Then el sistema debe aprobar la transaccion
    And el mensaje debe contener "Retiro exitoso"
    And el saldo debe permanecer en 300.00

  Scenario: Retiro del saldo exacto disponible
    Given que el saldo de la cuenta es 200.00
    When el usuario intenta retirar 200.00
    Then el sistema debe aprobar la transaccion
    And el mensaje debe contener "Retiro exitoso"
    And el saldo debe permanecer en 0.00

  Scenario: Retiro de monto cero es invalido
    Given que el saldo de la cuenta es 300.00
    When el usuario intenta retirar 0.00
    Then el sistema debe rechazar la transaccion
    And el mensaje de error debe contener "Monto inválido"
    And el saldo debe permanecer en 300.00

  Scenario: Retiro de monto negativo es invalido
    Given que el saldo de la cuenta es 300.00
    When el usuario intenta retirar -50.00
    Then el sistema debe rechazar la transaccion
    And el mensaje de error debe contener "Monto inválido"
    And el saldo debe permanecer en 300.00

  Scenario: Deposito exitoso incrementa el saldo correctamente
    Given que el saldo de la cuenta es 100.00
    When el usuario deposita 400.00
    Then el sistema debe aprobar la transaccion
    And el mensaje debe contener "Depósito exitoso"
    And el saldo debe permanecer en 500.00

  Scenario: Deposito de monto negativo es invalido
    Given que el saldo de la cuenta es 100.00
    When el usuario deposita -200.00
    Then el sistema debe rechazar la transaccion
    And el mensaje de error debe contener "Monto inválido"
    And el saldo debe permanecer en 100.00

  Scenario Outline: Validacion de multiples retiros con distintos saldos
    Given que el saldo de la cuenta es <saldo>
    When el usuario intenta retirar <monto>
    Then el resultado debe ser <resultado>

    Examples:
      | saldo  | monto  | resultado  |
      | 500.00 | 100.00 | aprobado   |
      | 100.00 | 150.00 | rechazado  |
      | 200.00 | 200.00 | aprobado   |
      | 50.00  | 51.00  | rechazado  |
      | 0.00   | 1.00   | rechazado  |
