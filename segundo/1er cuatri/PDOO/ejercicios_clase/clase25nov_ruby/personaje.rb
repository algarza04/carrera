# frozen_string_literal: true
require_relative 'ser_vivo'

class Personaje < SerVivo
  @@TIPO_MONSTRUO = "MONSTRUO"
  @@TIPO_JUGADOR = "JUGADOR"

  def initialize(nombre, vida)
    super(nombre, vida)
    @tipo
  end

  attr_reader :tipo

  def atacar
    raise "Metodo abstracto"

  end

  def defender
    raise "Metodo abstracto"
  end
end
