require_relative 'controlador/controlador'
require_relative 'modelo/usuario'
require_relative 'modelo/contacto'
require_relative 'vista/vista'

def flujoApp(controlador)
  # Flujo de la aplicación
  controlador.mostrar_perfil
  controlador.actualizar_perfil
  controlador.actualizar_informacion_contacto
end


# Inicialización de MVC
contacto = Modelo::Contacto.new("calle", "manu@correo", "955555555")
usuario = Modelo::Usuario.new("Manu","Perez", contacto)
vista = Vista::VistaPerfilUsuario.new
controlador = Controlador::ControladorPerfilUsuario.new(usuario, vista)

# llamada a la función flujoApp
flujoApp(controlador)


