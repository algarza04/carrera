# frozen_string_literal: true

require_relative 'jugador'
require_relative 'mago'
require_relative 'personaje'

class Jugador
  personajes = Array.new

  personaje = Personaje.new("personaje", 10)
  jugador = Jugador.new("jugador", 5, 2)
  mago = Mago.new("mago", 3, 1, "fuego")

  personajes.push(personaje)
  personajes.push(jugador)
  personajes.push(mago)

  for i in 0...personajes.size
    personajes.at(i).atacar
  end

end