/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/Classes/Class.java to edit this template
 */
package irrgarten;

/**
 *
 * @author alvarogz
 */
public class test {
    
    public static void main(String[] args) {
        Weapon w = new Weapon(3,1);
        System.out.println(w.toString());
        System.out.println(w.attack());
        System.out.println(w.discard());
         System.out.println(w.toString());
        Shield s = new Shield(2,10);
        System.out.println(s.toString());
    }
}
