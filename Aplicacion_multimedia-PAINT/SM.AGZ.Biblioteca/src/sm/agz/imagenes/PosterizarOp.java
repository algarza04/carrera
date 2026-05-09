/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/Classes/Class.java to edit this template
 */
package sm.agz.imagenes;

import java.awt.image.BufferedImage;
import java.awt.image.WritableRaster;
import sm.image.BufferedImageOpAdapter;

/**
 * Esta clase se encarga de aplicar la operación posterizado en una imágen.
 * Esta operación consiste en reducir el número de colores existentes en una imágen
 * @author alvarogz
 */
public class PosterizarOp extends BufferedImageOpAdapter {
    private int niveles, k;

    /**
     * Constructor de la clase.
     * Crea una nueva instancia de la clase con el número de niveles deseado.
     * @param niveles número de niveles de color por canal
     */
    public PosterizarOp(int niveles) {
        this.niveles = niveles;
        k = 256 / this.niveles;
    }

    /**
     * Aplicar la operación de posterización a la imágen de entrada(src).
     * Aplica el efecto visual de reducción de coloresé.
     * 
     * @param src imagen fuente a la que se aplica la operación.
     * @param dest imagen destino, en ella se guardará el resultado. 
     * @return imagen resultante al aplicar la operación
     */
    @Override
    public BufferedImage filter(BufferedImage src, BufferedImage dest) {
        if (src == null) {
            throw new NullPointerException("src image is null");
        }
        if (dest == null) {
            dest = createCompatibleDestImage(src, null);
        }
        WritableRaster srcRaster = src.getRaster();
        WritableRaster destRaster = dest.getRaster();
        int sample;
        for (int x = 0; x < src.getWidth(); x++) {
            for (int y = 0; y < src.getHeight(); y++) {
                for (int band = 0; band < srcRaster.getNumBands(); band++) {
                    sample = srcRaster.getSample(x, y, band);
                    sample = k * (sample / k);
                    destRaster.setSample(x, y, band, sample);
                }
            }
        }
        return dest;
    }
}
