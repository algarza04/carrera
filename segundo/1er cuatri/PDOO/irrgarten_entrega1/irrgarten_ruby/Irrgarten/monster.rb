# frozen_string_literal: true
require_relative 'dice'

class Monster
  @@INITIAL_HEALTH = 5

  def initialize(name, intelligence, strength)
    @name = name
    @intelligence = intelligence
    @strength = strength
    @health = @@INITIAL_HEALTH
    @row = -1
    @col = -1
  end

  def dead
    true if @health == 0
  end

  def attack
    Dice.intensity(@strength)
  end

  def defend(received_attack)
    is_dead = dead

    unless is_dead
      defensive_energy = Dice.intensity(@intelligence)

      if defensive_energy < received_attack
        got_wounded
        is_dead = dead
      end
    end

    is_dead
  end

  def to_s
    "[Nombre: #{@name}, intelligence: #{@intelligence}, strength: #{@strength}, health: #{@health}, row: #{@row}, col: #{@col} ]\n"
  end

  def inspect
    to_s
  end
  
  def got_wounded
    @health -= 1
  end

  def set_pos(row, col)
    @row = row
    @col = col
  end
end
