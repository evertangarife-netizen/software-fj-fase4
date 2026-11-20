"""
Módulo de registro de eventos y errores (Logs).
Único componente con persistencia en archivo plano para auditoría del sistema.
"""
import logging


class GestorLogs:
    """Centraliza la escritura de eventos informativos y errores en un archivo .log."""

    def __init__(self, nombre_archivo: str = "software_fj.log"):
        # Configuración del logger con nombre único para evitar duplicados
        self._logger = logging.getLogger("SoftwareFJ")
        self._logger.setLevel(logging.DEBUG)

        # Evita agregar múltiples manejadores si se instancia varias veces
        if not self._logger.handlers:
            # Formato con fecha, nivel de severidad y mensaje detallado
            formato = logging.Formatter(
                "%(asctime)s | %(levelname)-8s | %(message)s",
                datefmt="%Y-%m-%d %H:%M:%S"
            )

            # Manejador para guardar en archivo de texto (UTF-8)
            manejador_archivo = logging.FileHandler(nombre_archivo, mode="a", encoding="utf-8")
            manejador_archivo.setLevel(logging.DEBUG)
            manejador_archivo.setFormatter(formato)
            self._logger.addHandler(manejador_archivo)

    def registrar_info(self, mensaje: str) -> None:
        """Registra una operación exitosa o evento informativo."""
        self._logger.info(mensaje)

    def registrar_advertencia(self, mensaje: str) -> None:
        """Registra una situación anómala controlada."""
        self._logger.warning(mensaje)

    def registrar_error(self, mensaje: str, excepcion: Exception = None) -> None:
        """Registra un error detallado incluyendo su causa encadenada si existe."""
        if excepcion is not None:
            causa = f" | Causa original: {type(excepcion.__cause__).__name__}: {excepcion.__cause__}" if excepcion.__cause__ else ""
            self._logger.error(f"{mensaje} -> [{type(excepcion).__name__}] {excepcion}{causa}")
        else:
            self._logger.error(mensaje)