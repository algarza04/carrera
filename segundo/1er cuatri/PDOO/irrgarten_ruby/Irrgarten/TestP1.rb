# frozen_string_literal: true
require_relative 'weapon'
require_relative 'shield'
require_relative 'orientation'
require_relative 'game_state'
require_relative 'dice'
require_relative 'game_character'
require_relative 'directions'

class TestP1
  arma1=Weapon.new(Dice.weapon_power, 5)
  arma2=Weapon.new(1.3, Dice.uses_left)
  arma3=Weapon.new(6.2, 6)
  puts arma1.attack
  puts arma1.to_s
  puts "\n\n"
  escudo1=Shield.new(Dice.shield_power, 1)
  puts escudo1.protect


  escudo2=Shield.new(4.2, 2)
  puts escudo2.to_s
  escudo3=Shield.new(5.2, 3)
  puts "\n\n"
  jugada=GameState.new("pachuru", "paquirrin", "el feo", 1, false, "ronda 1")
  puts jugada.labyrinth
  puts jugada.players
  puts jugada.monsters
  puts jugada.current_player
  puts jugada.log

  100.times do |i|
    puts Dice.resurrect_player
    puts Dice.intensity(i)
    puts Dice.uses_left
    puts Dice.shields_reward
    puts Dice.who_starts(3)
    puts Dice.random_pos(i+1)
    puts Dice.health_reward
    puts Dice.weapon_power
    puts Dice.weapons_reward
    puts Dice.random_strength
    puts Dice.shield_power
    puts Dice.random_intelligence
    puts "\n\n"

  end

end