from reports import listado_turnos_por_medico, listado_turnos_por_especialidad

# Mocks mínimos para probar los reportes
class MockTurno:
    def __init__(self, desc): self.desc = desc
    def __repr__(self): return f"Turno({self.desc})"

class MockEspecialidad:
    def __init__(self, nombre): self.nombre = nombre
    def get_nombre(self): return self.nombre

class MockMedico:
    def __init__(self, mat, nombre, ape, especialidades, turnos):
        self._mat = mat
        self._nombre = nombre
        self._ape = ape
        self._esp = especialidades
        self._turnos = turnos
    def get_matricula(self): return self._mat
    def get_nombre(self): return self._nombre
    def get_apellido(self): return self._ape
    def get_especialidades(self): return list(self._esp)
    def get_turnos(self): return list(self._turnos)

med1 = MockMedico(123, "Ana", "Lopez", [MockEspecialidad("Cardiología")], [MockTurno("09:00"), MockTurno("10:00")])
med2 = MockMedico(456, "Diego", "Pérez", [MockEspecialidad("Dermatología")], [MockTurno("11:00")])
medicos = [med1, med2]

print("=== Por médico ===")
print(listado_turnos_por_medico(medicos))
print("\n=== Por especialidad (cardio) ===")
print(listado_turnos_por_especialidad(medicos, "cardio"))