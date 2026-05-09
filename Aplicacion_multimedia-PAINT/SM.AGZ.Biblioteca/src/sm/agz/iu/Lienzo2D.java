/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/GUIForms/JPanel.java to edit this template
 */
package sm.agz.iu;

import java.awt.BasicStroke;
import java.awt.Color;
import java.awt.Graphics;
import java.awt.Graphics2D;
import java.awt.Stroke;
import java.awt.geom.Point2D;
import java.awt.image.BufferedImage;
import java.io.File;
import java.util.ArrayList;
import java.util.List;
import javax.sound.sampled.AudioSystem;
import javax.sound.sampled.Clip;
import sm.agz.eventos.LienzoEvent;
import sm.agz.eventos.LienzoListener;
import sm.agz.graficos.MiCurva;
import sm.agz.graficos.MiElipse;
import sm.agz.graficos.MiLinea;
import sm.agz.graficos.MiRectangulo;
import sm.agz.graficos.MiShape;
import sm.agz.graficos.TipoForma;

/**
 * Clase para crear una instancia de Lienzo2D.
 * En dicho lienzo podremos pintar imágenes con los objetos de la clase MiShape.
 * @author alvarogz
 */
public class Lienzo2D extends javax.swing.JPanel {
    private Color color = Color.BLACK;
    private Stroke grosor = new BasicStroke();
    private TipoForma tipo_activo = TipoForma.LINEA; 
    private MiShape forma = null; 
    private boolean relleno = false;
    private boolean mover = false;
    private boolean transparencia = false;
    private boolean alisado = false;
    private boolean released = false;   //atributo para mover el punto de control de la curva
    private boolean fijar = false;
    private boolean eliminar = false;
    private Point2D arreglar_salto;
    private BufferedImage img;
    List<MiShape> listaFiguras = new ArrayList();
    private final ArrayList<LienzoListener> lienzoListeners = new ArrayList<>();
    private File sonidoFijar, sonidoEliminar;
    
    /**
     * Creates new form Lienzo2D
     */
    public Lienzo2D() {
        initComponents();
    }

    /**
     * Dibujar las figuras almacenadas.
     * @param g Objeto para pintar
     */
    @Override
    public void paint(Graphics g){  //aqui no debe haber ningun new
        super.paint(g);
        Graphics2D g2d = (Graphics2D)g;
       
        if(img!=null){ 
            g2d.drawImage(img,0,0,this);
            g2d.setClip(0, 0, img.getWidth(), img.getHeight());
        }
        for (MiShape s: listaFiguras)
            s.draw(g2d);
        
    }
    

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
        
        if (forma != null && isMover()) {
            forma.setColor(getColor());
            repaint();
        } 
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
        
        if (forma != null && isMover()) {
            forma.setRelleno(isRelleno());
            repaint();
        }
    }
    
    /**
     * @return True si hay que mover la figura
     */
    public boolean isMover() {
        return mover;
    }

    /**
     * Modificar el parametro mover.
     * @param mover True si hay que mover, false si no 
     */
    public void setMover(boolean mover) {
        this.mover = mover;
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
    public void setGrosor(int grosor) {
        this.grosor = new BasicStroke(grosor);
        
        if (forma != null && isMover()) {
            forma.setGrosor(getGrosor());
            repaint();
        }
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
        
        if (forma != null && isMover()) {
            forma.setTransparencia(isTransparencia());
            repaint();
        }
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
        
        if (forma != null && isMover()) {
            forma.setAlisado(isAlisado());
            repaint();
        }
    }

    /**
     * @return Devuelve el tipo actual
     */
    public TipoForma getTipo_activo() {
        return tipo_activo;
    }

    /**
     * Modificar el tipo actual activo.
     * @param tipo_activo tipo al que hay que cambiar
     */
    public void setTipo_activo(TipoForma tipo_activo) {
        this.tipo_activo = tipo_activo;
        for (MiShape s : listaFiguras) s.setMover(false);   //si cambia el tipo activo deja de haber figura seleccionda
        repaint();
    }

    /**
     * Nos indica si fijar esta activo.
     * @return Devuelve true si la herramienta fijar esta activa
     */
    public boolean isFijar() {
        return fijar;
    }

    /**
     * Modificar el parámetro fijar.
     * @param fijar true si hay que fijar
     */
    public void setFijar(boolean fijar) {
        this.fijar = fijar;
        for (MiShape s : listaFiguras) s.setMover(false);   //si cambia el tipo activo deja de haber figura seleccionda
        repaint();
    }
    
    /**
     * Nos indica si eliminar esta activo.
     * @return Devuelve true si la herramienta fijar esta activa 
     */
    public boolean isEliminar() {
        return eliminar;
    }

    /**
     * Modificar el parámetro eliminar.
     * @param eliminar true si hay que eliminar
     */
    public void setEliminar(boolean eliminar) {
        this.eliminar = eliminar;
        for (MiShape s : listaFiguras) s.setMover(false);   //si cambia el tipo activo deja de haber figura seleccionda
        repaint();
    }
    
    /**
     * Esta función pone los botones que se pueden seleccionar a false y pone el valor tipo_activo a null.
     */
    public void setGrupoBotones() {
        setMover(false);
        setEliminar(false);
        setFijar(false);
        setTipo_activo(null);
    }
    
    /**
     * Establece la imagen a utilizar.
     * 
     * @param img Un objeto BufferedImage que representa la nueva imagen.
     */
    public void setImage(BufferedImage img){
        this.img = img;
    }
    
    /**
     * 
     * Devuelve la imagen actual.
     *
     * @return Un objeto BufferedImage que contiene la imagen actual.
     */
    public BufferedImage getImage(){
        return img;
    }
    
    /**
     * Devuelve el resultado de convinar una imágen y las figuras dibujadas en ella.
     * Crea una nueva imágen y usando un objeto Graphics2D pinta las figuras almacenadas en la lista de
     * figuras.
     * @return Imágen pintada con las figuras
     */
    public BufferedImage getPaintedImage() {
        BufferedImage imgout = new BufferedImage(img.getWidth(), img.getHeight(), img.getType());
    
        Graphics2D g2dImagen = imgout.createGraphics();
        
        if(img!=null) g2dImagen.drawImage(img,0,0,this);
        
        for(MiShape s: listaFiguras) s.draw(g2dImagen);
       
        return imgout;        
    }

    /**
     * Devuelve el archivo que contiene el sonido de fijar.
     * @return el objeto que representa el sonido fijar.
     */
    public File getSonidoFijar() {
        return sonidoFijar;
    }

    /**
     * Establece el archivo que contendrá el sonido fijar.
     * @param sonidoFijar Objeto que representa el fichero de sonido.
     */
    public void setSonidoFijar(File sonidoFijar) {
        this.sonidoFijar = sonidoFijar;
    }

    /**
     * Devuelve el archivo que contiene el sonido de eliminar.
     * @return el objeto que representa el sonido eliminar.
     */
    public File getSonidoEliminar() {
        return sonidoEliminar;
    }

    /**
     * Establece el archivo que contendrá el sonido eliminar.
     * @param sonidoEliminar Objeto que representa el fichero de sonido.
     */
    public void setSonidoEliminar(File sonidoEliminar) {
        this.sonidoEliminar = sonidoEliminar;
    }
    
    
    /**
     * @param p
     * @return si en el punto seleccionado esta la figura i la devuelve
     */
    private MiShape figuraSeleccionada(Point2D p){
        for (MiShape s : listaFiguras) s.setMover(false);
        repaint(); 
        
        for (int i = listaFiguras.size()-1; i >= 0 ; i--) {
            if (listaFiguras.get(i).contiene(p)) {
                listaFiguras.get(i).setMover(isMover());
                
                arreglar_salto = new Point2D.Double(p.getX() - listaFiguras.get(i).getPoint().getX(), p.getY() - listaFiguras.get(i).getPoint().getY());
                return listaFiguras.get(i);
            }
        }
     
        return null;
    }
    
    /**
     * Función encargada de reproducir el sonido que se encuentra en el archivo f.
     * Obtiene un objeto clip y lo inicia para reproducir el sonido. 
     * En caso de error imprime una excepción.
     * @param f Es el archivo de audio que se quiere reproducir
     */
    private void play(File f) {
        try {
            Clip sound = AudioSystem.getClip();
            sound.open(AudioSystem.getAudioInputStream(f));
            sound.start();
        } catch (Exception ex) {
            System.err.println(ex);
        }
    }
    
    public void addLienzoListener(LienzoListener listener) {
        if (listener != null) {
            lienzoListeners.add(listener);
        }
    }
    
    private void notifyShapeAddedEvent(LienzoEvent evt) {
        if (!lienzoListeners.isEmpty()) {
            for (LienzoListener listener : lienzoListeners) {
                listener.shapeAdded(evt);
            }
        }
    }

    private void notifyShapeSelectedEvent(LienzoEvent evt) {
        if (!lienzoListeners.isEmpty()) {
            for (LienzoListener listener : lienzoListeners) {
                listener.shapeSelected(evt);
            }
        }
    }

       private void notifyMouseMovedEvent(LienzoEvent evt) {
        if (!lienzoListeners.isEmpty()) {
            for (LienzoListener listener : lienzoListeners) {
                listener.mouseMoved(evt);
            }
        }
    }
    
    /**
     * This method is called from within the constructor to initialize the form.
     * WARNING: Do NOT modify this code. The content of this method is always
     * regenerated by the Form Editor.
     */
    @SuppressWarnings("unchecked")
    // <editor-fold defaultstate="collapsed" desc="Generated Code">//GEN-BEGIN:initComponents
    private void initComponents() {

        addMouseMotionListener(new java.awt.event.MouseMotionAdapter() {
            public void mouseDragged(java.awt.event.MouseEvent evt) {
                formMouseDragged(evt);
            }
            public void mouseMoved(java.awt.event.MouseEvent evt) {
                formMouseMoved(evt);
            }
        });
        addMouseListener(new java.awt.event.MouseAdapter() {
            public void mousePressed(java.awt.event.MouseEvent evt) {
                formMousePressed(evt);
            }
            public void mouseReleased(java.awt.event.MouseEvent evt) {
                formMouseReleased(evt);
            }
        });

        javax.swing.GroupLayout layout = new javax.swing.GroupLayout(this);
        this.setLayout(layout);
        layout.setHorizontalGroup(
            layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addGap(0, 400, Short.MAX_VALUE)
        );
        layout.setVerticalGroup(
            layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addGap(0, 300, Short.MAX_VALUE)
        );
    }// </editor-fold>//GEN-END:initComponents

    private void formMousePressed(java.awt.event.MouseEvent evt) {//GEN-FIRST:event_formMousePressed
        //aqui se crea la forma
        if(mover && listaFiguras != null) {   
            forma = figuraSeleccionada(evt.getPoint()); 
            notifyShapeSelectedEvent( new LienzoEvent(this,forma, evt.getPoint()) );
        }
        else {
            if (tipo_activo != null){
                switch (tipo_activo) {
                    case LINEA:
                        forma = new MiLinea(evt.getPoint());
                        break;
                    case RECTANGULO:
                        forma = new MiRectangulo(evt.getPoint());
                        break;    
                    case ELIPSE:
                        forma = new MiElipse(evt.getPoint());
                        break;
                    case CURVA:
                        if (!released)
                            forma = new MiCurva(evt.getPoint());
                        break;
                }
                if (forma != null ){
                    forma.setAlisado(isAlisado());
                    forma.setColor(getColor());
                    forma.setGrosor(getGrosor());
                    forma.setRelleno(isRelleno());
                    forma.setTransparencia(isTransparencia());

                    listaFiguras.add(forma);

                    notifyShapeAddedEvent( new LienzoEvent(this,forma, evt.getPoint()) );
                }
            }
        }
    }//GEN-LAST:event_formMousePressed

    private void formMouseDragged(java.awt.event.MouseEvent evt) {//GEN-FIRST:event_formMouseDragged
        if (mover && listaFiguras != null){
            if (forma instanceof MiShape) {              
                forma.setLocation(evt.getPoint(), arreglar_salto);
            }
               
        }
        else
            if (forma instanceof MiLinea)
                ((MiLinea) forma).setMiLinea(evt.getPoint());
            else if (forma instanceof MiRectangulo)
                ((MiRectangulo) forma).setMiRectangulo(evt.getPoint());
            else if (forma instanceof MiElipse)
                ((MiElipse) forma).setMiElipse(evt.getPoint());
            else if (forma instanceof MiCurva) 
                if (!released)
                    ((MiCurva) forma).setMiCurva(evt.getPoint());
                else
                    ((MiCurva) forma).setPtoCtrl(evt.getPoint());
        
        this.repaint();
    }//GEN-LAST:event_formMouseDragged

    private void formMouseReleased(java.awt.event.MouseEvent evt) {//GEN-FIRST:event_formMouseReleased
        if (tipo_activo == TipoForma.CURVA)
            if (released)
                released = false;
            else
                released = true;            
    }//GEN-LAST:event_formMouseReleased

    private void formMouseMoved(java.awt.event.MouseEvent evt) {//GEN-FIRST:event_formMouseMoved
        notifyMouseMovedEvent(new LienzoEvent(this,forma, evt.getPoint()));
        
        if (fijar){
            MiShape figura_fijada = null;
            for (MiShape figura : listaFiguras)
                if (figura.contiene(evt.getPoint())) {
                    figura_fijada = figura;
                    
                    Graphics2D g2d = img.createGraphics();
                    figura_fijada.draw(g2d);
                    break;
                }
            
            if (figura_fijada != null) {
                listaFiguras.remove(figura_fijada);
                repaint();
                play(sonidoFijar);
            } 
            
        }
        if (eliminar) {
            MiShape figura_encontrada = null;
            for (MiShape figura : listaFiguras)
                if (figura.contiene(evt.getPoint())) {
                    figura_encontrada = figura;
                    break;
                }
            
            if (figura_encontrada != null) {
                listaFiguras.remove(figura_encontrada);
                repaint();
                play(sonidoEliminar);
            } 
        }
    }//GEN-LAST:event_formMouseMoved


    // Variables declaration - do not modify//GEN-BEGIN:variables
    // End of variables declaration//GEN-END:variables
}
