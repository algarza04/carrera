/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/Classes/Main.java to edit this template
 */
package clase25nov;

/**
 *
 * @author alvarogz
 */
public class Clase25nov {

    /**
     * @param args the command line arguments
     */
    public static void main(String[] args) {
        // TODO code application logic here
        Jugador j = new Jugador("caballero1", 10);
        j.atacar();
        j.defender();
        System.out.println("Es de tipo " + j.getTipo());
        
        Monstruo m= new Monstruo("ogro1", 10);
        m.atacar();
        m.defender();
        System.out.println("Es de tipo " + m.getTipo());
    }
    
}
