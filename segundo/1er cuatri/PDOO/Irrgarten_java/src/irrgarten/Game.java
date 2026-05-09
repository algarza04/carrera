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
public class Game {
    private static final int MAX_ROUNDS = 10;
    
    private int currentPlayerIndex;
    private String log;
    private int tamanio_tablero = 10;
    
    private Labyrinth laberinto;
    private ArrayList<Monster> monsters = new ArrayList<>();
    private ArrayList<Player> players = new ArrayList<>();
    private Player currentPlayer;
    
    public Game(int nplayers, boolean modoDebug) {
        if(!modoDebug){
            for (int i = 0; i < nplayers; i++){
                Player p = new Player((char) (i + '0'), Dice.randomIntelligence(), Dice.randomStrength());
                players.add(p);
            }

            this.currentPlayerIndex =  Dice.whoStarts(nplayers);
            currentPlayer = players.get(currentPlayerIndex);
            this.log = "";

            laberinto = new Labyrinth(tamanio_tablero, tamanio_tablero, 2, 3);
            configureLabyrinth();
            laberinto.spreadPlayers(players, modoDebug);
        }
        else {
            currentPlayerIndex = 0;
            log = "";
            Player aux = new Player('0', Dice.randomIntelligence(), Dice.randomStrength());
            players.add(aux);
            configureLabyrinthDEBUG();
            laberinto.spreadPlayers(players, modoDebug);
            currentPlayer = players.get(currentPlayerIndex);
        }
        
    }
    
    public boolean finished() {
        return laberinto.haveAWinner();
    }
    
    public boolean nextStep(Directions preferredDirection) {
        log = "";
        boolean dead = currentPlayer.dead();
        
        if (!dead){
            Directions direction = actualDirection(preferredDirection);
            
            if (direction != preferredDirection)
                logPlayerNoOrders();
            
            Monster monster = laberinto.putPlayer(direction, currentPlayer);
            
            if (monster == null)
                logNoMonster();
            else {
                if (!monster.dead()){
                    GameCharacter winner = combat(monster);
                    manageReward(winner);
                }
            }
        }
        else {
            manageResurrection();
        }
        
        boolean endGame = finished();
        
        if (!endGame)
            nextPlayer();
        
        return endGame;
    }
    
    public GameState getGameState() {
        return new GameState(laberinto.toString(), currentPlayer.toString(), monsters.toString(), currentPlayerIndex, laberinto.haveAWinner(), log);
    }
    
    private void configureLabyrinth() {
        int num_muros = 12;
        int length = 2;
        
        for (int i = 0; i < num_muros; i++){
            int pos[] = laberinto.randomEmptyPos();
            int fil_muro = pos[0];
            int col_muro = pos[1];
            laberinto.addBlock(Orientation.HORIZONTAL, fil_muro, col_muro, length);
        }
        
        //---------------------
        int num_mons = 16;
        
        for (int i = 0; i < num_mons; i++){
            int pos[] = laberinto.randomEmptyPos();
            int fil_random = pos[0];
            int col_random = pos[1];
          
            Monster monster = new Monster("M", Dice.randomIntelligence(), Dice.randomStrength());
            laberinto.addMonster(fil_random, col_random, monster); 
            monster.setPos(fil_random, col_random);
            monsters.add(monster);
        }
    }
    
    private void configureLabyrinthDEBUG() {
        int nRows = 3;
        int nCols = 3;

        laberinto = new Labyrinth(nRows,nCols,2,2);

        Monster monster = new Monster("Monster",(float)6,(float)6);

        laberinto.addMonster(1, 0, monster);
        monster.setPos(1, 0);
        monsters.add(monster);
    }
    
    private void nextPlayer() {
        if (currentPlayerIndex == players.size()-1)
            currentPlayerIndex = 0;
        else
            currentPlayerIndex++;
        
        currentPlayer = players.get(currentPlayerIndex);
        
    }
    
    private Directions actualDirection(Directions preferredDirection) {
        int currentRow = currentPlayer.getRow();
        int currentCol = currentPlayer.getCol();
        
        return currentPlayer.move(preferredDirection, laberinto.validMoves(currentRow, currentCol));
    }
    
    private GameCharacter combat(Monster monster) {
        int rounds = 0;
        GameCharacter winner = GameCharacter.PLAYER;

        float playerAttack = currentPlayer.attack();   
        boolean lose = monster.defend(playerAttack);

        while (!lose && rounds < MAX_ROUNDS){
            winner = GameCharacter.MONSTER;
            rounds++;

            float monsterAttack = monster.attack();
            lose = currentPlayer.defend(monsterAttack);

            if (!lose){
                playerAttack = currentPlayer.attack();
                winner = GameCharacter.PLAYER;
                lose = monster.defend(playerAttack);
            }    
        }

        logRounds(rounds, MAX_ROUNDS);

        if(winner == GameCharacter.MONSTER)
            logMonsterWon();
        else
            logPlayerWon();
        
        return winner; 
    }
    
    private void manageReward(GameCharacter winner) {    
        if (winner == GameCharacter.PLAYER)
            currentPlayer.receiveReward();
    }
    
    private void manageResurrection() {
        boolean resurrect = Dice.resurrectPlayer();
        
        if (resurrect){
            /*currentPlayer.resurrect();
            FuzzyPlayer fuzzy = new FuzzyPlayer(currentPlayer);
            players.remove(currentPlayer);
            players.add(fuzzy);
            logResurrected();*/
            
            currentPlayer.resurrect();
            FuzzyPlayer fuzzy = new FuzzyPlayer(currentPlayer);
            players.set(currentPlayerIndex, fuzzy);
            laberinto.colocaFuzzyPlayer(fuzzy, fuzzy.getRow(), fuzzy.getCol());
            logResurrected();
        }
        else {
            logPlayerSkipTurn();
        }
    }
    
    private void logPlayerWon() {
        log += "El jugador ha ganado el combate. \n";
    }
    
    private void logMonsterWon() {
        log += "El monstruo ha ganado el combate. \n";
    }
    
    private void logResurrected() {
        log += "El jugador ha resucitado. Soy un FuzzyPlayer. \n";
    }
    
    private void logPlayerSkipTurn() {
        log += "El jugador ha perdido el turno por estar muerto. \n";
    }
    
    private void logPlayerNoOrders() {
        log += "El jugador no ha seguido las instrucciones del jugador humano. \n";
    }
    
    private void logNoMonster() {
        log += "El jugador se ha movido a una celda vacía\n";
    }
    
    private void logRounds(int rounds, int max) {
        log += "Se han producido " + rounds + " de " + max + " rondas de combate. \n";
    }
}