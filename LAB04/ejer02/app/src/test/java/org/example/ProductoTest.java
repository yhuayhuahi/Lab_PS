package org.example;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

import org.junit.jupiter.api.DisplayName;

public class ProductoTest {
  @Test
  @DisplayName("Test de getters de Producto")
  public void testGettersFuncionales() {
    Producto p = new Producto(1, "Laptop", 999.99, true);
    
    assertAll(
        () -> assertEquals(1, p.getId()),
        () -> assertEquals("Laptop", p.getNombre()),
        () -> assertEquals(999.99, p.getPrecio(), 1e-9),   // delta por ser double
        () -> assertTrue(p.getDisponibilidad())
    );
  }
}
