# frozen_string_literal: true
require_relative 'dice'
require_relative 'combat_element'

class Shield < CombatElement
  def initialize(protection, uses)
    super(protection, uses)
  end

  def protect
    produce_effect
  end

  def to_s
    "S[#{super.to_s}]"
  end

  def inspect
    to_s
  end
end
