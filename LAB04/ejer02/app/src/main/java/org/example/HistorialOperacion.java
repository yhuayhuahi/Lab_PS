package org.example;

import java.time.LocalDateTime;

public class HistorialOperacion {

    private String operacion;
    private LocalDateTime fecha;

    public HistorialOperacion(String operacion) {
        this.operacion = operacion;
        this.fecha = LocalDateTime.now();
    }

    public String getOperacion() {
        return operacion;
    }

    public LocalDateTime getFecha() {
        return fecha;
    }
}