# frozen_string_literal: true
require_relative 'monstruos/monstruo'
require_relative 'monstruos/s'

class T1S2
  Monstruo.add_random_monstruo
  Monstruo.add_random_monstruo
  Monstruo.add_random_monstruo
  Monstruo.add_random_monstruo
  Monstruo.add_random_monstruo
  Monstruo.add_random_monstruo
  Monstruo.add_random_monstruo


  ut = Utils.new
  mons = ut.buscar_monstruo("Monstruo5")
  mons.mostrar_info

end