from typing import List, Optional, Dict, TYPE_CHECKING
from datetime import date, datetime
import os

from .utils import _turno_fecha, _especialidad_nombre

if TYPE_CHECKING:
    from medico import Medico


def _turno_estado_nombre(turno) -> Optional[str]:
    if hasattr(turno, "get_estado"):
        estado = turno.get_estado()
    elif hasattr(turno, "estado"):
        estado = getattr(turno, "estado")
    elif hasattr(turno, "get_estado_turno"):
        estado = turno.get_estado_turno()
    else:
        return None
    if estado is None:
        return None
    if hasattr(estado, "get_nombre"):
        return estado.get_nombre()
    if hasattr(estado, "nombre"):
        return str(getattr(estado, "nombre"))
    return str(estado)


def _turno_asistio(turno) -> Optional[bool]:
    name = _turno_estado_nombre(turno)
    if not name:
        if hasattr(turno, "asistio"):
            return bool(getattr(turno, "asistio"))
        if hasattr(turno, "asistido"):
            return bool(getattr(turno, "asistido"))
        return None
    n = name.lower()
    if "asi" in n or "attend" in n or "present" in n:
        return True
    if "cancel" in n or "no asis" in n or "inasist" in n or "libre" in n or "no-show" in n or "no show" in n:
        return False
    return None


def calcular_asistencia(
    medicos: List['Medico'],
    fecha_inicio: Optional[date] = None,
    fecha_fin: Optional[date] = None,
    nombre_especialidad: Optional[str] = None,
    matricula: Optional[int] = None
) -> Dict[str, int]:
    asistieron = 0
    no_asistieron = 0
    desconocido = 0

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
            a = _turno_asistio(t)
            if a is True:
                asistieron += 1
            elif a is False:
                no_asistieron += 1
            else:
                desconocido += 1

    total = asistieron + no_asistieron + desconocido
    return {"asistieron": asistieron, "no_asistieron": no_asistieron, "desconocido": desconocido, "total": total}


def reporte_asistencia_text(
    medicos: List['Medico'],
    fecha_inicio: Optional[date] = None,
    fecha_fin: Optional[date] = None,
    nombre_especialidad: Optional[str] = None,
    matricula: Optional[int] = None
) -> str:
    c = calcular_asistencia(medicos, fecha_inicio, fecha_fin, nombre_especialidad, matricula)
    lines = []
    lines.append("Asistencia a turnos")
    parts = []
    if fecha_inicio or fecha_fin:
        parts.append(f"Periodo: {fecha_inicio or '...'} - {fecha_fin or '...'}")
    if matricula:
        parts.append(f"Matrícula: {matricula}")
    if nombre_especialidad:
        parts.append(f"Especialidad: {nombre_especialidad}")
    if parts:
        lines[0] = lines[0] + " (" + " | ".join(parts) + ")"
    lines.append("-" * 40)
    if c["total"] == 0:
        lines.append("No se encontraron turnos en los criterios especificados.")
        return "\n".join(lines)
    lines.append(f"Total: {c['total']}")
    lines.append(f"Asistieron: {c['asistieron']} ({c['asistieron']*100/c['total']:.1f}%)")
    lines.append(f"No asistieron: {c['no_asistieron']} ({c['no_asistieron']*100/c['total']:.1f}%)")
    if c["desconocido"]:
        lines.append(f"Desconocido: {c['desconocido']} ({c['desconocido']*100/c['total']:.1f}%)")
    return "\n".join(lines)


def generar_grafico_asistencia(
    medicos: List['Medico'],
    ruta: str,
    fecha_inicio: Optional[date] = None,
    fecha_fin: Optional[date] = None,
    nombre_especialidad: Optional[str] = None,
    matricula: Optional[int] = None,
    tipo: str = "pie"  # "pie" o "bar"
) -> str:
    stats = calcular_asistencia(medicos, fecha_inicio, fecha_fin, nombre_especialidad, matricula)
    total = stats.get("total", 0)

    try:
        import matplotlib.pyplot as plt
    except Exception as e:
        raise ImportError("matplotlib no está instalado. Instalar con: pip install matplotlib") from e

    if total == 0:
        fig, ax = plt.subplots(figsize=(6, 4))
        ax.text(0.5, 0.5, "No hay datos de asistencia en el rango indicado", ha="center", va="center", fontsize=12)
        ax.axis("off")
        parent = os.path.dirname(ruta)
        if parent and not os.path.exists(parent):
            os.makedirs(parent, exist_ok=True)
        plt.tight_layout()
        plt.savefig(ruta, dpi=150)
        plt.close(fig)
        return ruta

    labels = []
    values = []
    if stats.get("asistieron", 0) > 0:
        labels.append("Asistieron")
        values.append(stats["asistieron"])
    if stats.get("no_asistieron", 0) > 0:
        labels.append("No asistieron")
        values.append(stats["no_asistieron"])
    if stats.get("desconocido", 0) > 0:
        labels.append("Desconocido")
        values.append(stats["desconocido"])

    if not values:
        labels = ["Asistieron", "No asistieron", "Desconocido"]
        values = [stats.get("asistieron", 0), stats.get("no_asistieron", 0), stats.get("desconocido", 0)]

    fig, ax = plt.subplots(figsize=(6, 4))
    if tipo == "pie":
        ax.pie(values, labels=labels, autopct="%1.1f%%", startangle=90, colors=["#4CAF50", "#F44336", "#9E9E9E"][:len(values)])
        ax.axis("equal")
    else:
        ax.bar(labels, values, color=["#4CAF50", "#F44336", "#9E9E9E"][:len(values)])
        maxv = max(values) if values else 0
        for i, v in enumerate(values):
            ax.text(i, v + maxv * 0.01, str(v), ha="center")
        ax.set_ylabel("Cantidad")

    parent = os.path.dirname(ruta)
    if parent and not os.path.exists(parent):
        os.makedirs(parent, exist_ok=True)
    plt.tight_layout()
    plt.savefig(ruta, dpi=150)
    plt.close(fig)
    return ruta