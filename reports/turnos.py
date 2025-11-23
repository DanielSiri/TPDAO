from typing import List, Optional, TYPE_CHECKING
from .utils import _especialidad_nombre

if TYPE_CHECKING:
    from medico import Medico
    from turno import Turno
    from especialidad import Especialidad

def listado_turnos_por_medico(medicos: List['Medico'], matricula: Optional[int] = None) -> str:
    lines: List[str] = []
    for m in medicos:
        if matricula is not None and m.get_matricula() != matricula:
            continue
        turnos = m.get_turnos()
        lines.append(f"{m.get_nombre()} {m.get_apellido()} (Mat: {m.get_matricula()}) - {len(turnos)} turnos")
        for t in turnos:
            lines.append(f"  - {t}")
        lines.append("")
    return "\n".join(lines).strip()

def listado_turnos_por_especialidad(medicos: List['Medico'], nombre_especialidad: str) -> str:
    lines: List[str] = []
    nombre_lower = nombre_especialidad.lower()
    for m in medicos:
        especialidades = [e for e in m.get_especialidades() if nombre_lower in _especialidad_nombre(e).lower()]
        if not especialidades:
            continue
        turnos = m.get_turnos()
        esp_nombres = ", ".join(_especialidad_nombre(e) for e in especialidades)
        lines.append(f"{m.get_nombre()} {m.get_apellido()} (Mat: {m.get_matricula()}) - Especialidad(es): {esp_nombres} - {len(turnos)} turnos")
        for t in turnos:
            lines.append(f"  - {t}")
        lines.append("")
    return "\n".join(lines).strip()