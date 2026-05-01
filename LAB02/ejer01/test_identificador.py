
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

