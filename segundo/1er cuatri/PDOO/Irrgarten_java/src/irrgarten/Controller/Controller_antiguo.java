package irrgarten.Controller;

import irrgarten.Directions;
import irrgarten.Game;
import irrgarten.UI.TextUI;

public class Controller_antiguo {    
    private Game game;
    private TextUI view;
    
    public Controller_antiguo(Game game, TextUI view) {
        this.game = game;
        this.view = view;
    }
    
    public void play() {
        boolean endOfGame = false;
        while (!endOfGame) {
            view.showGame(game.getGameState()); 
            Directions direction = view.nextMove(); 
            endOfGame = game.nextStep(direction);
        }
      view.showGame(game.getGameState());        
    }
    
}
