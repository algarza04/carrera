# frozen_string_literal: true

require_relative 'monstruos/monstruo'
require_relative 'monstruos/enum_monstruos'

class T1S1
  include EnumMonstruos
  mons = Monstruo.new("pepe",ORCO )
  mons.mostrar_info
end
