/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/Classes/Class.java to edit this template
 */
package irrgarten;

/**
 *
 * @author alvarogz
 */
public class WeaponsCardDeck extends CardDeck<Weapon> {
    @Override
    protected void addCards() {
        for(int i = 0; i < 5; i++) {
            Weapon arma = new Weapon(Dice.weaponPower(), Dice.usesLeft());
            super.addCard(arma);
        }
    }
}
