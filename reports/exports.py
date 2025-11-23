import os
import csv
import json
from typing import List, Optional, TYPE_CHECKING
from datetime import date

from .pacientes import pacientes_atendidos_en_rango
from .utils import _especialidad_nombre

if TYPE_CHECKING:
    from medico import Medico

def guardar_reporte_a_archivo(texto: str, ruta: str) -> None:
    parent = os.path.dirname(ruta)
    if parent and not os.path.exists(parent):
        os.makedirs(parent, exist_ok=True)
    with open(ruta, "w", encoding="utf-8") as f:
        f.write(texto)

def export_turnos_to_csv(medicos: List['Medico'], ruta: str, nombre_especialidad: Optional[str] = None, matricula: Optional[int] = None) -> None:
    parent = os.path.dirname(ruta)
    if parent and not os.path.exists(parent):
        os.makedirs(parent, exist_ok=True)

    fieldnames = ['matricula', 'nombre', 'apellido', 'especialidades', 'turno_index', 'turno']
    with open(ruta, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for m in medicos:
            if matricula is not None and m.get_matricula() != matricula:
                continue
            esp_nombres = [_especialidad_nombre(e) for e in m.get_especialidades()]
            if nombre_especialidad:
                nombre_lower = nombre_especialidad.lower()
                if not any(nombre_lower in en.lower() for en in esp_nombres):
                    continue
            for idx, t in enumerate(m.get_turnos(), start=1):
                writer.writerow({
                    'matricula': m.get_matricula(),
                    'nombre': m.get_nombre(),
                    'apellido': m.get_apellido(),
                    'especialidades': ";".join(esp_nombres),
                    'turno_index': idx,
                    'turno': repr(t)
                })

def export_turnos_to_json(medicos: List['Medico'], ruta: str, nombre_especialidad: Optional[str] = None, matricula: Optional[int] = None) -> None:
    parent = os.path.dirname(ruta)
    if parent and not os.path.exists(parent):
        os.makedirs(parent, exist_ok=True)

    data = []
    for m in medicos:
        if matricula is not None and m.get_matricula() != matricula:
            continue
        esp_nombres = [_especialidad_nombre(e) for e in m.get_especialidades()]
        if nombre_especialidad:
            nombre_lower = nombre_especialidad.lower()
            if not any(nombre_lower in en.lower() for en in esp_nombres):
                continue
        for idx, t in enumerate(m.get_turnos(), start=1):
            data.append({
                'matricula': m.get_matricula(),
                'nombre': m.get_nombre(),
                'apellido': m.get_apellido(),
                'especialidades': esp_nombres,
                'turno_index': idx,
                'turno': repr(t)
            })

    with open(ruta, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def export_pacientes_to_csv(
    medicos: List['Medico'],
    ruta: str,
    fecha_inicio: Optional[date] = None,
    fecha_fin: Optional[date] = None,
    nombre_especialidad: Optional[str] = None,
    matricula: Optional[int] = None
) -> None:
    parent = os.path.dirname(ruta)
    if parent and not os.path.exists(parent):
        os.makedirs(parent, exist_ok=True)

    fieldnames = ['identificador', 'nombre', 'apellido', 'visitas', 'primera_fecha', 'ultima_fecha', 'medicos']
    rows = pacientes_atendidos_en_rango(medicos, fecha_inicio, fecha_fin, nombre_especialidad, matricula)
    with open(ruta, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for r in rows:
            writer.writerow({
                'identificador': r['identificador'],
                'nombre': r['nombre'],
                'apellido': r['apellido'],
                'visitas': r['visitas'],
                'primera_fecha': r['primera_fecha'].isoformat() if r['primera_fecha'] else '',
                'ultima_fecha': r['ultima_fecha'].isoformat() if r['ultima_fecha'] else '',
                'medicos': ";".join(map(str, r['medicos']))
            })

def export_pacientes_to_json(
    medicos: List['Medico'],
    ruta: str,
    fecha_inicio: Optional[date] = None,
    fecha_fin: Optional[date] = None,
    nombre_especialidad: Optional[str] = None,
    matricula: Optional[int] = None
) -> None:
    parent = os.path.dirname(ruta)
    if parent and not os.path.exists(parent):
        os.makedirs(parent, exist_ok=True)

    rows = pacientes_atendidos_en_rango(medicos, fecha_inicio, fecha_fin, nombre_especialidad, matricula)
    for r in rows:
        r['primera_fecha'] = r['primera_fecha'].isoformat() if r['primera_fecha'] else None
        r['ultima_fecha'] = r['ultima_fecha'].isoformat() if r['ultima_fecha'] else None

    with open(ruta, 'w', encoding='utf-8') as f:
        json.dump(rows, f, ensure_ascii=False, indent=2)