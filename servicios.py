"""
Módulo de servicios de Software FJ.
Implementa abstracción, herencia, polimorfismo y sobrecarga simulada de métodos.
"""
from abc import abstractmethod
from entidad import Entidad
from excepciones import (
    ErrorParametroFaltante,
    ErrorDatosInvalidos,
    ErrorCalculoInconsistente,
)


class Servicio(Entidad):
    """Clase abstracta base para todos los servicios ofrecidos por Software FJ."""

    def __init__(self, id_servicio: str, nombre: str, tarifa_base: float):
        super().__init__(id_servicio)
        if nombre is None or str(nombre).strip() == "":
            raise ErrorParametroFaltante("El nombre del servicio es obligatorio.")
        if not isinstance(tarifa_base, (int, float)) or tarifa_base <= 0:
            raise ErrorDatosInvalidos("La tarifa base debe ser un valor numérico mayor que cero.")

        self._nombre = nombre.strip()
        self._tarifa_base = float(tarifa_base)
        self._disponible = True

    @property
    def nombre(self) -> str:
        return self._nombre

    @property
    def tarifa_base(self) -> float:
        return self._tarifa_base

    @property
    def disponible(self) -> bool:
        return self._disponible

    @disponible.setter
    def disponible(self, estado: bool) -> None:
        if not isinstance(estado, bool):
            raise ErrorDatosInvalidos("La disponibilidad debe ser un valor booleano (True/False).")
        self._disponible = estado

    def validar_parametros_calculo(self, duracion: int, impuesto: float, descuento: float) -> None:
        """Valida coherencia numérica para evitar cálculos inconsistentes."""
        if not isinstance(duracion, (int, float)) or duracion <= 0:
            raise ErrorCalculoInconsistente("La duración debe ser un número positivo mayor a cero.")
        if not (0.0 <= impuesto <= 0.50):
            raise ErrorCalculoInconsistente("El impuesto debe estar entre 0% (0.0) y 50% (0.50).")
        if not (0.0 <= descuento <= 0.60):
            raise ErrorCalculoInconsistente("El descuento permitido debe estar entre 0% (0.0) y 60% (0.60).")

    @abstractmethod
    def calcular_costo(self, duracion: int, impuesto: float = 0.19, descuento: float = 0.0, **extras) -> float:
        """
        Método polimórfico con sobrecarga simulada mediante parámetros opcionales:
        permite calcular el costo solo con duración, con impuestos, con descuentos
        o con cargos adicionales específicos de cada servicio (**extras).
        """
        pass

    @abstractmethod
    def describir(self) -> str:
        """Retorna una descripción especializada del servicio."""
        pass

    @abstractmethod
    def validar_parametros(self) -> bool:
        """Valida los parámetros particulares de cada tipo de servicio."""
        pass

    def validar(self) -> bool:
        return self.validar_parametros()

    def obtener_resumen(self) -> str:
        return self.describir()


class ReservaSala(Servicio):
    """Servicio especializado para reserva de salas de reuniones o capacitación."""

    def __init__(self, id_servicio: str, nombre: str, tarifa_hora: float, capacidad: int, tiene_proyector: bool = True):
        self._capacidad = capacidad
        self._tiene_proyector = tiene_proyector
        super().__init__(id_servicio, nombre, tarifa_hora)
        self.validar_parametros()

    def validar_parametros(self) -> bool:
        if not isinstance(self._capacidad, int) or self._capacidad <= 0:
            raise ErrorDatosInvalidos("La capacidad de la sala debe ser un entero mayor a cero.")
        if not isinstance(self._tiene_proyector, bool):
            raise ErrorDatosInvalidos("El parámetro 'tiene_proyector' debe ser booleano.")
        return True

    def calcular_costo(self, duracion: int, impuesto: float = 0.19, descuento: float = 0.0, **extras) -> float:
        """
        Calcula costo por horas.
        Sobrecarga opcional en **extras: servicio_catering=True (+50.000 COP).
        """
        self.validar_parametros_calculo(duracion, impuesto, descuento)
        subtotal = self._tarifa_base * duracion
        # Recargo por proyector integrado
        if self._tiene_proyector:
            subtotal += 15000.0
        # Parámetro opcional adicional (sobrecarga)
        if extras.get("servicio_catering", False):
            subtotal += 50000.0

        monto_descuento = subtotal * descuento
        base_gravable = subtotal - monto_descuento
        total = base_gravable * (1 + impuesto)
        return round(total, 2)

    def describir(self) -> str:
        estado = "Disponible" if self._disponible else "Ocupada"
        proyector = "Sí" if self._tiene_proyector else "No"
        return (
            f"[Sala] {self._nombre} (ID: {self.id_entidad}) | Capacidad: {self._capacidad} pers. | "
            f"Proyector: {proyector} | Tarifa/h: ${self._tarifa_base:,.2f} | Estado: {estado}"
        )


class AlquilerEquipo(Servicio):
    """Servicio especializado para alquiler de equipos tecnológicos."""

    def __init__(self, id_servicio: str, nombre: str, tarifa_dia: float, categoria: str, unidades: int):
        self._categoria = categoria
        self._unidades = unidades
        super().__init__(id_servicio, nombre, tarifa_dia)
        self.validar_parametros()

    def validar_parametros(self) -> bool:
        if self._categoria is None or str(self._categoria).strip() == "":
            raise ErrorParametroFaltante("La categoría del equipo es obligatoria.")
        if not isinstance(self._unidades, int) or self._unidades <= 0:
            raise ErrorDatosInvalidos("La cantidad de unidades debe ser un entero mayor que cero.")
        return True

    def calcular_costo(self, duracion: int, impuesto: float = 0.19, descuento: float = 0.0, **extras) -> float:
        """
        Calcula costo por días y unidades.
        Sobrecarga opcional en **extras: incluir_seguro=True (+10% del subtotal).
        """
        self.validar_parametros_calculo(duracion, impuesto, descuento)
        subtotal = self._tarifa_base * duracion * self._unidades
        if extras.get("incluir_seguro", False):
            subtotal += subtotal * 0.10

        base_gravable = subtotal * (1 - descuento)
        total = base_gravable * (1 + impuesto)
        return round(total, 2)

    def describir(self) -> str:
        estado = "Disponible" if self._disponible else "Alquilado"
        return (
            f"[Equipo] {self._nombre} ({self._categoria}, ID: {self.id_entidad}) | "
            f"Unidades: {self._unidades} | Tarifa/día: ${self._tarifa_base:,.2f} | Estado: {estado}"
        )


class AsesoriaEspecializada(Servicio):
    """Servicio especializado para consultorías y asesorías técnicas."""

    def __init__(self, id_servicio: str, nombre: str, tarifa_hora: float, area: str, consultor: str):
        self._area = area
        self._consultor = consultor
        super().__init__(id_servicio, nombre, tarifa_hora)
        self.validar_parametros()

    def validar_parametros(self) -> bool:
        if not self._area or not str(self._area).strip():
            raise ErrorParametroFaltante("El área de especialización de la asesoría es obligatoria.")
        if not self._consultor or not str(self._consultor).strip():
            raise ErrorParametroFaltante("El nombre del consultor asignado es obligatorio.")
        return True

    def calcular_costo(self, duracion: int, impuesto: float = 0.19, descuento: float = 0.0, **extras) -> float:
        """
        Calcula costo por horas de asesoría.
        Sobrecarga opcional en **extras: es_urgente=True (+25% recargo por prioridad).
        """
        self.validar_parametros_calculo(duracion, impuesto, descuento)
        subtotal = self._tarifa_base * duracion
        if extras.get("es_urgente", False):
            subtotal *= 1.25

        base_gravable = subtotal * (1 - descuento)
        total = base_gravable * (1 + impuesto)
        return round(total, 2)

    def describir(self) -> str:
        estado = "Disponible" if self._disponible else "Asignada"
        return (
            f"[Asesoría] {self._nombre} | Área: {self._area} | Consultor: {self._consultor} | "
            f"Tarifa/h: ${self._tarifa_base:,.2f} | Estado: {estado}"
        )