/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/Classes/Class.java to edit this template
 */
package practica2_ejercicios_clase;

/**
 *
 * @author alvarogz
 */
public class Jugador {
    private String nombre;
    private int nivel;
    private int vida;
    private Inventario inventario;

    public Jugador(String nombre, int nivel, int vida, Inventario inventario) {
        this.nombre = nombre;
        this.nivel = nivel;
        this.vida = vida;
        this.inventario = inventario;
    }

    public String getNombre() {
        return nombre;
    }

    public int getNivel() {
        return nivel;
    }

    public int getVida() {
        return vida;
    }

    public void setNombre(String nombre) {
        this.nombre = nombre;
    }

    public void setNivel(int nivel) {
        this.nivel = nivel;
    }

    public void setVida(int vida) {
        this.vida = vida;
    }
    
    @Override
    public String toString(){
        return "Nombre: " + nombre + ", nivel: " + nivel + ", vida: " + vida + "\ninventario: " + inventario;
    }
    
}
