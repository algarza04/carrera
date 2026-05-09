# frozen_string_literal: true
require_relative 'inventario'
require_relative 'jugador'
require_relative 'objeto'
require_relative 'tipo_objeto'

class Test
    inv1 = Inventario.new(1, 3)
    inv2 = Inventario.new(2, 2)

    jugador1 = Jugador.new("Manolo", 2, 5, inv1)
    jugador2 = Jugador.new("Jose", 3, 8, inv2)

    espada = Objeto.new("espada", TipoObjeto::ESPADA, 50, 0)
    casco = Objeto.new("casco", TipoObjeto::CASCO, 0, 20)
    escudo = Objeto.new("escudo", TipoObjeto::ESCUDO, 10, 40)

    inv1.add_objeto(escudo)
    inv1.add_objeto(espada)
    inv2.add_objeto(casco)
    inv2.add_objeto(espada)

    puts jugador1.to_s
    puts jugador2.to_s
end