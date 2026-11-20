"""
Módulo de gestión de reservas.
Aplica manejo avanzado de excepciones: try/except/else, try/except/finally y encadenamiento.
"""
from entidad import Entidad
from cliente import Cliente
from servicios import Servicio
from gestor_logs import GestorLogs
from excepciones import (
    ErrorDatosInvalidos,
    ErrorServicioNoDisponible,
    ErrorOperacionNoPermitida,
    ErrorReservaIncorrecta,
    ErrorCalculoInconsistente,
)


class Reserva(Entidad):
    """Integra un Cliente, un Servicio, la duración y el ciclo de vida de una reserva."""

    ESTADOS_VALIDOS = ("PENDIENTE", "CONFIRMADA", "PROCESADA", "CANCELADA")

    def __init__(self, id_reserva: str, cliente: Cliente, servicio: Servicio, duracion: int, logs: GestorLogs):
        super().__init__(id_reserva)

        if not isinstance(cliente, Cliente):
            raise ErrorDatosInvalidos("La reserva requiere un objeto Cliente válido.")
        if not isinstance(servicio, Servicio):
            raise ErrorDatosInvalidos("La reserva requiere un objeto Servicio válido.")
        if not isinstance(duracion, int) or duracion <= 0:
            raise ErrorDatosInvalidos("La duración de la reserva debe ser un número entero positivo.")

        self.__cliente = cliente
        self.__servicio = servicio
        self.__duracion = duracion
        self.__estado = "PENDIENTE"
        self.__costo_total = 0.0
        self.__logs = logs

    @property
    def estado(self) -> str:
        return self.__estado

    @property
    def costo_total(self) -> float:
        return self.__costo_total

    @property
    def servicio(self) -> Servicio:
        return self.__servicio

    def confirmar(self) -> None:
        """
        Confirma la reserva verificando disponibilidad del servicio.
        Usa el bloque try/except/else/finally.
        """
        try:
            if self.__estado != "PENDIENTE":
                raise ErrorOperacionNoPermitida(
                    f"No se puede confirmar la reserva {self.id_entidad} porque está en estado '{self.__estado}'."
                )
            if not self.__servicio.disponible:
                raise ErrorServicioNoDisponible(
                    f"El servicio '{self.__servicio.nombre}' no está disponible actualmente."
                )
        except (ErrorOperacionNoPermitida, ErrorServicioNoDisponible) as error:
            self.__logs.registrar_error(f"Error al confirmar reserva {self.id_entidad}", error)
            # Encadenamiento de excepciones preservando el error original
            raise ErrorReservaIncorrecta(f"Confirmación rechazada para reserva {self.id_entidad}.") from error
        else:
            # Solo se ejecuta si el bloque try finalizó sin excepciones
            self.__servicio.disponible = False
            self.__estado = "CONFIRMADA"
            self.__logs.registrar_info(
                f"Reserva {self.id_entidad} CONFIRMADA para {self.__cliente.nombre} -> {self.__servicio.nombre}"
            )
        finally:
            # Se ejecuta siempre, con o sin error, para trazabilidad
            self.__logs.registrar_info(
                f"[Auditoría] Intento de confirmación finalizado para {self.id_entidad}. Estado actual: {self.__estado}"
            )

    def procesar(self, impuesto: float = 0.19, descuento: float = 0.0, **extras) -> float:
        """
        Calcula el costo total usando polimorfismo y sobrecarga simulada.
        Usa try/except/else y encadenamiento de excepciones ante cálculos inconsistentes.
        """
        try:
            if self.__estado != "CONFIRMADA":
                raise ErrorOperacionNoPermitida(
                    f"Solo se pueden procesar reservas CONFIRMADAS. Estado actual: '{self.__estado}'."
                )
            # Llamada polimórfica al método calcular_costo del servicio concreto
            costo = self.__servicio.calcular_costo(
                duracion=self.__duracion,
                impuesto=impuesto,
                descuento=descuento,
                **extras
            )
        except (ErrorOperacionNoPermitida, ErrorCalculoInconsistente) as error:
            self.__logs.registrar_error(f"Fallo al procesar cobro de reserva {self.id_entidad}", error)
            raise ErrorReservaIncorrecta(f"No se pudo procesar la reserva {self.id_entidad}.") from error
        else:
            self.__costo_total = costo
            self.__estado = "PROCESADA"
            self.__logs.registrar_info(
                f"Reserva {self.id_entidad} PROCESADA exitosamente. Total cobrado: ${self.__costo_total:,.2f}"
            )
            return self.__costo_total

    def cancelar(self) -> None:
        """
        Cancela la reserva y libera el servicio si estaba bloqueado.
        Usa try/except/finally.
        """
        try:
            if self.__estado in ("CANCELADA", "PROCESADA"):
                raise ErrorOperacionNoPermitida(
                    f"No es posible cancelar una reserva en estado '{self.__estado}'."
                )
            if self.__estado == "CONFIRMADA":
                # Libera el servicio para que otro cliente pueda reservarlo
                self.__servicio.disponible = True
            self.__estado = "CANCELADA"
            self.__logs.registrar_advertencia(f"Reserva {self.id_entidad} fue CANCELADA.")
        except ErrorOperacionNoPermitida as error:
            self.__logs.registrar_error(f"Intento inválido de cancelación en {self.id_entidad}", error)
            raise
        finally:
            self.__logs.registrar_info(
                f"[Auditoría] Proceso de cancelación cerrado para {self.id_entidad}. Estado: {self.__estado}"
            )

    def validar(self) -> bool:
        return self.__estado in self.ESTADOS_VALIDOS and self.__duracion > 0

    def obtener_resumen(self) -> str:
        return (
            f"Reserva [{self.id_entidad}] | Cliente: {self.__cliente.nombre} | "
            f"Servicio: {self.__servicio.nombre} | Duración: {self.__duracion} | "
            f"Estado: {self.__estado} | Total: ${self.__costo_total:,.2f}"
        )