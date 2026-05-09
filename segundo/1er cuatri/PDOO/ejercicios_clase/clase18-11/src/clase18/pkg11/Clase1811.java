/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/Classes/Main.java to edit this template
 */
package clase18.pkg11;
import com.sun.nio.sctp.PeerAddressChangeNotification;
import java.util.ArrayList;
/**
 *
 * @author alvarogz
 */
public class Clase1811 {

    /**
     * @param args the command line arguments
     */
    public static void main(String[] args) {
        // TODO code application logic here
        ArrayList<Personaje> personajes;
        personajes= new ArrayList<>();
        
        Personaje personaje = new Personaje("Personaje", 10);
        Jugador jugador = new Jugador("jugador", 5, 2);
        Mago mago = new Mago("mago", 3, 1, "fuego");
        
        personajes.add(personaje);
        personajes.add(jugador);
        personajes.add(mago);
        
        for(int i = 0; i < personajes.size(); i++){
            personajes.get(i).atacar();
        }
        
        System.out.println(personaje.men);
    }
    
}
