package org.example;

import java.util.ArrayList;
import java.util.List;

public class CarritoCompra {

    private List<ItemCarrito> items;
    private ServicioPrecio servicioPrecio;
    private List<HistorialOperacion> historial;

    public CarritoCompra(ServicioPrecio servicioPrecio) {
        this.items = new ArrayList<>();
        this.servicioPrecio = servicioPrecio;
        this.historial = new ArrayList<>();
    }

    public void agregarProducto(Producto producto, int cantidad) {

        if (!producto.isDisponible()) {
            throw new IllegalArgumentException("Producto no disponible");
        }

        if (cantidad <= 0) {
            throw new IllegalArgumentException("Cantidad inválida");
        }

        for (ItemCarrito item : items) {

            if (item.getProducto().getId() == producto.getId()) {
                item.setCantidad(item.getCantidad() + cantidad);

                historial.add(
                    new HistorialOperacion("Cantidad actualizada")
                );

                return;
            }
        }

        items.add(new ItemCarrito(producto, cantidad));

        historial.add(
            new HistorialOperacion(
                "Agregado: " + producto.getNombre()
            )
        );
    }

    public void removerProducto(int productoId) {
        String nombreProducto = null;

        for (ItemCarrito item : items) {
            if (item.getProducto().getId() == productoId) {
                nombreProducto = item.getProducto().getNombre();
                break;
            }
        }

        items.removeIf(
            item -> item.getProducto().getId() == productoId
        );

        if (nombreProducto == null) {
            nombreProducto = "Producto " + productoId;
        }

        historial.add(
            new HistorialOperacion(
                "Removido: " + nombreProducto
            )
        );
    }

    public void vaciarCarrito() {

        items.clear();

        historial.add(
            new HistorialOperacion("Carrito vaciado")
        );
    }

    public double calcularTotal() {

        if (items.isEmpty()) {
            return 0;
        }

        double subtotal = 0;

        for (ItemCarrito item : items) {
            subtotal += item.getSubtotal();
        }

        double descuento =
            servicioPrecio.calcularDescuento(subtotal);

        double impuesto =
            servicioPrecio.calcularImpuesto(subtotal);

        double descuentoAplicado = Math.min(descuento, subtotal);

        return subtotal - descuentoAplicado + impuesto;
    }

    public String obtenerResumenCompra() {

        StringBuilder resumen = new StringBuilder();
        double subtotal = 0;

        for (ItemCarrito item : items) {

            subtotal += item.getSubtotal();

            resumen.append(item.getProducto().getNombre())
                   .append(" x ")
                   .append(item.getCantidad())
                   .append("\n");
        }

        resumen.append("Subtotal: ")
               .append(subtotal)
               .append("\n")
               .append("Total: ")
               .append(calcularTotal());

        return resumen.toString();
    }

    public List<ItemCarrito> getItems() {
        return items;
    }

    public List<HistorialOperacion> getHistorial() {
        return historial;
    }
}