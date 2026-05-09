/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/Classes/Class.java to edit this template
 */
package sm.agz.graficos;

import java.awt.AlphaComposite;
import java.awt.Graphics2D;
import java.awt.RenderingHints;
import java.awt.geom.Ellipse2D;
import java.awt.geom.Point2D;
import java.awt.geom.Rectangle2D;

/**
 * Clase para crear un objeto de tipo elipse.
 * Extiende de MiShape.
 * @author alvarogz
 */
public class MiElipse extends MiShape {
    private Ellipse2D.Float elipse;
    private Point2D punto_inicio;

    /**
     * Constructor de la clase MiElipse.
     * Crear una nueva elipse.
     * @param p primer punto de la elipse, posteriormente se usara como la referencia para terminar de crear la elipse
     */
    public MiElipse(Point2D p) {
        punto_inicio = p;
        elipse = new Ellipse2D.Float((float)p.getX(), (float)p.getY(), 0, 0);
    }
    
    /**
     * Modificar la elipse ajustando su segundo punto. 
     * Este metodo permite redibujar la elipse, dandole asi un alto y ancho
     * @param p segundo punto de la elipse
     */
    public void setMiElipse(Point2D p) {
        elipse.setFrameFromDiagonal(punto_inicio, p);
    }

    @Override
    public void setLocation(Point2D pos, Point2D punto_agarre) {
        elipse.setFrame(pos.getX()-punto_agarre.getX(), pos.getY()-punto_agarre.getY(), elipse.width, elipse.height);
    }

    /**
     * Funcion que se encarga de dibujar la elipse. Le aplica las configuraciones de grosor, color, 
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

        if (isRelleno()) g2d.fill(elipse);//&& s != null

        g2d.draw(elipse);
        
        if (isMover()) marcarFiguraSeleccionada(g2d);
    }
    
    @Override
    public boolean contiene(Point2D p) {
        return elipse.contains(p);
    }

    @Override
    public Rectangle2D getAreaSeleccionada() {
        return elipse.getBounds2D();
    }
    
    @Override
    public Point2D getPoint() {
        Point2D punto = new Point2D.Double(elipse.getX(), elipse.getY());
        return punto;
    }
}
