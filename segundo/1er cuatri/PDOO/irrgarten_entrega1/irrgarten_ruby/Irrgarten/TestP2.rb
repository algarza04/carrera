# frozen_string_literal: true
require_relative 'monster'
require_relative 'dice'
require_relative 'player'
require_relative 'labyrinth'

class TestP2
  puts "----------Monster-----------"
  m = Monster.new("p", 2, 5)

  m.set_pos(1,2)
  if m.dead == true
    puts "Estoy muerto"
  else
    puts "Estoy vivo"
  end

  puts m.attack
  puts m.to_s
  m.got_wounded
  puts m.to_s


  puts "----------Player-----------"
  p = Player.new("1", Dice.random_intelligence, Dice.random_strength)
  puts p.to_s
  puts p.attack
  if p.dead == true
    puts "Estoy muerto"
  else
    puts "Estoy vivo"
  end

  begin
    p.resurrect
  end while p.dead == true

  puts p.to_s

  puts "----------Labyrinth-----------"
  l = Labyrinth.new(3,3,2,2)
  puts l.to_s
  puts "Añado el monstruo m :"
  l.add_monster(1,1,m)
  puts l.to_s
  pos = Array.new

  for i in 0...20 do
    pos = l.random_empty_pos
    puts "\n pos: #{pos[0]}, #{pos[1]} \n"
  end
end