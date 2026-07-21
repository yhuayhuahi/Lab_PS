package org.example;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.Mockito.*;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.ValueSource;

public class CarritoCompraTest {
  private CarritoCompra carrito;

  @BeforeEach
  void setUp() {
    carrito = new CarritoCompra(new ServicioPrecioImpl());
  }

  @Test
  void p01_agregarProductoNoDisponible_lanzaExcepcion() {
    Producto producto = new Producto(1, "Pan", 10.0, false);

    IllegalArgumentException error = assertThrows(
        IllegalArgumentException.class,
        () -> carrito.agregarProducto(producto, 1)
    );

    assertEquals("Producto no disponible", error.getMessage());
  }

  @Test
  void p02_agregarCantidadNegativaOCero_lanzaExcepcion() {
    Producto producto = new Producto(1, "Pan", 10.0, true);

    IllegalArgumentException error = assertThrows(
        IllegalArgumentException.class,
        () -> carrito.agregarProducto(producto, 0)
    );

    assertEquals("Cantidad inválida", error.getMessage());
  }

  @Test
  void p03_agregarProductoNuevoValido_incrementaListaYCantidad() {
    Producto producto = new Producto(1, "Pan", 10.0, true);

    carrito.agregarProducto(producto, 5);

    assertEquals(1, carrito.getItems().size());
    assertEquals(5, carrito.getItems().get(0).getCantidad());
  }

  @Test
  void p04_agregarProductoExistente_actualizaCantidad() {
    Producto producto = new Producto(1, "Pan", 10.0, true);

    carrito.agregarProducto(producto, 5);
    carrito.agregarProducto(producto, 3);

    assertEquals(1, carrito.getItems().size());
    assertEquals(8, carrito.getItems().get(0).getCantidad());
  }

  @Test
  void p05_removerProductoExistente_eliminaDeLista() {
    Producto producto = new Producto(1, "Pan", 10.0, true);

    carrito.agregarProducto(producto, 5);
    carrito.removerProducto(1);

    assertTrue(carrito.getItems().isEmpty());
  }

  @Test
  void p06_removerProductoNoRegistrado_noCambiaLista() {
    Producto producto = new Producto(1, "Pan", 10.0, true);

    carrito.agregarProducto(producto, 5);
    carrito.removerProducto(2);

    assertEquals(1, carrito.getItems().size());
    assertEquals(1, carrito.getItems().get(0).getProducto().getId());
  }

  @Test
  void p07_vaciarCarrito_dejaListaVacia() {
    Producto producto = new Producto(1, "Pan", 10.0, true);

    carrito.agregarProducto(producto, 5);
    carrito.vaciarCarrito();

    assertTrue(carrito.getItems().isEmpty());
  }

  @Test
  void p08_casoLimiteInferior_unProductoSubtotalCoincide() {
    Producto producto = new Producto(1, "Producto 1", 12.5, true);

    carrito.agregarProducto(producto, 1);

    assertEquals(12.5, carrito.getItems().get(0).getSubtotal());
  }

  @Test
  void p09_casoLimiteSuperior_carritoMasivoProcesa100Productos() {
    for (int i = 1; i <= 100; i++) {
      Producto producto = new Producto(i, "Producto " + i, 1.0, true);
      carrito.agregarProducto(producto, 1);
    }

    assertEquals(100, carrito.getItems().size());
  }

  @Test
  void p10_registrarHistorial_alAgregarProducto() {
    Producto producto = new Producto(1, "Producto 1", 10.0, true);

    carrito.agregarProducto(producto, 1);

    assertFalse(carrito.getHistorial().isEmpty());
    assertEquals(
        "Agregado: Producto 1",
        carrito.getHistorial().get(0).getOperacion()
    );
  }

  @Test
  void p11_registrarHistorial_alRemoverProducto() {
    Producto producto = new Producto(1, "Producto 1", 10.0, true);

    carrito.agregarProducto(producto, 1);
    carrito.removerProducto(1);

    assertEquals(
        "Removido: Producto 1",
        carrito.getHistorial().get(1).getOperacion()
    );
  }

  @Test
  void p12_registrarHistorial_alVaciarCarrito() {
    Producto producto = new Producto(1, "Producto 1", 10.0, true);

    carrito.agregarProducto(producto, 1);
    carrito.vaciarCarrito();

    assertEquals(
        "Carrito vaciado",
        carrito.getHistorial().get(1).getOperacion()
    );
  }

  @Test
  void p13_calcularTotal_sinProductos_devuelveCero() {
    assertEquals(0.0, carrito.calcularTotal());
  }

  @Test
  void p14_calcularTotal_conEnteros_formulaBasica() {
    ServicioPrecio servicioPrecio = mock(ServicioPrecio.class);
    CarritoCompra carritoConMock = new CarritoCompra(servicioPrecio);
    Producto producto = new Producto(1, "Producto 1", 100.0, true);

    when(servicioPrecio.calcularDescuento(100.0)).thenReturn(10.0);
    when(servicioPrecio.calcularImpuesto(100.0)).thenReturn(18.0);

    carritoConMock.agregarProducto(producto, 1);

    assertEquals(108.0, carritoConMock.calcularTotal(), 0.0001);
  }

  @Test
  void p15_validarDecimales_calculoTotalCorrecto() {
    ServicioPrecio servicioPrecio = mock(ServicioPrecio.class);
    CarritoCompra carritoConMock = new CarritoCompra(servicioPrecio);
    Producto producto = new Producto(1, "Producto 1", 25.0, true);

    when(servicioPrecio.calcularDescuento(25.0)).thenReturn(2.5);
    when(servicioPrecio.calcularImpuesto(25.0)).thenReturn(4.5);

    carritoConMock.agregarProducto(producto, 1);

    assertEquals(27.0, carritoConMock.calcularTotal(), 0.0001);
  }

  @Test
  void p16_enviaSubtotalExacto_alServicioExterno() {
    ServicioPrecio servicioPrecio = mock(ServicioPrecio.class);
    CarritoCompra carritoConMock = new CarritoCompra(servicioPrecio);
    Producto producto = new Producto(1, "Producto 1", 50.0, true);

    when(servicioPrecio.calcularDescuento(150.0)).thenReturn(0.0);
    when(servicioPrecio.calcularImpuesto(150.0)).thenReturn(0.0);

    carritoConMock.agregarProducto(producto, 3);
    carritoConMock.calcularTotal();

    verify(servicioPrecio).calcularDescuento(150.0);
    verify(servicioPrecio).calcularImpuesto(150.0);
  }

  @Test
  void p17_descuentoMayorAlSubtotal_calculoTotalCorrecto() {
    ServicioPrecio servicioPrecio = mock(ServicioPrecio.class);
    CarritoCompra carritoConMock = new CarritoCompra(servicioPrecio);
    Producto producto = new Producto(1, "Producto 1", 50.0, true);

    when(servicioPrecio.calcularDescuento(50.0)).thenReturn(60.0);
    when(servicioPrecio.calcularImpuesto(50.0)).thenReturn(9.0);

    carritoConMock.agregarProducto(producto, 1);

    assertEquals(9.0, carritoConMock.calcularTotal(), 0.0001);
  }

  @ParameterizedTest
  @ValueSource(doubles = {10.0, 50.0, 500.0})
  void p18_parametrizada_multiplesMontos(double subtotal) {
    ServicioPrecio servicioPrecio = mock(ServicioPrecio.class);
    CarritoCompra carritoConMock = new CarritoCompra(servicioPrecio);

    when(servicioPrecio.calcularDescuento(subtotal))
        .thenAnswer(invocation -> subtotal * 0.10);
    when(servicioPrecio.calcularImpuesto(subtotal))
        .thenAnswer(invocation -> subtotal * 0.18);

    Producto producto = new Producto(1, "Producto 1", subtotal, true);
    carritoConMock.agregarProducto(producto, 1);

    double totalEsperado = subtotal - (subtotal * 0.10) + (subtotal * 0.18);
    assertEquals(totalEsperado, carritoConMock.calcularTotal(), 0.0001);
  }

  @Test
  void p19_resumenCompra_contienePalabrasClave() {
    Producto producto = new Producto(1, "Producto 1", 10.0, true);

    carrito.agregarProducto(producto, 1);

    String resumen = carrito.obtenerResumenCompra();

    assertTrue(resumen.contains("Subtotal:"));
    assertTrue(resumen.contains("Total:"));
  }
}
