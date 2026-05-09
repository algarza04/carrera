/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/Classes/Class.java to edit this template
 */
package sm.agz.graficos;

import java.awt.BasicStroke;
import java.awt.Color;
import java.awt.Graphics2D;
import java.awt.Point;
import java.awt.Stroke;
import java.awt.geom.Point2D;
import java.awt.geom.Rectangle2D;
import java.util.ArrayList;

/**
 * Clase que contiene los metodos comunes de los distintos tipos de objetos de dibujo.
 * @author alvarogz
 */
public abstract class MiShape {
    private Color color;
    private boolean relleno = false;
    private Stroke grosor = new BasicStroke();
    private boolean transparencia = false;
    private boolean alisado = false;
    private boolean mover = false;

    /**
     * @return Color actual
     */
    public Color getColor() {
        return color;
    }
    
    /**
     * Modificar el color activo.
     * @param color Incica el color que se debe aplicar
     */
    public void setColor(Color color) {
        this.color = color;
    }

    /**
     * @return True si hay que rellenar y False en caso contrario
     */
    public boolean isRelleno() {
        return relleno;
    }

    /**
     * Modificar el parametro relleno.
     * @param relleno Indica si se debe realizar relleno
     */
    public void setRelleno(boolean relleno) {
        this.relleno = relleno;
    }

    /**
     * @return Valor del grosor
     */
    public Stroke getGrosor() {
        return grosor;
    }

    /**
     * Modificar el parametro grosor.
     * @param grosor Indica el nuevo valor del grosor
     */
    public void setGrosor(Stroke grosor) {
        this.grosor = grosor;
    }

    /**
     * @return True si hay que realizar transparencia y False en caso contrario
     */
    public boolean isTransparencia() {
        return transparencia;
    }

    /**
     * Modificar el parametro transparencia.
     * @param transparencia True si hay que realizar transparencia
     */
    public void setTransparencia(boolean transparencia) {
        this.transparencia = transparencia;
    }

    /**
     * @return True si hay que realizar alisado y False en caso contrario
     */
    public boolean isAlisado() {
        return alisado;
    }

    /**
     * Modificar el parametro alisado.
     * @param alisado True si hay que realizar alisado
     */
    public void setAlisado(boolean alisado) {
        this.alisado = alisado;
    }

    /**
     * @return true si esta en modo movimiento/edicion
     */
    public boolean isMover() {
        return mover;
    }

    /**
     * Modificar el parametro mover/edicion.
     * @param mover true si se puede mover o cambiar sus propiedades
     */
    public void setMover(boolean mover) {
        this.mover = mover;
    }
    
    /**
     * Crear un nuevo punto a partir de dos coordenadas.
     * @param x coordenada del eje x
     * @param y coordenada del eje y
     * @return devuelve el nuevo punto
     *
    public Point2D crearPunto(float x, float y) {
        return new Point2D.Float(x, y);
    }*/
    
    /**
     * Esta función marca la figuras seleccionada y sus esquinas. Recibe el área de la figura seleccionada
     * y marca con una línea discontinua dicho áera y sus esquinas.
     * @param g2d Objeto de Graphics2D encargado de dibujar
     */
    public void marcarFiguraSeleccionada(Graphics2D g2d) {
        ArrayList<Point2D.Float> esquinas_area = new ArrayList<>(); //array que contendrá cada esquina del area
        ArrayList<Point2D.Float> esquinas_marca = new ArrayList<>(); //array que contendrá las coordenadas que tendrá cada marca cuadrada de las esquinas del area seleccionada
        ArrayList<Rectangle2D> esquinas = new ArrayList<>();    //array que contendrá cada uno de los cuadrados de las esquinas
        
        float maxX = (float)getAreaSeleccionada().getMaxX();
        float maxY = (float) getAreaSeleccionada().getMaxY();
        float minX = (float)getAreaSeleccionada().getMinX();
        float minY = (float) getAreaSeleccionada().getMinY();

        esquinas_area.add(new Point2D.Float(minX, minY));
        esquinas_area.add(new Point2D.Float(minX, maxY));
        esquinas_area.add(new Point2D.Float(maxX, minY));
        esquinas_area.add(new Point2D.Float(maxX, maxY));
        esquinas_marca.add(new Point2D.Float(minX+5, minY+5));
        esquinas_marca.add(new Point2D.Float(minX+5, maxY+5));
        esquinas_marca.add(new Point2D.Float(maxX+5, minY+5));
        esquinas_marca.add(new Point2D.Float(maxX+5, maxY+5));

        for (int i = 0; i < 4; i++){
            Rectangle2D rectArea = new Rectangle2D.Float();
            rectArea.setFrameFromCenter(esquinas_area.get(i), esquinas_marca.get(i));
            esquinas.add(rectArea);
        }

        float discontinuidad[] = {8.0f, 4.0f};
        g2d.setStroke(new BasicStroke(1.0f, BasicStroke.CAP_ROUND, BasicStroke.JOIN_MITER, 1.0f, discontinuidad, 0.0f));
        g2d.setPaint(Color.RED);      
        g2d.draw(getAreaSeleccionada());

        for (Rectangle2D esq : esquinas)
            g2d.draw(esq);
    }
                
    /**
     * Modifica la posicion de la forma
     * @param pos Indica la nueva posicion
     */
    public abstract void setLocation(Point2D pos, Point2D pos2);
   
   
    public abstract Point2D getPoint();
    
    /**
     * Dibuja la forma
     * @param g2d Objeto para pintar
     */
    public abstract void draw(Graphics2D g2d);
    
    /**
     * Indica si un punto esta dentro del area de una figura.
     * @param p Punto a comprobar
     * @return True si corresponde al area, false en caso contrario
     */
    public abstract boolean contiene(Point2D p);
    
    /**
     * Función para conocer el área de una figura. Esta función nos devolverá el área que ocupa una
     * figura para posteriormente poder remarcarla.
     * @return un rectangulo que indica su área
     */
    public abstract Rectangle2D getAreaSeleccionada();
}
