"""
Módulo de gestión de clientes con encapsulación y validaciones robustas.
"""
import re
from entidad import Entidad
from excepciones import ErrorParametroFaltante, ErrorDatosInvalidos


class Cliente(Entidad):
    """Representa un cliente de Software FJ con protección de datos personales."""

    def __init__(self, id_cliente: str, nombre: str, documento: str, correo: str, telefono: str):
        # Invoca el constructor de la clase abstracta Entidad
        super().__init__(id_cliente)

        # Asignación mediante setters para garantizar validaciones desde la creación
        self.nombre = nombre
        self.documento = documento
        self.correo = correo
        self.telefono = telefono
        self.validar()

    @property
    def nombre(self) -> str:
        return self.__nombre

    @nombre.setter
    def nombre(self, valor: str) -> None:
        if valor is None or str(valor).strip() == "":
            raise ErrorParametroFaltante("El nombre del cliente es obligatorio.")
        if len(valor.strip()) < 3:
            raise ErrorDatosInvalidos("El nombre del cliente debe tener al menos 3 caracteres.")
        self.__nombre = valor.strip()

    @property
    def documento(self) -> str:
        return self.__documento

    @documento.setter
    def documento(self, valor: str) -> None:
        if valor is None or str(valor).strip() == "":
            raise ErrorParametroFaltante("El documento de identidad es obligatorio.")
        if not str(valor).strip().isdigit() or not (6 <= len(str(valor).strip()) <= 15):
            raise ErrorDatosInvalidos("El documento debe contener únicamente entre 6 y 15 dígitos.")
        self.__documento = str(valor).strip()

    @property
    def correo(self) -> str:
        return self.__correo

    @correo.setter
    def correo(self, valor: str) -> None:
        if valor is None or str(valor).strip() == "":
            raise ErrorParametroFaltante("El correo electrónico es obligatorio.")
        # Expresión regular para verificar formato estándar de correo
        patron = r"^[\w\.-]+@[\w\.-]+\.\w{2,}$"
        if not re.match(patron, valor.strip()):
            raise ErrorDatosInvalidos(f"El correo '{valor}' no tiene un formato válido.")
        self.__correo = valor.strip().lower()

    @property
    def telefono(self) -> str:
        return self.__telefono

    @telefono.setter
    def telefono(self, valor: str) -> None:
        if valor is None or str(valor).strip() == "":
            raise ErrorParametroFaltante("El teléfono de contacto es obligatorio.")
        if not str(valor).strip().isdigit() or len(str(valor).strip()) < 7:
            raise ErrorDatosInvalidos("El teléfono debe contener al menos 7 dígitos numéricos.")
        self.__telefono = str(valor).strip()

    def validar(self) -> bool:
        """Verifica que todos los atributos encapsulados estén correctamente definidos."""
        return all([self.__nombre, self.__documento, self.__correo, self.__telefono])

    def obtener_resumen(self) -> str:
        """Sobrescribe el método abstracto para mostrar los datos del cliente."""
        return f"Cliente [{self.id_entidad}] {self.__nombre} | Doc: {self.__documento} | Email: {self.__correo}"