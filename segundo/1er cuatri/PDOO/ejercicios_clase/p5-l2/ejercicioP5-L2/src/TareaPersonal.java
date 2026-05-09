/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/Classes/Class.java to edit this template
 */

/**
 *
 * @author alvarogz
 */
public class TareaPersonal extends Tarea {
    
    public TareaPersonal(String titulo, Prioridad prioridad, String descripcion) {
        super(titulo, prioridad, descripcion);
    }
    
     @Override
    public TipoTarea getCategoria() {
        return TipoTarea.Personal;
    }
    
    public String toString(){
        return super.toString() + "Soy una tarea de personal " +getTitulo()+ " " +mostrarDetalles() + "\n ";
    }
}
