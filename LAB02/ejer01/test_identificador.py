
import unittest
from identificador import es_identificador_valido

# =============================================================================
# Fase 1 – Regla de longitud (1 a 6 caracteres)
# =============================================================================
class TestLongitud(unittest.TestCase):
    """
    TDD – Iteración 1: implementar la validación de longitud.
    Valores límite según Myers: 0, 1, 6, 7.
    """

    # --- Valores límite INVÁLIDOS -------------------------------------------

    def test_cadena_vacia_longitud_0_es_invalida(self):
        self.assertFalse(es_identificador_valido(""))

    def test_longitud_7_es_invalida(self):
        self.assertFalse(es_identificador_valido("ABCDEFG"))

    def test_longitud_8_es_invalida(self):
        self.assertFalse(es_identificador_valido("ABCDEFGH"))

    # --- Valores límite VÁLIDOS ---------------------------------------------

    def test_longitud_1_es_valida(self):
        self.assertTrue(es_identificador_valido("A"))

    def test_longitud_6_es_valida(self):
        self.assertTrue(es_identificador_valido("ABCDE6"))

    # --- Valores interiores al rango ----------------------------------------

    def test_longitud_2_es_valida(self):
        self.assertTrue(es_identificador_valido("AB"))

    def test_longitud_3_es_valida(self):
        self.assertTrue(es_identificador_valido("ABC"))

    def test_longitud_5_es_valida(self):
        self.assertTrue(es_identificador_valido("ABCDE"))


# =============================================================================
# Fase 2 – Regla del primer carácter (debe ser letra)
# =============================================================================
class TestPrimerCaracter(unittest.TestCase):
    """
    TDD – Iteración 2: el primer carácter debe ser una letra (A-Z / a-z).
    Se usan las clases de equivalencia: letra, dígito, carácter especial.
    """

    # --- Primer carácter INVÁLIDO -------------------------------------------

    def test_primer_caracter_digito_es_invalido(self):
        self.assertFalse(es_identificador_valido("1ABC"))

    def test_primer_caracter_digito_cero_es_invalido(self):
        self.assertFalse(es_identificador_valido("0VAR"))

    def test_primer_caracter_underscore_es_invalido(self):
        self.assertFalse(es_identificador_valido("_VAR"))

    def test_primer_caracter_signo_dolar_es_invalido(self):
        self.assertFalse(es_identificador_valido("$VAR"))

    def test_primer_caracter_espacio_es_invalido(self):
        self.assertFalse(es_identificador_valido(" VAR"))

    def test_primer_caracter_at_es_invalido(self):
        self.assertFalse(es_identificador_valido("@VAR"))

    # --- Primer carácter VÁLIDO (letras) ------------------------------------

    def test_primer_caracter_mayuscula_es_valido(self):
        self.assertTrue(es_identificador_valido("ALPHA"))

    def test_primer_caracter_minuscula_es_valido(self):
        self.assertTrue(es_identificador_valido("x123"))

    def test_solo_una_letra_mayuscula(self):
        self.assertTrue(es_identificador_valido("Z"))

    def test_solo_una_letra_minuscula(self):
        self.assertTrue(es_identificador_valido("z"))

