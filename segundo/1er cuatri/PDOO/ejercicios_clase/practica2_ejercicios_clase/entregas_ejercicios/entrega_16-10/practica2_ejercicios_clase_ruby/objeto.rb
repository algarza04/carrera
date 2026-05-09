# frozen_string_literal: true

class Objeto
  def initialize(nombre, tipo, ataque, defensa)
    @nombre = nombre
    @tipo = tipo
    @ataque = ataque
    @defensa = defensa
  end

  def to_s
    "Objeto #{@nombre}, tipo: #{@tipo}, ataque: #{@ataque}, defensa : #{@defensa})"
  end
end
