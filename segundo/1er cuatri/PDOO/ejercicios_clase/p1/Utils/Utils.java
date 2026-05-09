/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/Classes/Class.java to edit this template
 */
package ejercicios_clase.Utils;

import ejercicios_clase.monstruos.Monstruo;
import ejercicios_clase.monstruos.EnumMonstruos;

import java.util.Random;

/**
 *
 * @author alvarogz
 */
public class Utils {
    private static Random generator = new Random();
    private final static int VIDA_MAX = 10;
    private final static float ATAQUE_MAX = 10;
private int orc = 0;    //posicones en las que se encuentran en el array
    private int drag = 1;
    private int esq = 2;
        
    public static int generarVidaAleatoria() {
        return generator.nextInt(VIDA_MAX);
    }
    
    public static float generarAtaqueAleatorio() {
        return generator.nextFloat(ATAQUE_MAX);
    }
    
    public static String generarNombreAleatorio() {
        return "Monstruo"+Monstruo.lista_monstruos.size();
    }
    
    public static EnumMonstruos generatTipoAleatorio() {
        EnumMonstruos[] tipo_mons = {EnumMonstruos.Orco, EnumMonstruos.Dragon, EnumMonstruos.Esqueleto}; 
        int aux = generator.nextInt(tipo_mons.length);
        return tipo_mons[aux];
    }
    
    public Monstruo buscarMonstruo(String nombre) {
        int max = Monstruo.lista_monstruos.size();
        for(Monstruo m : Monstruo.lista_monstruos) {
            if (nombre.equals(m.getNombre())) {
               //System.out.println("Hemos encontrado a: " + nombre);
               return m;
            }
        }
        
        //throw new IllegalArgumentException("No existe ningun monstruo con dicho nombre");
        System.out.println("No esta en la lista");
        return null;
    }
    
    public static void addRandomMosntruo(){
        Monstruo m = new Monstruo();
        m.addRandomMonstruo();
    }
}
