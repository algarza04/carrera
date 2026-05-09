
import java.util.ArrayList;

/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/Classes/Class.java to edit this template
 */

/**
 *
 * @author alvarogz
 */
public class game {
    public ArrayList<TareaEstudio> tarea_estudio= new ArrayList<>();
    public ArrayList<TareaPersonal> tarea_personal = new ArrayList<>();
    public ArrayList<TareaTrabajo> tarea_trabajo = new ArrayList<>(); 
    public ArrayList<Tarea> tarea = new ArrayList<>();
    public game() {
       
    }
    
    @Override
    public String toString(){
        String estudio = "";
        for (int i = 0; i < tarea.size(); i++){
            estudio += tarea.get(i).toString();
        }
        
        return estudio;
    }
    
}
