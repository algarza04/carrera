/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/Classes/Class.java to edit this template
 */
package clase25nov;

/**
 *
 * @author alvarogz
 */
public class Monstruo extends Personaje {

    public Monstruo(String nombre, int vida) {
        super(nombre, vida);
        tipo = TIPO_MONSTRUO;
    }

    @Override
    public void atacar() {
        System.out.println(getNombre() + " esta atacando con las garras");
    }

    @Override
    public void defender() {
        System.out.println(getNombre() + " se esta defendiendo con su pie");
    }
    
    
}
