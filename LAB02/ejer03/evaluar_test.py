from evaluar import evaluar_rendimiento
import random

def test_evaluar_rendimiento_insuficiente():
    assert evaluar_rendimiento(random.randint(0,10)) == "Insuficiente"

def test_evaluar_rendimiento_regular():
    assert evaluar_rendimiento(random.randint(11, 15)) == "Regular"


