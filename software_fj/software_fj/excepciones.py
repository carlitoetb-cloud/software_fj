
"""Excepciones personalizadas del sistema Software FJ."""


class SoftwareFJError(Exception):
    """Excepción base de la aplicación."""


class ValidacionError(SoftwareFJError):
    """Se presenta cuando un dato no cumple las reglas."""


class ClienteDuplicadoError(SoftwareFJError):
    """Se presenta cuando un cliente ya está registrado."""


class ServicioNoDisponibleError(SoftwareFJError):
    """Se presenta cuando un servicio o recurso no está disponible."""


class ReservaError(SoftwareFJError):
    """Excepción general relacionada con las reservas."""


class EstadoReservaError(ReservaError):
    """Se presenta cuando una operación no corresponde al estado de la reserva."""


class RecursoNoEncontradoError(SoftwareFJError):
    """Se presenta cuando no se encuentra un cliente o servicio."""
