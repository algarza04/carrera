# frozen_string_literal: true

class LabyrinthCharacter
  def initialize(name, intelligence, strength, health)
    @name = name
    @intelligence = intelligence
    @strength = strength
    @health = health
    @row = 0
    @col = 0
  end

  def self.copy(other)
    new(other.name, other.intelligence, other.strength, other.health, other.row, other.col)
  end

  def dead
    true if @health == 0
  end

  def to_s
    "[#{@name}, inteligencia: #{@intelligence}, fuerza: #{@strength}, vida: #{@health}, fila: #{@row}, columna: #{@col}"
  end

  def got_wounded
    @health -= 1
  end

  attr_accessor :health
  attr_reader :intelligence, :strength, :row, :col
  protected :got_wounded

  def set_pos(row, col)
    @row = row
    @col = col
  end

  def attack
    raise "Metodo abstracto"
  end

  def defend(attack)
    raise "Metodo abstracto"
  end
end
