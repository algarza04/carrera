# frozen_string_literal: true
require_relative '../UI/textUI'
require_relative '../Controller/controller'
require_relative '../Irrgarten/game'

class Main
  puts "Selecciona el numero de jugadores: "
  nplayers = gets
  nplayers = nplayers.to_i

  game = Game.new(nplayers, false)
  view = UI::TextUI.new

  controlador = Control::Controller.new(game, view)

  controlador.play
end
