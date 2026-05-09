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
public class Labyrinth {
    static private final char BLOCK_CHAR = 'X';
    static private final char EMPTY_CHAR = '-';
    static private final char MONSTER_CHAR = 'M';
    static private final char COMBAT_CHAR = 'C';
    static private final char EXIT_CHAR = 'E';
    static private final int ROW = 0;
    static private final int COL = 1;
    
    private int nRows;
    private int nCols;
    private int exitRow;
    private int exitCol;
    
    private Monster[][] monsters;
    private Player[][] players;
    private char[][] laberinto;
     
    public Labyrinth(int nRows, int nCols, int exitRow, int exitCol) {
        this.exitRow = exitRow;
        this.exitCol = exitCol;
        this.nRows = nRows;
        this.nCols = nCols;
        
        monsters = new Monster[this.nRows][this.nCols];
        players = new Player[this.nRows][this.nCols];
        laberinto = new char[this.nRows][this.nCols];
        
        for (int i = 0; i < this.nRows; i++){
            for (int j = 0; j < this.nCols; j++){
                laberinto[i][j] = EMPTY_CHAR;
            }
        }
        
         laberinto[exitRow][exitCol] = EXIT_CHAR;
    }
    
    public void spreadPlayers(ArrayList<Player> players, boolean modoDebug) {
        if (!modoDebug){   
            for (Player p : players){
                int pos[] = randomEmptyPos();

                int oldRow = -1;
                int oldCol = -1;
                putPlayer2D(oldRow, oldCol, pos[ROW], pos[COL], p);
            }
        }
        else {
            Player p = players.get(0);
            this.putPlayer2D(-1, -1, 0, 0, p);
        }
    }
    
    public boolean haveAWinner() {
        return laberinto[this.exitRow][this.exitCol] != EXIT_CHAR;
    }
    
    @Override
    public String toString() {
        String laux = "Tablero: \n";
        
        for (int i = 0; i < this.nRows; i++){
            for (int j = 0; j < this.nCols; j++){
                laux += laberinto[i][j] + "   ";
            }
            
            laux += "\n";
        }
        
        return laux;
    }
    
    public void addMonster(int row, int col, Monster monster) {
        if (posOk(row, col) && emptyPos(row, col)){
            laberinto[row][col] = MONSTER_CHAR;
            this.monsters[row][col] = monster;
        }
    }
    
    public Monster putPlayer(Directions direction, Player player) {
        int oldRow = player.getRow();
        int oldCol = player.getCol();
        
        int newPos[] = dir2Pos(oldRow, oldCol, direction);
        Monster monster = putPlayer2D(oldRow, oldCol, newPos[ROW], newPos[COL], player);
        
        return monster;
    }
    
    public void addBlock(Orientation orientation, int startRow, int startCol, int length) {
        int incRow;
        int incCol;
        int row;
        int col;
        
        if (orientation == Orientation.VERTICAL){
            incRow = 1;
            incCol = 0;
        }
        else {
            incRow = 0;
            incCol = 1;
        }
        
        row = startRow;
        col = startCol;
        
        while (posOk(row, col) && emptyPos(row, col) && length > 0){
            laberinto[row][col] = BLOCK_CHAR;
            length -= 1;
            row += incRow;
            col += incCol;
        }
    }
    
    public ArrayList<Directions> validMoves(int row, int col) {
        ArrayList<Directions> output = new ArrayList<>();
        
        if (canStepOn(row+1, col))
            output.add(Directions.DOWN);
        if (canStepOn(row-1, col))
            output.add(Directions.UP);
        if (canStepOn(row, col+1))
            output.add(Directions.RIGHT);
        if (canStepOn(row, col-1))
            output.add(Directions.LEFT);
                    
        return output;
    }
    
    public void colocaFuzzyPlayer(FuzzyPlayer fuzzy, int row, int col){
        players[row][col] = fuzzy;
    }
        
    private boolean posOk(int row, int col) {
        return 0 <= row && row < this.nRows && 0 <= col && col < this.nCols;
    } 
    
    private boolean emptyPos(int row, int col) {
        return laberinto[row][col] == EMPTY_CHAR;
    }
    
    private boolean monsterPos(int row, int col) {
        return laberinto[row][col] == MONSTER_CHAR;
    }
    
    private boolean exitPos(int row, int col) {
        return laberinto[row][col] == EXIT_CHAR;
    }
    
    private boolean combatPos(int row, int col) {
        return laberinto[row][col] == COMBAT_CHAR;
    }
    
    private boolean canStepOn(int row, int col) {
        return posOk(row, col) && (emptyPos(row, col) || monsterPos(row, col) || exitPos(row, col));
    }
    
    private void updateOldPos(int row, int col) {
        if (posOk(row, col)){
            if (laberinto[row][col] == COMBAT_CHAR)
                laberinto[row][col] = MONSTER_CHAR;
            else
                laberinto[row][col] = EMPTY_CHAR;
        }
    }
    
    private int[] dir2Pos(int row, int col, Directions direction) {
        int[] pos = {row, col}; //creamos una variable auxiliar con nuestra posició
        
        switch (direction) {
            case UP:
                pos[ROW]--;
                break;
            case DOWN:
                pos[ROW]++;
                break;
            case RIGHT:
                pos[COL]++;
                break;
            case LEFT:
                pos[COL]--;
                break;
        }
        
        return pos;
    }
    
    public int[] randomEmptyPos() {
        int[] pos = {-1, -1};
        
        do {
            pos[ROW] = Dice.randomPos(nRows);
            pos[COL] = Dice.randomPos(nCols);
        }while (!emptyPos(pos[ROW], pos[COL]));
        
        return pos;
    }
    
    private Monster putPlayer2D(int oldRow, int oldCol, int row, int col, Player player) {
        Monster output = null;
        
        if (canStepOn(row, col)){
            if (posOk(oldRow, oldCol)){
                Player p = players[oldRow][oldCol];
                
                if (p == player){
                    updateOldPos(oldRow, oldCol);
                    players[oldRow][oldCol] = null;
                }
            }
            
            if (monsterPos(row, col)){
                laberinto[row][col] = COMBAT_CHAR;
                output = monsters[row][col];
            }
            else {
                char number = player.getNumber();
                laberinto[row][col] = number;               
            }
            
            players[row][col] = player;
            player.setPos(row, col);
        }
        
        return output;
    }
}
