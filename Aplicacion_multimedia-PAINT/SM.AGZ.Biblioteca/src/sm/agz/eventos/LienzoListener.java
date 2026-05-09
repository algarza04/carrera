/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/Classes/Interface.java to edit this template
 */
package sm.agz.eventos;

import java.util.EventListener;

/**
 * Clase para responder ante eventos que ocurran con el lienzo.
 * @author alvarogz
 */
public interface LienzoListener extends EventListener {
    void shapeAdded(LienzoEvent evt);
    void shapeSelected(LienzoEvent evt);
    void mouseMoved(LienzoEvent evt);
}
