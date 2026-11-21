
"""Lógica principal y administración de datos en memoria."""

import logging
from pathlib import Path

from .modelos import Cliente, Servicio, Reserva
from .excepciones import (
    ClienteDuplicadoError,
    RecursoNoEncontradoError,
    ValidacionError,
)


class SistemaFJ:
    """Administra clientes, servicios y reservas de Software FJ."""

    def __init__(self, archivo_log="logs/software_fj.log"):
        self.clientes = []
        self.servicios = []
        self.reservas = []

        ruta = Path(archivo_log)
        ruta.parent.mkdir(parents=True, exist_ok=True)

        self.logger = logging.getLogger(f"SoftwareFJ.{id(self)}")
        self.logger.setLevel(logging.INFO)
        self.logger.propagate = False

        if not self.logger.handlers:
            handler = logging.FileHandler(ruta, encoding="utf-8")
            formato = logging.Formatter(
                "%(asctime)s | %(levelname)s | %(message)s"
            )
            handler.setFormatter(formato)
            self.logger.addHandler(handler)

    def registrar_cliente(self, cliente: Cliente):
        if not isinstance(cliente, Cliente):
            raise ValidacionError(
                "El objeto suministrado no es un Cliente."
            )

        duplicado = any(
            c.documento == cliente.documento
            or c.correo == cliente.correo
            for c in self.clientes
        )

        if duplicado:
            self.logger.warning(
                "Intento de registro duplicado: %s",
                cliente.documento
            )
            raise ClienteDuplicadoError(
                "Ya existe un cliente con ese documento o correo."
            )

        self.clientes.append(cliente)
        self.logger.info(
            "Cliente registrado: %s", cliente.identificador
        )

        return cliente

    def registrar_servicio(self, servicio: Servicio):
        if not isinstance(servicio, Servicio):
            raise ValidacionError(
                "El objeto suministrado no es un Servicio."
            )

        if any(
            s.identificador == servicio.identificador
            for s in self.servicios
        ):
            raise ValidacionError(
                "Ya existe un servicio con ese identificador."
            )

        self.servicios.append(servicio)
        self.logger.info(
            "Servicio registrado: %s", servicio.identificador
        )

        return servicio

    def crear_reserva(
        self, identificador, id_cliente, id_servicio,
        duracion, **parametros
    ):
        try:
            cliente = next(
                c for c in self.clientes
                if c.identificador == id_cliente
            )

            servicio = next(
                s for s in self.servicios
                if s.identificador == id_servicio
            )

        except StopIteration as exc:
            self.logger.exception(
                "No se pudo crear la reserva por referencia inexistente."
            )
            raise RecursoNoEncontradoError(
                "Cliente o servicio no encontrado."
            ) from exc

        if any(
            r.identificador == identificador
            for r in self.reservas
        ):
            raise ValidacionError(
                "El identificador de reserva ya está registrado."
            )

        reserva = Reserva(
            identificador,
            cliente,
            servicio,
            duracion,
            parametros
        )

        self.reservas.append(reserva)
        self.logger.info(
            "Reserva creada: %s", identificador
        )

        return reserva

    def buscar_cliente(self, identificador):
        for cliente in self.clientes:
            if cliente.identificador == identificador:
                return cliente

        raise RecursoNoEncontradoError(
            f"No existe el cliente {identificador}."
        )

    def listar_reservas(self):
        return [
            reserva.resumen()
            for reserva in self.reservas
        ]

    def cerrar(self):
        """Cierra los archivos de registro."""
        for handler in self.logger.handlers[:]:
            handler.flush()
            handler.close()
            self.logger.removeHandler(handler)
