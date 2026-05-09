# frozen_string_literal: true
require_relative 'enum_monstruos'

class Monstruo
  include EnumMonstruos

  @@MAX_MONSTRUOS = 10
  @@generator = Random.new
  @@lista_monstruos = []

  def initialize(nombre, tipo)
    @nombre = nombre
    @tipo = tipo
  end

  attr_reader :nombre

  def mostrar_info
    puts "Nombre monstruo: #{@nombre}, tipo: #{@tipo}"
  end

  def self.add_random_monstruo
    if @@lista_monstruos.size < @@MAX_MONSTRUOS
      aux = @@generator.rand(3)
      tipo_monst = [ORCO, ESQUELETO, DRAGON]
      m = Monstruo.new("Monstruo#{@@lista_monstruos.size+1}", tipo_monst[aux])
      @@lista_monstruos.push(m)
    else
      puts "No se pueden añadir más de 10"
    end
  end

  def self.get_elementos
    @@lista_monstruos
  end

  protected_methods :add_random_monstruo
end
