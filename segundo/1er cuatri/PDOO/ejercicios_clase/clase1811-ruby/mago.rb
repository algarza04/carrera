# frozen_string_literal: true
require_relative 'jugador'

class Mago < Jugador
  def initialize(nombre, vida, nivel, hechizo)
    super(nombre, vida, nivel)
    @hechizo = hechizo
  end

  def aprender(nuevo_hechizo)
    @hechizo = nuevo_hechizo
  end

  def atacar
    super
    puts "con el hecho #{@hechizo} "
  end
end
