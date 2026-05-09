# frozen_string_literal: true
require_relative 'player'
require_relative 'game_character'
require_relative 'game_state'
require_relative 'monster'
require_relative 'labyrinth'
require_relative 'fuzzy_player'
class Game
  @@MAX_ROUNDS = 10

  def initialize(nplayers, modo_debug)
    @log = ""
    @monsters = Array.new
    @players = Array.new

    if !modo_debug
      for i in 0...nplayers do
        p = Player.new(i, Dice.random_intelligence, Dice.random_strength)
        @players.push(p)
      end

      @current_player_index = Dice.who_starts(nplayers)
      @curren_player = @players[@current_player_index]
      @laberinto = Labyrinth.new(5,5,2,3)
      configure_labyrinth
      @laberinto.spread_players(@players, modo_debug)

    else
      @current_player_index = 0
      aux = Player.new('0', Dice.random_intelligence, Dice.random_strength)
      @players.push(aux)
      configure_labyrinth_debug
      @laberinto.spread_players(@players, modo_debug)
      @curren_player = @players[@current_player_index]
    end
  end

  def finished
    true if @laberinto.have_a_winner
  end

  def next_step(preferred_direction)
    @log = ""
    dead = @curren_player.dead

    unless dead
      direction = actual_direction(preferred_direction)

      if direction != preferred_direction
        log_player_no_orders
      end

      monster = @laberinto.put_player(direction, @curren_player)

      if monster == nil
        log_no_monster
      else
        unless monster.dead
          winner = combat(monster)
          manage_reward(winner)
        end
      end
    else
      manage_resurrection
    end

    end_game = finished

    unless end_game
      next_player
    end

    end_game
  end

  def get_game_state
    GameState.new(@laberinto.to_s, @curren_player.to_s, @monsters.inspect, @current_player_index, @laberinto.have_a_winner, @log)
  end

  def configure_labyrinth
    num_muros = 5
    length = 2

    for i in 0...num_muros do
      pos = @laberinto.random_empty_pos
      fil_muro = pos[0]
      col_muro = pos[1]
      @laberinto.add_block(Orientation::HORIZONTAL, fil_muro, col_muro, length)
    end

    #----------------------
    num_mons = 5

    for i in 0...num_mons do
      pos = @laberinto.random_empty_pos
      fil_mons = pos[0]
      col_mons = pos[1]

      monster = Monster.new("Monster", Dice.random_intelligence, Dice.random_strength)
      @laberinto.add_monster(fil_mons,col_mons, monster)
      monster.set_pos(fil_mons,col_mons)
      @monsters.push(monster)
    end
  end

  def configure_labyrinth_debug
    n_rows = 3
    n_cols = 3

    @laberinto = Labyrinth.new(n_rows,n_cols,2,2)

    monster = Monster.new("Monster", Dice.random_intelligence, Dice.random_strength)
    @laberinto.add_monster(1, 0, monster)
    monster.set_pos(1,0)
    @monsters.push(monster)
  end

  def next_player
    if @current_player_index == @players.size-1
      @current_player_index = 0
    else
      @current_player_index += 1
    end

    @curren_player = @players[@current_player_index]
  end

  def actual_direction(preferred_direction)
    current_row = @curren_player.row
    current_col = @curren_player.col

    @curren_player.move(preferred_direction, @laberinto.valid_moves(current_row, current_col))
  end

  def combat(monster)
    rounds = 0
    winner = GameCharacter::PLAYER

    player_attack = @curren_player.attack
    lose = monster.defend(player_attack)

    while !lose && rounds < @@MAX_ROUNDS
      winner = GameCharacter::MONSTER
      rounds += 1

      monster_attack = monster.attack
      lose = @curren_player.defend(monster_attack)

      unless lose
        player_attack = @curren_player.attack
        winner = GameCharacter::PLAYER
        lose = monster.defend(player_attack)
      end
    end

    log_rounds(rounds, @@MAX_ROUNDS)

    if winner == GameCharacter::MONSTER
      log_monster_won
    else
      log_player_won
    end

    winner
  end

  def manage_reward(winner)
    if winner == GameCharacter::PLAYER
      @curren_player.receive_reward
    end
  end

  def manage_resurrection
    resurrect = Dice.resurrect_player

    if resurrect
      @curren_player.resurrect
      fuzzy = FuzzyPlayer.new(@curren_player)
      @players[@current_player_index] = fuzzy
      @laberinto.coloca_fuzzy_player(fuzzy, fuzzy.row, fuzzy.col)
      log_resurrected
    else
      log_player_skip_turn
    end
  end

  def log_player_won
    @log += "El jugador ha ganado el combate. \n"
  end

  def log_monster_won
    @log += "El monstruo ha ganado el combate. \n"
  end

  def log_resurrected
    @log += "El jugador ha resucitado. \n"
  end

  def log_player_skip_turn
    @log += "El jugador ha perdido el turno por estar muerto. \n";
  end

  def log_player_no_orders
    @log += "El jugador no ha seguido las instrucciones del jugador humano. \n"
  end

  def log_no_monster
    @log += "El jugador se ha movido a una celda vacía"
  end

  def log_rounds(rounds, max)
    @log += "Se han producido #{rounds} de #{max} rondas de combate. \n"
  end

  private :configure_labyrinth, :next_player, :actual_direction, :combat, :manage_reward, :manage_resurrection, :log_player_won, :log_monster_won, :log_resurrected, :log_player_skip_turn, :log_player_no_orders, :log_no_monster, :log_rounds
end
