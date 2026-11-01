import sqlite3
import tempfile
import unittest
from pathlib import Path
from objetos import Almacen, Cliente

class Pruebas(unittest.TestCase):
    def test_persistencia_modificacion_rollback_y_cierre(self):
        with tempfile.TemporaryDirectory() as d:
            ruta=Path(d)/'objetos.yaml'
            with Almacen(ruta) as a:
                with a.transaccion():a.clientes.append(Cliente(1,'Demo','demo@example.test','prospecto'))
                original=ruta.read_bytes()
                with self.assertRaises(ValueError):
                    with a.transaccion():a.clientes.append(Cliente(1,'Duplicado','x@example.test','activo'))
                self.assertEqual(ruta.read_bytes(),original)
                self.assertEqual(len(a.consultar()),1)
                with a.transaccion():a.clientes[0].estado='activo'
            with self.assertRaises(RuntimeError):a.consultar()
            with Almacen(ruta) as b:self.assertEqual(b.consultar('dem')[0].estado,'activo')

    def test_integracion_relacional(self):
        with tempfile.TemporaryDirectory() as d:
            bd=Path(d)/'origen.sqlite'
            c=sqlite3.connect(bd)
            c.executescript("CREATE TABLE clientes(id,nombre,email,estado);CREATE TABLE proyectos(id,cliente_id,nombre,estado);INSERT INTO clientes VALUES(1,'ITC demo','demo@example.test','activo');INSERT INTO proyectos VALUES(2,1,'Portal','pendiente');")
            c.commit();c.close()
            with Almacen(Path(d)/'objetos.yaml') as a:
                with a.transaccion():a.importar_sqlite(bd)
            with Almacen(Path(d)/'objetos.yaml') as a:
                self.assertEqual(a.consultar()[0].proyectos[0].nombre,'Portal')
if __name__=='__main__':unittest.main()
