from typing import List, Optional, Dict, TYPE_CHECKING
from datetime import date
from .utils import _turno_fecha, _especialidad_nombre

if TYPE_CHECKING:
    from medico import Medico

def _extract_paciente_from_turno(turno):
    if hasattr(turno, "get_paciente"):
        return turno.get_paciente()
    if hasattr(turno, "paciente"):
        return getattr(turno, "paciente")
    if hasattr(turno, "pac"):
        return getattr(turno, "pac")
    return None

def _patient_id_and_names(paciente) -> (str, Dict[str, str]):
    if paciente is None:
        return ("<sin_paciente>", {"identificador": "<sin_paciente>", "nombre": "", "apellido": ""})
    if hasattr(paciente, "get_dni"):
        pid = paciente.get_dni()
    elif hasattr(paciente, "dni"):
        pid = getattr(paciente, "dni")
    elif hasattr(paciente, "get_id"):
        pid = paciente.get_id()
    elif hasattr(paciente, "id"):
        pid = getattr(paciente, "id")
    else:
        pid = repr(paciente)
    nombre = paciente.get_nombre() if hasattr(paciente, "get_nombre") else getattr(paciente, "nombre", "")
    apellido = paciente.get_apellido() if hasattr(paciente, "get_apellido") else getattr(paciente, "apellido", "")
    return (str(pid), {"identificador": str(pid), "nombre": nombre or "", "apellido": apellido or ""})

def pacientes_atendidos_en_rango(
    medicos: List['Medico'],
    fecha_inicio: Optional[date] = None,
    fecha_fin: Optional[date] = None,
    nombre_especialidad: Optional[str] = None,
    matricula: Optional[int] = None
) -> List[Dict]:
    """
    Devuelve lista de pacientes únicos atendidos en el rango [fecha_inicio, fecha_fin].
    Cada item: {'identificador','nombre','apellido','visitas','primera_fecha','ultima_fecha','medicos': [matriculas]}
    """
    nombre_lower = nombre_especialidad.lower() if nombre_especialidad else None
    pacientes: Dict[str, Dict] = {}

    for m in medicos:
        if matricula is not None and m.get_matricula() != matricula:
            continue
        esp_nombres = [_especialidad_nombre(e) for e in m.get_especialidades()]
        if nombre_lower and not any(nombre_lower in en.lower() for en in esp_nombres):
            continue
        for t in m.get_turnos():
            f = _turno_fecha(t)
            if f is None:
                continue
            if fecha_inicio and f < fecha_inicio:
                continue
            if fecha_fin and f > fecha_fin:
                continue
            paciente = _extract_paciente_from_turno(t)
            pid, info = _patient_id_and_names(paciente)
            entry = pacientes.get(pid)
            if not entry:
                entry = {
                    "identificador": info["identificador"],
                    "nombre": info["nombre"],
                    "apellido": info["apellido"],
                    "visitas": 0,
                    "primera_fecha": f,
                    "ultima_fecha": f,
                    "medicos": set()
                }
                pacientes[pid] = entry
            entry["visitas"] += 1
            if f < entry["primera_fecha"]:
                entry["primera_fecha"] = f
            if f > entry["ultima_fecha"]:
                entry["ultima_fecha"] = f
            entry["medicos"].add(m.get_matricula())

    # convertir sets a listas y ordenar por ultima_fecha descendente
    result = []
    for p in pacientes.values():
        result.append({
            "identificador": p["identificador"],
            "nombre": p["nombre"],
            "apellido": p["apellido"],
            "visitas": p["visitas"],
            "primera_fecha": p["primera_fecha"],
            "ultima_fecha": p["ultima_fecha"],
            "medicos": sorted(list(p["medicos"]))
        })
    result.sort(key=lambda x: x["ultima_fecha"] or date.min, reverse=True)
    return result

def reporte_pacientes_atendidos_en_rango_text(
    medicos: List['Medico'],
    fecha_inicio: Optional[date] = None,
    fecha_fin: Optional[date] = None,
    nombre_especialidad: Optional[str] = None,
    matricula: Optional[int] = None
) -> str:
    pacientes = pacientes_atendidos_en_rango(medicos, fecha_inicio, fecha_fin, nombre_especialidad, matricula)
    lines = []
    title = "Pacientes atendidos"
    parts = []
    if fecha_inicio or fecha_fin:
        parts.append(f"Periodo: {fecha_inicio or '...'} - {fecha_fin or '...'}")
    if matricula:
        parts.append(f"Matrícula: {matricula}")
    if nombre_especialidad:
        parts.append(f"Especialidad: {nombre_especialidad}")
    if parts:
        title = f"{title} ({' | '.join(parts)})"
    lines.append(title)
    lines.append("-" * 40)
    if not pacientes:
        lines.append("No se encontraron pacientes en los criterios especificados.")
        return "\n".join(lines)
    for p in pacientes:
        lines.append(f"{p['identificador']} - {p['nombre']} {p['apellido']} - visitas: {p['visitas']} - última: {p['ultima_fecha']} - médicos: {', '.join(map(str,p['medicos']))}")
    return "\n".join(lines)