/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/Classes/Class.java to edit this template
 */
package irrgarten;

import java.util.Random;
import java.util.ArrayList;

/**
 *
 * @author alvarogz
 */
public class Dice {

    private static final int MAX_USES = 5;
    private static final float MAX_INTELLIGENCE = (float)10.0;
    private static final float MAX_STRENGTH = (float)10.0;
    private static final float RESURRECT_PROB = (float)0.3;
    private static final int WEAPONS_REWARD = 2;
    private static final int SHIELDS_REWARD = 3;
    private static final int HEALTH_REWARD = 5;
    private static final int MAX_ATTACK = 3;
    private static final int MAX_SHIELD = 2;
    private static Random generator = new Random();
    
    public static int randomPos(int max){   //nunca va a crear un número mayor o igual a max
        return generator.nextInt(max);
    }
    
    public static int whoStarts(int nplayers) {
        return generator.nextInt(nplayers);
    }
    
    public static float randomIntelligence(){
        return generator.nextFloat() * MAX_INTELLIGENCE;
    }
    
    public static float randomStrength() {
         return generator.nextFloat() * MAX_STRENGTH;
    }
    
    public static boolean resurrectPlayer() { 
        return generator.nextFloat() < RESURRECT_PROB; 
    }
    
    public static int weaponsReward() {
        return generator.nextInt(WEAPONS_REWARD + 1);
    }
    
    public static int shieldsReward() {
        return generator.nextInt(SHIELDS_REWARD + 1);
    }
    
    public static int healthReward() {
        return generator.nextInt(HEALTH_REWARD + 1);
    }
    
    public static float weaponPower() {
       return generator.nextFloat() * MAX_ATTACK;
    }
   
    public static float shieldPower() {
        return generator.nextFloat() * MAX_SHIELD;
    }
    
    public static int usesLeft() {
        return generator.nextInt(MAX_USES + 1);
    }
    
    public static float intensity(float competence) {
        return generator.nextFloat() * competence;
    }
    
    public static boolean discardElement(int usesLeft) {
        return generator.nextFloat() >= (float)(usesLeft) / MAX_USES;    
    }    
    
    public static Directions nextStep(Directions preference, ArrayList<Directions> validMoves, float intelligence) {
        if(generator.nextFloat() * MAX_INTELLIGENCE < intelligence)
            return preference;
        else
            return validMoves.get(generator.nextInt(validMoves.size()));
        
    }
}
