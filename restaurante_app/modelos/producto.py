class Producto:
    CATEGORIAS_VALIDAS: tuple[str, ...] = (
        "PARRILLA",
        "MARISCOS",
        "VEGETARIANO",
        "PASTA",
        "BEBIDA",
    )

    def __init__(
        self,
        codigo: str,
        nombre: str,
        precio: float,
        categoria: str,
        tiempo_preparacion: int = 10,
        stock: int = 0,
    ) -> None:
        self.codigo = codigo
        self.nombre = nombre
        self.precio = precio
        self.categoria = categoria
        self.tiempo_preparacion = tiempo_preparacion
        self.stock = stock

    @staticmethod
    def construir_codigo(valor: str) -> str:
        return valor.strip().upper()

    @property
    def codigo(self) -> str:
        return self._codigo

    @codigo.setter
    def codigo(self, valor: str) -> None:
        if not valor or not valor.strip():
            raise ValueError("El codigo del producto es obligatorio.")
        self._codigo = Producto.construir_codigo(valor)

    @property
    def nombre(self) -> str:
        return self._nombre

    @nombre.setter
    def nombre(self, valor: str) -> None:
        if not valor or not valor.strip():
            raise ValueError("El nombre del producto no puede quedar vacio.")
        self._nombre = valor.strip()

    @property
    def precio(self) -> float:
        return self._precio

    @precio.setter
    def precio(self, valor: float) -> None:
        try:
            precio = float(valor)
        except (TypeError, ValueError):
            raise ValueError("El precio debe ser un valor numerico.")
        if precio < 0:
            raise ValueError("El precio no puede ser negativo.")
        self._precio = round(precio, 2)

    @property
    def categoria(self) -> str:
        return self._categoria

    @categoria.setter
    def categoria(self, valor: str) -> None:
        if not valor or not valor.strip():
            raise ValueError("La categoria es requerida.")
        cat = valor.strip().upper()
        if cat not in self.CATEGORIAS_VALIDAS:
            raise ValueError(
                f"Categoria no reconocida. Opciones validas: {', '.join(self.CATEGORIAS_VALIDAS)}"
            )
        self._categoria = cat

    @property
    def tiempo_preparacion(self) -> int:
        return self._tiempo_preparacion

    @tiempo_preparacion.setter
    def tiempo_preparacion(self, valor: int) -> None:
        try:
            minutos = int(valor)
        except (TypeError, ValueError):
            raise ValueError("El tiempo de preparacion debe ser un entero.")
        if minutos <= 0:
            raise ValueError("El tiempo de preparacion debe ser mayor que cero.")
        self._tiempo_preparacion = minutos

    @property
    def stock(self) -> int:
        return self._stock

    @stock.setter
    def stock(self, valor: int) -> None:
        try:
            stock = int(valor)
        except (TypeError, ValueError):
            raise ValueError("El stock debe ser un numero entero.")
        if stock < 0:
            raise ValueError("El stock no puede ser negativo.")
        self._stock = stock

    def vender(self, cantidad: int) -> bool:
        if cantidad <= 0 or self._stock < cantidad:
            return False
        self._stock -= cantidad
        return True

    def resumen_tiempo(self) -> str:
        return f"{self._tiempo_preparacion} min"

    def convertir_a_diccionario(self) -> dict:
        return {
            "codigo": self.codigo,
            "nombre": self.nombre,
            "precio": self.precio,
            "categoria": self.categoria,
            "tiempo_preparacion": self.tiempo_preparacion,
            "stock": self.stock,
        }

    def __str__(self) -> str:
        return (
            f"Codigo: {self.codigo} | Nombre: {self.nombre} | "
            f"Precio: ${self.precio:.2f} | Categoria: {self.categoria} | "
            f"Preparacion: {self.resumen_tiempo()} | Stock: {self.stock}"
        )
