"""
Módulo controlador del sistema Software FJ.
Gestiona clientes, servicios y reservas únicamente mediante objetos y listas en memoria.
"""
from typing import List, Optional
from cliente import Cliente
from servicios import Servicio
from reserva import Reserva
from gestor_logs import GestorLogs
from excepciones import ErrorSoftwareFJ, ErrorDatosInvalidos


class SistemaSoftwareFJ:
    """Controlador principal del sistema sin uso de bases de datos."""

    def __init__(self, archivo_log: str = "software_fj.log"):
        # Listas internas en memoria (sin motor de base de datos)
        self.__clientes: List[Cliente] = []
        self.__servicios: List[Servicio] = []
        self.__reservas: List[Reserva] = []
        self.__logs = GestorLogs(archivo_log)
        self.__logs.registrar_info("=== Inicio de sesión del Sistema Software FJ ===")

    def registrar_cliente(self, id_c: str, nombre: str, documento: str, correo: str, telefono: str) -> Optional[Cliente]:
        """Crea y almacena un cliente en la lista interna controlando excepciones."""
        try:
            # Verifica que no exista un cliente con el mismo ID o documento
            if any(c.id_entidad == id_c or c.documento == documento for c in self.__clientes):
                raise ErrorDatosInvalidos(f"Ya existe un cliente con ID '{id_c}' o documento '{documento}'.")
            nuevo_cliente = Cliente(id_c, nombre, documento, correo, telefono)
        except ErrorSoftwareFJ as error:
            self.__logs.registrar_error(f"Error al registrar cliente '{nombre}'", error)
            print(f"[ERROR CONTROLADO] Registro de cliente fallido: {error}")
            return None
        else:
            self.__clientes.append(nuevo_cliente)
            self.__logs.registrar_info(f"Cliente registrado: {nuevo_cliente.obtener_resumen()}")
            print(f"[OK] {nuevo_cliente.obtener_resumen()}")
            return nuevo_cliente

    def registrar_servicio(self, constructor_servicio, *args, **kwargs) -> Optional[Servicio]:
        """Instancia y registra cualquier subclase de Servicio usando polimorfismo."""
        try:
            nuevo_servicio = constructor_servicio(*args, **kwargs)
            if any(s.id_entidad == nuevo_servicio.id_entidad for s in self.__servicios):
                raise ErrorDatosInvalidos(f"Ya existe un servicio con ID '{nuevo_servicio.id_entidad}'.")
        except ErrorSoftwareFJ as error:
            self.__logs.registrar_error("Error al crear servicio", error)
            print(f"[ERROR CONTROLADO] Creación de servicio fallida: {error}")
            return None
        else:
            self.__servicios.append(nuevo_servicio)
            self.__logs.registrar_info(f"Servicio creado: {nuevo_servicio.describir()}")
            print(f"[OK] {nuevo_servicio.describir()}")
            return nuevo_servicio

    def crear_y_confirmar_reserva(self, id_r: str, cliente: Cliente, servicio: Servicio, duracion: int) -> Optional[Reserva]:
        """Crea y confirma una reserva protegiendo la continuidad del sistema."""
        try:
            reserva = Reserva(id_r, cliente, servicio, duracion, self.__logs)
            reserva.confirmar()
        except ErrorSoftwareFJ as error:
            causa = f" (Causa: {error.__cause__})" if error.__cause__ else ""
            print(f"[ERROR CONTROLADO] Reserva {id_r} fallida: {error}{causa}")
            return None
        else:
            self.__reservas.append(reserva)
            print(f"[OK] Reserva confirmada: {reserva.obtener_resumen()}")
            return reserva

    def procesar_reserva(self, reserva: Reserva, impuesto: float = 0.19, descuento: float = 0.0, **extras) -> None:
        """Procesa el cobro de una reserva con parámetros opcionales."""
        try:
            if reserva is None:
                raise ErrorDatosInvalidos("No se puede procesar una reserva nula.")
            total = reserva.procesar(impuesto=impuesto, descuento=descuento, **extras)
        except ErrorSoftwareFJ as error:
            causa = f" (Causa: {error.__cause__})" if error.__cause__ else ""
            print(f"[ERROR CONTROLADO] Procesamiento fallido: {error}{causa}")
        else:
            print(f"[OK] Cobro procesado para {reserva.id_entidad}: Total = ${total:,.2f}")

    def cancelar_reserva(self, reserva: Reserva) -> None:
        """Cancela una reserva existente controlando estados inválidos."""
        try:
            if reserva is None:
                raise ErrorDatosInvalidos("No se puede cancelar una reserva nula.")
            reserva.cancelar()
        except ErrorSoftwareFJ as error:
            print(f"[ERROR CONTROLADO] Cancelación rechazada: {error}")
        else:
            print(f"[OK] Reserva {reserva.id_entidad} cancelada correctamente.")

    def mostrar_reporte_general(self) -> None:
        """Imprime el resumen actual de todas las listas en memoria."""
        print("\n" + "=" * 75)
        print("REPORTE FINAL EN MEMORIA - SOFTWARE FJ (SIN BASE DE DATOS)")
        print("=" * 75)
        print(f"Total Clientes válidos : {len(self.__clientes)}")
        for c in self.__clientes:
            print(f"  - {c.obtener_resumen()}")

        print(f"\nTotal Servicios válidos: {len(self.__servicios)}")
        for s in self.__servicios:
            print(f"  - {s.describir()}")

        print(f"\nTotal Reservas activas : {len(self.__reservas)}")
        for r in self.__reservas:
            print(f"  - {r.obtener_resumen()}")
        print("=" * 75)
        self.__logs.registrar_info("=== Fin de ejecución controlada del Sistema Software FJ ===")