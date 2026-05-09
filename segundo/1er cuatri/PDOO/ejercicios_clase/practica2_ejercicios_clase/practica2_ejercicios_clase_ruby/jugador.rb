# frozen_string_literal: true

class Jugador
  def initialize(nombre, nivel, vida, inventario)
    @nombre = nombre
    @nivel = nivel
    @vida = vida
    @inventario = inventario
  end

  attr_accessor :nombre, :nivel, :vida

  def to_s
    "Nombre: #{@nombre}, Nivel: #{@nivel}, Vida: #{@vida}, \nInventario: #{@inventario}"
  end
end
