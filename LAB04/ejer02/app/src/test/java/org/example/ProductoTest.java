package org.example;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class ProductoTest {
  @Test
  public void testGettersFuncionales() {
    Producto producto = new Producto(1, "Laptop", 999.99, true);
    
    assertEquals(1, producto.getId());
    assertEquals("Laptop", producto.getNombre());
    assertEquals(999.99, producto.getPrecio());
    assertTrue(producto.getDisponibilidad());
  }
}
