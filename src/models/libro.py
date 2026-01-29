from sqlmodel import Field, SQLModel
from datetime import date

class Libro(SQLModel, table = True):
    id: int | None = Field(default= None, primary_key=True)
    titulo: str = Field(index= True, max_length= 50)
    autor: str  = Field(index= True, max_length= 50)
    fecha_publicacion: date | None =  Field(nullable=True)
    digital: bool | None = Field(nullable=True)
