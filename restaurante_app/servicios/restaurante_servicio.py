from datetime import date

from modelos.producto import Producto
from modelos.usuario import Usuario
from modelos.venta import Venta


class RestauranteServicio:
    def __init__(self, archivo_servicio) -> None:
        self.archivo_servicio = archivo_servicio
        self.usuarios: list[Usuario] = []
        self.productos: list[Producto] = []
        self.ventas: list[Venta] = []
        self.cargar_datos()

    def cargar_datos(self) -> None:
        # Convierte los registros de usuarios.json, productos.json y ventas.json en objetos del dominio.
        usuarios_json = self.archivo_servicio.leer_json("usuarios.json")
        productos_json = self.archivo_servicio.leer_json("productos.json")
        ventas_json = self.archivo_servicio.leer_json("ventas.json")

        self.usuarios = []
        for datos in usuarios_json:
            try:
                usuario = Usuario(
                    datos.get("identificacion", ""),
                    datos.get("nombre", ""),
                    datos.get("mesa", ""),
                    datos.get("usuario", ""),
                    datos.get("contrasena", ""),
                )
                self.usuarios.append(usuario)
            except ValueError as error:
                print(f"Cliente con datos invalidos, se omite: {error}")

        self.productos = []
        for datos in productos_json:
            try:
                producto = Producto(
                    datos.get("codigo", ""),
                    datos.get("nombre", ""),
                    datos.get("precio", 0),
                    datos.get("categoria", ""),
                    datos.get("tiempo_preparacion", 10),
                    datos.get("stock", 0),
                )
                self.productos.append(producto)
            except ValueError as error:
                print(f"Producto con datos invalidos, se omite: {error}")

        # Semana 15: convierte las ventas persistidas para reconstruir el historial de pedidos.
        self.ventas = []
        for datos in ventas_json:
            try:
                venta = Venta(
                    datos.get("identificador", ""),
                    datos.get("usuario_identificacion", ""),
                    datos.get("producto_codigo", ""),
                    datos.get("fecha", ""),
                )
                self.ventas.append(venta)
            except ValueError as error:
                print(f"Venta con datos invalidos, se omite: {error}")

    def validar_acceso(self, usuario: str, contrasena: str) -> Usuario | None:
        # Recorre los clientes cargados y delega la comparacion de credenciales.
        for usuario_registrado in self.usuarios:
            if usuario_registrado.validar_credenciales(usuario, contrasena):
                return usuario_registrado
        return None

    def listar_usuarios(self) -> list[Usuario]:
        return self.usuarios.copy()

    def listar_productos(self) -> list[Producto]:
        return self.productos.copy()

    def listar_ventas(self) -> list[Venta]:
        return self.ventas.copy()

    def cantidad_usuarios(self) -> int:
        return len(self.usuarios)

    def cantidad_productos(self) -> int:
        return len(self.productos)

    def cantidad_ventas(self) -> int:
        return len(self.ventas)

    def buscar_producto_por_codigo(self, codigo: str) -> Producto | None:
        # Localiza un plato ya cargado a partir de su codigo.
        codigo_normalizado = Producto.construir_codigo(codigo)
        for producto in self.productos:
            if producto.codigo == codigo_normalizado:
                return producto
        return None

    def buscar_usuario_por_identificacion(self, identificacion: str) -> Usuario | None:
        # Localiza un cliente ya cargado a partir de su identificacion.
        identificacion_normalizada = identificacion.strip()
        for usuario in self.usuarios:
            if usuario.identificacion == identificacion_normalizada:
                return usuario
        return None

    def guardar_productos(self) -> None:
        # Persiste el estado actual de los platos del menu en productos.json.
        datos = [producto.convertir_a_diccionario() for producto in self.productos]
        self.archivo_servicio.escribir_json("productos.json", datos)

    def registrar_producto(
        self,
        codigo: str,
        nombre: str,
        precio: float,
        categoria: str,
        tiempo_preparacion: int,
        stock: int,
    ) -> Producto:
        # Valida los datos mediante el modelo antes de agregar el plato al menu.
        nuevo_producto = Producto(codigo, nombre, precio, categoria, tiempo_preparacion, stock)

        if self.buscar_producto_por_codigo(nuevo_producto.codigo) is not None:
            raise ValueError("Ya existe un plato registrado con ese codigo.")

        self.productos.append(nuevo_producto)
        self.guardar_productos()
        return nuevo_producto

    def actualizar_producto(
        self,
        codigo: str,
        nombre: str,
        precio: float,
        categoria: str,
        tiempo_preparacion: int,
        stock: int,
    ) -> Producto:
        # El codigo identifica al plato existente; el resto se actualiza.
        producto_actual = self.buscar_producto_por_codigo(codigo)

        if producto_actual is None:
            raise ValueError("No existe un plato registrado con ese codigo.")

        datos_validados = Producto(codigo, nombre, precio, categoria, tiempo_preparacion, stock)
        producto_actual.nombre = datos_validados.nombre
        producto_actual.precio = datos_validados.precio
        producto_actual.categoria = datos_validados.categoria
        producto_actual.tiempo_preparacion = datos_validados.tiempo_preparacion
        producto_actual.stock = datos_validados.stock

        self.guardar_productos()
        return producto_actual

    def eliminar_producto(self, codigo: str) -> Producto:
        # Quita el plato de la lista en memoria y actualiza el archivo.
        producto_actual = self.buscar_producto_por_codigo(codigo)

        if producto_actual is None:
            raise ValueError("No existe un plato registrado con ese codigo.")

        self.productos.remove(producto_actual)
        self.guardar_productos()
        return producto_actual

    # -----------------------------------------------------------------
    # Semana 15: gestion de ventas (fundamentos de manejo de eventos).
    # El callback de la interfaz solo recolecta la seleccion; toda la
    # validacion y la persistencia de la venta se resuelven aqui.
    # -----------------------------------------------------------------
    def guardar_ventas(self) -> None:
        # Persiste el estado actual de ventas en ventas.json.
        datos = [venta.convertir_a_diccionario() for venta in self.ventas]
        self.archivo_servicio.escribir_json("ventas.json", datos)

    def generar_identificador_venta(self) -> str:
        # Genera un identificador secuencial simple para el nuevo pedido.
        siguiente = len(self.ventas) + 1
        return f"P{siguiente:03d}"

    def registrar_venta(self, usuario_identificacion: str, producto_codigo: str) -> Venta:
        # Relaciona un cliente existente con un plato existente del menu.
        if not usuario_identificacion or not usuario_identificacion.strip():
            raise ValueError("Debe seleccionar el cliente que realiza el pedido.")
        if not producto_codigo or not producto_codigo.strip():
            raise ValueError("Debe seleccionar el plato vendido.")

        usuario_encontrado = self.buscar_usuario_por_identificacion(usuario_identificacion)
        if usuario_encontrado is None:
            raise ValueError("El cliente seleccionado no esta registrado.")

        producto_encontrado = self.buscar_producto_por_codigo(producto_codigo)
        if producto_encontrado is None:
            raise ValueError("El plato seleccionado no esta registrado.")

        nueva_venta = Venta(
            self.generar_identificador_venta(),
            usuario_encontrado.identificacion,
            producto_encontrado.codigo,
            date.today().isoformat(),
        )

        self.ventas.append(nueva_venta)
        self.guardar_ventas()
        return nueva_venta
