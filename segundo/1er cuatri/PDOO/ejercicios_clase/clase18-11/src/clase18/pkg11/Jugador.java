/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/Classes/Class.java to edit this template
 */
package clase18.pkg11;

/**
 *
 * @author alvarogz
 */
public class Jugador extends Personaje {
    private int nivel;
    
    public Jugador(String nombre, int salud, int nivel){
        super(nombre, salud);
        this.nivel = nivel;
    }
    
    public void subirNivel(){
        this.nivel++;
    }
    
    public void atacar(){
        super.atacar();
        System.out.print( " con el nivel " + nivel);
    }
}
