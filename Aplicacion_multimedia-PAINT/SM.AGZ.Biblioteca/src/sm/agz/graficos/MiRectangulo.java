/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/Classes/Class.java to edit this template
 */
package sm.agz.graficos;

import java.awt.AlphaComposite;
import java.awt.Graphics2D;
import java.awt.Point;
import java.awt.RenderingHints;
import java.awt.geom.Point2D;
import java.awt.geom.Rectangle2D;

/**
 * Clase para crear un objeto de tipo rectangulo.
 * Extiende de MiShape.
 * @author alvarogz
 */
public class MiRectangulo extends MiShape {
    private Rectangle2D.Float rectangulo;
    private Point2D punto_inicio;

    /**
     * Constructor de la clase MiRectangulo.
     * Crear un nuevo rectangulo.
     * @param p primer punto del rectangulo, posteriormente se usara como la referencia para terminar de crearlo
     */
    public MiRectangulo(Point2D p) {
        punto_inicio = p;
        rectangulo = new Rectangle2D.Float((float)p.getX(), (float)p.getY(), 0, 0);
    }
    
    public MiRectangulo(float x, float y, float w, float h ) {
        rectangulo = new Rectangle2D.Float(x, y, w, h);
    }
    
    /**
     * Modificar el rectangulo ajustando su segundo punto. 
     * Este metodo permite redibujar el rectangulo, dandole asi un alto y ancho
     * @param p segundo punto del rectangulo
     */
    public void setMiRectangulo(Point2D p) {
        rectangulo.setFrameFromDiagonal(punto_inicio, p);
    }
    
    public void setFrameFromCenter(Point2D centerX, Point2D corner) {
        rectangulo.setFrameFromCenter(centerX, corner);
    }

    /**
     * Funcion para mover un rectangulo.ó
     * @param pos 
     */
    @Override
    public void setLocation(Point2D pos, Point2D punto_agarre) {
        rectangulo.setFrame(pos.getX()-punto_agarre.getX(), pos.getY()-punto_agarre.getY(), rectangulo.width, rectangulo.height);
    }

    /**
     * Funcion que se encarga de dibujar el rectangulo. Le aplica las configuraciones de grosor, color, 
     * transparencia, alisado y relleno correspondientes.
     * @param g2d Objeto de Graphics2D encargado de dibujar
     */
    @Override
    public void draw(Graphics2D g2d) {
        g2d.setStroke(getGrosor());

        g2d.setPaint(getColor());

        if (isTransparencia()) g2d.setComposite(AlphaComposite.getInstance(AlphaComposite.SRC_OVER, 0.5f));
        else g2d.setComposite(AlphaComposite.getInstance(AlphaComposite.SRC_OVER, 1f));

        if (isAlisado()) g2d.setRenderingHint(RenderingHints.KEY_ANTIALIASING, RenderingHints.VALUE_ANTIALIAS_ON);
        else g2d.setRenderingHint(RenderingHints.KEY_ANTIALIASING, RenderingHints.VALUE_ANTIALIAS_OFF); 

        if (isRelleno() && rectangulo != null) g2d.fill(rectangulo);//&& s != null

        g2d.draw(rectangulo);
        
        if (isMover()) marcarFiguraSeleccionada(g2d);
    }
    
    /**
     * Funcion que nos indica si un punto esta dentro del area del rectangulo.
     * @param p Punto que queremos saber si corresponde o no al rectangulo.
     * @return Devuelve true o false en funcion de si lo esta o de si no.
     */
    @Override
    public boolean contiene(Point2D p) {
        return rectangulo.contains(p);
    }

    @Override
    public Rectangle2D getAreaSeleccionada() {
        return rectangulo.getBounds2D();
    }

       @Override
    public Point2D getPoint() {
        Point2D punto = new Point2D.Double(rectangulo.getX(), rectangulo.getY());
        return punto;
    }
}
