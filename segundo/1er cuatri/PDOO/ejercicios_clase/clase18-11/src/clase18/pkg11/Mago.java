/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/Classes/Class.java to edit this template
 */
package clase18.pkg11;

/**
 *
 * @author alvarogz
 */
public class Mago extends Jugador{
    private String hechizo;
    
    public Mago(String nombre, int vida, int nivel, String hechizo){
        super(nombre, vida, nivel);
        this.hechizo = hechizo;
    }
    
    public void aprender(String nuevo_hechizo){
        hechizo = nuevo_hechizo;
    }
    public void atacar() {
        super.atacar();
        System.out.println(" con el hechizo " + this.hechizo);
    }
}
