from typing import Optional


class Database:
    """Clase Singleton para gestionar la conexión a la base de datos"""
    
    _instancia: Optional['Database'] = None
    _inicializado = False
    
    def __new__(cls):
        """Patrón Singleton - garantiza una única instancia"""
        if cls._instancia is None:
            cls._instancia = super().__new__(cls)
        return cls._instancia
    
    def __init__(self):
        """Inicializa la conexión a la BD solo una vez"""
        if not Database._inicializado:
            self._conexion = None
            self._conectado = False
            Database._inicializado = True
    
    def conectar(self, cadena_conexion: str) -> bool:
        """Conecta a la base de datos"""
        try:
            print(f"✓ Conectando a la base de datos: {cadena_conexion}")
            self._conexion = True
            self._conectado = True
            print("✓ Conexión exitosa")
            return True
        except Exception as e:
            print(f"✗ Error de conexión: {e}")
            self._conectado = False
            return False
    
    def desconectar(self) -> bool:
        """Desconecta de la base de datos"""
        try:
            if self._conectado:
                print("✓ Desconectando de la base de datos")
                self._conexion = None
                self._conectado = False
                return True
            return False
        except Exception as e:
            print(f"✗ Error al desconectar: {e}")
            return False
    
    def is_conectado(self) -> bool:
        """Verifica si está conectado a la BD"""
        return self._conectado
    
    def ejecutar_query(self, query: str) -> Optional[list]:
        """Ejecuta una consulta en la BD"""
        if not self._conectado:
            print("✗ No hay conexión a la base de datos")
            return None
        print(f"✓ Ejecutando: {query}")
        return []
    
    def __repr__(self) -> str:
        estado = "Conectado" if self._conectado else "Desconectado"
        return f"Database({estado})"