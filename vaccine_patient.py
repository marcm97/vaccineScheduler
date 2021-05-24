import pymssql
# from vaccine_reservation_scheduler import VaccineReservationScheduler as reservation

class VaccinePatient:
    def __init__(self,name,cursor):
        self.patientId =0
        self.vaccine_name = ''
        self.name = name
        self.first_VaccineAppointmentId = 0
        self.second_VaccineAppointmentId = 0
        self.insertPatientSQL = "INSERT INTO Patients (PatientName,VaccineStatus) VALUES ('" + name + "',0)"
        try: 
            cursor.execute(self.insertPatientSQL)
            cursor.connection.commit()
            cursor.execute("SELECT @@IDENTITY AS 'Identity'; ")
            _identityRow = cursor.fetchone()
            self.patientId = _identityRow['Identity']
            print('Query executed successfully. Patient: ' + name 
            +  ' added to the database using Patient ID = ' + str(self.patientId))
        except pymssql.Error as db_err:
            print("Database Programming Error in SQL Query processing for Patient! ")
            print("Exception code: " + str(db_err.args[0]))
            if len(db_err.args) > 1:
                print("Exception message: " + db_err.args[1])
            print("SQL text that resulted in an Error: " + self.insertPatientSQL)


    def ReserveAppointment(self,CaregiverSchedulingID, Vaccine, cursor):
        # check if id is on hold
        print(CaregiverSchedulingID)
        self.getAppointmentSQL = '''SELECT * 
                                    FROM CareGiverSchedule 
                                    WHERE CareGiverSchedule.CaregiverSlotSchedulingID = {id}
                                    AND SlotStatus = 1 '''.format(id =  CaregiverSchedulingID)
        try:
            cursor.execute(self.getAppointmentSQL)

            rows  = cursor.fetchall()

            if len(rows)==0:
                print("CaregiverSchedulingId not available")
                return -1

            else:
                
                self.ReservationDate = rows[0]['WorkDay']
                self.SlotStatus = rows[0]['SlotStatus']

                # Create entry in vaccineAppointenmnet table 
                self.createAppointmentSQL = '''
                INSERT INTO VaccineAppointments 
                (VaccineName,
                PatientId, 
                CaregiverId, 
                SlotStatus,
                ReservationDate,
                AppointmentDuration,
                DoseNumber) 

                VALUES ('{v_name}',{p_id},{c_id},{slot_status},'{date}',{duration},{dose_number})

                    '''.format(
                                v_name = Vaccine,
                                p_id = self.patientId,
                                c_id = rows[0]['CaregiverId'],
                                date = rows[0]['WorkDay'],
                                duration = 15,
                                slot_status = int(rows[0]['SlotStatus']),
                                # date_administered = rows[0]['WorkDay']
                                dose_number = 1
                                )
                cursor.execute(self.createAppointmentSQL)
                cursor.execute("SELECT @@IDENTITY AS 'Identity'; ")
                _identityRow = cursor.fetchone()
                vaccine_id = _identityRow['Identity']

                # flag as "Queued for first dose"
                self.updatePatientSQL = '''
                Update Patients
                Set VaccineStatus = (
                    SELECT StatusCodeId
                    FROM PatientAppointmentStatusCodes
                    WHERE StatusCode = 'Queued for 1st Dose'
                )'''
                cursor.execute(self.updatePatientSQL)
                return vaccine_id




        except pymssql.Error as db_err:    
            print("Database Programming Error in SQL Query processing! ")
            print("Exception code: " + db_err.args[0])
            if len(db_err.args) > 1:
                print("Exception message: " + str(db_err.args[1]))  
            print("SQL text that resulted in an Error: " + self.getAppointmentSQL)
            cursor.rollback()
            return -1

        

    def ScheduleAppointment(self,Vaccine,cursor):
        # Patient: VaccineStatus = Scheduled
        self.updatePatientSQL = '''
                Update Patients
                Set VaccineStatus = (
                    SELECT StatusCodeId
                    FROM PatientAppointmentStatusCodes
                    WHERE StatusCode = '1st Dose Scheduled'
                )'''
        cursor.execute(self.updatePatientSQL)

        # Vaccine Inventory updated
        self.sqltext = '''UPDATE Vaccines 
                        SET ReservedDoses = ReservedDoses+1, AvailableDoses = AvailableDoses-1
                        WHERE VaccineName = '{v_name}' '''.format(v_name = self.vaccine_name)

        cursor.execute(self.sqltext)
        # self.sqltext = '''SELECT * FROM Vaccines '''
        # cursor.execute(self.sqltext)
        # rows  = cursor.fetchall()
        # print(rows)
        # Vaccine Appointment Slot Status


