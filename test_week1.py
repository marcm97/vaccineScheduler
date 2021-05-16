import unittest
import os

from sql_connection_manager import SqlConnectionManager
from vaccine_caregiver import VaccineCaregiver
from enums import *
from utils import *
from COVID19_vaccine import COVID19Vaccine as covid
# from vaccine_patient import VaccinePatient as patient


class TestDB(unittest.TestCase):

    def test_db_connection(self):
        try:
            self.connection_manager = SqlConnectionManager(Server=os.getenv("Server"),
                                                           DBname=os.getenv("DBName"),
                                                           UserId=os.getenv("UserID"),
                                                           Password=os.getenv("Password"))
            self.conn = self.connection_manager.Connect()
        except Exception:
            self.fail("Connection to databse failed")

class TestVaccine(unittest.TestCase):
    def test_init(self):
        with SqlConnectionManager(Server=os.getenv("Server"),
                                  DBname=os.getenv("DBName"),
                                  UserId=os.getenv("UserID"),
                                  Password=os.getenv("Password")) as sqlClient:
            with sqlClient.cursor(as_dict=True) as cursor:
                try:
                    # clear the tables before testing
                    clear_tables(sqlClient)
                    # create a new Vaccine object
                    self.vaccine_a = covid("Pfizer","Biotech",2,21,cursor)
                    # check if the vaccine is correctly inserted into the database
                    sqlQuery = '''
                               SELECT *
                               FROM Vaccines
                               WHERE VaccineName = 'Pfizer'
                               '''
                    cursor.execute(sqlQuery)
                    rows = cursor.fetchall()
                    if len(rows) < 1:
                        self.fail("Creating Vaccine failed")
                    # clear the tables after testing, just in-case
                    clear_tables(sqlClient)
                except Exception:
                    # clear the tables if an exception occurred
                    clear_tables(sqlClient)
                    self.fail("Creating vaccine failed")

    def test_addDoses(self):
        with SqlConnectionManager(Server=os.getenv("Server"),
                                DBname=os.getenv("DBName"),
                                UserId=os.getenv("UserID"),
                                Password=os.getenv("Password")) as sqlClient:
            with sqlClient.cursor(as_dict=True) as cursor:
                try:
                    # clear the tables before testing
                    clear_tables(sqlClient)
                    # create a new Vaccine object
                    self.vaccine_a = covid(name = "Pfizer",supplier = "Biotech",doses_per_patient = 2,days_between_doses = 21,cursor = cursor)

                    self.vaccine_a.AddDoses("Pfizer",10,cursor)
                    # check if schedule has been correctly inserted into CareGiverSchedule
                    sqlQuery = '''
                            SELECT *
                            FROM Vaccines
                            WHERE VaccineName = 'Pfizer'
                            '''
                    cursor.execute(sqlQuery)
                    rows = cursor.fetchall()
                    if len(rows)>1:
                        self.fail("AddDoses verification failed")
                    available = rows[0]["AvailableDoses"]
                    if available!=10:
                        self.fail("AddDoses verification failed")
                    # clear the tables after testing, just in-case
                    clear_tables(sqlClient)
                except Exception:
                    # clear the tables if an exception occurred
                    clear_tables(sqlClient)
                    self.fail("AddDoses verification failed")

    def test_addDoses2(self):
        with SqlConnectionManager(Server=os.getenv("Server"),
                                DBname=os.getenv("DBName"),
                                UserId=os.getenv("UserID"),
                                Password=os.getenv("Password")) as sqlClient:
            with sqlClient.cursor(as_dict=True) as cursor:
                try:
                    # clear the tables before testing
                    clear_tables(sqlClient)
                    # create a new Vaccine object


                    self.vaccine_a = covid(name = "Pfizer",supplier = "Biotech",doses_per_patient = 2,days_between_doses = 21,cursor = cursor)
                    self.vaccine_a.AddDoses("Pfizer",10,cursor)
                    self.vaccine_a.AddDoses("Pfizer",10,cursor)


                    sqlQuery = '''
                            SELECT *
                            FROM Vaccines
                            WHERE VaccineName = 'Pfizer'
                            '''
                    cursor.execute(sqlQuery)
                    rows = cursor.fetchall()
                    if len(rows)>1:
                        self.fail("AddDoses verification failed")
                    available = rows[0]["AvailableDoses"]
                    if available!=20:
                        self.fail("AddDoses verification failed")
                    # clear the tables after testing, just in-case
                    clear_tables(sqlClient)
                except Exception:
                    # clear the tables if an exception occurred
                    clear_tables(sqlClient)
                    self.fail("AddDoses verification failed")

    def test_reserve(self):
        with SqlConnectionManager(Server=os.getenv("Server"),
                                DBname=os.getenv("DBName"),
                                UserId=os.getenv("UserID"),
                                Password=os.getenv("Password")) as sqlClient:
            with sqlClient.cursor(as_dict=True) as cursor:
                try:
                    # clear the tables before testing
                    clear_tables(sqlClient)
                    # create a new Vaccine object
                    self.vaccine_a = covid(name = "Pfizer",supplier = "Biotech",doses_per_patient = 2,days_between_doses = 21,cursor = cursor)

                    self.vaccine_a.AddDoses("Pfizer",10,cursor)
                    self.vaccine_a.ReserveDoses("Pfizer", cursor)
                    # check if schedule has been correctly inserted into CareGiverSchedule
                    sqlQuery = '''
                            SELECT *
                            FROM Vaccines
                            WHERE VaccineName = 'Pfizer'
                            '''
                    cursor.execute(sqlQuery)
                    rows = cursor.fetchall()
                    
                    available = rows[0]["AvailableDoses"]
                    reserved = rows[0]["ReservedDoses"]
                    if available!=8 or reserved!=2:
                        self.fail("Reserve doses verification failed")
                    # clear the tables after testing, just in-case
                    clear_tables(sqlClient)
                except Exception:
                    # clear the tables if an exception occurred
                    clear_tables(sqlClient)
                    self.fail("Reserve Doses verification failed")
     

class TestVaccineCaregiver(unittest.TestCase):
    def test_init(self):
        with SqlConnectionManager(Server=os.getenv("Server"),
                                  DBname=os.getenv("DBName"),
                                  UserId=os.getenv("UserID"),
                                  Password=os.getenv("Password")) as sqlClient:
            with sqlClient.cursor(as_dict=True) as cursor:
                try:
                    # clear the tables before testing
                    clear_tables(sqlClient)
                    # create a new VaccineCaregiver object
                    self.caregiver_a = VaccineCaregiver(name="Steve Ma",
                                                    cursor=cursor)
                    # check if the patient is correctly inserted into the database
                    sqlQuery = '''
                               SELECT *
                               FROM Caregivers
                               WHERE CaregiverName = 'Steve Ma'
                               '''
                    cursor.execute(sqlQuery)
                    rows = cursor.fetchall()
                    if len(rows) < 1:
                        self.fail("Creating caregiver failed")
                    # clear the tables after testing, just in-case
                    # clear_tables(sqlClient)
                except Exception:
                    # clear the tables if an exception occurred
                    clear_tables(sqlClient)
                    self.fail("Creating caregiver failed")
    
    def test_verify_schedule(self):
        with SqlConnectionManager(Server=os.getenv("Server"),
                                  DBname=os.getenv("DBName"),
                                  UserId=os.getenv("UserID"),
                                  Password=os.getenv("Password")) as sqlClient:
            with sqlClient.cursor(as_dict=True) as cursor:
                try:
                    # clear the tables before testing
                    clear_tables(sqlClient)
                    # create a new VaccineCaregiver object
                    self.caregiver_a = VaccineCaregiver(name="Steve Ma",
                                                    cursor=cursor)
                    # check if schedule has been correctly inserted into CareGiverSchedule
                    sqlQuery = '''
                               SELECT *
                               FROM Caregivers, CareGiverSchedule
                               WHERE Caregivers.CaregiverName = 'Steve Ma'
                                   AND Caregivers.CaregiverId = CareGiverSchedule.CaregiverId
                               '''
                    cursor.execute(sqlQuery)
                    rows = cursor.fetchall()
                    hoursToSchedlue = [10,11]
                    minutesToSchedlue = [0, 15, 30, 45]
                    for row in rows:
                        slot_hour = row["SlotHour"]
                        slot_minute = row["SlotMinute"]
                        if slot_hour not in hoursToSchedlue or slot_minute not in minutesToSchedlue:
                            self.fail("CareGiverSchedule verification failed")
                    # clear the tables after testing, just in-case
                    clear_tables(sqlClient)
                except Exception:
                    # clear the tables if an exception occurred
                    clear_tables(sqlClient)
                    self.fail("CareGiverSchedule verification failed")


if __name__ == '__main__':
    unittest.main()
