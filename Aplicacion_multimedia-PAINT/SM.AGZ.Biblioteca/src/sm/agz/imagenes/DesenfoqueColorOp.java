/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/Classes/Class.java to edit this template
 */
package sm.agz.imagenes;

import java.awt.Color;
import java.awt.image.BufferedImage;
import java.awt.image.ConvolveOp;
import java.awt.image.Kernel;
import java.awt.image.WritableRaster;
import static java.lang.Math.abs;
import sm.image.BufferedImageOpAdapter;

/**
 * Esta clase emborrona lo que se asemeje al color seleccionado.
 * Se encarga de emborronar los pixeles cuya distancia al 
 * color base elegido sea menor o igual que el umbral establecido.
 * @author alvarogz
 */
public class DesenfoqueColorOp extends BufferedImageOpAdapter {
    private Color color;
    private float umbral;
    private int tam_mascara;

    /**
     * Constructor de la clase.
     * Crea una nueva instancia de la clase con el color deseado, el umbral y el tam_mascara(emborronamiento).
     * 
     * @param color indica el tono al que habrá que realizarle el emborronamiento
     * @param umbral valor para definir la similitud entre tonos (0-180)
     * @param tam_mascara nivel de emborronamiento
     */
    public DesenfoqueColorOp(Color color, float umbral, int tam_mascara) {
        this.color = color;
        this.umbral = umbral;
        this.tam_mascara = tam_mascara;
    }

    /**
     * Aplicar la operación de emborronamiento del color.
     * Esta es la función que se encarga de llevar a cabo el emborronamiento, para ello 
     * aplica la máscara de emborronamiento a los pixeles que se asemejen al color 
     * base.
     * Esta función calcula internamente el emborronamiento con la OP ConvolveOp
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

        tam_mascara = tam_mascara * 2 + 1;
        float[] filtro = new float[tam_mascara * tam_mascara];
        for (int i = 0; i < filtro.length; i++) {
            filtro[i] = 1.0f / (tam_mascara * tam_mascara);
        }
        Kernel k = new Kernel(tam_mascara, tam_mascara, filtro);
        ConvolveOp cop = new ConvolveOp(k);
        BufferedImage imgDesenfocada = cop.filter(src, null);

        WritableRaster srcRaster = src.getRaster();
        WritableRaster destRaster = dest.getRaster();

        float[] hsb = Color.RGBtoHSB(color.getRed(), color.getGreen(), color.getBlue(), null);
        float Hc = hsb[0] * 360f;

        float[] pixelComp = new float[srcRaster.getNumBands()];
        int[] pixelCompDest = new int[srcRaster.getNumBands()];

        for (int x = 0; x < src.getWidth(); x++) {
            for (int y = 0; y < src.getHeight(); y++) {
                srcRaster.getPixel(x, y, pixelComp);

                float[] hsbPixel = Color.RGBtoHSB((int) pixelComp[0], (int) pixelComp[1], (int) pixelComp[2], null);
                float H = hsbPixel[0] * 360f;

                if (calcularDistancia(Hc, H) <= umbral) {
                    Color colorRBG = new Color(imgDesenfocada.getRGB(x, y));
                    pixelCompDest[0] = colorRBG.getRed();
                    pixelCompDest[1] = colorRBG.getGreen();
                    pixelCompDest[2] = colorRBG.getBlue();
                } else {
                    for (int i = 0; i < srcRaster.getNumBands(); i++)
                        pixelCompDest[i] = (int) pixelComp[i];
                }
                
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
