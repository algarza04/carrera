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
public class Player extends LabyrinthCharacter{
    private static final int MAX_WEAPONS = 2;
    private static final int MAX_SHIELD = 3;
    private static final int INITIAL_HEALTH = 1;
    private static final int HIT2LOSE = 3;
    
    private char number;
    private int consecutiveHits = 0;
    
    private ArrayList<Weapon> weapons = new ArrayList<>();
    private ArrayList<Shield> shields = new ArrayList<>();
    private WeaponsCardDeck weaponCardDeck;
    private ShieldCardDeck shieldCardDeck;
    
    public Player(char number, float intelligence, float strength) {
        super("Player#"+number, intelligence, strength, INITIAL_HEALTH);
        this.number = number;
        weaponCardDeck = new WeaponsCardDeck();
        shieldCardDeck = new ShieldCardDeck();
    }
    
    public Player(Player other){
        super(other);
    }
    
    public void resurrect() {
        weapons = new ArrayList<>();
        shields = new ArrayList<>();
        super.setHealth(INITIAL_HEALTH);
        this.consecutiveHits = 0;
    }
    
    public char getNumber() {
        return this.number;
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
    
    @Override
    public float attack() {
        return super.getStrength() + sumWeapons();
    }
    
    @Override
    public boolean defend(float receivedAttack) {
        return manageHit(receivedAttack);
    }
    
    public void receiveReward() {
        int wReward = Dice.weaponsReward();
        int sReward = Dice.shieldsReward();
        
        for (int i = 1; i <= wReward; i++){
            Weapon wnew = weaponCardDeck.nextCard();
            receiveWeapon(wnew);
        }
        
        for (int i = 1; i <= sReward; i++){
            Shield snew = shieldCardDeck.nextCard();
            receiveShield(snew);
        }
        
        int extraHealth = Dice.healthReward();
        
        super.setHealth(getHealth()+extraHealth);
    }
    
    @Override
    public String toString() {
        return "[" + super.toString() +"\n" + "armas: " + weapons + ", escudos: " + shields + "\n\n" + "]";
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
    
    protected float sumWeapons() {
        float suma = 0f;
        
        for (Weapon w : weapons){
           suma += w.attack();
        }
        
        return suma;
    }
    
    protected float sumShields() {
        float suma = 0f;
        
        for (Shield s : shields){
            suma += s.protect();
        }
        
        return suma;
    }
    
    protected float defensiveEnergy() {
        return super.getIntelligence() + sumShields();
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
    
    private void incConsecutiveHits() {
        this.consecutiveHits++;
    }   
}
