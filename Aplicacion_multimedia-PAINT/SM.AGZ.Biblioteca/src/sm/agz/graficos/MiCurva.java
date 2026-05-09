/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/Classes/Class.java to edit this template
 */
package sm.agz.graficos;

import java.awt.AlphaComposite;
import java.awt.Graphics2D;
import java.awt.RenderingHints;
import java.awt.geom.Point2D;
import java.awt.geom.QuadCurve2D;
import java.awt.geom.Rectangle2D;

/**
 * Clase para crear un objeto de tipo curva.
 * Extiende de MiShape.
 * @author alvarogz
 */
public class MiCurva extends MiShape {
    private QuadCurve2D.Float curva;
    Point2D punto_inicio;
    Point2D segundo_punto;

    /**
     * Constructor de la clase MiCurva.
     * Crear una nueva curva.
     * @param p primer punto de la curva, posteriormente se usara como la referencia para terminar de crearla
     */
    public MiCurva(Point2D p) {
        punto_inicio = p;
        curva = new QuadCurve2D.Float((float)p.getX(), (float)p.getY(), (float)p.getX(), (float)p.getY(),(float)p.getX(), (float)p.getY());
    }
 
    /**
     * Modificar la curva ajustando su segundo punto. 
     * Este metodo permite redibujar la curva, dandole asi la distancia entre puntos
     * @param p segundo punto de la curva
     */
    public void setMiCurva(Point2D p) {
        segundo_punto = p;
        curva.setCurve(punto_inicio, p, p);
    }
    
    /**
     * Modificar el punto de control de la curva.
     * Este metodo permite dar el aspecto de curva
     * @param p indica en que punto se encontrara el pto de control
     */
    public void setPtoCtrl(Point2D p){
        curva.setCurve(punto_inicio, p, segundo_punto);
    }

    @Override
    public void setLocation(Point2D pos, Point2D punto_agarre) {   
        double x_arreglado = pos.getX() - punto_agarre.getX();
        double y_arreglado = pos.getY() - punto_agarre.getY();
        
        Point2D newp1 = new Point2D.Double(x_arreglado, y_arreglado);
        
        double dx = x_arreglado - curva.getX1();
        double dy = y_arreglado - curva.getY1();

        
        //Point2D newp1 = new Point2D.Double(curva.getX1()+dx,curva.getY1()+dy);
        Point2D newp2 = new Point2D.Double(curva.getX2()+dx,curva.getY2()+dy);
        Point2D newpCntl = new Point2D.Double(curva.getCtrlX()+dx,curva.getCtrlY()+dy);
        curva.setCurve(newp1, newpCntl, newp2);  
    }

    /**
     * Funcion que se encarga de dibujar la curva. Le aplica las configuraciones de grosor, color, 
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
        
        if (isRelleno()) g2d.fill(curva);//&& s != null
        
        g2d.draw(curva);
        
        if (isMover()) marcarFiguraSeleccionada(g2d);
    }

    @Override
    public boolean contiene(Point2D p) {
        return curva.contains(p);
    }

    @Override
    public Rectangle2D getAreaSeleccionada() {
        return curva.getBounds2D();
    }
    
    @Override
    public Point2D getPoint() {
        return curva.getP1();
    }
}
