import unittest
import os
import datetime

from sql_connection_manager import SqlConnectionManager
from vaccine_caregiver import VaccineCaregiver
from enums import *
from utils import *
from COVID19_vaccine import COVID19Vaccine as covid
from vaccine_patient import VaccinePatient as patient
from vaccine_reservation_scheduler import VaccineReservationScheduler

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


class TestPatient(unittest.TestCase):
    def test_init(self):
        with SqlConnectionManager(Server=os.getenv("Server"),
                                  DBname=os.getenv("DBName"),
                                  UserId=os.getenv("UserID"),
                                  Password=os.getenv("Password")) as sqlClient:
            with sqlClient.cursor(as_dict=True) as cursor:
                try:
                    # clear the tables before testing
                    clear_tables(sqlClient)

                    # create a new Patient object
                    self.patient_a = patient(name='dj',cursor=cursor)
                    
                    sqlQuery = '''
                               SELECT *
                               FROM Patients
                               WHERE PatientName = 'dj'
                               '''
                    cursor.execute(sqlQuery)
                    rows = cursor.fetchall()

                    if len(rows) < 1:
                        self.fail("Patientnot found")

                    # clear the tables after testing, just in-case
                    clear_tables(sqlClient)
                    print(rows[0])
                except Exception:
                    # clear the tables if an exception occurred
                    # clear_tables(sqlClient)
                    self.fail("Creating Patient failed")

    def test_reservation(self):
        with SqlConnectionManager(Server=os.getenv("Server"),
                                  DBname=os.getenv("DBName"),
                                  UserId=os.getenv("UserID"),
                                  Password=os.getenv("Password")) as sqlClient:
            with sqlClient.cursor(as_dict=True) as cursor:
                cursor.connection.autocommit(False)
                try:
                    # clear the tables before testing
                    clear_tables(sqlClient)

                    # initialize vaccines
                    self.vaccine_1 = covid("Pfizer","Biotech",2,21,cursor)
                    self.vaccine_2 = covid('Moderna','Moderna',2,28, cursor)
                    self.vaccines = [self.vaccine_1,self.vaccine_2]

                    self.vaccine_1.AddDoses("Pfizer",2,cursor)
                    self.vaccine_2.AddDoses("Moderna",3,cursor)

                     # create a new VaccineCaregiver object
                    self.caregiver_a = VaccineCaregiver(name="John",
                                                    cursor=cursor)
                    self.caregiver_b = VaccineCaregiver(name="Steve",
                                                    cursor=cursor)
                    # create a new Patient object

                    self.patients = [patient(name='Marc',cursor=cursor),
                                    patient(name='Marc2',cursor=cursor),
                                    patient(name='Marc3',cursor=cursor),
                                    patient(name='Marc4',cursor=cursor),
                                    patient(name='Marc5',cursor=cursor)
                                    ]
                    # for each patient:
                    for patient_a in self.patients:
                        # See what vaccines are available
                        for vaccine_a in self.vaccines:
                            sqlQuery = '''
                                SELECT *
                                FROM Vaccines
                                WHERE VaccineName = '{name}'
                                '''.format(name = vaccine_a.name)
                            cursor.execute(sqlQuery)
                            rows = cursor.fetchall()
                            if len(rows)>0:
                                if rows[0]['AvailableDoses']>=rows[0]['DosesPerPatient']:
                                # if enough doses are available
                                    # 1) create a reservation 
                                    self.reservation_a = VaccineReservationScheduler()
                                    # 2) get first caregiver slot ID & reserve it & schedule it
                                    self.reservedId = self.reservation_a.PutHoldOnAppointmentSlot(cursor =cursor)
                                    # if no slot is available, rollback commit
                                    if self.reservedId in [0,-1]: 
                                        cursor.connection.rollback()
                                        patient_a.first_VaccineAppointmentId =  0
                                        print("No slots available in the next 3 weeks")
                                        break
                                    else:
                                        patient_a.first_VaccineAppointmentId = patient_a.ReserveAppointment(self.reservedId,vaccine_a.name,cursor)
                                        patient_a.vaccine_name = vaccine_a.name
                                        
                                        # 3) get second slot & reserve it 
                                        self.reservation_a.ScheduleAppointmentSlot(slotid = self.reservedId,cursor = cursor)
                                        patient_a.ScheduleAppointment(Vaccine = vaccine_a,cursor = cursor)
                    
                                        days_between_doses = int(rows[0]['DaysBetweenDoses'])
                                        if int(rows[0]['DosesPerPatient'])==2:
                                            self.reservedId = self.reservation_a.PutHoldOnAppointmentSlot(cursor =cursor,date = datetime.datetime.now()+ datetime.timedelta(days=days_between_doses))
                                            if self.reservedId in [0,-1]: 
                                                
                                                cursor.connection.rollback()
                                                patient_a.first_VaccineAppointmentId =  0
                                                patient_a.second_VaccineAppointmentId =  0
                                                patient_a.vaccine_name = ''
                                                # if second slot is not available try next vaccine
                                                print("second slot not available for, cancelling first appointment & checking other vaccines",vaccine_a.name)
                                                continue
                                            else:
                                                patient_a.second_VaccineAppointmentId  = patient_a.ReserveAppointment(self.reservedId,vaccine_a.name,cursor)
                                                patient_a.vaccine_name = vaccine_a.name
                                                self.reservation_a.ScheduleAppointmentSlot(slotid = self.reservedId,cursor = cursor)
                                                patient_a.ScheduleAppointment(Vaccine = vaccine_a,cursor = cursor)

                                                break
    
                                else:
                                    print(vaccine_a.name, "not enough doses available")

                        if patient_a.first_VaccineAppointmentId!=0:
                            print("Reservation Successful for Patient!!!!!!!!!!!" ,patient_a.name)
                            cursor.connection.commit()
                        else:
                            print("not successful")
                        



                except Exception:
                    # clear the tables if an exception occurred
                    clear_tables(sqlClient)
                    self.fail("Reservation failed")


# class Test(unittest.TestCase):
#     def test(self):
#         #allocate 2 caregivers

#         #add 2 doses of the vaccine

#         #Initialize a patient

#         #check for first 
#         pass

if __name__ == '__main__':
    unittest.main()