class Venta:
    def __init__(
        self,
        identificador: str,
        usuario_identificacion: str,
        producto_codigo: str,
        fecha: str,
    ) -> None:
        self.identificador = identificador
        self.usuario_identificacion = usuario_identificacion
        self.producto_codigo = producto_codigo
        self.fecha = fecha

    @property
    def identificador(self) -> str:
        return self._identificador

    @identificador.setter
    def identificador(self, valor: str) -> None:
        if not valor or not valor.strip():
            raise ValueError("El identificador de la venta es obligatorio.")
        self._identificador = valor.strip()

    @property
    def usuario_identificacion(self) -> str:
        return self._usuario_identificacion

    @usuario_identificacion.setter
    def usuario_identificacion(self, valor: str) -> None:
        if not valor or not valor.strip():
            raise ValueError("Debe indicarse el cliente que realiza el pedido.")
        self._usuario_identificacion = valor.strip()

    @property
    def producto_codigo(self) -> str:
        return self._producto_codigo

    @producto_codigo.setter
    def producto_codigo(self, valor: str) -> None:
        if not valor or not valor.strip():
            raise ValueError("Debe indicarse el plato vendido.")
        self._producto_codigo = valor.strip()

    @property
    def fecha(self) -> str:
        return self._fecha

    @fecha.setter
    def fecha(self, valor: str) -> None:
        if not valor or not valor.strip():
            raise ValueError("La fecha de la venta es obligatoria.")
        self._fecha = valor.strip()

    def convertir_a_diccionario(self) -> dict:
        return {
            "identificador": self.identificador,
            "usuario_identificacion": self.usuario_identificacion,
            "producto_codigo": self.producto_codigo,
            "fecha": self.fecha,
        }

    def __str__(self) -> str:
        return (
            f"Venta: {self.identificador} | Cliente: {self.usuario_identificacion} | "
            f"Plato: {self.producto_codigo} | Fecha: {self.fecha}"
        )
