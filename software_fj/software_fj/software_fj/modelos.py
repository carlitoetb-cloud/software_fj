
"""Modelos, entidades y servicios del sistema Software FJ."""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import overload
import re

from .excepciones import (
    ValidacionError,
    ServicioNoDisponibleError,
    EstadoReservaError,
)


class Entidad(ABC):
    """Clase abstracta que representa una entidad del sistema."""

    def __init__(self, identificador: str):
        if not isinstance(identificador, str) or not identificador.strip():
            raise ValidacionError("El identificador es obligatorio.")

        self._identificador = identificador.strip()

    @property
    def identificador(self):
        return self._identificador

    @abstractmethod
    def resumen(self):
        """Devuelve un resumen de la entidad."""


class Cliente(Entidad):
    """Representa un cliente con atributos encapsulados."""

    def __init__(self, identificador, nombre, documento, correo, telefono):
        super().__init__(identificador)
        self.nombre = nombre
        self.documento = documento
        self.correo = correo
        self.telefono = telefono

    @property
    def nombre(self):
        return self._nombre

    @nombre.setter
    def nombre(self, valor):
        if not isinstance(valor, str) or len(valor.strip()) < 3:
            raise ValidacionError(
                "El nombre debe contener al menos 3 caracteres."
            )
        self._nombre = valor.strip()

    @property
    def documento(self):
        return self._documento

    @documento.setter
    def documento(self, valor):
        valor = str(valor).strip()

        if not re.fullmatch(r"[A-Za-z0-9-]{5,20}", valor):
            raise ValidacionError(
                "Documento inválido. Use entre 5 y 20 caracteres."
            )

        self._documento = valor

    @property
    def correo(self):
        return self._correo

    @correo.setter
    def correo(self, valor):
        if (
            not isinstance(valor, str)
            or not re.fullmatch(
                r"[^@\s]+@[^@\s]+\.[^@\s]+", valor.strip()
            )
        ):
            raise ValidacionError(
                "El correo electrónico no tiene un formato válido."
            )

        self._correo = valor.strip().lower()

    @property
    def telefono(self):
        return self._telefono

    @telefono.setter
    def telefono(self, valor):
        limpio = re.sub(r"[\s()+-]", "", str(valor))

        if not limpio.isdigit() or not 7 <= len(limpio) <= 15:
            raise ValidacionError(
                "El teléfono debe contener entre 7 y 15 dígitos."
            )

        self._telefono = str(valor).strip()

    def resumen(self):
        return (
            f"Cliente {self.identificador}: "
            f"{self.nombre} | {self.correo}"
        )


class Servicio(Entidad, ABC):
    """Clase abstracta que define las características de un servicio."""

    def __init__(
        self, identificador, nombre, tarifa_base, disponible=True
    ):
        super().__init__(identificador)

        if not isinstance(nombre, str) or not nombre.strip():
            raise ValidacionError("El nombre del servicio es obligatorio.")

        if (
            isinstance(tarifa_base, bool)
            or not isinstance(tarifa_base, (int, float))
            or tarifa_base <= 0
        ):
            raise ValidacionError(
                "La tarifa base debe ser un número positivo."
            )

        self._nombre = nombre.strip()
        self._tarifa_base = float(tarifa_base)
        self._disponible = bool(disponible)

    @property
    def nombre(self):
        return self._nombre

    @property
    def tarifa_base(self):
        return self._tarifa_base

    @property
    def disponible(self):
        return self._disponible

    def validar_disponibilidad(self):
        if not self._disponible:
            raise ServicioNoDisponibleError(
                f"El servicio '{self.nombre}' no está disponible."
            )

    def _validar_duracion(self, duracion):
        if (
            isinstance(duracion, bool)
            or not isinstance(duracion, (int, float))
            or duracion <= 0
        ):
            raise ValidacionError(
                "La duración debe ser un número positivo."
            )

    @abstractmethod
    def calcular_costo(
        self, duracion, descuento=0.0, impuesto=0.19
    ):
        """Calcula el valor del servicio."""

    @abstractmethod
    def describir(self):
        """Describe el servicio."""

    @abstractmethod
    def validar_parametros(self, **parametros):
        """Valida los datos particulares de cada servicio."""

    def resumen(self):
        return self.describir()


class ReservaSala(Servicio):
    """Servicio de alquiler de salas."""

    def __init__(
        self, identificador, nombre, tarifa_base, capacidad,
        disponible=True
    ):
        super().__init__(
            identificador, nombre, tarifa_base, disponible
        )

        if (
            isinstance(capacidad, bool)
            or not isinstance(capacidad, int)
            or capacidad < 1
        ):
            raise ValidacionError(
                "La capacidad de la sala debe ser un entero positivo."
            )

        self.capacidad = capacidad

    @overload
    def calcular_costo(self, duracion: float) -> float:
        ...

    @overload
    def calcular_costo(
        self, duracion: float, descuento: float,
        impuesto: float = 0.19
    ) -> float:
        ...

    def calcular_costo(
        self, duracion, descuento=0.0, impuesto=0.19
    ):
        self.validar_disponibilidad()
        self._validar_duracion(duracion)

        if not 0 <= descuento <= 1 or not 0 <= impuesto <= 1:
            raise ValidacionError(
                "Descuento e impuesto deben estar entre 0 y 1."
            )

        subtotal = self.tarifa_base * duracion * (1 - descuento)
        return round(subtotal * (1 + impuesto), 2)

    def validar_parametros(self, **parametros):
        asistentes = parametros.get("asistentes")

        if (
            isinstance(asistentes, bool)
            or not isinstance(asistentes, int)
            or asistentes < 1
        ):
            raise ValidacionError(
                "Debe indicar un número válido de asistentes."
            )

        if asistentes > self.capacidad:
            raise ValidacionError(
                f"La sala admite máximo {self.capacidad} asistentes."
            )

    def describir(self):
        return (
            f"Sala '{self.nombre}' para {self.capacidad} personas. "
            f"Tarifa por hora: ${self.tarifa_base:,.0f}"
        )


class AlquilerEquipo(Servicio):
    """Servicio de alquiler de equipos tecnológicos."""

    def __init__(
        self, identificador, nombre, tarifa_base,
        unidades_disponibles, disponible=True
    ):
        super().__init__(
            identificador, nombre, tarifa_base, disponible
        )

        if (
            isinstance(unidades_disponibles, bool)
            or not isinstance(unidades_disponibles, int)
            or unidades_disponibles < 0
        ):
            raise ValidacionError(
                "Las unidades disponibles deben ser un entero no negativo."
            )

        self.unidades_disponibles = unidades_disponibles

    @overload
    def calcular_costo(self, duracion: float) -> float:
        ...

    @overload
    def calcular_costo(
        self, duracion: float, descuento: float,
        impuesto: float = 0.19
    ) -> float:
        ...

    def calcular_costo(
        self, duracion, descuento=0.0, impuesto=0.19, unidades=1
    ):
        self.validar_disponibilidad()
        self._validar_duracion(duracion)

        if (
            isinstance(unidades, bool)
            or not isinstance(unidades, int)
            or not 1 <= unidades <= self.unidades_disponibles
        ):
            raise ServicioNoDisponibleError(
                "La cantidad solicitada supera los equipos disponibles."
            )

        if not 0 <= descuento <= 1 or not 0 <= impuesto <= 1:
            raise ValidacionError(
                "Descuento e impuesto deben estar entre 0 y 1."
            )

        total = (
            self.tarifa_base
            * duracion
            * unidades
            * (1 - descuento)
            * (1 + impuesto)
        )

        return round(total, 2)

    def validar_parametros(self, **parametros):
        unidades = parametros.get("unidades", 1)

        if (
            isinstance(unidades, bool)
            or not isinstance(unidades, int)
            or unidades < 1
        ):
            raise ValidacionError(
                "La cantidad de equipos debe ser un entero positivo."
            )

        if unidades > self.unidades_disponibles:
            raise ServicioNoDisponibleError(
                "No hay suficientes equipos disponibles."
            )

    def describir(self):
        return (
            f"Alquiler de {self.nombre}. "
            f"Disponibles: {self.unidades_disponibles}. "
            f"Tarifa por unidad/hora: ${self.tarifa_base:,.0f}"
        )


class Asesoria(Servicio):
    """Servicio de asesoría especializada."""

    def __init__(
        self, identificador, nombre, tarifa_base,
        especialidad, disponible=True
    ):
        super().__init__(
            identificador, nombre, tarifa_base, disponible
        )

        if not isinstance(especialidad, str) or not especialidad.strip():
            raise ValidacionError(
                "La especialidad de la asesoría es obligatoria."
            )

        self.especialidad = especialidad.strip()

    @overload
    def calcular_costo(self, duracion: float) -> float:
        ...

    @overload
    def calcular_costo(
        self, duracion: float, descuento: float,
        impuesto: float = 0.19
    ) -> float:
        ...

    def calcular_costo(
        self, duracion, descuento=0.0, impuesto=0.19
    ):
        self.validar_disponibilidad()
        self._validar_duracion(duracion)

        if not 0 <= descuento <= 1 or not 0 <= impuesto <= 1:
            raise ValidacionError(
                "Descuento e impuesto deben estar entre 0 y 1."
            )

        total = (
            self.tarifa_base
            * duracion
            * (1 - descuento)
            * (1 + impuesto)
        )

        return round(total, 2)

    def validar_parametros(self, **parametros):
        tema = parametros.get("tema")

        if not isinstance(tema, str) or len(tema.strip()) < 4:
            raise ValidacionError(
                "Debe especificar un tema de mínimo 4 caracteres."
            )

    def describir(self):
        return (
            f"Asesoría especializada en {self.especialidad}. "
            f"Tarifa por hora: ${self.tarifa_base:,.0f}"
        )


class EstadoReserva(Enum):
    """Estados posibles de una reserva."""

    PENDIENTE = "Pendiente"
    CONFIRMADA = "Confirmada"
    CANCELADA = "Cancelada"
    PROCESADA = "Procesada"


@dataclass
class Reserva:
    """Representa una reserva realizada por un cliente."""

    identificador: str
    cliente: Cliente
    servicio: Servicio
    duracion: float
    parametros: dict
    estado: EstadoReserva = EstadoReserva.PENDIENTE
    fecha_creacion: datetime = None
    costo: float = 0.0

    def __post_init__(self):
        if (
            not isinstance(self.identificador, str)
            or not self.identificador.strip()
        ):
            raise ValidacionError(
                "La reserva requiere un identificador válido."
            )

        if (
            not isinstance(self.cliente, Cliente)
            or not isinstance(self.servicio, Servicio)
        ):
            raise ValidacionError(
                "La reserva debe asociar un cliente y un servicio válidos."
            )

        if (
            isinstance(self.duracion, bool)
            or not isinstance(self.duracion, (int, float))
            or self.duracion <= 0
        ):
            raise ValidacionError(
                "La duración de la reserva debe ser positiva."
            )

        if not isinstance(self.parametros, dict):
            raise ValidacionError(
                "Los parámetros deben entregarse en un diccionario."
            )

        self.fecha_creacion = self.fecha_creacion or datetime.now()

    def confirmar(self, descuento=0.0, impuesto=0.19):
        if self.estado is not EstadoReserva.PENDIENTE:
            raise EstadoReservaError(
                "Solo se pueden confirmar reservas pendientes."
            )

        self.servicio.validar_disponibilidad()
        self.servicio.validar_parametros(**self.parametros)

        try:
            if isinstance(self.servicio, AlquilerEquipo):
                self.costo = self.servicio.calcular_costo(
                    self.duracion,
                    descuento,
                    impuesto,
                    unidades=self.parametros.get("unidades", 1)
                )
            else:
                self.costo = self.servicio.calcular_costo(
                    self.duracion, descuento, impuesto
                )

        except (TypeError, ValueError) as exc:
            raise EstadoReservaError(
                "No fue posible calcular el costo de la reserva."
            ) from exc

        if self.costo <= 0:
            raise EstadoReservaError(
                "El costo calculado debe ser mayor que cero."
            )

        self.estado = EstadoReserva.CONFIRMADA
        return self.costo

    def cancelar(self):
        if self.estado in (
            EstadoReserva.CANCELADA,
            EstadoReserva.PROCESADA
        ):
            raise EstadoReservaError(
                f"No se puede cancelar una reserva "
                f"{self.estado.value.lower()}."
            )

        self.estado = EstadoReserva.CANCELADA

    def procesar(self):
        if self.estado is not EstadoReserva.CONFIRMADA:
            raise EstadoReservaError(
                "Solo se pueden procesar reservas confirmadas."
            )

        self.estado = EstadoReserva.PROCESADA
        return self.costo

    def resumen(self):
        return (
            f"Reserva {self.identificador} | "
            f"{self.cliente.nombre} | "
            f"{self.servicio.nombre} | "
            f"{self.estado.value} | "
            f"${self.costo:,.2f}"
        )
