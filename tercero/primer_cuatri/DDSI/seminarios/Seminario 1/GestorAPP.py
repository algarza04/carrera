from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.popup import Popup
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from datetime import datetime
import sys

from GestorBD import GestorDB
from kivy.uix.dropdown import DropDown

#------------------------------------------------------------------------------------
#                                   Ventanas
# -----------------------------------------------------------------------------------

# -------Gestor de ventanas--------
class WindowManager(ScreenManager):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.admin = GestorDB('{Oracle in instantclient_23_6}', 'oracle0.ugr.es', 'practbd', '1521', 'x5385032', 'x5385032')
        self.admin.connect() #Conexión a la base de datos
        self.Cpedido = int
    pass

# -------Menu--------
class Menu(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.tablas_creadas = False

    #Método enlazado al boton encargado de crear tablas en caso de que estás no existan y borrado en caso de que existan
    def administrar_tablas(self):
        if not self.tablas_creadas:
            self.manager.admin.CrearTablas()
            self.tablas_creadas = True
            self.ids.btn_administrar_tablas.text = "BORRAR TABLAS"
        else:
            self.manager.admin.BorrarTablas()
            self.tablas_creadas = False
            self.ids.btn_administrar_tablas.text = "CREAR TABLAS"

    #Método para cerrar la conexión y cerrar la aplicación
    def salir(self):
        self.manager.admin.close()
        sys.exit()

# -------Ventana para introducir los datos a ingresas en la tabla PEDIDO--------
class IniciarPedido(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.Cpedido = ""
        self.Ccliente = ""
        self.fecha = datetime.now()
        self.popup = None

    # ----------------------
    #Metodo encargado de insertar una fila en la ta
    #-----------------------------------------
    def solicitar_registro(self):
        if not self.Cpedido.isdigit() or not self.Ccliente.isdigit():
            advertencia = BoxLayout(orientation='vertical')
            error = Label(text="Solo se pueden introducir números")
            cerrar = Button(text="Cerrar")
            cerrar.bind(on_press=self.cerrar)
            advertencia.add_widget(error)
            advertencia.add_widget(cerrar)
            # Crear el Popup
            self.popup = Popup(title="Error",
                               content=advertencia,
                               size_hint=(None, None), size=(400, 200))
            self.popup.open()
        elif self.manager.admin.ObtenerUnPedido(self.Cpedido):
            advertencia = BoxLayout(orientation='vertical')
            error = Label(text="Ese codigo de pedido ya existe")
            cerrar = Button(text="Cerrar")
            cerrar.bind(on_press=self.cerrar)
            advertencia.add_widget(error)
            advertencia.add_widget(cerrar)
            # Crear el Popup
            self.popup = Popup(title="Error",
                               content=advertencia,
                               size_hint=(None, None), size=(400, 200)                              )
            self.popup.open()
        else:
            self.fecha = datetime.now()
            self.manager.admin.Insertar_Pedido(int(self.Cpedido), int(self.Ccliente), self.fecha)
            self.manager.current = 'Pedido'
            self.manager.admin.SavePoint("inicio")

    #-----------------------------------------
    #Metodo encargado de obtener el Ccliente ingresado en la interfaz
    #-----------------------------------------
    def obtener_Ccliente(self, instance):
        if instance.text.isdigit():
            self.Ccliente = instance.text
        else:
            advertencia = BoxLayout(orientation='vertical')
            error = Label(text="Solo se pueden introducir números")
            cerrar = Button(text="Cerrar")
            cerrar.bind(on_press=self.cerrar)
            advertencia.add_widget(error)
            advertencia.add_widget(cerrar)
            # Crear el Popup
            self.popup = Popup(title="Error",
                          content=advertencia,
                          size_hint=(None, None), size=(400, 200))
            self.popup.open()
            self.Ccliente = instance.text

    #-----------------------------------------
    #Metodo encargado de obtener el Cpedido ingresado en la interfaz
    #-----------------------------------------
    def obtener_Cpedido(self, instance):
        if instance.text.isdigit():
            self.Cpedido = instance.text
        else:
            advertencia = BoxLayout(orientation='vertical')
            error = Label(text="Solo se pueden introducir números")
            cerrar = Button(text="Cerrar")
            cerrar.bind(on_press=self.cerrar)
            advertencia.add_widget(error)
            advertencia.add_widget(cerrar)
            # Crear el Popup
            self.popup = Popup(title="Error",
                          content=advertencia,
                          size_hint=(None, None), size=(400, 200))
            self.popup.open()
            self.Cpedido = instance.text

    #-----------------------------------------
    #Getter de Cpedido
    #-----------------------------------------
    def get_Cpedido(self):
        return int(self.Cpedido)
    #-----------------------------------------
    #Metodo encargado de cerrar popups al pulsar el boton cerrar
    #-----------------------------------------
    def cerrar(self,instance):
        self.popup.dismiss()

# -------Información del pedido--------
class DarAltaPedido(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.producto = int
        self.cantidad = ''
        self.pedido_solicitado = False
        self.producto_seleccionado = False
        self.popup = None #Necesario para guardar la referencia al popup y poder cerrarlo usando un botón

    #-----------------------------------------
    #Metodo encargado de desplegar los producto a elegir para a hacer el pedido
    #-----------------------------------------
    def display_productos(self):
        productos = DropDown()
        for producto in self.manager.admin.ObtenerTabla("STOCK"):
            btn_producto = Button(text=f' {producto[0]}', size_hint_y=None, height=40)
            btn_producto.bind(on_release=self.seleccionar_producto)
            productos.add_widget(btn_producto)
        productos.open(self.ids.productos)

    #-----------------------------------------
    #Metodo encargado de la selección los productos desplegados
    #-----------------------------------------
    def seleccionar_producto(self, instance):
        self.ids.productos.text = instance.text
        instance.parent.parent.dismiss()
        self.producto = int(instance.text)
        self.manager.admin.VolverCheckpoint("inicio")
        self.producto_seleccionado = True
    #-----------------------------------------
    #Metodo encargado de obtener la cantidad a pedir a través de la interfaz
    #-----------------------------------------
    def seleccionar_cantidad(self, instance):
        if instance.text.isdigit():
            self.cantidad = instance.text
            self.manager.admin.VolverCheckpoint("inicio")
        else:
            advertencia = BoxLayout(orientation='vertical')
            error = Label(text="Solo se pueden introducir números")
            cerrar = Button(text="Cerrar")
            cerrar.bind(on_press=self.cerrar)
            advertencia.add_widget(error)
            advertencia.add_widget(cerrar)
            # Crear el Popup
            self.popup = Popup(title="Error",
                          content=advertencia,
                          size_hint=(None, None), size=(400, 200))
            self.popup.open()
            self.cantidad = instance.text
            self.manager.admin.VolverCheckpoint("inicio")
    #-----------------------------------------
    #Metodo encargado de comprobar que se hayan especificado todos los campos e insertar en la base de datos lo especificado
    #-----------------------------------------
    def solicitar_pedido(self):
        self.manager.admin.VolverCheckpoint("inicio")

        if self.producto_seleccionado == False:
            advertencia = BoxLayout(orientation='vertical')
            error = Label(text="Por favor rellena todos los campos")
            cerrar = Button(text="Cerrar")
            cerrar.bind(on_press=self.cerrar)
            advertencia.add_widget(error)
            advertencia.add_widget(cerrar)
            # Crear el Popup
            self.popup = Popup(title="Error",
                               content=advertencia,
                               size_hint=(None, None), size=(400, 200))
            self.popup.open()
        elif not self.cantidad.isdigit():
            advertencia = BoxLayout(orientation='vertical')
            error = Label(text="Solo se permiten numeros en cantidad")
            cerrar = Button(text="Cerrar")
            cerrar.bind(on_press=self.cerrar)
            advertencia.add_widget(error)
            advertencia.add_widget(cerrar)
            # Crear el Popup
            self.popup = Popup(title="Error",
                               content=advertencia,
                               size_hint=(None, None), size=(400, 200))
            self.popup.open()

        elif self.manager.admin.ObtenerUnProducto(self.producto)[1] <= 0 or self.manager.admin.ObtenerUnProducto(self.producto)[1] < int(self.cantidad):
            advertencia = BoxLayout(orientation='vertical')
            error = Label(text="No hay stock")
            cerrar = Button(text="Cerrar")
            cerrar.bind(on_press=self.cerrar)
            advertencia.add_widget(error)
            advertencia.add_widget(cerrar)
            # Crear el Popup
            self.popup = Popup(title="Error",
                               content=advertencia,
                               size_hint=(None, None), size=(400, 200))
            self.popup.open()
        else:
            Cantidad = self.manager.admin.ObtenerUnProducto(self.producto)[1]
            self.manager.admin.Insertar_Detalle_Pedido(self.manager.get_screen("IniciarPedido").get_Cpedido(),self.producto,int(self.cantidad))
            self.manager.admin.Modificar_Stock(self.producto,Cantidad-int(self.cantidad))

            self.pedido_solicitado= True
    #-----------------------------------------
    #Metodo encargado de confirmar la transacción y regresar al menu
    #-----------------------------------------
    def confirmar(self):
        if self.pedido_solicitado == False:
            advertencia = BoxLayout(orientation='vertical')
            error = Label(text="Rellene todos los campos")
            cerrar = Button(text="Cerrar")
            cerrar.bind(on_press=self.cerrar)
            advertencia.add_widget(error)
            advertencia.add_widget(cerrar)
            # Crear el Popup
            self.popup = Popup(title="Error",
                               content=advertencia,
                               size_hint=(None, None), size=(400, 200))
            self.popup.open()
        else:
            self.manager.admin.Confirmar()
            self.manager.current = 'Menu'

    #-----------------------------------------
    #Metodo encargado de cancelar la transacción
    #-----------------------------------------
    def cancelar(self):
        self.manager.admin.CancelarTransaccion()

    #-----------------------------------------
    #Metodo encargado de cerrar los popups
    #-----------------------------------------
    def cerrar(self,instance):
        self.popup.dismiss()

class Tablas(Screen):

    #-----------------------------------------
    #Metodo encargado de generar un popup con la tabla especificada
    #-----------------------------------------
    def mostrar_tabla(self, nombre):
        datos = GridLayout(cols=len(self.manager.admin.NombresTabla(nombre)), padding=10, spacing=10, size_hint_y=None)
        datos.bind(minimum_height=datos.setter('height'))

        for fila in self.manager.admin.NombresTabla(nombre):
            label = Label(text=f'{fila[0]}')
            datos.add_widget(label)

        for fila in self.manager.admin.ObtenerTabla(nombre):
            for fila_2 in fila:
                label = Label(text=f'{fila_2}', size_hint_y=None, height=20)  # altura fija para las celdas
                datos.add_widget(label)
        scroll_view = ScrollView(size_hint=(1, 1))
        scroll_view.add_widget(datos)
        tabla = Popup(title=f'{nombre}',
                      content=scroll_view,
                      size_hint=(0.75, 0.75))
        tabla.open()

    pass

# El código KV como un string
kv_code = ''' 
WindowManager:
    Menu:
    DarAltaPedido:
    Tablas:
    IniciarPedido:
<Menu>:
    name: "Menu"
    BoxLayout:
        orientation: 'vertical'
        size: root.width, root.height
        padding: [30, 50, 30, 30]
        spacing: 20  # Espaciado entre los botones

        Label:
            text: 'Menú'
            font_size: 32
            size_hint_y: None
            height: 50
            halign: 'center'  # Centra el texto en el label

        Button:
            id:btn_administrar_tablas
            text: 'CREAR TABLAS'
            on_press: 
                root.administrar_tablas()

        Button:
            text: 'Nuevo pedido'
            on_press: 
                app.root.current="IniciarPedido"
                root.manager.transition.direction="left"


        Button:
            text: 'Mostrar tablas'
            on_press: 
                app.root.current="Tablas"
                root.manager.transition.direction="left"

        Button:
            text: 'Cerrar'
            on_press: root.salir()

<DarAltaPedido>:
    name: "Pedido"
    
    BoxLayout:
        orientation: 'vertical'
        padding: [30, 50, 30, 30]
        spacing: 20 

        Label:
            text: "PEDIDO"
            size_hint_y: 0.25
        BoxLayout:
            orientation: 'horizontal'  # Organizar los elementos en una fila
            size_hint_y: 0.25
            Button:
                text: "Productos"
                id: productos
                size_hint_x: 0.5  # El botón ocupará el 30% del espacio horizontal disponible
                on_press: root.display_productos()

                
            TextInput:
                hint_text: "Cantidad"
                size_hint_x: 0.3  # Este botón ocupará el 40% del espacio horizontal
                halign: 'center' 
                text_vertical_align: 'middle' 
                on_text: 
                    root.seleccionar_cantidad(self)

            Button:
                text: "Enviar"
                size_hint_x: 0.2  # Este botón ocupará el 30% del espacio horizontal
                on_press: root.solicitar_pedido()
        BoxLayout:
            orientation: 'vertical'   
            size_hint_y: 0.5
            spacing: 20  # Espaciado entre los botones

            Button:
                text: 'CONFIRMAR PEDIDO'
                on_press: 
                    root.confirmar()
                    root.manager.transition.direction="right"
    
            Button:
                text: 'CANCELAR'
                on_press: 
                    root.cancelar()
                    app.root.current="Menu"
                    root.manager.transition.direction="right"

<Tablas>:
    name: "Tablas"
    BoxLayout:
        orientation: 'vertical'
        size: root.width, root.height
        padding: [50, 50, 50, 50]
        spacing: 20  # Espaciado entre los botones

        Label:
            text: 'TABLAS'
            font_size: 32
            size_hint_y: None
            height: 50
            halign: 'center'  # Centra el texto en el label

        Button:
            text: 'STOCK'
            on_press:                
                root.mostrar_tabla("STOCK")


        Button:
            text: 'PEDIDO'
            on_press: 
                root.mostrar_tabla("PEDIDO")

        Button:
            text: 'DETALLE_PEDIDO'
            on_press:
                root.mostrar_tabla("DETALLE_PEDIDO")


        Button:
            text: 'Volver'
            on_press: 
                app.root.current="Menu"
                root.manager.transition.direction="right"
                
<IniciarPedido>
    name: "IniciarPedido"
    BoxLayout:
        orientation: 'vertical'
        padding: [30, 50, 30, 30]
        spacing: 20 

        Label:
            text: 'Nuevo pedido'
            font_size: 32
            halign: 'center'  # Centra el texto en el label
            
        TextInput:
            hint_text: "Cpedido" 
            on_text: 
                root.obtener_Cpedido(self)

        TextInput:
            hint_text: "Ccliente" 
            on_text: 
                root.obtener_Ccliente(self)
        Button:
            text: 'Confirmar'
            on_press:
                root.solicitar_registro()
                root.manager.transition.direction="left"
                
'''

# Cargar el archivo KV
kv = Builder.load_string(kv_code)

class SuperChachiApp(App):
    def build(self):
        return kv

# Iniciar la aplicación
if __name__ == '__main__':
    SuperChachiApp().run()
