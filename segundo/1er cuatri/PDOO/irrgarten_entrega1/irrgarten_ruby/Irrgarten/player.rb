# frozen_string_literal: true
require_relative 'weapon'
require_relative 'shield'
require_relative 'directions'
require_relative 'dice'

class Player
  @@MAX_WEAPONS = 2
  @@MAX_SHIELDS = 3
  @@INITIAL_HEALTH = 10
  @@HITS2LOSE = 3

  def initialize(number, intelligence, strength)
    @number = number
    @name = "Player##{@number}"
    @intelligence = intelligence
    @strength = strength
    @health = @@INITIAL_HEALTH
    @row = -1
    @col = -1
    @consecutive_hits = 0
    @weapons = Array.new
    @shields = Array.new
  end

  attr_reader :number, :row, :col

  def resurrect
    @shields = Array.new
    @weapons = Array.new
    @health = @@INITIAL_HEALTH
    @consecutive_hits = 0
  end

  def dead
    true if @health == 0
  end

  def move(direction, valid_moves)
    size = valid_moves.size
    contained = valid_moves.include?(direction)

    if size > 0 && !contained
      first_element = valid_moves[0]
      first_element
    else
      direction
    end
  end

  def attack
    (@strength+sum_weapons).to_f
  end

  def set_pos(row, col)
    @row = row
    @col = col
  end

  def defend(received_attack)
    manage_hit(received_attack)
  end

  def receive_reward
    w_reward = Dice.weapons_reward
    s_reward = Dice.shields_reward

    (1..w_reward).each do
      wnew = new_weapon
      receive_weapon(wnew)
    end

    (1..s_reward).each do
      snew = new_shield
      receive_shield(snew)
    end

    extra_health = Dice.health_reward

    @health += extra_health
  end

  def to_s
    "[#{@name}, inteligencia: #{@intelligence}, fuerza: #{@strength}, vida: #{@health}, fila: #{@row}, columna: #{@col} \n armas: #{@weapons.to_s}, shields: #{@shields.to_s}]"
  end

  def receive_weapon(w)
    @weapons.delete_if {|i| i.discard}

    size = @weapons.size

    if size < @@MAX_WEAPONS
      @weapons.push(w)
    end
  end

  def receive_shield(s)
    @shields.delete_if {|i| i.discard}

    size = @shields.size

    if size < @@MAX_SHIELDS
      @shields.push(s)
    end
  end

  def new_weapon
    Weapon.new(Dice.weapon_power, Dice.uses_left)
  end

  def new_shield
    Shield.new(Dice.shield_power, Dice.uses_left)
  end

  def sum_weapons
    sum = 0.to_f

    for w in @weapons
      sum += w.attack
    end

    sum
  end

  def sum_shields
    sum = 0.to_f

    for s in @shields
      sum += s.protect
    end

    sum
  end

  def defensive_energy
    @intelligence + sum_shields
  end

  def manage_hit(received_attack)
    defense = defensive_energy

    if defense < received_attack
      got_wounded
      inc_consecutive_hits
    else
      reset_hits
    end

    if @consecutive_hits == @@HITS2LOSE || dead
      reset_hits
      lose = true
    else
      lose = false
    end

    lose
  end

  def reset_hits
    @consecutive_hits = 0
  end

  def got_wounded
    @health -= 1
  end

  def inc_consecutive_hits
    @consecutive_hits += 1
  end

  private :receive_weapon, :receive_shield,:new_weapon, :new_shield, :sum_weapons, :sum_shields, :defensive_energy, :manage_hit, :reset_hits, :got_wounded, :inc_consecutive_hits
end
