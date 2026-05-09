/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/Classes/Class.java to edit this template
 */
package sm.agz.graficos;

import java.awt.AlphaComposite;
import java.awt.Graphics2D;
import java.awt.RenderingHints;
import java.awt.geom.Line2D;
import java.awt.geom.Point2D;
import java.awt.geom.Rectangle2D;

/**
 * Clase para crear un objeto de tipo linea.
 * Extiende de MiShape.
 * @author alvarogz
 */
public class MiLinea extends MiShape {
    private Line2D.Float linea;
    private Point2D punto_ini;

    /**
     * Constructor de la clase MiLinea.
     * Crear una nueva linea.
     * @param p primer punto de la linea, posteriormente se usara como la referencia para terminar de crearla 
     */
    public MiLinea(Point2D p) {
        punto_ini = p;
        linea = new Line2D.Float(p, p);
    }
    
     /**
     * Modificar la linea ajustando su segundo punto. 
     * Este metodo permite redibujar la linea, dandole asi la distancia entre puntos
     * @param p segundo punto de la linea
     */
    public void setMiLinea(Point2D p) {
        linea.setLine(punto_ini, p);
    }
    
    public boolean isNear(Point2D p){
        if(linea.getP1().equals(linea.getP2())) return linea.getP1().distance(p)<=2.0; //p1=p2
        
        return linea.ptLineDist(p)<=2.0; // p1!=p2
    }
    
    @Override
    public boolean contiene(Point2D p) {
        return isNear(p);
    }

    @Override
    public void setLocation(Point2D pos, Point2D punto_agarre) {          
        double x_arreglado = pos.getX() - punto_agarre.getX();
        double y_arreglado = pos.getY() - punto_agarre.getY();
        
        Point2D newp1 = new Point2D.Double(x_arreglado, y_arreglado);
        
        double dx = x_arreglado - linea.getX1();
        double dy = y_arreglado - linea.getY1();

        Point2D newp2 = new Point2D.Double(linea.getX2()+dx,linea.getY2()+dy);
     
        linea.setLine(newp1,newp2);    
    }

    /**
     * Funcion que se encarga de dibujar la linea. Le aplica las configuraciones de grosor, color, 
     * transparencia y alisado correspondientes.
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

        g2d.draw(linea);
        
        if (isMover()) marcarFiguraSeleccionada(g2d);
    }

    @Override
    public Rectangle2D getAreaSeleccionada() {
        return linea.getBounds2D();
    }
    
    @Override
    public Point2D getPoint() {
        return linea.getP1();
    }
}
