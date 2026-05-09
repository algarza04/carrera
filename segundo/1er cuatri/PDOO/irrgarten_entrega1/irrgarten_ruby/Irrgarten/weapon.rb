# frozen_string_literal: true
require_relative 'dice'

class Weapon
  def initialize(power, uses)
    @power = power
    @uses = uses

  end

  def attack
    if @uses > 0
      @uses = @uses-1
      @power
    else
      0.to_f
    end
  end

  def to_s
    "W[#{@power}, #{@uses}]"
  end

  def inspect
    to_s
  end

  def discard
    Dice.discard_element(@uses)
  end
end
