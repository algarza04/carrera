/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/Classes/Class.java to edit this template
 */

/**
 *
 * @author alvarogz
 */
public class TareaTrabajo extends Tarea {
    
    public TareaTrabajo(String titulo, Prioridad prioridad, String descripcion) {
        super(titulo, prioridad, descripcion);
    }
    
     @Override
    public TipoTarea getCategoria() {
        return TipoTarea.Trabajo;
    }
    
    public String toString(){
        return super.toString() + "Soy una tarea de trabajo " +getTitulo()+ " " +mostrarDetalles() + "\n ";
    }
}
