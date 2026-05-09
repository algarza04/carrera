# frozen_string_literal: true

class Personaje
  def initialize(nombre, salud)
    @nombre = nombre
    @salud = salud
  end

  def atacar
    puts  "#{@nombre} va a atacar"
  end

  def recibir(danio)
    @salud -= danio
  end
end
