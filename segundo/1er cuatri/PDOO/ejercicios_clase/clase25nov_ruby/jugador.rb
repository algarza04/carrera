# frozen_string_literal: true
require_relative 'personaje'

class Jugador < Personaje
  def initialize(nombre, vida)
    super(nombre, vida)
    @tipo = @@TIPO_JUGADOR
  end

  def atacar
    puts "#{@nombre} esta atacando con la espada"
  end

  def defender
    puts "#{@nombre} se esta defendiendo con su escudo"
  end
end
