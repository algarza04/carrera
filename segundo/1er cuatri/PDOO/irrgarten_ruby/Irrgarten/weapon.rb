# frozen_string_literal: true
require_relative 'dice'
require_relative 'combat_element'

class Weapon < CombatElement

  def initialize(power, uses)
    super(power, uses)
  end

  def attack
    produce_effect
  end

  def to_s
    "W[#{super.to_s}]"
  end

  def inspect
    to_s
  end
end
