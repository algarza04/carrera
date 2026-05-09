# frozen_string_literal: true

class Dice
  @@MAX_USES = 5
  @@MAX_INTELLIGENCE = 10.to_f
  @@MAX_STRENGTH = 10.to_f
  @@RESURRECT_PROB = 0.3.to_f
  @@WEAPONS_REWARD = 2
  @@SHIELDS_REWARD = 3
  @@HEALTH_REWARD = 5
  @@MAX_ATTACK = 3
  @@MAX_SHIELD = 2

  @@generator = Random.new

  def self.random_pos(max)
    @@generator.rand(max)
  end

  def self.who_starts(nplayers)   #nplayers int
    @@generator.rand(nplayers)
  end

  def self.random_intelligence
    @@generator.rand * @@MAX_INTELLIGENCE
  end

  def self.random_strength
    @@generator.rand * @@MAX_STRENGTH
  end

  def self.resurrect_player
    @@generator.rand < @@RESURRECT_PROB
  end

  def self.weapons_reward
    @@generator.rand(@@WEAPONS_REWARD+1)
  end

  def self.shields_reward
    @@generator.rand(@@SHIELDS_REWARD+1)
  end

  def self.health_reward
    @@generator.rand(@@HEALTH_REWARD+1)
  end

  def self.weapon_power
    @@generator.rand * @@MAX_ATTACK
  end

  def self.shield_power
    @@generator.rand * @@MAX_SHIELD
  end

  def self.uses_left
    @@generator.rand(@@MAX_USES+1)
  end

  def self.intensity(competence)  #competence float
    @@generator.rand * competence
  end

  def self.discard_element(uses_left) #uses left int
    @@generator.rand >= uses_left.to_f/@@MAX_USES.to_f
  end

  def self.next_step(preference, validMoves, intelligence)
    if @@generator.rand * @@MAX_INTELLIGENCE < intelligence
      preference
    else
      validMoves[@@generator.rand(validMoves.size)]
    end
  end
end
