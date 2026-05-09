/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/Classes/Class.java to edit this template
 */

/**
 *
 * @author alvarogz
 */
public class TareaEstudio extends Tarea {
    
    public TareaEstudio(String titulo, Prioridad prioridad, String descripcion) {
        super(titulo, prioridad, descripcion);
    }
    
    public String toString(){
        return super.toString() + "Soy una tarea de estudio " +getTitulo()+ " " +mostrarDetalles() + "\n ";
    }
    
     @Override
    public TipoTarea getCategoria() {
        return TipoTarea.Estudio; 
    }
}
