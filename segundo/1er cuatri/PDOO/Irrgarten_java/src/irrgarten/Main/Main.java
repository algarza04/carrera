/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/Classes/Class.java to edit this template
 */
package irrgarten.Main;

import irrgarten.Game;
import irrgarten.UI.TextUI;
import irrgarten.UI.TextGUI;
import irrgarten.controller.Controller;
import java.util.Scanner;

/**
 *
 * @author alvarogz
 */
public class Main {

    /**
     * @param args the command line arguments
     */
    public static void main(String[] args) {
        // TODO code application logic here
        Scanner in = new Scanner(System.in);
        System.out.println("Selecciona el número de jugadores: \n");
        
        
        //Introduce un numero
         //int nplayers=in.nextInt();
         int nplayers = 1;
         //System.out.println("Elegiste jugar con: " + nplayers + " jugadores. Ahora toca jugar. \n");
       
     
        Game game = new Game (nplayers, false);
        TextGUI view = new TextGUI();
        
        Controller Controlador = new Controller(game, view);
        
        Controlador.play();   
    }
}
