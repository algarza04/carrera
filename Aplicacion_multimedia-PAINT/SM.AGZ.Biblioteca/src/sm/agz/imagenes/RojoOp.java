/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/Classes/Class.java to edit this template
 */
package sm.agz.imagenes;

import java.awt.image.BufferedImage;
import java.awt.image.WritableRaster;
import sm.image.BufferedImageOpAdapter;

/**
 * Esta clase se encarga de resaltar los píxeles rojos de una imagen.
 * Los pixeles que no superen el umbral se convierten a escala de grises.
 * @author alvarogz
 */
public class RojoOp extends BufferedImageOpAdapter {
    private int umbral;
    
    /**
     * Constructor de la clase. 
     * Crea una nueva instancia de la clase con el umbral pasado.
     * 
     * @param umbral valor mínimo en el canal rojo para que mantenga el color.
     */
    public RojoOp(int umbral) {
        this.umbral = umbral;
    }

    /**
     * Aplicar la operación de resaltar el rojo a la imágen src. 
     * 
     * Si la diferencia entre el componente rojo y la suma de verde y azul es mayor o igual que 
     * el umbral se mantendrá el color, en cambio si el rojo no es significativo se convierte a 
     * gris a través de la médoa de los componentes.ñ
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
        int[] pixelComp = new int[srcRaster.getNumBands()];
        int[] pixelCompDest = new int[srcRaster.getNumBands()];
        for (int x = 0; x < src.getWidth(); x++) {
            for (int y = 0; y < src.getHeight(); y++) {
                srcRaster.getPixel(x, y, pixelComp);
          
                int R = pixelComp[0];
                int G = pixelComp[1];
                int B = pixelComp[2];
                
                if ((R-G-B) >= umbral){
                    pixelCompDest[0] = R;
                    pixelCompDest[1] = G;
                    pixelCompDest[2] = B;
                }
                else {
                    int media = (R+G+B)/3;
                    for (int z = 0; z < srcRaster.getNumBands(); z++)
                        pixelCompDest[z] = media;
                }
                    
                destRaster.setPixel(x, y, pixelCompDest);
            }
        }
        return dest;
    }
}
