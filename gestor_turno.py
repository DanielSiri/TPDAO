from datetime import date
from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from turno import Turno
    from medico import Medico

from libre import Libre


class GestorTurno:
    """Clase gestora de operaciones de turnos"""
    
    def __init__(self):
        self.__turnos: List['Turno'] = []
    
    # Getters
    def get_turnos(self) -> List['Turno']:
        """Obtiene la lista de turnos"""
        return self.__turnos.copy()
    
    # Métodos de negocio
    def registrar_turno(self, turno: 'Turno') -> None:
        """Registra un turno en el gestor"""
        self.__turnos.append(turno)
        print(f"✓ Turno {turno.get_nro_turno()} registrado en gestor")
    
    def consultar_disponibilidad(self, medico: 'Medico', fecha: date) -> List['Turno']:
        """Consulta turnos disponibles para un médico en una fecha"""
        disponibles = [t for t in self.__turnos if t.get_medico() == medico and 
                      t.get_fecha() == fecha and isinstance(t.get_estado_turno(), Libre)]
        return disponibles
    
    def cancelar_turno(self, nro_turno: int) -> bool:
        """Cancela un turno por su número"""
        for turno in self.__turnos:
            if turno.get_nro_turno() == nro_turno:
                turno.cancelar_turno()
                return True
        return False
    
    def listar_turnos_medico(self, medico: 'Medico') -> List['Turno']:
        """Lista todos los turnos de un médico"""
        return [t for t in self.__turnos if t.get_medico() == medico]
    
    def __repr__(self) -> str:
        return f"GestorTurno(Total turnos: {len(self.__turnos)})"