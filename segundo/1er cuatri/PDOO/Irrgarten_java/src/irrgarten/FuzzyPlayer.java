/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/Classes/Class.java to edit this template
 */
package irrgarten;
import java.util.ArrayList;
/**
 *
 * @author alvarogz
 */
public class FuzzyPlayer extends Player {
    public FuzzyPlayer(Player other){
        
        super(other.getNumber(), other.getIntelligence(), other.getStrength());
        setPos(other.getRow(), other.getCol());
    }
    
    public Directions move(Directions direction, ArrayList<Directions> validMoves){
        int size = validMoves.size();
        boolean contained = validMoves.contains(direction);
        Directions preference;
        
        if (size == 0 || !contained){
            preference = validMoves.get(0);
        }
        else{
            preference = direction;
        }
        
        return Dice.nextStep(preference, validMoves, super.getIntelligence());
    }
    
    @Override
    public float attack(){
    return Dice.intensity(super.getStrength()) + super.attack();

    //return Dice.intensity(super.getStrength()) + super.sumWeapons();
    }
    
    @Override
    protected float defensiveEnergy(){
        //        return Dice.intensity(super.getIntelligence())+ super.sumShields();
        return Dice.intensity(super.getIntelligence())+ super.defensiveEnergy();
    }
    
    @Override
    public String toString(){
        return "Fuzzy" + super.toString();
    }
}
