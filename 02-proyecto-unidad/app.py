"""Visor y editor gráfico del almacén YAML de ITC."""
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from objetos import Almacen, Cliente, Proyecto

ventana=tk.Tk()
ventana.title('ITC · Objetos persistentes · RA4')
ventana.geometry('900x520')
almacen=Almacen('datos/clientes.yaml')
almacen.__enter__()
ttk.Label(ventana,text='Clientes y proyectos · Almacén YAML',font=('Segoe UI',18)).pack(pady=15)
busqueda=ttk.Entry(ventana)
busqueda.pack(fill='x',padx=20)
tabla=ttk.Treeview(ventana,columns=('id','nombre','estado','proyectos'),show='headings')
for campo in ('id','nombre','estado','proyectos'): tabla.heading(campo,text=campo.capitalize())
tabla.pack(fill='both',expand=True,padx=20,pady=10)
def refrescar(*args):
    tabla.delete(*tabla.get_children())
    for c in almacen.consultar(busqueda.get()): tabla.insert('', 'end',iid=str(c.id),values=(c.id,c.nombre,c.estado,', '.join(p.nombre for p in c.proyectos)))
def importar():
    ruta=filedialog.askopenfilename(filetypes=[('SQLite','*.sqlite'),('Todos','*.*')])
    if not ruta:return
    if not messagebox.askyesno('Importar','¿Sustituir el contenido YAML por una copia de los objetos de esta SQLite?'):return
    try:
        with almacen.transaccion(): almacen.importar_sqlite(ruta)
        refrescar()
    except Exception as e:messagebox.showerror('Importación revertida',str(e))
def activar():
    seleccion=tabla.selection()
    if not seleccion:return
    with almacen.transaccion():
        for c in almacen.clientes:
            if c.id==int(seleccion[0]):c.estado='activo'
    refrescar()
def demo():
    if almacen.consultar():return messagebox.showinfo('Demostración','El almacén ya contiene objetos.')
    with almacen.transaccion():
        almacen.clientes.append(Cliente(1,'Nexo Formación ficticia','demo@example.test','prospecto',[Proyecto(1,'Portal de formación','pendiente')]))
    refrescar()
botones=ttk.Frame(ventana);botones.pack(pady=15)
for titulo,accion in [('Importar SQLite RA2/RA3',importar),('Activar seleccionado',activar),('Cargar ejemplo ficticio',demo)]:ttk.Button(botones,text=titulo,command=accion).pack(side='left',padx=5)
busqueda.bind('<KeyRelease>',refrescar)
def cerrar():almacen.__exit__(None,None,None);ventana.destroy()
ventana.protocol('WM_DELETE_WINDOW',cerrar)
refrescar();ventana.mainloop()
