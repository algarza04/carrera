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
public class Player {
    private static final int MAX_WEAPONS = 2;
    private static final int MAX_SHIELD = 3;
    private static final int INITIAL_HEALTH = 10;
    private static final int HIT2LOSE = 3;
    
    private String name = "Player#";
    private char number;
    private float intelligence;
    private float strength;
    private float health;
    private int row; 
    private int col;
    private int consecutiveHits = 0;
    
    private ArrayList<Weapon> weapons = new ArrayList<>();
    private ArrayList<Shield> shields = new ArrayList<>();
    
    public Player(char number, float intelligence, float strength) {
        this.number = number;
        this.name += number;
        this.intelligence = intelligence;
        this.strength = strength;
        this.health = INITIAL_HEALTH;
    }
    
    public void resurrect() {
        weapons = new ArrayList<>();
        shields = new ArrayList<>();
        this.health = INITIAL_HEALTH;
        this.consecutiveHits = 0;
    }
    
    public int getRow() {
        return this.row;
    }   
    
    public int getCol() {
        return this.col;
    }
    
    public char getNumber() {
        return this.number;
    }
    
    public void setPos(int row, int col) {
        this.row = row;
        this.col = col;
    }
    
    public boolean dead() {
        return this.health == 0;
    }
    
    public Directions move(Directions direction, ArrayList<Directions> validMoves) {
        int size = validMoves.size();
        boolean contained = validMoves.contains(direction);
        
        if (size > 0 && !contained){
            Directions firstElement = validMoves.get(0);
            return firstElement;
        }
        else
            return direction;
    }
    
    public float attack() {
        return this.strength + sumWeapons();
    }
    
    public boolean defend(float receivedAttack) {
        return manageHit(receivedAttack);
    }
    
    public void receiveReward() {
        int wReward = Dice.weaponsReward();
        int sReward = Dice.shieldsReward();
        
        for (int i = 1; i <= wReward; i++){
            Weapon wnew = newWeapon();
            receiveWeapon(wnew);
        }
        
        for (int i = 1; i <= sReward; i++){
            Shield snew = newShield();
            receiveShield(snew);
        }
        
        int extraHealth = Dice.healthReward();
        
        health += extraHealth;
    }
    
    @Override
    public String toString() {
        return "[" + this.name + ", inteligencia " + this.intelligence + ", fuerza: " + this.strength + ", vida: " + this.health + ", fila: " + this.row + ", columna: " + this.col +"\n" + "armas: " + weapons + ", escudos: " + shields + "]\n";
    }
    
    private void receiveWeapon(Weapon w) {
        /*for (Weapon wi : weapons){
            boolean discard = wi.discard();
            
            if (discard)
                weapons.remove(wi);
        }
        
        int size = weapons.size();
        
        if (size < MAX_WEAPONS)
            weapons.add(w);*/
        for (int i = 0; i < weapons.size(); i++){
            Weapon wi = weapons.get(i);
            
            boolean discard = wi.discard();
            
            if (discard){
                weapons.remove(i);
            }
        }
        
        int size = weapons.size();
        
        if (size < MAX_WEAPONS)
            weapons.add(w);
    }
    
    private void receiveShield(Shield s) {
        /*for (Shield si : shields){
            boolean discard = si.discard();
            
            if (discard)
                shields.remove(si);
        }
        
        int size = shields.size();
        
        if (size < MAX_SHIELD)
            shields.add(s);
            */
        for (int i = 0; i < shields.size(); i++){
            Shield si = shields.get(i);
            
            boolean discard = si.discard();
            
            if (discard){
                shields.remove(i);
            }
        }
        
        int size = shields.size();
        
        if (size < MAX_SHIELD)
            shields.add(s);
    }
    
    private Weapon newWeapon() {
        Weapon w = new Weapon(Dice.weaponPower(), Dice.usesLeft());
        return w;
    }
    
    private Shield newShield() {
        Shield s = new Shield(Dice.shieldPower(), Dice.usesLeft());
        return s;
    }
    
    private float sumWeapons() {
        float suma = 0f;
        
        for (Weapon w : weapons){
           suma += w.attack();
        }
        
        return suma;
    }
    
    private float sumShields() {
        float suma = 0f;
        
        for (Shield s : shields){
            suma += s.protect();
        }
        
        return suma;
    }
    
    private float defensiveEnergy() {
        return this.intelligence + sumShields();
    }
    
    private boolean manageHit(float receivedAttack) {
        float defense = defensiveEnergy();
        boolean lose;
        
        if (defense < receivedAttack){
            gotWounded();
            incConsecutiveHits();
        }
        else
            resetHits();
        
        if (consecutiveHits == HIT2LOSE || dead()){
            resetHits();
            lose = true;
        }
        else
            lose = false;
        
        return lose;
    }
    
    private void resetHits() {
        this.consecutiveHits = 0;
    }
    
    private void gotWounded() {
        this.health--;
    }
    
    private void incConsecutiveHits() {
        this.consecutiveHits++;
    }   
}
