/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/Classes/Class.java to edit this template
 */
package sm.agz.imagenes;

import java.awt.Color;
import java.awt.image.BufferedImage;
import java.awt.image.WritableRaster;
import static java.lang.Math.abs;
import sm.image.BufferedImageOpAdapter;

/**
 * Esta clase realiza una modificación del tono de una imágen.
 * Se encarga de desplazar el tono de los pixeles (cambio de color) cuya distancia al 
 * color base elegido sea menor o igual que el umbral establecido.
 * @author alvarogz
 */
public class TonoOp extends BufferedImageOpAdapter {
    private Color color;
    private float umbral, desplazamiento_tono;
    
    /**
     * Constructor de la clase.
     * Crea una nueva instancia de la clase con el color deseado, el umbral y el desplazamiento.
     * @param color indica el tono al que habrá que realizarle el desplazamiento
     * @param umbral valor para definir la similitud entre tonos (0-180)
     * @param desplazamiento_tono grados a desplazar el tono (0-360)
     */
    public TonoOp(Color color, float umbral, float desplazamiento_tono) {
        this.color = color;
        this.umbral = umbral;
        this.desplazamiento_tono = desplazamiento_tono;
    }
    
    /**
     * Aplicar la operación de cambio de tono.
     * Esta es la función que se encarga de llevar a cabo el cambio de tono, para ello 
     * aplica el desplazamiento a los pixeles similares al color base cuando su distancia mínima 
     * sea menor o igual al tamaño del umbral.
     * @param src imagen fuente a la que se aplica la operación.
     * @param dest imagen destino, en ella se guardará el resultado. 
     * @return imagen resultante al aplicar la operación
     */
    @Override
    public BufferedImage filter(BufferedImage src, BufferedImage dest) {
        
        
        float[] hsb = Color.RGBtoHSB(color.getRed(), color.getGreen(), color.getBlue(), null);
        float Hc = hsb[0] * 360f;
        
        WritableRaster srcRaster = src.getRaster();
        WritableRaster destRaster = dest.getRaster();
        
        float[] pixelComp = new float[srcRaster.getNumBands()];
        int[] pixelCompDest = new int[srcRaster.getNumBands()];
        
        for (int x = 0; x < src.getWidth(); x++) {
            for (int y = 0; y < src.getHeight(); y++) {
                srcRaster.getPixel(x, y, pixelComp); // pixelComp creado fuera del bucle

                Color.RGBtoHSB((int)pixelComp[0], (int)pixelComp[1], (int)pixelComp[2], pixelComp);
                float H, S, B;
                H = pixelComp[0] * 360f;
                S = pixelComp[1];
                B = pixelComp[2];

                if (calcularDistancia(Hc, H) <= umbral) 
                    H = (H+desplazamiento_tono) % 360f;

                int colorint = Color.HSBtoRGB(H/360, S, B);
                pixelCompDest[0] = (colorint >> 16) & 0xFF;
                pixelCompDest[1] = (colorint >> 8) & 0xFF;
                pixelCompDest[2] = colorint & 0xFF;

                destRaster.setPixel(x, y, pixelCompDest);
            }
        }
        
        return dest;
    }

    /**
     * Función que calcula la distancia mínima entre dos tonos en HSB
     * @param H1 primer tono
     * @param H2 segundo tono
     * @return distancia mínima entre H1 y H2 (0-180)
     */
    private float calcularDistancia(float H1, float H2) {
        if (abs(H1-H2) <= 180)
            return abs(H1-H2);
        else
            return 360 - abs(H1-H2);
    }
}