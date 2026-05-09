# frozen_string_literal: true
require_relative 'dice'
require_relative 'labyrinth_character'

class Monster < LabyrinthCharacter
  @@INITIAL_HEALTH = 5

  def initialize(name, intelligence, strength)
    super(name, intelligence, strength, @@INITIAL_HEALTH)
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
    "[#{super.to_s} ]\n"
  end

  def inspect
    to_s
  end
end
