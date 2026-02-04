from sqlmodel import create_engine, SQLModel, Session
from models.libro import Libro
import os

DATABASE_URL = os.environ["DATABASE_URL"]

engine = create_engine(DATABASE_URL,echo=True,pool_pre_ping=True)

def get_session():
    with Session(engine) as session:
        yield session

def init_db():
    SQLModel.metadata.drop_all(engine)
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        session.add(Libro(id=1, titulo="La gran cacería", autor="Robert Jordan", fecha_publicacion="2023-09-10", digital=True))
        session.add(Libro(id=2, titulo="Festín de cuervos", autor="G.R.R. Martin", fecha_publicacion="2024-03-20",digital= True))
        session.add(Libro(id=3, titulo="El color de la magia",autor="Terry Pratchet", fecha_publicacion="2019-02-22",digital= False))
        session.add(Libro(id=4, titulo="El Silmarillion", autor=" J.R.R. y Christopher Tolkien", fecha_publicacion="2021-10-01", digital= False))
        session.add(Libro(id=5, titulo="El resplandor", autor="Stephen King", fecha_publicacion="2023-09-10",digital=True))
        session.commit()
        #session.refresh_all()

