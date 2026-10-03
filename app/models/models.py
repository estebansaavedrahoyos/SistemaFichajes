from app.database.db import Base
from typing import List
from sqlalchemy.orm import Mapped , mapped_column , relationship
from sqlalchemy import Integer , String ,DateTime ,ForeignKey,  CheckConstraint , Boolean
from datetime import datetime

class PuestosORM(Base):
    __tablename__ = "Puestos"
    id : Mapped[int] = mapped_column(Integer , primary_key=True , index=True , autoincrement=True )
    puesto : Mapped[str] = mapped_column(String , nullable=False , unique=True)
    
    #RELACIONES    

    empleados : Mapped[List["EmpleadosORM"]] = relationship(back_populates="puesto")
    
class MotivosORM(Base):
    __tablename__ = "Motivos"
    id : Mapped[int] = mapped_column(Integer , primary_key=True , index=True , autoincrement=True )
    motivo : Mapped[str] = mapped_column(String , nullable=False , unique=True)
    
    #RELACIONES
    
    fichajes : Mapped[List["FichajesORM"]] = relationship(back_populates="motivo")
    
class EmpleadosORM(Base):
    __tablename__ = "Empleados"
    id : Mapped[int] = mapped_column(Integer , primary_key=True , index=True , autoincrement=True )
    nombre : Mapped[str] = mapped_column(String , nullable=False ,  index=True)
    id_puesto : Mapped[int | None] = mapped_column(Integer , ForeignKey("Puestos.id" , ondelete="SET NULL" ) ,
                                            nullable=True  )
    admin : Mapped[bool] = mapped_column(Boolean , nullable=False)
    
    #RELACIONES 
    
    puesto : Mapped["PuestosORM"] = relationship(back_populates="empleados")
    
    usuario : Mapped["UsuariosORM"] = relationship(back_populates="empleado")
    
    @property
    def nombre_puesto(self):
        return self.puesto.puesto
    
    fichajes : Mapped[List["FichajesORM"]] = relationship(back_populates="empleado")
    
    
    
class FichajesORM(Base):
    __tablename__ = "Fichajes"
    id : Mapped[int] = mapped_column(Integer , primary_key=True , index=True , autoincrement=True)
    fecha_hora : Mapped[datetime] = mapped_column(DateTime , index=True , nullable=False)
    id_empleado : Mapped[int] = mapped_column(Integer , ForeignKey("Empleados.id" , ondelete="CASCADE"), nullable=True , index=True) 
    id_motivo : Mapped[int | None] = mapped_column(Integer , ForeignKey("Motivos.id" , ondelete="SET NULL") , nullable=True , index=True)
    tipo : Mapped[str] = mapped_column(String , CheckConstraint("tipo IN ('entrada' , 'salida')" , name="verifica_tipo") ,
                                       index=True , nullable=False)
    
  
    #RELACIONES
    
    empleado : Mapped["EmpleadosORM"] = relationship(back_populates="fichajes")
    
    @property
    def nombre_empleado(self):
        return self.empleado.nombre
    @property
    def puesto_empleado(self):
        return self.empleado.nombre_puesto
        
    motivo : Mapped["MotivosORM"] = relationship(back_populates="fichajes")
    
    @property
    def nombre_motivo(self):
        return self.motivo.motivo
    
    @property
    def fecha_hora_str(self):
        return self.fecha_hora.strftime("%d-%m-%Y   |     %H:%M:%S")
    
    


class UsuariosORM(Base):
    __tablename__ = "usuarios"
    id : Mapped[int] =  mapped_column(Integer , primary_key=True , autoincrement=True , nullable = False , index=True)
    usuario : Mapped[str] = mapped_column(String , nullable=False , index = True)
    contrasena_hasheada : Mapped[str] = mapped_column(String , nullable=False )
    id_empleado : Mapped[int] = mapped_column(Integer , ForeignKey("Empleados.id" , ondelete="CASCADE") ,nullable=False , index=True )
    
    empleado : Mapped["EmpleadosORM"] = relationship(back_populates="usuario")
    
    @property
    def nombre_empleado(self):
        return self.empleado.nombre

    