package org.example;

public class Producto {
  private int id;
  private String nombre;
  private double precio;
  private boolean disponibilidad;

  public Producto(int id, String nombre, double precio, boolean disponibilidad) {
    this.id = id;
    this.nombre = nombre;
    this.precio = precio;
    this.disponibilidad = disponibilidad;
  }

  public int getId() {
    return id;
  }

  public String getNombre() {
    return nombre;
  }

  public double getPrecio() {
    return precio;
  }

  public boolean getDisponibilidad() {
    return disponibilidad;
  }

  @Override
  public String toString() {
    return "Producto{" +
            "id=" + id +
            ", nombre='" + nombre + '\'' +
            ", precio=" + precio +
            ", disponibilidad=" + disponibilidad +
            '}';
  }
}
