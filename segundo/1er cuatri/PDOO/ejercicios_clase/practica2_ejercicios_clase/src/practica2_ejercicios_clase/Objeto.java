/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/Classes/Class.java to edit this template
 */
package practica2_ejercicios_clase;

/**
 *
 * @author alvarogz
 */
public class Objeto {
    private String nombre;
    private TipoObjeto tipo;
    private float ataque;
    private float defensa;

    public Objeto(String nombre, TipoObjeto tipo, float ataque, float defensa) {
        this.nombre = nombre;
        this.tipo = tipo;
        this.ataque = ataque;
        this.defensa = defensa;
    }
    
    @Override
    public String toString() {
        return "Objeto: " + nombre + ", tipo: " + tipo + ", ataque: " + ataque + ", defensa: " + defensa + "\n";
    }
}
