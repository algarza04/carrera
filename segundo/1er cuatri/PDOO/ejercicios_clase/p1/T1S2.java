/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/Classes/Class.java to edit this template
 */
package ejercicios_clase;

import ejercicios_clase.monstruos.Monstruo;
import ejercicios_clase.Utils.Utils;
import ejercicios_clase.monstruos.EnumMonstruos;

/**
 *
 * @author alvarogz
 */
public class T1S2 {
    public static void main(String[] args) {
        
        Monstruo m = new Monstruo(Utils.generarNombreAleatorio(), Utils.generatTipoAleatorio(), Utils.generarVidaAleatoria(), Utils.generarAtaqueAleatorio());
        m.mostrar_info();
        
    }
}
