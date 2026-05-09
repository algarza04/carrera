
import java.util.Scanner;

/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/Classes/Class.java to edit this template
 */

/**
 *
 * @author alvarogz
 */
public class main {
    /**
     * @param args the command line arguments
     */
    public static void main(String[] args) {
        game game = new game ();
        GUI view = new GUI();
        
        Controller Controlador = new Controller(game, view);   
    }
}
