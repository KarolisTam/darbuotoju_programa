from typing import Any
from sqlalchemy import Integer, String, Float, DateTime, create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase, mapped_column
from datetime import datetime

engine = create_engine('sqlite:///uzduotis.db')
Session = sessionmaker(bind=engine)
session = Session()

class Base(DeclarativeBase):
    pass

class Darbuotojai(Base):
    __tablemake_ = "Darbuotojai"
    id = mapped_column(Integer, primary_key=True)
    f_name = mapped_column(String, nullable=False)
    l_name = mapped_column(String, nullable=False)
    b_day = mapped_column(DateTime)
    position = mapped_column(String, nullable=False)
    worksince = mapped_column(DateTime)
    created = mapped_column(DateTime, default=datetime.utcnow)

    def __init__(self, **kw: Any):
        # super().__init__(**kw)
        for key, value in kw.items():
            setattr(self, key, value)

    def __repr__(self) -> str:
        return f"({self.id}, {self.f_name}, {self.l_name}, {self.b_day}, {self.position}, {self.worksince}, {self.created})"
    
Base.metadata.create_all(engine)

def spausdinti (session):
    darbuotojas = session.query(Darbuotojai).all()
    print("---------------")
    for darbuotojai in darbuotojas:
        print(darbuotojai)
    print("---------------")
    return darbuotojas

def prideti_darbuotoja(session):
    f_name = input("Įveskite darbuotojo varda: ")
    l_name = input("Įveskite darbuotojo pavardę: ")
    b_day = input("Įveskite darbuotojo gimimo data: ")
    position = input("Įveskite darbuotojo pareigas: ")
    worksince = input("Įveskite nuo kada pradėjo dirbti darbuotojas(skaičiais): ")
    darbuotojas = Darbuotojai(f_name=f_name, l_name=l_name, b_day=b_day, position=position, worksince=worksince)
    session.add(darbuotojas)
    session.commit()

def pakeisti_duomenis(session, darbuotojas):
    darbuotojas = spausdinti(session)
    keitimo_id = int(input("Nurodykite darbuotojo ID: "))
    keiciamas_darbuotojas = session.get(Darbuotojai, keitimo_id)
    pakeitimas = int(input("Ką norėtumėte pakeisti: 1 - Vardą, 2 - Pavardę, 3 - Gimimo data, 4 - Pareigas, 5 - Darbo pradžią"))
    if pakeitimas == 1:
        keiciamas_darbuotojas.f_name = input 