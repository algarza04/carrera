/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/Classes/Class.java to edit this template
 */
package irrgarten;

/**
 *
 * @author alvarogz
 */
public class Monster {
    private static final int INITIAL_HEALTH = 5;
    
    private String name;
    private float intelligence;
    private float strength;
    private float health;
    private int row;
    private int col;
    
    public Monster(String name, float intelligence, float strength) {
        this.name = name;
        this.intelligence = intelligence;
        this.strength = strength;
        this.health = INITIAL_HEALTH;
    }
    
    public boolean dead() {
        return this.health == 0;
    }
    
    public float attack() {
        return Dice.intensity(this.strength);
    }
    
    public boolean defend(float receivedAttack) {
        boolean isDead = dead();
        
        if (!isDead){
            float defensiveEnergy = Dice.intensity(intelligence);
            
            if (defensiveEnergy < receivedAttack){
                gotWounded();
                isDead = dead();
            }
        }
        
        return isDead;
    }
    
    public void setPos(int row, int col) {
        this.row = row;
        this.col = col;
    }
    
    @Override
    public String toString() {
        return "[Nombre: " + this.name + " , inteligencia: " + this.intelligence + ", fuerza: " + this.strength + ", vida: " + this.health + ", fila: " + this.row + ", columna: " + this.col + "]\n";
    }
    
    private void gotWounded() {
        this.health--;
    }   
 }
