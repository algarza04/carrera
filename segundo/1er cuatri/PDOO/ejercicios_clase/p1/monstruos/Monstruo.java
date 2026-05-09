/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/Classes/Class.java to edit this template
 */
package ejercicios_clase.monstruos;

import ejercicios_clase.monstruos.EnumMonstruos;
import java.util.ArrayList;
import java.util.Random;

/**
 *
 * @author alvarogz
 */

public class Monstruo {
    private static final int MAX_MONSTRUOS = 10;
    private String nombre;
    private EnumMonstruos tipo;
    private int vida;
    private float ataque;
    private static Random generator = new Random();
    private int orc = 0;    //posicones en las que se encuentran en el array
    private int drag = 1;
    private int esq = 2;
    

    public static ArrayList<Monstruo> lista_monstruos = new ArrayList<>();
    
    public Monstruo(String nombre, EnumMonstruos tipo) {
        this.nombre = nombre;
        this.tipo = tipo;
    }
    
    public Monstruo() {
        
    }
    
    public Monstruo(String nombre, EnumMonstruos tipo, int vida, float ataque) {
        this.nombre = nombre;
        this.tipo = tipo;
        this.vida = vida;
        this.ataque = ataque;
    }
    
    public void mostrar_info() {
        System.out.println("Nombre monstruo: " + this.nombre + ", tipo: " + this.tipo+ ", vida: " + this.vida + ",ataque: "+this.ataque);
    }   
    
    public String getNombre() {
        return this.nombre;
    }

    public EnumMonstruos getTipo() {
        return tipo;
    }

    public int getVida() {
        return vida;
    }
    
    public void addRandomMonstruo() {
        if(lista_monstruos.size() < MAX_MONSTRUOS) {
            EnumMonstruos[] tipo_mons = {EnumMonstruos.Orco, EnumMonstruos.Dragon, EnumMonstruos.Esqueleto}; 
            int aux = generator.nextInt(tipo_mons.length);   //3 ya que solo hay 3 tipos de monstruo
            int a = lista_monstruos.size();
                        
            Monstruo m = new Monstruo("Monstruo" + a, tipo_mons[aux]);
            lista_monstruos.add(m);
        }
        else
            System.out.println("No se pueden añadir más de 10 monstruos");
    }
}
