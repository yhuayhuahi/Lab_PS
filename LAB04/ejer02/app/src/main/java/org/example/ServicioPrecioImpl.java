package org.example;

public class ServicioPrecioImpl implements ServicioPrecio {

    @Override
    public double calcularDescuento(double subtotal) {
        return subtotal * 0.10;
    }

    @Override
    public double calcularImpuesto(double subtotal) {
        return subtotal * 0.18;
    }
}