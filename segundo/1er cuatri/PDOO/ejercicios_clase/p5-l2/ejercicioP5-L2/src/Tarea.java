/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/Classes/Class.java to edit this template
 */

/**
 *
 * @author alvarogz
 */
public abstract class Tarea implements Visualizable {
    private String titulo;
    private String descripcion;
    private Prioridad prioridad;

    public Tarea(String titulo, Prioridad prioridad, String descripcion) {
        this.titulo = titulo;
        this.descripcion = descripcion;
        this.prioridad = prioridad;
    }

    public String getTitulo() {
        return titulo;
    }

    public Prioridad getPrioridad() {
        return prioridad;
    }

    public void setPrioridad(Prioridad prioridad) {
        this.prioridad = prioridad;
    }
    
    public String toString(){
        return "";
    }


    @Override
    public String mostrarDetalles() {
        return descripcion;
    }
    
   
    public abstract TipoTarea getCategoria();
    
}
