from typing import Any
from darbuotoju_uzduotis import Darbininkai
from sqlalchemy import create_engine
import PySimpleGUI as sg
from sqlalchemy.orm import sessionmaker
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(filename='app.log', level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s: %(message)s')

engine = create_engine('sqlite:///darbuotojai.db', echo=True)
Session = sessionmaker(bind=engine)
session = Session()

class DarbuotojaiGui:
    sg.theme("LightBlue4")
    def get_data(self):
        self.employe_list = session.query(Darbininkai).all()
        data = [
            [item.id, item.f_name, item.l_name, item.b_day, item.position, item.salary, item.worksince]
            for item in self.employe_list
        ]
        return data
    
    def __init__(self):
        data = self.get_data()
        headers = ['ID', 'Vardas', 'Pavarde', 'Gimimo data', 'Pareigos', 'Atlyginimas', 'Nuo kada dirba']
        self.table = sg.Table(values=data, headings=headers, auto_size_columns=True, key="lentele", enable_events=True)
        # Create layout for employee tab
        employee_tab_layout = [
            [sg.Text("Insert employee First name:"), sg.Input("", key="f_name", size=15)],
            [sg.Text("Insert employee Last name:"), sg.Input("", key="l_name", size=15)],
            [sg.Text("Insert employee Birthday:"), sg.Input("", key="b_day", size=15)],
            [sg.Text("Insert employee Position:"), sg.Input("", key="position", size=15)],
            [sg.Text("Insert employee Salary:"), sg.Input("", key="salary", size=15, )],
            [sg.Button("Add New Employee", key="add"), sg.Button("Delete Employee", key="remove"), 
             sg.Button("Edit Employee", key="edit"), sg.Button("Exit", key="Exit")],
            [self.table]
        ]
        # Create layout for log tab
        log_tab_layout = [
            [sg.Output(size=(80, 20))]  # Output element to display log messages
        ]
        # Create the tab group
        self.tab_group = sg.TabGroup([[sg.Tab("Employees", employee_tab_layout), sg.Tab("Log", log_tab_layout)]],
                                     key="tab_group", enable_events=True)
        
        self.layout = [[self.tab_group]]
        self.window = sg.Window("Darbuotojai", layout=self.layout, finalize=True)
        self.window["tab_group"].bind('<TabGroup>', '_tab_group_')

    def refresh_log(self):
        try:
            with open("app.log", "r") as file:
                log_content = file.read()
            self.window["log_output"].update(log_content)
        except Exception as e:
            logging.error(f"Failed to refresh log: {str(e)}")

    def run(self):
        while True:
            event, values = self.window.read()
            if event == sg.WINDOW_CLOSED or event == "Exit":
                break
            elif event == "add":
                try:
                    darbuotojas = Darbininkai(
                        f_name=values["f_name"], 
                        l_name=values["l_name"], 
                        b_day=values["b_day"], 
                        position=values["position"], 
                        salary=values["salary"])
                    session.add(darbuotojas)
                    session.commit()
                    if isinstance(darbuotojas, Darbininkai):
                        self.table.update(values=self.get_data())
                        logging.info('User add new Employe')
                except Exception as e:
                    print(e)
            elif event == "remove":
                selected_rows = self.table.SelectedRows
                if selected_rows:
                    selected_row = selected_rows[0]
                    session.delete(self.employe_list[selected_row])
                    session.commit()
                    self.table.update(values=self.get_data())
                    logging.info('User deleted old Employe')
            elif event == "lentele":
                selected_rows = self.table.SelectedRows
                if selected_rows:
                    selected_row = selected_rows[0]
                    selected_employee = self.employe_list[selected_row]
                    self.window["f_name"].update(selected_employee.f_name)
                    self.window["l_name"].update(selected_employee.l_name)
                    self.window["b_day"].update(selected_employee.b_day)
                    self.window["position"].update(selected_employee.position)
                    self.window["salary"].update(selected_employee.salary)

            elif event == "edit":
                selected_rows = self.table.SelectedRows
                if selected_rows:
                    selected_row = selected_rows[0]
                    self.employe_list[selected_row].f_name=values["f_name"]
                    self.employe_list[selected_row].l_name=values["l_name"]
                    self.employe_list[selected_row].b_day=datetime.strptime(values["b_day"], "%Y-%m-%d")
                    self.employe_list[selected_row].position=values["position"]
                    self.employe_list[selected_row].salary=values["salary"]
                    session.commit()
                    self.table.update(values=self.get_data())
                    logging.info('User updated Employee')
            elif event == "_tab_group_":
                active_tab = values["tab_group"]
                if active_tab == "Log":
                    self.refresh_log()
                    self.window.close()

darbuotojai = DarbuotojaiGui()
darbuotojai.run() 