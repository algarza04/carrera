# frozen_string_literal: true
require_relative 'orientation'
require_relative 'directions'
require_relative 'dice'

class Labyrinth
  @@BLOCK_CHAR = 'X'
  @@EMPTY_CHAR = '-'
  @@MONSTER_CHAR = 'M'
  @@COMBAT_CHAR = 'C'
  @@EXIT_CHAR = 'E'
  @@ROW = 0
  @@COL = 1

  def initialize(n_rows, n_cols, exit_row, exit_col)
    @n_rows = n_rows
    @n_cols = n_cols
    @exit_row = exit_row
    @exit_col = exit_col

    @monsters = Array.new(@n_rows) { Array.new(@n_cols) } #Array.new(n_cols, 0) daria un valor 0 a tpdas las casillas
    @players = Array.new(@n_rows) { Array.new(@n_cols) }
    @laberinto = Array.new(@n_rows) { Array.new(@n_cols, @@EMPTY_CHAR) }
    @laberinto[@exit_row][@exit_col] = @@EXIT_CHAR
  end

  def spread_players(players, modo_debug)
    unless modo_debug
      for p in players
        pos = random_empty_pos

        old_row = -1
        old_col = -1
        put_player2d(old_row, old_col, pos[@@ROW], pos[@@COL], p)
      end
    end
    if modo_debug
      p = players[0]
      put_player2d(-1, -1, 0, 0, p)
    end
  end

  def have_a_winner
    true if @laberinto[@exit_row][@exit_col] != @@EXIT_CHAR
  end

  def to_s
    laux = "Tablero: \n"

    for i in 0..@n_rows-1 #si solo pones .. incluye el límite
      for j in 0..@n_cols-1
        laux += "#{@laberinto[i][j]}   "
      end

      laux += "\n"
    end

    laux
  end

  def add_monster(row, col, monster)
    if pos_ok(row, col) && empty_pos(row, col)
      @laberinto[row][col] = @@MONSTER_CHAR
      @monsters[row][col] = monster
    end
  end

  def put_player(direction, player)
    old_row = player.row
    old_col = player.col

    new_pos = dir2pos(old_row, old_col, direction)
    monster = put_player2d(old_row, old_col, new_pos[@@ROW], new_pos[@@COL], player)
    monster
  end

  def coloca_fuzzy_player(fuzzy, row, col)
    @players[row][col] = fuzzy
  end

  def add_block(orientation, start_row, start_col, length)
    if orientation == Orientation::VERTICAL
      inc_row = 1
      inc_col = 0
    else
      inc_row = 0
      inc_col = 1
    end

    row = start_row
    col = start_col

    while pos_ok(row, col) && empty_pos(row, col) && length > 0
      @laberinto[row][col] = @@BLOCK_CHAR
      length -= 1
      row += inc_row
      col += inc_col
    end
  end

  def valid_moves(row, col)
    output = Array.new

    if can_step_on(row+1, col)
      output.push(Directions::DOWN)
    end
    if can_step_on(row-1, col)
      output.push(Directions::UP)
    end
    if can_step_on(row, col+1)
      output.push(Directions::RIGHT)
    end
    if can_step_on(row, col-1)
      output.push(Directions::LEFT)
    end

    output
  end

  def pos_ok(row, col)
    true if 0 <= row && row < @n_rows && 0 <= col && col < @n_cols
  end

  def empty_pos(row, col)
    true if @laberinto[row][col] == @@EMPTY_CHAR
  end

  def monster_pos(row, col)
    true if @laberinto[row][col] == @@MONSTER_CHAR
  end

  def exit_pos(row, col)
    true if @laberinto[row][col] == @@EXIT_CHAR
  end

  def combat_pos(row, col)
    true if @laberinto[row][col] == @@COMBAT_CHAR
  end

  def can_step_on(row, col)
    true if pos_ok(row, col) && (empty_pos(row, col) || monster_pos(row, col) || exit_pos(row, col))
  end

  def update_old_pos(row, col)
    if pos_ok(row, col)
      if @laberinto[row][col] == @@COMBAT_CHAR
        @laberinto[row][col] = @@MONSTER_CHAR
      else
        @laberinto[row][col] = @@EMPTY_CHAR
      end
    end
  end

  def dir2pos(row, col, direction)
    pos = [row, col]

    case direction
    when Directions::UP
      pos[@@ROW] -= 1
    when Directions::DOWN
      pos[@@ROW] += 1
    when Directions::RIGHT
      pos[@@COL] += 1
    when Directions::LEFT
      pos[@@COL] -= 1
    end

    pos
  end

  def random_empty_pos
    pos = [-1, -1]

    begin
      pos[@@ROW] = Dice.random_pos(@n_rows)
      pos[@@COL] = Dice.random_pos(@n_cols)
    end while !empty_pos(pos[@@ROW], pos[@@COL])

    pos
  end

  def put_player2d(old_row, old_col, row, col, player)
    output = nil

    if can_step_on(row, col)
      if pos_ok(old_row, old_col)
        p = @players[old_row][old_col]

        if p == player
          update_old_pos(old_row, old_col)
          @players[old_row][old_col] = nil
        end
      end

      if monster_pos(row, col)
        @laberinto[row][col] = @@COMBAT_CHAR
        output = @monsters[row][col]
      else
        number = player.number
        @laberinto[row][col] = number
      end

      @players[row][col] = player
      player.set_pos(row, col)
    end

    output
  end

  private :pos_ok, :empty_pos, :monster_pos, :exit_pos, :combat_pos, :can_step_on, :update_old_pos, :dir2pos, :put_player2d

end
