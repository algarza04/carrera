# frozen_string_literal: true

class SerVivo
  def initialize(nombre, vida)
    @nombre = nombre
    @vida = vida
  end

  attr_reader :nombre, :vida
end
