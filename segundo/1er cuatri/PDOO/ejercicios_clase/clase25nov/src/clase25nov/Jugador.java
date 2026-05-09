/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/Classes/Class.java to edit this template
 */
package clase25nov;

/**
 *
 * @author alvarogz
 */
public class Jugador extends Personaje {

    public Jugador(String nombre, int vida) {
        super(nombre, vida);
        tipo = TIPO_JUGADOR;
    }
    
    @Override
    public void atacar() {
        System.out.println(getNombre() + " esta atacando con la espada");
    }

    @Override
    public void defender() {
        System.out.println(getNombre() + " se esta defendiendo con su escudo"); 
    }
    
}
