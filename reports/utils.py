from typing import Optional
from datetime import datetime, date

def _especialidad_nombre(especialidad) -> str:
    if hasattr(especialidad, "get_nombre"):
        return especialidad.get_nombre()
    if hasattr(especialidad, "nombre"):
        return getattr(especialidad, "nombre")
    return str(especialidad)

def _turno_fecha(turno) -> Optional[date]:
    if hasattr(turno, "get_fecha"):
        f = turno.get_fecha()
    elif hasattr(turno, "fecha"):
        f = getattr(turno, "fecha")
    elif hasattr(turno, "fecha_hora"):
        f = getattr(turno, "fecha_hora")
    else:
        return None
    if isinstance(f, datetime):
        return f.date()
    if isinstance(f, date):
        return f
    try:
        return datetime.fromisoformat(str(f)).date()
    except Exception:
        return None

def _label_sort_key(label: str, group_by: str):
    if group_by == "day":
        return date.fromisoformat(label)
    if group_by == "week":
        y, w = label.split("-W")
        return (int(y), int(w))
    if group_by == "month":
        y, m = label.split("-")
        return (int(y), int(m))
    if group_by == "year":
        return (int(label), 0)
    return label