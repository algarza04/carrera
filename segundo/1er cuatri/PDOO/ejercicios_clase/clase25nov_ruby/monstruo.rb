# frozen_string_literal: true
require_relative 'personaje'

class Monstruo < Personaje
  def initialize(nombre, vida)
    super(nombre, vida)
    @tipo = @@TIPO_MONSTRUO
  end

  def atacar
    puts "#{@nombre} esta atacando con las garras"
  end

  def defender
    puts "#{@nombre} se esta defendiendo con su pie"
  end
end
