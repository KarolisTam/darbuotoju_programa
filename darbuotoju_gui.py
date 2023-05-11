from typing import Any
from darbuotoju_uzduotis import *
import PySimpleGUI as sg
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///darbuotojai.db', echo=True)
Session = sessionmaker(bind=engine)
session = Session()

class DarbuotojaiGui:
    def __init__(self):
        self.employe_list = session.query(Darbininkai).all()
        data = [
            [item.id, item.f_name, item.l_name, item.b_day, item.position, item.salary, item.worksince]
            for item in self.employe_list
        ]
        headers = ['ID', 'Vardas', 'Pavarde', 'Gimimo data', 'Pareigos', 'Atlyginimas', 'Nuo kada dirba']
        self.table = sg.Table(values=data, headings=headers, auto_size_columns=True, key="-TABLE-")
        self.layout = [
            [self.table],
            [sg.Button("Add New Employe"), sg.Button("Delete New Employe"), sg.Button("Exit")],
        ]
        self.window = sg.Window("Darbuotojai", layout=self.layout)

    def run(self):
        while True:
            event, values = self.window.read()
            if event == sg.WINDOW_CLOSED or event == "Exit":
                break
            elif event == "Add New Employe":
                pass
            elif event == "Delete New Employe":
                pass
        self.window.close()

darbuotojai = DarbuotojaiGui()
darbuotojai.run() 