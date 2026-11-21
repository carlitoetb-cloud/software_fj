
# Software FJ
## Sistema Integral de Gestión de Clientes, Servicios y Reservas

Aplicación de consola desarrollada en Python mediante programación
orientada a objetos. Permite registrar clientes, administrar servicios
y gestionar reservas.

El sistema utiliza listas en memoria y no necesita una base de datos.

## Requisitos

- Python 3.10 o superior.
- No requiere instalar librerías externas.

## Cómo ejecutar

Abre una terminal en la carpeta principal del proyecto y escribe:

```bash
python main.py
```

El programa ejecutará una demostración de operaciones correctas
e incorrectas. Los errores se controlan para evitar que la aplicación
se cierre inesperadamente.

## Cómo ejecutar las pruebas

En la terminal escribe:

```bash
python -m unittest discover -s tests -v
```

## Organización del proyecto

```text
software-fj/
│
├── main.py
├── README.md
├── .gitignore
│
├── software_fj/
│   ├── __init__.py
│   ├── excepciones.py
│   ├── modelos.py
│   └── sistema.py
│
├── tests/
│   └── test_sistema.py
│
└── logs/
    └── .gitkeep
```

## Conceptos de programación orientada a objetos

- Abstracción: clases Entidad y Servicio.
- Encapsulamiento: atributos privados y propiedades de Cliente.
- Herencia: ReservaSala, AlquilerEquipo y Asesoria heredan de Servicio.
- Polimorfismo: cada servicio implementa su cálculo de costo y descripción.
- Sobrecarga: se documentan variantes de cálculo con typing.overload
  y se utilizan parámetros opcionales en la implementación.
- Excepciones: se utilizan errores personalizados.
- Registro de eventos: se guardan eventos y errores en un archivo de log.

Python no implementa sobrecarga tradicional de métodos por firma.
Por esa razón, el proyecto utiliza typing.overload para documentar
las variantes y una implementación flexible con parámetros opcionales.

## Servicios disponibles

1. Reserva de salas: valida la capacidad de asistentes.
2. Alquiler de equipos: valida las unidades disponibles.
3. Asesorías: valida el tema de la asesoría.

## Estados de las reservas

- Pendiente.
- Confirmada.
- Cancelada.
- Procesada.

## Registro de eventos

Los eventos se guardan en:

logs/software_fj.log

Los clientes, servicios y reservas se conservan en memoria mientras
la aplicación está en ejecución. Al cerrar el programa, estos datos
no se guardan de forma permanente.
