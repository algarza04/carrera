# frozen_string_literal: true

class Inventario
  def initialize(id, capacidad)
    @id = id
    @capacidad = capacidad
    @objetos = Array.new
  end

  def to_s
    "Inventario ID: #{@id}, Capacidad: #{@capacidad} \n Objetos: #{@objetos}"
  end

  def add_objeto(obj)
    if @objetos.size < @capacidad
      @objetos.push(obj)
    else
      puts "lleno"
    end
  end

  def quitar_objeto(obj)
    @objetos.delete(obj)
  end
end
