from sqlmodel import create_engine, SQLModel, Session
from models.libro import Libro
import os

db_user: str = "quevedo"  
db_password: str =  "1234"
db_server: str = "fastapi-db" 
db_port: int = 5432  
db_name: str = "librosdb"  

DATABASE_URL = f"postgresql+psycopg2://{db_user}:{db_password}@{db_server}:{db_port}/{db_name}"
engine = create_engine(os.getenv("DB_URL", DATABASE_URL), echo=True)

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

