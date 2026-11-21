
"""Programa principal de demostración del sistema Software FJ."""
import logging

from software_fj import (
    Cliente,
    ReservaSala,
    AlquilerEquipo,
    Asesoria,
    SistemaFJ,
)
from software_fj.excepciones import SoftwareFJError


def ejecutar_demo():
    sistema = SistemaFJ()
    operaciones = 0

    def ejecutar(etiqueta, accion):
        nonlocal operaciones
        operaciones += 1
        print(f"\n[{operaciones:02}] {etiqueta}")

        try:
            resultado = accion()
        except SoftwareFJError as exc:
            sistema.logger.exception("Operación controlada: %s", etiqueta)
            print(f"ERROR CONTROLADO: {exc}")
        except Exception as exc:
            sistema.logger.exception("Error inesperado: %s", etiqueta)
            print(f"ERROR INESPERADO: {exc}")
        else:
            sistema.logger.info("Operación exitosa: %s", etiqueta)
            print(resultado if resultado is not None else "Operación realizada.")
        finally:
            print("La aplicación continúa activa.")

    ejecutar(
        "Registrar cliente válido",
        lambda: sistema.registrar_cliente(
            Cliente(
                "C001", "Laura Méndez", "100200300",
                "laura@correo.com", "3001234567"
            )
        ).resumen()
    )

    ejecutar(
        "Intentar registrar correo inválido",
        lambda: Cliente(
            "C002", "Carlos Pérez", "100200301",
            "correo-invalido", "3001234568"
        )
    )

    ejecutar(
        "Registrar segundo cliente",
        lambda: sistema.registrar_cliente(
            Cliente(
                "C003", "Andrés Rojas", "100200302",
                "andres@correo.com", "3101234567"
            )
        ).resumen()
    )

    ejecutar(
        "Intentar documento duplicado",
        lambda: sistema.registrar_cliente(
            Cliente(
                "C004", "Otra Persona", "100200300",
                "otra@correo.com", "3001234569"
            )
        )
    )

    ejecutar(
        "Registrar sala de reuniones",
        lambda: sistema.registrar_servicio(
            ReservaSala("S001", "Sala de reuniones", 50000, 12)
        ).describir()
    )

    ejecutar(
        "Registrar alquiler de equipos",
        lambda: sistema.registrar_servicio(
            AlquilerEquipo("S002", "Proyector HD", 25000, 4)
        ).describir()
    )

    ejecutar(
        "Registrar asesoría especializada",
        lambda: sistema.registrar_servicio(
            Asesoria("S003", "Consultoría TI", 80000, "tecnología")
        ).describir()
    )

    ejecutar(
        "Intentar crear sala con tarifa negativa",
        lambda: ReservaSala("S004", "Sala inválida", -100, 10)
    )

    ejecutar(
        "Crear reserva de sala",
        lambda: sistema.crear_reserva(
            "R001", "C001", "S001", 2, asistentes=8
        ).resumen()
    )

    ejecutar(
        "Confirmar reserva de sala",
        lambda: f"Costo: ${sistema.reservas[0].confirmar():,.2f}"
    )

    ejecutar(
        "Procesar reserva confirmada",
        lambda: f"Procesada por ${sistema.reservas[0].procesar():,.2f}"
    )

    ejecutar(
        "Intentar cancelar reserva procesada",
        lambda: sistema.reservas[0].cancelar()
    )

    ejecutar(
        "Intentar reserva que supera capacidad",
        lambda: sistema.crear_reserva(
            "R002", "C003", "S001", 2, asistentes=30
        ).confirmar()
    )

    ejecutar(
        "Crear reserva de equipos",
        lambda: f"Costo: ${sistema.crear_reserva(
            'R003', 'C003', 'S002', 3, unidades=2
        ).confirmar(descuento=0.10, impuesto=0.19):,.2f}"
    )

    ejecutar(
        "Intentar alquilar más equipos de los disponibles",
        lambda: sistema.crear_reserva(
            "R004", "C001", "S002", 1, unidades=10
        ).confirmar()
    )

    ejecutar(
        "Crear reserva de asesoría",
        lambda: f"Costo: ${sistema.crear_reserva(
            'R005', 'C001', 'S003', 1.5,
            tema='Seguridad de redes'
        ).confirmar():,.2f}"
    )

    ejecutar(
        "Intentar reservar con cliente inexistente",
        lambda: sistema.crear_reserva(
            "R006", "C999", "S003", 1, tema="Redes"
        )
    )

    ejecutar(
        "Intentar crear reserva con duración negativa",
        lambda: sistema.crear_reserva(
            "R007", "C001", "S003", -2, tema="Redes"
        )
    )

    print("\n========== RESUMEN FINAL ==========")
    print(f"Operaciones ejecutadas: {operaciones}")
    print(f"Clientes registrados: {len(sistema.clientes)}")
    print(f"Servicios registrados: {len(sistema.servicios)}")
    print(f"Reservas creadas: {len(sistema.reservas)}")

    for reserva in sistema.listar_reservas():
        print(reserva)

    print("\nLos eventos quedaron registrados en logs/software_fj.log.")
    sistema.cerrar()


if __name__ == "__main__":
    ejecutar_demo()
