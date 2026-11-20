"""
Módulo de excepciones personalizadas para el sistema de Software FJ.
Permite identificar, clasificar y controlar errores específicos del negocio.
"""


class ErrorSoftwareFJ(Exception):
    """Excepción base para todos los errores controlados de Software FJ."""
    pass


class ErrorParametroFaltante(ErrorSoftwareFJ):
    """Se lanza cuando falta un dato obligatorio o llega vacío."""
    pass


class ErrorDatosInvalidos(ErrorSoftwareFJ):
    """Se lanza cuando un dato incumple el formato, tipo o rango válido."""
    pass


class ErrorServicioNoDisponible(ErrorSoftwareFJ):
    """Se lanza al intentar reservar un servicio que ya está ocupado o inactivo."""
    pass


class ErrorOperacionNoPermitida(ErrorSoftwareFJ):
    """Se lanza cuando se intenta una acción inválida según el estado actual."""
    pass


class ErrorReservaIncorrecta(ErrorSoftwareFJ):
    """Se lanza cuando falla la creación, confirmación o procesamiento de una reserva."""
    pass


class ErrorCalculoInconsistente(ErrorSoftwareFJ):
    """Se lanza cuando los parámetros de cálculo (impuestos/descuentos) son incoherentes."""
    pass