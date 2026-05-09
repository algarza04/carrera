/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/Classes/Class.java to edit this template
 */
package clase18.pkg11;

/**
 *
 * @author alvarogz
 */
public class Personaje {
    protected String nombre;
    protected static int salud;
    
    public Personaje(String nombre, int salud){
        this.nombre = nombre;
        this.salud = salud;
    }
    
    public void atacar(){
        System.out.print("\n" +nombre + " va a atacar");

    }
    
    public void recibir(int danio){
        salud -= danio;
    }
    
    private String men(){
        return "Hola";
    }
}
