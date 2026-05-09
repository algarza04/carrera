/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/Classes/Class.java to edit this template
 */
package sm.agz.eventos;

import java.awt.geom.Point2D;
import java.util.EventObject;
import sm.agz.graficos.MiShape;

/**
 * Clase para obtener información sobre un determinado evento.
 * @author alvarogz
 */
public class LienzoEvent extends EventObject {
    private MiShape forma;
    private Point2D punto;

    public LienzoEvent(Object source, MiShape forma, Point2D punto) {
        super(source);
        this.forma = forma;
        this.punto = punto;
    }

    public MiShape getForma() {
        return forma;
    }
    
    public Point2D getPunto() {
        return punto;
    }
}
