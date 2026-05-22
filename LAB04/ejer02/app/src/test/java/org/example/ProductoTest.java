package org.example;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

import org.junit.jupiter.api.BeforeEach;

public class ProductoTest {

  private Producto producto;

  @BeforeEach
  void setUp() {
    producto = new Producto(1, "Producto A", 10.99, true);
  }

  @Test
  void testGetId() {
    assertEquals(1, producto.getId());
  }

  @Test
  void testGetNombre() {
    assertEquals("Producto A", producto.getNombre());
  }

  @Test
  void testGetPrecio() {
    assertEquals(10.99, producto.getPrecio());
  }

  @Test
  void testIsDisponible() {
    assertTrue(producto.isDisponible());
  }
}
