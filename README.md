# restaurante_app — Semana 15

**Estudiante:** José Alberto Tarco Tipán  
**Materia:** Programación Orientada a Objetos  
**Institución:** Universidad Estatal Amazónica  
**Entrega:** Semana 15 — Conceptos fundamentales de manejo de eventos

---

## 1. Descripción general

Esta entrega evoluciona `restaurante_app` (Parrilla del Valle) a partir de la gestión completa del menú construida en la Semana 14. El objetivo central es comprender los **fundamentos básicos del manejo de eventos**: cómo una acción del usuario sobre un componente (un botón) dispara, mediante `command=`, un **callback** que coordina una operación de negocio sin concentrar la lógica dentro de la interfaz.

Como contexto práctico se incorpora la sección **Ventas**, que relaciona un **cliente** existente con un **plato** existente del menú y conserva el pedido en `ventas.json`. Se conservan íntegramente el inicio de sesión, la navegación y la gestión completa del menú ya construidas.

---

## 2. Estructura del proyecto

```
restaurante_app/
├── assets/
│   ├── icons/
│   └── logo/
├── datos/
│   ├── productos.json
│   ├── usuarios.json
│   └── ventas.json
├── modelos/
│   ├── __init__.py
│   ├── producto.py
│   ├── usuario.py
│   └── venta.py
├── servicios/
│   ├── __init__.py
│   ├── archivo_servicio.py
│   └── restaurante_servicio.py
├── ui/
│   ├── __init__.py
│   ├── login_view.py
│   └── main_view.py
├── main.py
└── README.md
```

No se modificó la organización heredada de la Semana 14; la evolución ocurre en `modelos/venta.py` (nuevo), `restaurante_servicio.py` (ampliado) y `ui/main_view.py` (nueva sección Ventas), además de incorporar la carpeta `assets/`, obligatoria esta semana.

---

## 3. Responsabilidad de cada capa

| Capa | Responsabilidad |
|---|---|
| `modelos/` | `Producto` (con tiempo de preparación) y `Usuario` (con mesa asignada), validados con `property`. `Venta` (nuevo) relaciona `usuario_identificacion`, `producto_codigo` y `fecha`. |
| `servicios/archivo_servicio.py` | Lee y escribe los archivos JSON de `datos/`. |
| `servicios/restaurante_servicio.py` | Convierte los datos en objetos, valida el acceso y expone el CRUD completo de platos, además de `registrar_venta`, `listar_ventas`, `cantidad_ventas` y `guardar_ventas`. Toda la validación y persistencia de la venta vive aquí, nunca en la interfaz. |
| `ui/` | `LoginView` y `MainView`, construidas con Tkinter; solicitan las operaciones a `RestauranteServicio` sin tocar el JSON directamente. |
| `main.py` | Crea la única ventana principal, configura el ícono del sistema desde `assets/` y controla el cambio entre vistas. |

---

## 4. Componentes y contenedores utilizados

- `Frame`: separa encabezado, barra de navegación, contenido y barra de estado.
- `LabelFrame`: agrupa el formulario ("Datos del plato"), el listado ("Platos del menu" / "Consulta de clientes") y ahora "Registrar pedido" / "Ventas registradas".
- `Entry`: código, nombre y precio del plato, y credenciales de acceso.
- `ttk.Combobox` (solo lectura): selector de categoría del plato, y ahora selector de cliente y de plato en la sección Ventas.
- `ttk.Spinbox`: selectores numéricos para el tiempo de preparación (minutos) y el stock del plato.
- `ttk.Treeview` + `ttk.Scrollbar`: tablas de platos, clientes y ahora ventas, con desplazamiento vertical.
- `ttk.Button` / `ttk.Style`: botones de acción conectados mediante `command=`, ahora con íconos de `assets/icons/`.
- Gestores de geometría: `pack()` para la estructura general y `grid()` dentro de los formularios.

---

## 5. Sección Ventas: flujo de eventos aplicado

```
Cliente elige un Cliente y un Plato en los Combobox
                ↓
Clic en "Registrar venta"  (command=self.registrar_venta)
                ↓
Callback registrar_venta() en MainView:
    - obtiene el texto seleccionado en cada Combobox
    - lo traduce a la identificacion / codigo real
    - llama a restaurante_servicio.registrar_venta(...)
                ↓
RestauranteServicio.registrar_venta():
    - valida que ambos campos vengan seleccionados
    - valida que el cliente exista
    - valida que el plato exista
    - crea un objeto Venta (el modelo valida sus propios datos)
    - agrega la venta en memoria y llama a guardar_ventas()
                ↓
ArchivoServicio.escribir_json() persiste en ventas.json
                ↓
MainView.refrescar_ventas() actualiza la tabla (Treeview)
y la barra de estado inferior
```

El callback de la interfaz **no** decide si la venta es válida ni toca el archivo JSON: solo recolecta la selección y coordina la llamada al servicio, que concentra las reglas de negocio y la persistencia.

---

## 6. Operaciones implementadas sobre el menú y las ventas

| Operación | Acción en la interfaz | Método en `RestauranteServicio` |
|---|---|---|
| Registrar plato | Botón **Registrar** | `registrar_producto(codigo, nombre, precio, categoria, tiempo_preparacion, stock)` |
| Consultar plato | Botón **Cargar / Consultar** | `buscar_producto_por_codigo(codigo)` |
| Actualizar plato | Botón **Actualizar** | `actualizar_producto(codigo, nombre, precio, categoria, tiempo_preparacion, stock)` |
| Eliminar plato | Botón **Eliminar** | `eliminar_producto(codigo)` |
| Registrar venta | Botón **Registrar venta** | `registrar_venta(usuario_identificacion, producto_codigo)` |

Todas las validaciones (campos vacíos, precio o tiempo no numérico, categoría inválida, código duplicado, cliente o plato inexistente) se resuelven en los modelos y en `RestauranteServicio`; la interfaz solo captura los datos y muestra el resultado con `messagebox`.

---

## 7. Recursos gráficos (`assets/`)

Esta semana es obligatorio incorporar íconos y el logotipo del sistema:

- `assets/logo/logo.png`: logotipo mostrado en la pantalla de inicio de sesión.
- `assets/logo/icono.png`: versión simplificada usada como ícono de la ventana principal y junto al título en el encabezado.
- `assets/icons/`: íconos para cada botón de navegación (Inicio, Productos, Usuarios, Ventas, Pedidos, Cerrar sesión) y para las acciones de los formularios (Registrar, Consultar, Actualizar, Eliminar, Limpiar).

---

## 8. Persistencia

Los cambios sobre el menú se guardan de inmediato en `datos/productos.json` mediante `RestauranteServicio.guardar_productos()`. Las ventas se guardan de la misma forma en `datos/ventas.json` mediante `guardar_ventas()`, ambos delegando en `ArchivoServicio`. Al reabrir la aplicación, los platos y las ventas registradas se conservan.

---

## 9. Flujo de la aplicación

```
Inicio de la aplicacion
        ↓
main.py prepara Tkinter, el icono del sistema y los servicios
        ↓
LoginView (usuario y clave del cliente)
        ↓
RestauranteServicio valida el acceso
        ↓
MainView
        ↓
Inicio (resumen) | Usuarios (clientes) | Productos (menu) | Ventas (pedidos)
        ↓
Ventas: seleccionar cliente + plato -> Registrar venta
        ↓
command= -> callback de venta -> RestauranteServicio valida y persiste
        ↓
Actualizacion de la tabla de ventas y de la barra de estado
```

---

## 10. Credenciales de acceso (demostración)

| Usuario | Contraseña |
|---|---|
| `jtarco` | `grill2026` |
| `admin` | `admin456` |

La contraseña debe incluir al menos un número, según la validación del modelo `Usuario`.

---

## 11. Ejecución

```bash
cd restaurante_app
python main.py
```

Requiere **Python 3.10 o superior** y Tkinter disponible en la instalación.

---

## 12. Pruebas realizadas

1. Se ejecutó `main.py` y la aplicación inició sin errores, con el ícono del sistema visible en la ventana.
2. El acceso mediante usuario y contraseña continúa funcionando y muestra el logotipo.
3. La interfaz principal y la gestión completa de Productos siguen funcionando igual que en la Semana 14.
4. La opción **Usuarios** permite consultar los clientes en una tabla, incluyendo su mesa.
5. Existe una sección visible **Ventas** con formulario y tabla.
6. Se puede seleccionar un cliente registrado y un plato registrado mediante los Combobox.
7. Se registró una venta mediante el botón **Registrar venta**, usando `command=` (no `command=callback()`).
8. El callback delega el registro a `RestauranteServicio.registrar_venta`.
9. La nueva venta se almacenó en `ventas.json` y apareció de inmediato en la tabla y en la barra de estado.
10. Al cerrar y volver a ejecutar la aplicación, las ventas registradas se recuperan correctamente.
11. Se probó el registro sin seleccionar cliente/plato: `RestauranteServicio` rechaza la operación con un mensaje claro y no modifica `ventas.json`.
12. La navegación y los controles resultan claros: barra superior, formulario, tabla y barra de estado, incorporando los íconos y el logotipo de `assets/`.

---

## 13. Nota educativa sobre autenticación

El acceso de esta etapa es una simulación pedagógica. Las contraseñas se guardan en JSON en texto plano solo con fines didácticos; no representa una práctica segura para un sistema real.
