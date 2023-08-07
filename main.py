import tkinter
from tkinter import ttk
from tkinter import*
import sqlite3


#Las aplicaciones de escritorio son parte del sistema operativo,
# son más clásicas como la calculadora de Windows.

#Usaremos el Frameware de Tkinter para hacer esta interfaz gráfica, Tkinter es el frameware oficial
# de Python para crear aplicaciones de escritorio, pero no es la única opción, QT, kivy. En esta
# practica no vamos a usar el ORM SQLarchemy, vamos a usar SQlite directamente sin ORM. TTK es del módulo


class Producto():
    db = 'database/productos.db'

    def db_consulta(self, consulta, parametros=()):
        with sqlite3.connect(self.db) as con: #Iniciamos una conexion con la base de datos (alias con)
         cursor = con.cursor() # Generamos un cursor de la conexion para poder operar en la base de datos
         resultado = cursor.execute(consulta, parametros) # Preparar la consulta SQL (con parametros si los hay)
         con.commit() # Ejecutar la consulta SQL preparada anteriormente
        return resultado  #Retornar el resultado de la consulta SQL

    def get_productos(self):
        # Lo primero, al iniciar la app, vamos a limpiar la tabla por si hubiera datos residuales o antiguos
        registros_tabla = self.tabla.get_children() # Obtener todos los datos de la tabla

        for fila in registros_tabla:
            self.tabla.delete(fila)

        #Consulta SQL
        query = "SELECT * FROM producto ORDER BY nombre DESC"
        registros= self.db_consulta(query)

        for fila in registros:
            print(fila)  # print para verificar por consola los datos
            self.tabla.insert('',0,text=fila[1],values=(fila[2],fila[3],fila[4])) #Se muestran todos los campos de nuestra
                                                                                 #tabla producto de la BDD en la app.

    def validacion_nombre(self):
        nombre_introducido_por_usuario = self.nombre.get()
        return len(nombre_introducido_por_usuario) != 0

    def validacion_precio(self):
        precio_introducido_por_usuario = self.precio.get()
        return len(precio_introducido_por_usuario) != 0

    def validacion_categoria(self):
        categoria_introducida_por_usuario = self.categoria.get()
        return len(categoria_introducida_por_usuario) != 0

    def validacion_stock(self):
        stock_introducida_por_usuario = self.stock.get()
        return len(stock_introducida_por_usuario) != 0

    def add_producto(self):

        pendiente = 'Pendiente'

        if self.validacion_nombre() and self.validacion_precio():

            if self.validacion_categoria() and self.validacion_stock()==False:

                query = 'INSERT INTO producto VALUES(NULL,?,?,?,?)'  #Consulta SQL (sin los datos)

                #El id no hay que indicárselo cuando hagamos referencia a que una columna es
                #Autoincrementada hay que poner un NULL sino nos da error.


                parametros = (self.nombre.get(), self.precio.get(),self.categoria.get(),pendiente)  # Parametros de la consulta SQL self.db_consulta(query, parametros)
                self.db_consulta(query,parametros)

                print("Datos guardados")
                self.mensaje['text'] = 'Producto {} añadido con éxito'.format(self.nombre.get())
                #Label ubicado entre el boton y la tabla
                self.nombre.delete(0, END)  # Borrar el campo nombre del formulario
                self.precio.delete(0, END)#Borrar el campo precio del formulario
                self.categoria.delete(0, END)  # Borrar el campo categoria del formulario

            elif self.validacion_stock() and self.validacion_categoria()==False:

                query = 'INSERT INTO producto VALUES(NULL,?,?,?,?)'  #Consulta SQL (sin los datos)

                parametros = (self.nombre.get(), self.precio.get(),pendiente,self.stock.get())  # Parametros de la consulta SQL self.db_consulta(query, parametros)
                self.db_consulta(query,parametros)

                print("Datos guardados")
                self.mensaje['text'] = 'Producto {} añadido con éxito'.format(self.nombre.get())
                #Label ubicado entre el boton y la tabla
                self.nombre.delete(0, END)  # Borrar el campo nombre del formulario
                self.precio.delete(0, END)#Borrar el campo precio del formulario
                self.stock.delete(0, END)  # Borrar el campo stock del formulario

            elif self.validacion_stock() == False and self.validacion_categoria()==False:

                query = 'INSERT INTO producto VALUES(NULL,?,?,?,?)'  # Consulta SQL (sin los datos)

                parametros = (self.nombre.get(), self.precio.get(), pendiente,pendiente)  # Parametros de la consulta SQL self.db_consulta(query, parametros)
                self.db_consulta(query, parametros)

                print("Datos guardados")
                self.mensaje['text'] = 'Producto {} añadido con éxito'.format(self.nombre.get())
                # Label ubicado entre el boton y la tabla
                self.nombre.delete(0, END)  # Borrar el campo nombre del formulario
                self.precio.delete(0, END)  # Borrar el campo precio del formulario


            elif self.validacion_nombre() and self.validacion_precio() and self.validacion_categoria() and self.validacion_stock():

                query = 'INSERT INTO producto VALUES(NULL,?,?,?,?)'  # Consulta SQL (sin los datos)

                parametros = (self.nombre.get(), self.precio.get(), self.categoria.get(),self.stock.get())  # Parametros de la consulta SQL self.db_consulta(query, parametros)
                self.db_consulta(query, parametros)

                print("Datos guardados")
                self.mensaje['text'] = 'Producto {} añadido con éxito'.format(self.nombre.get())
                self.nombre.delete(0, END)
                self.precio.delete(0, END)  # Borrar el campo precio del formulario
                self.categoria.delete(0, END)  # Borrar el campo categoria del formulario
                self.stock.delete(0, END)  # Borrar el campo stock del formulario


        elif self.validacion_nombre() and self.validacion_precio() == False:
             self.mensaje['text'] = 'El precio es obligatorio'

        elif self.validacion_nombre() == False and self.validacion_precio():
             self.mensaje['text'] = 'El nombre es obligatorio'

        elif self.validacion_nombre() == False and self.validacion_precio():
             self.mensaje['text'] = 'El nombre es obligatorio'
        else:
             self.mensaje['text'] = 'El nombre y el precio son obligatorio'

        self.get_productos()

    def del_producto(self):

        self.mensaje['text'] = ''  # Mensaje inicialmente vacio # Comprobacion de que se seleccione un producto para poder eliminarlo
        try:
            self.tabla.item(self.tabla.selection())['text'][0]
        except IndexError as e:
            self.mensaje['text'] = 'Por favor, seleccione un producto'
            return

        self.mensaje['text'] = ''
        nombre = self.tabla.item(self.tabla.selection())['text']
        query = 'DELETE FROM producto WHERE nombre = ?' # Consulta SQL self.db_consulta(query, (nombre,)) # Ejecutar la consulta
        self.db_consulta(query, (nombre,))  # Ejecutar la consulta
        self.mensaje['text'] = 'Producto {} eliminado con éxito'.format(nombre)
        self.get_productos()  # Actualizar la tabla de productos

    #tabla.item nos está mostrando en el terminal un diccionario con el ítem que esta seleccionado en nuestra app.

    def edit_producto(self):
        self.mensaje['text'] = ''  # Mensaje inicialmente vacio

        try:
            self.tabla.item(self.tabla.selection())['text'][0]
        except IndexError as e:
            self.mensaje['text'] = 'Por favor, seleccione un producto'
            return

        nombre = self.tabla.item(self.tabla.selection())['text']
        old_precio = self.tabla.item(self.tabla.selection())['values'][0]  # El precio se encuentra dentro de una lista
        old_categoria=self.tabla.item(self.tabla.selection())['values'][1]
        old_stock=self.tabla.item(self.tabla.selection())['values'][2]

        self.ventana_editar = Toplevel()  # Crear una ventana por delante de la principal self.ventana_editar.title = "Editar Producto" # Titulo de la ventana self.ventana_editar.resizable(1, 1) # Activar la redimension de la ventana. Para desactivarla: (0,0)
        self.ventana_editar.title = "Editar Producto"  # Titulo de la ventana
        self.ventana_editar.resizable(1,1)  # Activar la redimension de la ventana. Para desactivarla: (0,0) self.ventana_editar.wm_iconbitmap('recursos/icon.ico') # Icono de la ventana
        self.ventana_editar.wm_iconbitmap('recursos/icon.ico')  # Icono de la ventana
        titulo = Label(self.ventana_editar, text='Edición de Productos', font=('Calibri', 50, 'bold'))
        titulo.grid(column=0, row=0)

        # Creacion del contenedor Frame de la ventana de Editar Producto
        frame_ep = LabelFrame(self.ventana_editar, text="Editar el siguiente Producto",font=('Calibri', 16, 'bold')) #frame_ep: Frame Editar Producto
        frame_ep.grid(row=1, column=0, columnspan=20, pady=20)

        # Label Nombre antiguo
        self.etiqueta_nombre_anituguo = Label(frame_ep, text="Nombre antiguo: ",font=('Calibri', 13))
        # Etiqueta de texto ubicada en el frame
        self.etiqueta_nombre_anituguo.grid(row=2, column=0) #Posicionamiento a traves de grid

        # Entry Nombre antiguo (texto que no se podra modificar)
        self.input_nombre_antiguo = Entry(frame_ep, textvariable=StringVar(self.ventana_editar, value=nombre),state='readonly',font=('Calibri', 13))
        self.input_nombre_antiguo.grid(row=2, column=1)

        # Label Nombre nuevo
        self.etiqueta_nombre_nuevo = Label(frame_ep, text="Nombre nuevo: ",font=('Calibri', 13))
        self.etiqueta_nombre_nuevo.grid(row=3, column=0)

        # Entry Nombre nuevo (texto que si se podra modificar)
        self.input_nombre_nuevo = Entry(frame_ep,font=('Calibri', 13))
        self.input_nombre_nuevo.grid(row=3, column=1)
        self.input_nombre_nuevo.focus()  # Para que el foco del raton vaya a este Entry al inicio # Label Precio antiguo

        # Label Precio antiguo
        self.etiqueta_precio_anituguo = Label(frame_ep,text="Precio antiguo: ",font=('Calibri', 13))  # Etiqueta de texto ubicada en el frame
        self.etiqueta_precio_anituguo.grid(row=4, column=0)  # Posicionamiento a traves de grid

        #Entry Precio antiguo (texto que no se podra modificar)
        self.input_precio_antiguo = Entry(frame_ep, textvariable=StringVar(self.ventana_editar, value=old_precio),state='readonly',font=('Calibri', 13))
        self.input_precio_antiguo.grid(row=4, column=1)

        # Label Precio nuevo
        self.etiqueta_precio_nuevo = Label(frame_ep, text="Precio nuevo: ",font=('Calibri', 13))
        self.etiqueta_precio_nuevo.grid(row=5, column=0)

        #Entry Precio nuevo (texto que si se podra modificar)
        self.input_precio_nuevo = Entry(frame_ep,font=('Calibri', 13))
        self.input_precio_nuevo.grid(row=5, column=1)
#-----------------------------------------------------------------------------------
        # Label categoria antigua
        self.etiqueta_categoria_antigua = Label(frame_ep, text="Categoria antigua: ", font=('Calibri', 13))
        # Etiqueta de texto ubicada en el frame
        self.etiqueta_categoria_antigua.grid(row=6, column=0)  # Posicionamiento a traves de grid

        # Entry categoria antigua (texto que no se podra modificar)
        self.input_categoria_antigua = Entry(frame_ep, textvariable=StringVar(self.ventana_editar,value= old_categoria),state='readonly', font=('Calibri', 13))
        self.input_categoria_antigua.grid(row=6, column=1)

        # Label categoria nueva
        self.etiqueta_categoria_nueva = Label(frame_ep, text="Categoria nueva: ", font=('Calibri', 13))
        self.etiqueta_categoria_nueva.grid(row=7, column=0)

        # Entry categoria nueva (texto que si se podra modificar)
        self.input_categoria_nueva = Entry(frame_ep, font=('Calibri', 13))
        self.input_categoria_nueva.grid(row=7, column=1)
#----------------------------------------------------------------------------------------------------
        # Label stock antiguo
        self.etiqueta_stock_antigua = Label(frame_ep, text="Stock antiguo: ", font=('Calibri', 13))
        # Etiqueta de texto ubicada en el frame
        self.etiqueta_stock_antigua.grid(row=8, column=0)  # Posicionamiento a traves de grid

        # Entry stock antiguo (texto que no se podra modificar)
        self.input_stock_antiguo = Entry(frame_ep, textvariable=StringVar(self.ventana_editar, value=old_stock),
                                             state='readonly', font=('Calibri', 13))
        self.input_stock_antiguo.grid(row=8, column=1)

        # Label stock nuevo
        self.etiqueta_stock_nuevo= Label(frame_ep, text="Stock nuevo: ", font=('Calibri', 13))
        self.etiqueta_stock_nuevo.grid(row=9, column=0)

        # Entry stock nuevo (texto que si se podra modificar)
        self.input_stock_nuevo = Entry(frame_ep, font=('Calibri', 13))
        self.input_stock_nuevo.grid(row=9, column=1)

#----------------------------------------------------------------------------------------------------
        # Boton Actualizar Producto
        s = ttk.Style()
        s.configure('my.TButton', font=('Calibri', 14, 'bold'))
        self.boton_actualizar = ttk.Button(frame_ep, text="Actualizar Producto", style='my.TButton',
                                           command=lambda: self.actualizar_productos(self.input_nombre_nuevo.get(),
                                                                                     self.input_nombre_antiguo.get(),
                                                                                     self.input_precio_nuevo.get(),
                                                                                     self.input_precio_antiguo.get(),
                                                                                     self.input_categoria_nueva.get(),
                                                                                     self.input_categoria_antigua.get(),
                                                                                     self.input_stock_nuevo.get(),
                                                                                     self.input_stock_antiguo.get()))

        self.boton_actualizar.grid(row=10, columnspan=2, sticky=W + E)

    def actualizar_productos(self, nuevo_nombre, antiguo_nombre, nuevo_precio, antiguo_precio,categoria_nueva,categoria_antigua,stock_nuevo,stock_antiguo):
        producto_modificado = False
        query = 'UPDATE producto SET nombre = ?, precio = ?, categoria = ?,stock = ? WHERE nombre = ? AND precio = ? AND categoria = ? AND stock= ?'

        if nuevo_nombre != '' and nuevo_precio != '' and categoria_nueva !='' and stock_nuevo !='':
        #Si el usuario el producto entero, se cambia todo.
            parametros = (nuevo_nombre, nuevo_precio, categoria_nueva, stock_nuevo, antiguo_nombre, antiguo_precio,categoria_antigua,stock_antiguo)
            producto_modificado = True
        elif nuevo_nombre != '' and nuevo_precio == '' and categoria_nueva =='' and stock_nuevo == '':
            # Si el usuario deja vacio el nuevo precio, se mantiene el pecio anterior
            parametros = (nuevo_nombre, antiguo_precio,categoria_antigua,stock_antiguo,antiguo_nombre, antiguo_precio,categoria_antigua,stock_antiguo)
            producto_modificado = True

        elif nuevo_nombre == '' and nuevo_precio != '' and categoria_nueva =='' and stock_nuevo == '':
            # Si el usuario deja vacio el nuevo precio, se mantiene el pecio anterior
            parametros = (antiguo_nombre, nuevo_precio,categoria_antigua,stock_antiguo,antiguo_nombre, antiguo_precio,categoria_antigua,stock_antiguo)
            producto_modificado = True

        elif nuevo_nombre != '' and nuevo_precio != '' and categoria_nueva =='' and stock_nuevo == '':
            #Si el usuario deja vacio el nuevo nombre, se mantiene el nombre anterior
             parametros = (nuevo_nombre, nuevo_precio,categoria_antigua,stock_antiguo,antiguo_nombre, antiguo_precio,categoria_antigua,stock_antiguo)
             producto_modificado = True

        elif nuevo_nombre != '' and nuevo_precio != '' and categoria_nueva !='' and stock_nuevo == '':
            #Si el usuario deja vacio el nuevo nombre, se mantiene el nombre anterior
             parametros = (nuevo_nombre, nuevo_precio,categoria_nueva,stock_antiguo,antiguo_nombre, antiguo_precio,categoria_antigua,stock_antiguo)
             producto_modificado = True

        elif nuevo_nombre == '' and nuevo_precio  == '' and categoria_nueva  =='' and stock_nuevo == '':
            #Si el usuario deja vacio el nuevo nombre, se mantiene el nombre anterior
             parametros = (antiguo_nombre, antiguo_precio,categoria_antigua,stock_antiguo,antiguo_nombre, antiguo_precio,categoria_antigua,stock_antiguo)
             producto_modificado = False

        elif nuevo_nombre == '' and nuevo_precio  == '' and categoria_nueva  =='' and stock_nuevo != '':
            #Si el usuario deja vacio el nuevo nombre, se mantiene el nombre anterior
             parametros = (antiguo_nombre, antiguo_precio,categoria_antigua,stock_nuevo,antiguo_nombre, antiguo_precio,categoria_antigua,stock_antiguo)
             producto_modificado = True

        elif nuevo_nombre == '' and nuevo_precio == '' and categoria_nueva != '' and stock_nuevo == '':
            # Si el usuario deja vacio el nuevo nombre, se mantiene el nombre anterior
            parametros = ( antiguo_nombre, antiguo_precio, categoria_nueva, stock_antiguo, antiguo_nombre, antiguo_precio,categoria_antigua, stock_antiguo)
            producto_modificado = True

        if producto_modificado==True:

            self.db_consulta(query, parametros)  # Ejecutar la consulta
            self.ventana_editar.destroy()  # Cerrar la ventana de edicion de productos
            self.mensaje['text'] = 'El producto {} ha sido actualizado con éxito'.format(antiguo_nombre)  # Mostrar mensaje para el usuario
            self.get_productos()  # Actualizar la tabla de productos

        else:
            self.ventana_editar.destroy()  # Cerrar la ventana de edicion de productos
            self.mensaje['text'] = 'El producto {} NO ha sido actualizado'.format(antiguo_nombre)  # Mostrar mensaje para el usuario

    def __init__(self, root):


     self.ventana = root #root es un objeto que se le envia a nuestra clase por parametro.
     self.ventana.title("App Gestor de Produtos") # Titulo de la ventana
     self.ventana.resizable(1,1) # Activar la redimension de la ventana. Para desactivarla: (0,0)
     self.ventana.wm_iconbitmap('recursos/icon.ico') #El icono de la aplicación de tkinter se puede cambiar, pero
                                                     # la instrucción cambia de un OS a otro.

    #Creación del contenedor Frame principal
     frame = LabelFrame(self.ventana, text="Registrar un nuevo Producto",font=('Calibri', 16, 'bold'))
     frame.pack(expand=True, fill=tkinter.X,padx=20)
#Con el método frame.pack Se incluyen márgenes de 20 pixeles por arriba y por los laterales, padx=20 y pady=20 y
#a medida que cambien el tamaño de la ventana se va a expandir o contraer este frame en ambos sentidos x e y.


#Label Nombre
     self.etiqueta_nombre = Label(frame, text="Nombre: ") # Etiqueta de texto ubicada en el frame
     self.etiqueta_nombre.pack()
     self.nombre = Entry(frame,justify=CENTER) # Caja de texto (input de texto) ubicada en el frame
     self.nombre.focus() # Para que el foco del raton vaya a este Entry al inicio. El foco del teclado quiero que este en
#el cajón de texto de la label nombre.
     self.nombre.pack(expand=True,fill=tkinter.X,padx=10,pady=5,ipadx=5,ipady=5)

#Label Precio
     self.etiqueta_precio = Label(frame, text="Precio: ") # Etiqueta de texto ubicada en el frame
     self.etiqueta_precio.pack() #Entry Precio (caja de texto que recibira el precio)
     self.precio = Entry(frame,justify=CENTER)
     self.precio.pack(expand=True,fill=tkinter.X,padx=10,pady=5,ipadx=5,ipady=5)

#Label de categoría
     self.etiqueta_categoria = Label(frame, text="Categoria: ")  # Etiqueta de texto ubicada en el frame
     self.etiqueta_categoria.pack()
     # Entry categoria (caja de texto que recibira el precio)

     self.categoria= Entry(frame,justify=CENTER)  # Caja de texto (input de texto) ubicada en el frame
     self.categoria.pack(expand=True,fill=tkinter.X,padx=10,pady=5,ipadx=5,ipady=5)

#Label de stock
     self.etiqueta_stock = Label(frame, text="Stock: ")
     self.etiqueta_stock.pack()
     # Entry stock (caja de texto que recibira el precio)
     self.stock = Entry(frame,justify=CENTER)  # Caja de texto (input de texto) ubicada en el frame
     self.stock.pack(expand=True,fill=tkinter.X,padx=10,pady=5,ipadx=5,ipady=5)

    # Boton Añadir Producto
     s = ttk.Style()
     s.configure('my.TButton', font=('Calibri', 14, 'bold'))
     self.boton_aniadir = ttk.Button(frame, text="Guardar Producto", style='my.TButton',command=self.add_producto) #va un command aqui
     self.boton_aniadir.pack(expand=True,fill=tkinter.BOTH,padx=10,pady=10,ipadx=5,ipady=5)

      #IMPORTANTE= Excepción del command dentro de los botones, al método NO SE LE ponen los paréntesis.
      ##stiky sirve para rellenar columnas con# coordenadas norte-sur-este etc.

     # Mensaje informativo para el usuario
     self.mensaje = Label(text='', fg='red')
     self.mensaje.pack(expand=True,fill=tkinter.X)

     # Tabla de Productos
     # Estilo personalizado para la tabla

     style = ttk.Style()
     style.configure("mystyle.Treeview", highlightthickness=0, bd=0, font=('Calibri', 11))  # Se modifica la fuente de la tabla

     style.configure("mystyle.Treeview.Heading", font=('Calibri', 13, 'bold'))  # Se modifica la fuente de las cabeceras
     style.layout("mystyle.Treeview",
                 [('mystyle.Treeview.treearea', {'sticky': 'nswe'})])  # Eliminamos los bordes # Estructura de la tabla

     # Estructura de la tabla
     self.tabla = ttk.Treeview(height=10, columns=("#0","#1","#2"), style="mystyle.Treeview")
     self.tabla.pack(expand=True,fill=tkinter.BOTH)
     self.tabla.heading('#0', text='Nombre', anchor=CENTER)
     self.tabla.heading('#1', text='Precio', anchor=CENTER)
     self.tabla.heading('#2', text='Categoria', anchor=CENTER)
     self.tabla.heading('#3', text='Stock', anchor=CENTER)


     # Llamada al metodo get_productos() para obtener el listado de productos al inicio de la app

     #Botones de Eliminar y Editar

     s = ttk.Style()
     s.configure('my.TButton', font=('Calibri', 14, 'bold'))

     boton_eliminar = ttk.Button(text='ELIMINAR', style='my.TButton',command=self.del_producto) #va un command aqui
     boton_eliminar.pack(expand=True,fill=tkinter.BOTH,side=tkinter.LEFT)
     boton_editar = ttk.Button(text='EDITAR', style='my.TButton',command=self.edit_producto)
     boton_editar.pack(expand=True,fill=tkinter.BOTH,side=tkinter.RIGHT)



     self.get_productos()

#todos los objetos creados tienen como mínimo el parámetro “frame”, donde quiero crear ese objeto.

#Todas las configuraciones de la ventana (tamaño, nombre etc) lo hacemos desde la clase.
#En Tkinter la interfaz gráfica siempre debe estar vinculada a un objeto, modelo de datos para poder ser manipulada.

if __name__ == '__main__':
    # En el main lo primero que tenemos que hacer es inicializar nuestra ventana grafica y dentro
    #de esa ventana rellenamos el contenido.
    root = Tk()  # Instancia de la ventana principal, Tk() es el constructor de nuestra ventana
    # grafica y siempre es así.
    app = Producto(root)  # Se envia a la clase Producto el control sobre la ventana root root.mainloop()
    root.mainloop()  # Comenzamos el bucle de aplicacion, es como un while True,para que la ventana se quede abierta
    # y se cierre cuando el usuario pulse la x.



#Nota importante: como Tkinter viene con Python no hay que instalarlo en este entorno virtual
# con pip install.Se podría hacer este proyecto sin entorno virtual, ya que no tenemos que instalar nada.


#Como este ejemplo es muy pequeño, nuestro modelo de datos lo hacemos en el main en vez
#de externalizarlo en el fichero models.py.

#A través de ventanas es l forma que tiene Tkinter varias ventanas asociadas a varios modelos de datos, #podemos crear
#varias clases y asignar cada clase a tantas ventanas como queramos y tantas ventanas a #tantas clases como queramos,
# una aplicación a veces tiene una única ventana.




#Para pintar dentro de la ventana, hay que saber cómo pinta Tkinter en la interfaz gráfica. Lo hace en un #formato de
# celdas (grid), nos crea celdas haciendo referencia a cuantas filas y columnas queremos.  Y #para poner elementos
# (widgets=cualquier elemento gráfico) en pantalla lo hacemos haciendo #referencia a las coordenadas.

#Nosotros tenemos que decir el tamaño del elemento y donde lo queremos ubicar.
#Frame: Grupo de widgets
#Tengo 6 elementos, aquí no tenemos HTML hay que tirar de Tkinter.

#Tengo 6 elementos, aquí no tenemos HTML hay que tirar de Tkinter.  Nosotros maquetaremos todo con Frames y dentro
#de ese Frame metemos todos los elementos, de esta manera vamos a poder hacer cambios en el Frame que se va a aplicar
#a todos los elementos que hay dentro, más fácil.



#En este ejemplo vamos a crear la BDD directamente desde DBbrower, a diferencia del ejemplo anterior que la creamos
# desde la programación. Habrá veces en que se tenga que crear la BDD a parte porque el proyecto nos lo requiere o se
# nos prohíbe.
