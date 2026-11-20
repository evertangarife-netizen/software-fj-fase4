"""
Módulo base que define la abstracción general para las entidades del sistema.
"""
from abc import ABC, abstractmethod
from datetime import datetime
from excepciones import ErrorParametroFaltante, ErrorDatosInvalidos


class Entidad(ABC):
    """Clase abstracta que representa cualquier entidad gestionada por Software FJ."""

    def __init__(self, id_entidad: str):
        # Valida que el identificador exista y sea una cadena no vacía
        if id_entidad is None or str(id_entidad).strip() == "":
            raise ErrorParametroFaltante("El ID de la entidad es obligatorio y no puede estar vacío.")
        if not isinstance(id_entidad, str):
            raise ErrorDatosInvalidos("El ID de la entidad debe ser una cadena de texto.")

        # Atributos encapsulados comunes a toda entidad
        self._id_entidad = id_entidad.strip()
        self._fecha_creacion = datetime.now()

    @property
    def id_entidad(self) -> str:
        """Retorna el identificador único de la entidad."""
        return self._id_entidad

    @property
    def fecha_creacion(self) -> datetime:
        """Retorna la fecha y hora de creación de la entidad."""
        return self._fecha_creacion

    @abstractmethod
    def validar(self) -> bool:
        """Método abstracto que obliga a validar la consistencia interna de cada entidad."""
        pass

    @abstractmethod
    def obtener_resumen(self) -> str:
        """Método abstracto que retorna una descripción legible de la entidad."""
        pass