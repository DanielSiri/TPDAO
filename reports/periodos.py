from typing import List, Optional, Dict
from datetime import datetime, date
from collections import defaultdict
from .utils import _especialidad_nombre, _turno_fecha, _label_sort_key

if TYPE_CHECKING := False:
    from medico import Medico

def contar_turnos_por_periodo(
    medicos: List['Medico'],
    fecha_inicio: Optional[date] = None,
    fecha_fin: Optional[date] = None,
    group_by: str = "month",
    nombre_especialidad: Optional[str] = None,
    matricula: Optional[int] = None
) -> Dict[str, int]:
    counts = defaultdict(int)
    if isinstance(fecha_inicio, datetime):
        fecha_inicio = fecha_inicio.date()
    if isinstance(fecha_fin, datetime):
        fecha_fin = fecha_fin.date()
    nombre_lower = nombre_especialidad.lower() if nombre_especialidad else None

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
            if group_by == "day":
                label = f.isoformat()
            elif group_by == "week":
                y, w, _ = f.isocalendar()
                label = f"{y}-W{w:02d}"
            elif group_by == "month":
                label = f"{f.year}-{f.month:02d}"
            elif group_by == "year":
                label = f"{f.year}"
            else:
                raise ValueError("group_by debe ser one of: day, week, month, year")
            counts[label] += 1

    items = sorted(counts.items(), key=lambda kv: _label_sort_key(kv[0], group_by))
    return dict(items)

def reporte_turnos_por_periodo_text(
    medicos: List['Medico'],
    fecha_inicio: Optional[date] = None,
    fecha_fin: Optional[date] = None,
    group_by: str = "month",
    nombre_especialidad: Optional[str] = None,
    matricula: Optional[int] = None
) -> str:
    counts = contar_turnos_por_periodo(medicos, fecha_inicio, fecha_fin, group_by, nombre_especialidad, matricula)
    lines = []
    title_parts = [f"Agrupado por: {group_by}"]
    if fecha_inicio or fecha_fin:
        title_parts.append(f"Periodo: {fecha_inicio or '...'} - {fecha_fin or '...'}")
    if matricula:
        title_parts.append(f"Matrícula: {matricula}")
    if nombre_especialidad:
        title_parts.append(f"Especialidad: {nombre_especialidad}")
    lines.append(" | ".join(title_parts))
    lines.append("-" * 40)
    if not counts:
        lines.append("No se encontraron turnos en los criterios especificados.")
        return "\n".join(lines)
    for label, cnt in counts.items():
        lines.append(f"{label}: {cnt}")
    return "\n".join(lines)