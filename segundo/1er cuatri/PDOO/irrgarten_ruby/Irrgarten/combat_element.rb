# frozen_string_literal: true
require_relative 'dice'

class CombatElement
  def initialize(effect, uses)
    @effect = effect
    @uses = uses
  end

  def produce_effect()
    if @uses > 0
      @uses-=1
      @effect
    else
      0
    end
  end

  def discard()
    Dice.discard_element(@uses)
  end

  def to_s
    "#{@effect}, #{@uses}"
  end

  protected :produce_effect
end
