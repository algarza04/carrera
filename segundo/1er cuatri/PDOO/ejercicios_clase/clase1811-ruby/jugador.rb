# frozen_string_literal: true
require_relative 'personaje'

class Jugador < Personaje
  def initialize(nombre, salud, nivel)
    super(nombre, salud)
    @nivel = nivel
  end

  def subir_nivel
    @nivel += 1
  end

  def atacar
    super
    puts " con el nivel #{@nivel}"
  end

end
