# frozen_string_literal: true
require_relative '../monstruos/monstruo'
class Utils
  def buscar_monstruo(nombre)
    elementos = Monstruo.get_elementos

    for i in 0..elementos.size-1
      if elementos[i].nombre == nombre
        puts "Hemos encontradas #{nombre}"
        return elementos[i]
      end
    end

      puts "No esta en la lista"
      null
  end

  def self.add_random_monstruo()
    Monstruo.add_random_monstruo
  end

end
