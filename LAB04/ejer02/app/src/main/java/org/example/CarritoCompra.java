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
            new HistorialOperacion("Producto agregado")
        );
    }

    public void removerProducto(int productoId) {

        items.removeIf(
            item -> item.getProducto().getId() == productoId
        );

        historial.add(
            new HistorialOperacion("Producto removido")
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

        return subtotal - descuento + impuesto;
    }

    public String obtenerResumenCompra() {

        StringBuilder resumen = new StringBuilder();

        for (ItemCarrito item : items) {

            resumen.append(item.getProducto().getNombre())
                   .append(" x ")
                   .append(item.getCantidad())
                   .append("\n");
        }

        resumen.append("TOTAL: ")
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