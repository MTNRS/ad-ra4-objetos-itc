"""Almacén didáctico de objetos en YAML, para uso local de un proceso."""
from contextlib import contextmanager
from copy import deepcopy
from dataclasses import dataclass, field, asdict
from pathlib import Path
import os
import sqlite3
import tempfile
import yaml

@dataclass
class Proyecto:
    id: int
    nombre: str
    estado: str

@dataclass
class Cliente:
    id: int
    nombre: str
    email: str
    estado: str
    proyectos: list[Proyecto] = field(default_factory=list)

class Almacen:
    def __init__(self, ruta):
        self.ruta = Path(ruta)
        self.clientes = []
        self.abierto = False
        self.en_transaccion = False

    def __enter__(self):
        if self.ruta.exists():
            datos = yaml.safe_load(self.ruta.read_text(encoding='utf-8')) or []
            self.clientes = [Cliente(**{k:v for k,v in x.items() if k!='proyectos'}, proyectos=[Proyecto(**p) for p in x.get('proyectos',[])]) for x in datos]
        self.abierto = True
        return self

    def __exit__(self, *args):
        self.clientes = []
        self.abierto = False

    def consultar(self, texto=''):
        if not self.abierto: raise RuntimeError('Almacén cerrado')
        return deepcopy([c for c in self.clientes if texto.lower() in c.nombre.lower()])

    @contextmanager
    def transaccion(self):
        if not self.abierto or self.en_transaccion: raise RuntimeError('Estado de transacción incorrecto')
        anterior = deepcopy(self.clientes)
        self.en_transaccion = True
        try:
            yield self
            ids = [c.id for c in self.clientes]
            if len(ids)!=len(set(ids)): raise ValueError('Identificadores duplicados')
            self.ruta.parent.mkdir(parents=True, exist_ok=True)
            # Sustitución atómica: un fallo conserva el fichero anterior.
            temporal = None
            try:
                with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', dir=self.ruta.parent, delete=False) as f:
                    temporal = f.name
                    yaml.safe_dump([asdict(c) for c in self.clientes],f,allow_unicode=True,sort_keys=False)
                    f.flush()
                    os.fsync(f.fileno())
                os.replace(temporal,self.ruta)
            finally:
                if temporal and Path(temporal).exists(): Path(temporal).unlink()
        except Exception:
            self.clientes = anterior
            raise
        finally:
            self.en_transaccion = False

    def importar_sqlite(self, ruta):
        if not self.en_transaccion: raise RuntimeError('Se necesita transacción')
        # Solo lectura sobre la base relacional: no crea ni modifica el origen.
        conexion = sqlite3.connect(Path(ruta).resolve().as_uri()+'?mode=ro',uri=True)
        try:
            objetos = []
            for id,nombre,email,estado in conexion.execute('SELECT id,nombre,email,estado FROM clientes'):
                proyectos = [Proyecto(*p) for p in conexion.execute('SELECT id,nombre,estado FROM proyectos WHERE cliente_id=?',(id,))]
                objetos.append(Cliente(id,nombre,email,estado,proyectos))
            self.clientes = objetos
        finally:
            conexion.close()
