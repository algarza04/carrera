/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/Classes/Class.java to edit this template
 */
package irrgarten;

/**
 *
 * @author alvarogz
 */
public class TestP2 {
    public static void main(String[] args) {
        System.out.println("----Monster-----");
        Monster m = new Monster ("m", Dice.randomIntelligence(), Dice.randomStrength());
        m.setPos(1, 2);
        System.out.println(m.toString());
        
        if (m.dead())
            System.out.println("Esta muerto");
        else
            System.out.println("NO esta muerto");
        
        System.out.println(m.attack());
        
        System.out.println("---------------------");
       
      
        System.out.println("----Player-----");
        Player p = new Player ('1', Dice.randomIntelligence(), Dice.randomStrength());
        System.out.println(p.toString());
        System.out.println(p.attack());
   
        if (p.dead())
            System.out.println("Esta muerto");
        else
            System.out.println("NO esta muerto");

       
        while (p.dead()) p.resurrect();
        
        System.out.println(p.toString());
        
        System.out.println("----------------------------");
      
        System.out.println("---------Labyrinth----------");
        Labyrinth l = new Labyrinth (3, 3, 2, 2);
        System.out.println(l.toString());
        System.out.println("Añado el monstruo m :");
        l.addMonster(1, 1, m);   
       
        System.out.println(l.toString());
        int pos[];
        for(int i = 0; i < 20; i++){
            pos= l.randomEmptyPos();
            System.out.println("\n pos: "+pos[0] +", "+ pos[1] +"\n");
            
        }
        
        System.out.println("----------------------------");
        
        System.out.println("------------Game------------");
        
        System.out.println("----------------------------");
    }
}
