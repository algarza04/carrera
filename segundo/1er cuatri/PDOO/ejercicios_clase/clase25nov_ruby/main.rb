# frozen_string_literal: true
require_relative 'monstruo'
require_relative 'jugador'

class Principal
  j = Jugador.new("caballero", 10)
  j.atacar
  j.defender
  puts j.tipo

  m = Monstruo.new("monstruo", 10)
  m.atacar
  m.defender
  puts m.tipo
end
