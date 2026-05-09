/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/Classes/Class.java to edit this template
 */
package clase25nov;

/**
 *
 * @author alvarogz
 */
public abstract class Personaje extends SerVivo{
    public static String TIPO_MONSTRUO = "MONSTRUO";
    public static String TIPO_JUGADOR = "JUGADOR";
    protected String tipo;

    public Personaje(String nombre, int vida) {
        super(nombre, vida);
    }

    public String getTipo() {
        return tipo;
    }

    public abstract void atacar();
    
    public abstract void defender();
}
