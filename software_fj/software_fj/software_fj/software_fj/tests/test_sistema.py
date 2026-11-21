
"""Pruebas unitarias del sistema Software FJ."""

import tempfile
import unittest
from pathlib import Path

from software_fj import (
    Cliente,
    ReservaSala,
    AlquilerEquipo,
    Asesoria,
    SistemaFJ,
)

from software_fj.excepciones import (
    ValidacionError,
    ClienteDuplicadoError,
    EstadoReservaError,
)


class SistemaFJTests(unittest.TestCase):

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()

        self.sistema = SistemaFJ(
            Path(self.temp.name) / "test.log"
        )

        self.cliente = self.sistema.registrar_cliente(
            Cliente(
                "C1",
                "María López",
                "12345678",
                "maria@test.com",
                "3001234567"
            )
        )

        self.sala = self.sistema.registrar_servicio(
            ReservaSala("S1", "Sala A", 40000, 10)
        )

    def tearDown(self):
        self.sistema.cerrar()
        self.temp.cleanup()

    def test_cliente_invalido(self):
        with self.assertRaises(ValidacionError):
            Cliente(
                "C2",
                "Jo",
                "12345678",
                "mal-correo",
                "123"
            )

    def test_cliente_duplicado(self):
        with self.assertRaises(ClienteDuplicadoError):
            self.sistema.registrar_cliente(
                Cliente(
                    "C3",
                    "Otro Nombre",
                    "12345678",
                    "otro@test.com",
                    "3001234567"
                )
            )

    def test_confirmar_y_procesar_reserva(self):
        reserva = self.sistema.crear_reserva(
            "R1", "C1", "S1", 2, asistentes=5
        )

        self.assertGreater(reserva.confirmar(), 0)
        self.assertEqual(
            reserva.procesar(),
            reserva.costo
        )

    def test_reserva_no_confirmada_no_se_procesa(self):
        reserva = self.sistema.crear_reserva(
            "R2", "C1", "S1", 1, asistentes=3
        )

        with self.assertRaises(EstadoReservaError):
            reserva.procesar()

    def test_validar_capacidad_de_sala(self):
        reserva = self.sistema.crear_reserva(
            "R3", "C1", "S1", 1, asistentes=20
        )

        with self.assertRaises(ValidacionError):
            reserva.confirmar()

    def test_polimorfismo_de_servicios(self):
        servicios = [
            self.sala,
            AlquilerEquipo("S2", "Portátil", 10000, 3),
            Asesoria("S3", "Asesoría", 50000, "software"),
        ]

        for servicio in servicios:
            self.assertGreater(
                servicio.calcular_costo(1),
                0
            )
            self.assertTrue(servicio.describir())


if __name__ == "__main__":
    unittest.main()
