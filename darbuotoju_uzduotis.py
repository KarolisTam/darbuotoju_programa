from typing import Any
from sqlalchemy import create_engine, Integer, String, Float, Date, DateTime
from sqlalchemy.orm import sessionmaker, DeclarativeBase, mapped_column
from datetime import datetime


class Base(DeclarativeBase):
    pass


class Darbininkai(Base):
    __tablename__ = "darbuotojas"
    id = mapped_column(Integer, primary_key=True)
    f_name = mapped_column(String(50), nullable=False)
    l_name = mapped_column(String(50), nullable=False)
    b_day = mapped_column(Date, nullable=False)
    position = mapped_column(String(50), nullable=False)
    salary = mapped_column(Float(50), nullable=False)
    worksince = mapped_column(DateTime, default=datetime.today)

    def __init__(self, **kw: Any):
        # super().__init__(**kw)
        for key, value in kw.items():
            if key == 'b_day':
                value = datetime.strptime(value, '%Y-%m-%d')
            setattr(self, key, value)

    def __repr__(self) -> str:
        return f"({self.id}, {self.f_name}, {self.l_name}, {self.b_day}, {self.position}, {self.salary}, {self.worksince})"


def spausdinti(session):
    employe = session.query(Darbininkai).all()
    print("-------------------")
    for employe in  employe:
        print(employe)
    print("-------------------")
    return  employe

if __name__ == "__main__":
    
    engine = create_engine('sqlite:///darbuotojai.db')
    Session = sessionmaker(bind=engine)
    session = Session()
    Base.metadata.create_all(engine)
    
    
    while True:
        choice = input("""Pasirinkite veiksmą: 
    1 - Parodyti darbuotojus
    2 - Pridėti darbuotojus
    3 - Pakeisti darbuotojo info
    4 - Panaikinti darbuotoja
    0 - Išeiti
    >:""")

        try:
            choice = int(choice)
        except:
            pass

        if choice == 1:
            employe = spausdinti(session)

        elif choice == 2:
            f_name = input("Įveskite darbuotojo varda: ")
            l_name = input("Įveskite darbuotojo pavardę: ")
            b_day = input("Įveskite darbuotojo gimimo data(YYYY-MM-DD): ")
            position = input("Įveskite darbuotojo pareigas: ")
            salary = float(input("Įveskite darbuotojo alyginimą: "))
            employe = Darbininkai(f_name=f_name, l_name=l_name, b_day=b_day, position=position, salary=salary)
            session.add(employe)
            session.commit()

        elif choice == 3:
            employe = spausdinti(session)
            try:
                select_id = int(input("Pasirinkite norimo pakeisti darbuotojo ID: "))
                edit_employe = session.get(Darbininkai, select_id)
            except Exception as e:
                print(f"Klaida: {e}")
            else:
                choice = int(input("""Ką norėtumėte pakeisti: 
    1 - Vardą
    2 - Pavardę
    3 - Gimimo data
    4 - Atlyginimas
    5 - Pareigas
    Jūsų choice: """))

                if choice == 1:
                    edit_employe.f_name = input("Įveskite darbuotojo Vardą: ")

                if choice == 2:
                    edit_employe.l_name = input("Įveskite darbuotojo Pavardę: ")

                if choice == 3:
                    insert_date = input("Įveskite darbuotojo gimimo datą(YYYY-MM-DD): ")
                    edit_employe.b_day = datetime.strptime(insert_date, '%Y-%m-%d')
                if choice == 4:
                    edit_employe.salary = input("Įveskite darbuojo pareigas: ")

                if choice == 5:
                    edit_employe.position = input("Įveskite darbuojo pareigas: ")

                session.commit()

        elif choice == 4:
            employe = spausdinti(session)
            delete_employe = int(input("Pasirinkite norimo ištrinti projekto ID: "))
            try:
                deleted_employe = session.get(Darbininkai, delete_employe)
                session.delete(deleted_employe)
                session.commit()
            except Exception as e:
                print(f"Klaida: {e}")

        elif choice == 0:
            print("Ačiū už tvarkingą uždarymą")
            break

        else:
            print("Klaida: Neteisingas choice")