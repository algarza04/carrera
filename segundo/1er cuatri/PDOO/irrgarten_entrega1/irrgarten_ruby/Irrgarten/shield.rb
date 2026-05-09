# frozen_string_literal: true
require_relative 'dice'

class Shield
  def initialize(protection, uses)
    @protection = protection
    @uses = uses
  end

  def protect
    if @uses > 0
      @uses = @uses-1
      @protection
    else
      0.to_f
    end
  end

  def to_s
    "S[#{@protection}, #{@uses}]"
  end

  def inspect
    to_s
  end

  def discard
    Dice.discard_element(@uses)
  end
end
