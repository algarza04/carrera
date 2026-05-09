/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/Classes/Class.java to edit this template
 */
package practica2_ejercicios_clase;
import java.util.ArrayList;
/**
 *
 * @author alvarogz
 */
public class Inventario {
    private int id;
    private int capacidad;
    private ArrayList<Objeto> objetos;

    public Inventario(int id, int capacidad) {
        this.id = id;
        this.capacidad = capacidad;
        objetos = new ArrayList<>();
    }
    
    @Override
    public String toString() {
        return "Inventario ID: " + id + ", capacidad: " + capacidad + "\nobjetos: "+ objetos;
    }
    
    public void addObjeto(Objeto objeto) {
        if (objetos.size() < capacidad){
            objetos.add(objeto);
        }
        else
            System.out.println("Lleno");
    }
    
    public void quitarObjeto(Objeto objeto) {
        objetos.remove(objeto);
    }
            
}
