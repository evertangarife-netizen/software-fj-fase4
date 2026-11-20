"""
Script principal de ejecución y validación del Sistema Software FJ.
Simula 12 operaciones completas (exitosas y fallidas) verificando estabilidad y logs.
"""
from sistema_gestion import SistemaSoftwareFJ
from servicios import ReservaSala, AlquilerEquipo, AsesoriaEspecializada


def ejecutar_simulacion():
    sistema = SistemaSoftwareFJ("software_fj.log")
    print("\n--- INICIANDO SIMULACIÓN DE 12 OPERACIONES EN SOFTWARE FJ ---\n")

    # OPERACIÓN 1: Registro válido de cliente 1
    print("Op 1: Registrar cliente válido (Laura Gómez)")
    cli1 = sistema.registrar_cliente("CLI-01", "Laura Gómez", "10203040", "laura.gomez@correo.com", "3105551234")

    # OPERACIÓN 2: Registro inválido de cliente (correo mal formado)
    print("\nOp 2: Registrar cliente con correo inválido")
    sistema.registrar_cliente("CLI-02", "Carlos Ruiz", "99887766", "correo_invalido.com", "3204449876")

    # OPERACIÓN 3: Registro inválido de cliente (parámetro faltante)
    print("\nOp 3: Registrar cliente con nombre faltante")
    sistema.registrar_cliente("CLI-03", "", "55443322", "ana@correo.com", "3157778899")

    # OPERACIÓN 4: Registro válido de cliente 2
    print("\nOp 4: Registrar segundo cliente válido (Andrés Silva)")
    cli2 = sistema.registrar_cliente("CLI-04", "Andrés Silva", "80706050", "andres.silva@empresa.co", "3009998877")

    # OPERACIÓN 5: Creación válida de Sala (Servicio 1)
    print("\nOp 5: Crear servicio válido - Reserva de Sala")
    sala1 = sistema.registrar_servicio(
        ReservaSala, "SRV-S01", "Sala Innovación A", 80000, 12, True
    )

    # OPERACIÓN 6: Creación inválida de Alquiler de Equipo (tarifa negativa)
    print("\nOp 6: Crear servicio inválido - Alquiler de Equipo con tarifa negativa")
    sistema.registrar_servicio(
        AlquilerEquipo, "SRV-E99", "Portátil Gamer", -50000, "Cómputo", 3
    )

    # OPERACIÓN 7: Creación válida de Alquiler de Equipo (Servicio 2)
    print("\nOp 7: Crear servicio válido - Alquiler de Equipos")
    equipo1 = sistema.registrar_servicio(
        AlquilerEquipo, "SRV-E01", "Laptop Dell Latitude", 45000, "Cómputo", 2
    )

    # OPERACIÓN 8: Creación válida de Asesoría Especializada (Servicio 3)
    print("\nOp 8: Crear servicio válido - Asesoría Especializada")
    asesoria1 = sistema.registrar_servicio(
        AsesoriaEspecializada, "SRV-A01", "Arquitectura Cloud", 150000, "Nube AWS", "Ing. Mateo Rojas"
    )

    # OPERACIÓN 9: Reserva exitosa + procesamiento con sobrecarga (catering y descuento 10%)
    print("\nOp 9: Reservar y procesar Sala Innovación A (con catering y 10% de descuento)")
    res1 = sistema.crear_y_confirmar_reserva("RES-001", cli1, sala1, 3)
    sistema.procesar_reserva(res1, impuesto=0.19, descuento=0.10, servicio_catering=True)

    # OPERACIÓN 10: Reserva fallida (intento de reservar la misma sala ya ocupada)
    print("\nOp 10: Intentar reservar Sala Innovación A mientras está ocupada (Servicio no disponible)")
    sistema.crear_y_confirmar_reserva("RES-002", cli2, sala1, 2)

    # OPERACIÓN 11: Reserva exitosa de Equipos + intento de cobro con descuento inconsistente (90%)
    print("\nOp 11: Reservar equipos y probar cálculo con descuento inválido (90%)")
    res3 = sistema.crear_y_confirmar_reserva("RES-003", cli2, equipo1, 4)
    sistema.procesar_reserva(res3, impuesto=0.19, descuento=0.90, incluir_seguro=True)
    # Corrección controlada tras el error: procesar con descuento válido (15%)
    print("       -> Reintentando cobro con descuento válido (15%):")
    sistema.procesar_reserva(res3, impuesto=0.19, descuento=0.15, incluir_seguro=True)

    # OPERACIÓN 12: Reserva de Asesoría, cancelación exitosa e intento inválido de procesar cancelada
    print("\nOp 12: Reservar Asesoría, cancelarla y luego intentar procesarla (operación no permitida)")
    res4 = sistema.crear_y_confirmar_reserva("RES-004", cli1, asesoria1, 2)
    sistema.cancelar_reserva(res4)
    sistema.procesar_reserva(res4, impuesto=0.19, es_urgente=True)

    # Reporte final demostrando que la aplicación terminó estable y sin interrupciones
    sistema.mostrar_reporte_general()
    print("\nConsulta el archivo 'software_fj.log' generado en esta carpeta para revisar la auditoría completa.")


if __name__ == "__main__":
    ejecutar_simulacion()