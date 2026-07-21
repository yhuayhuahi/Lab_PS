
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


# =============================================================================
# Fase 3 – Regla de caracteres restantes (letras o dígitos)
# =============================================================================
class TestCaracteresRestantes(unittest.TestCase):
    """
    TDD – Iteración 3: posiciones 2..N solo aceptan letras (A-Z, a-z) o
    dígitos (0-9). Cualquier otro símbolo invalida el identificador.
    """

    # --- Caracteres restantes INVÁLIDOS -------------------------------------

    def test_guion_bajo_en_medio_es_invalido(self):
        self.assertFalse(es_identificador_valido("A_B"))

    def test_guion_en_medio_es_invalido(self):
        self.assertFalse(es_identificador_valido("A-B"))

    def test_punto_en_medio_es_invalido(self):
        self.assertFalse(es_identificador_valido("A.B"))

    def test_espacio_en_medio_es_invalido(self):
        self.assertFalse(es_identificador_valido("A B"))

    def test_signo_exclamacion_en_medio_es_invalido(self):
        self.assertFalse(es_identificador_valido("A!2"))

    def test_signo_mas_en_medio_es_invalido(self):
        self.assertFalse(es_identificador_valido("A+2"))

    def test_caracter_especial_al_final_es_invalido(self):
        self.assertFalse(es_identificador_valido("ABC#"))

    # --- Caracteres restantes VÁLIDOS ---------------------------------------

    def test_solo_letras_mayusculas_es_valido(self):
        self.assertTrue(es_identificador_valido("ABCDEF"))

    def test_solo_letras_minusculas_es_valido(self):
        self.assertTrue(es_identificador_valido("abcde"))

    def test_letras_y_digitos_es_valido(self):
        self.assertTrue(es_identificador_valido("A1B2C3"))

    def test_letra_seguida_de_digitos_es_valido(self):
        self.assertTrue(es_identificador_valido("X99"))

    def test_digito_al_final_es_valido(self):
        self.assertTrue(es_identificador_valido("LOOP1"))



# =============================================================================
# Fase 4 – Casos de integración (combinación de reglas)
# =============================================================================
class TestCasosIntegracion(unittest.TestCase):
    """
    TDD – Iteración 4: casos que ejercitan dos o más reglas simultáneamente.
    Incluye ejemplos representativos de nombres de variables Fortran reales.
    """

    # --- Casos VÁLIDOS de integración ---------------------------------------

    def test_nombre_tipico_fortran_I(self):
        self.assertTrue(es_identificador_valido("I"))

    def test_nombre_tipico_fortran_N(self):
        self.assertTrue(es_identificador_valido("N"))

    def test_nombre_tipico_fortran_X(self):
        self.assertTrue(es_identificador_valido("X"))

    def test_contador_tipico(self):
        self.assertTrue(es_identificador_valido("COUNT"))

    def test_nombre_mixto_6_caracteres(self):
        self.assertTrue(es_identificador_valido("Var123"))

    # --- Casos INVÁLIDOS de integración -------------------------------------

    def test_nombre_largo_con_especiales(self):
        self.assertFalse(es_identificador_valido("MY_VAR!"))

    def test_digito_primero_y_largo(self):
        self.assertFalse(es_identificador_valido("1ABCDEF"))

    def test_solo_digitos(self):
        self.assertFalse(es_identificador_valido("123"))

    def test_solo_especiales(self):
        self.assertFalse(es_identificador_valido("@#$"))

    def test_cadena_con_nueva_linea(self):
        self.assertFalse(es_identificador_valido("A\nB"))

    def test_cadena_con_tabulacion(self):
        self.assertFalse(es_identificador_valido("A\tB"))



if __name__ == "__main__":
    unittest.main(verbosity=2)