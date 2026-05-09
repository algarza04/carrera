/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/Classes/Class.java to edit this template
 */
package ejercicios_clase;

import ejercicios_clase.monstruos.Monstruo;
import ejercicios_clase.monstruos.EnumMonstruos;

/**
 *
 * @author alvarogz
 */
public class T1S1 {
    public static void main(String[] args) {
        Monstruo mons1 = new Monstruo("Pepe", EnumMonstruos.Orco);
        Monstruo mons2 = new Monstruo("Pepa", EnumMonstruos.Esqueleto);
        
        mons1.mostrar_info();
        mons2.mostrar_info();
    }
}
