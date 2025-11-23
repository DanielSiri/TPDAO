"""
Script principal - Ejemplo de uso del sistema de gestión médica
"""

from datetime import date, time, datetime
from database import Database
from medico import Medico
from paciente import Paciente
from especialidad import Especialidad
from consultorio import Consultorio
from agenda import Agenda
from turno import Turno
from gestor_turno import GestorTurno
from receta import Receta
from detalle_receta import DetalleDeReceta
from historial_clinico import HistorialClinico
from medicamento import Medicamento
from laboratorio import Laboratorio
from notificacion import Notificacion
from enums import TipoLaboratorioEnum


def main():
    print("=" * 60)
    print("SISTEMA DE GESTIÓN MÉDICA - DEMOSTRACIÓN")
    print("=" * 60)
    
    # ========== INICIALIZAR BASE DE DATOS ==========
    print("\n🗄️  Inicializando base de datos...")
    db = Database()
    db.conectar("localhost:5432/hospital_db")
    print(f"   Estado: {db}")
    
    # ========== CREAR PERSONAS ==========
    print("\n📋 1. Creando personas del sistema...")
    
    medico = Medico(
        matricula=12345,
        nombre="Juan",
        apellido="Pérez",
        telefono="123456789",
        email="juan.perez@hospital.com",
        fecha_alta=date(2020, 1, 15)
    )
    print(f"   ✓ {medico}")
    
    paciente = Paciente(
        nro_paciente=1001,
        nombre="María",
        apellido="González",
        telefono="987654321",
        fecha_nacimiento=date(1990, 5, 15),
        direccion="Calle Falsa 123"
    )
    print(f"   ✓ {paciente}")
    
    # ========== ESPECIALIDADES ==========
    print("\n📚 2. Creando especialidades...")
    
    cardiologia = Especialidad(
        nro_especialidad=1,
        nombre="Cardiología",
        descripcion="Especialidad del corazón"
    )
    cardiologia.registrar_especialidad()
    
    medico.asignar_especialidad(cardiologia)
    print(f"   ✓ Especialidad asignada a {medico.get_nombre()}")
    
    # ========== CONSULTORIO ==========
    print("\n🏥 3. Creando consultorio...")
    
    consultorio = Consultorio(
        numero=101,
        piso=1,
        equipamiento="Completo - Ecocardiograma"
    )
    consultorio.registrar_consultorio()
    
    # ========== AGENDA ==========
    print("\n📅 4. Creando agenda...")
    
    agenda = Agenda(
        nro_agenda=1,
        medico=medico,
        consultorio=consultorio,
        dia_semana="Lunes",
        hora_inicio=time(9, 0),
        hora_fin=time(17, 0)
    )
    print(f"   ✓ {agenda}")
    consultorio.agregar_agenda(agenda)
    
    # ========== TURNO ==========
    print("\n⏰ 5. Creando y gestionando turno...")
    
    turno = Turno(
        nro_turno=5001,
        medico=medico,
        paciente=paciente,
        consultorio=consultorio,
        fecha=date(2025, 11, 25),
        hora=time(10, 30)
    )
    print(f"   ✓ {turno}")
    
    agenda.agregar_turno(turno)
    
    gestor = GestorTurno()
    gestor.registrar_turno(turno)
    
    print("\n   Transiciones de estado:")
    turno.programar_turno()
    turno.registrar_asistencia()
    
    # ========== HISTORIAL CLÍNICO ==========
    print("\n📝 6. Creando historial clínico...")
    
    historial = HistorialClinico(
        nro_historial=2001,
        turno=turno,
        paciente=paciente
    )
    print(f"   ✓ {historial}")
    
    historial.registrar_diagnostico("Arritmia cardíaca leve")
    historial.registrar_tratamiento("Medicación y seguimiento")
    
    # ========== FARMACIA ==========
    print("\n💊 7. Creando medicamentos y laboratorio...")
    
    laboratorio = Laboratorio(
        numero_laboratorio=1,
        nombre="Laboratorio Bayer",
        direccion="Av. Corrientes 1000",
        telefono="1123456789"
    )
    print(f"   ✓ {laboratorio}")
    
    medicamento1 = Medicamento(
        numero_medicamento=101,
        nombre="Digoxina",
        dosis="0.25 mg",
        formato="Comprimido"
    )
    medicamento1.registrar_medicamento()
    laboratorio.agregar_medicamento(medicamento1)
    
    medicamento2 = Medicamento(
        numero_medicamento=102,
        nombre="Metoprolol",
        dosis="50 mg",
        formato="Comprimido"
    )
    medicamento2.registrar_medicamento()
    laboratorio.agregar_medicamento(medicamento2)
    
    # ========== RECETA ==========
    print("\n📋 8. Creando receta...")
    
    receta = Receta(
        nro_receta=3001,
        fecha_emision=date.today(),
        observaciones="Tomar con comida"
    )
    print(f"   ✓ {receta}")
    
    detalle1 = DetalleDeReceta(
        nro_item=1,
        receta=receta,
        medicamento=medicamento1,
        indicacion="1 comprimido cada 24 horas"
    )
    detalle1.agregar_medicamento()
    
    detalle2 = DetalleDeReceta(
        nro_item=2,
        receta=receta,
        medicamento=medicamento2,
        indicacion="1 comprimido cada 12 horas"
    )
    detalle2.agregar_medicamento()
    
    historial.vincular_receta(receta)
    
    # ========== NOTIFICACIÓN ==========
    print("\n📲 9. Creando notificación...")
    
    notificacion = Notificacion(
        nro_notificacion=4001,
        turno=turno,
        fecha_hora_envio=datetime(2025, 11, 24, 18, 0)
    )
    print(f"   ✓ {notificacion}")
    
    notificacion.enviar_recordatorio()
    
    # ========== RESUMEN FINAL ==========
    print("\n" + "=" * 60)
    print("📊 RESUMEN DEL SISTEMA")
    print("=" * 60)
    
    print(f"\n👨‍⚕️  Médico: {medico}")
    print(f"   Especialidades: {[e.get_nombre() for e in medico.get_especialidades()]}")
    print(f"   Turnos: {len(medico.get_turnos())}")
    
    print(f"\n👤 Paciente: {paciente}")
    print(f"   Turnos: {len(paciente.get_turnos())}")
    print(f"   Historiales: {len(paciente.get_historiales())}")
    
    print(f"\n🏥 Consultorio: {consultorio}")
    print(f"   Equipamiento: {consultorio.get_equipamiento()}")
    
    print(f"\n⏰ Turno: {turno}")
    print(f"   Notificaciones: {len(turno.get_notificaciones())}")
    print(f"   Cambios de estado: {len(turno.get_cambios_estado())}")
    
    print(f"\n💊 Laboratorio: {laboratorio}")
    print(f"   Medicamentos: {[m.get_nombre() for m in laboratorio.get_medicamentos()]}")
    
    print(f"\n📋 Receta: {receta}")
    print(f"   Detalles: {[f'{d.get_medicamento().get_nombre()}' for d in receta.get_detalles()]}")
    
    print("\n" + "=" * 60)
    print("✅ Demostración completada")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    main()