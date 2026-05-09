# frozen_string_literal: true
require_relative 'player'
require_relative 'dice'

class FuzzyPlayer < Player
  def initialize(other)
    super(other.number, other.intelligence, other.strength)
    set_pos(other.row, other.col)
  end

  def move(direction, valid_moves)
    size = valid_moves.size
    contained = valid_moves.include?(direction)

    if size == 0 || !contained
      preference = valid_moves[0]
    else
      preference = direction
    end

    Dice.next_step(preference, valid_moves, @intelligence)
  end

  def attack
    Dice.intensity(@strength) + super.attack
  end

  def defensive_energy
    Dice.intensity(@intelligence ) + super.defensive_energy
  end

  def to_s
    "Fuzzy: #{super.to_s}"
  end
  protected :defensive_energy
end
