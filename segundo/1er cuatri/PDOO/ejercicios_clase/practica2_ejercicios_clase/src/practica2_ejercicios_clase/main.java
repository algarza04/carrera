/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/Classes/Class.java to edit this template
 */
package practica2_ejercicios_clase;

/**
 *
 * @author alvarogz
 */
public class main {
    public static void main(String[] args) {
        Inventario inv1 = new Inventario(1, 3);
        Inventario inv2 = new Inventario(2, 2);
        Jugador jugador1 = new Jugador("Manolo", 2, 5, inv1);
        Jugador jugador2 = new Jugador("Jose", 3, 8, inv2);
        Objeto espada = new Objeto("espada", TipoObjeto.ESPADA, 50, 0);
        Objeto casco = new Objeto("casco", TipoObjeto.CASCO, 0, 20);
        Objeto escudo = new Objeto("escudo", TipoObjeto.ESCUDO, 10, 40);
        
        inv1.addObjeto(escudo);
        inv1.addObjeto(espada);
        inv2.addObjeto(casco);
        inv2.addObjeto(espada);
        
        System.out.println(jugador1.toString());
        System.out.println(jugador2.toString());
    }
}
