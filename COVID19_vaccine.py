import pymssql

class COVID19Vaccine:

    def __init__(self,name,supplier,doses_per_patient,days_between_doses,cursor):
        self.name = name
        self.doses_per_patient = doses_per_patient
        self.days_between_doses = days_between_doses
        self.sqltext = "INSERT INTO Vaccines (VaccineName, VaccineSupplier, AvailableDoses, ReservedDoses, TotalDoses, DosesPerPatient, DaysBetweenDoses) VALUES ('" + name + "','" + supplier + "',0,0,0,{doses},{days})".format(doses =doses_per_patient,days = days_between_doses)
        try: 
            cursor.execute(self.sqltext)
            cursor.connection.commit()

            # cursor.connection.commit()
            print('Query executed successfully. Vaccine: ' + name)
        except pymssql.Error as db_err:
            print("Database Programming Error in SQL Query processing for Vaccine! ")
            print("Exception code: " + str(db_err.args[0]))
            if len(db_err.args) > 1:
                print("Exception message: " + db_err.args[1])
            print("SQL text that resulted in an Error: " + self.sqltext)

    def AddDoses(self,vaccineName,count,cursor):

        
        self.sqltext = "UPDATE Vaccines SET AvailableDoses =AvailableDoses + {count} ,TotalDoses = TotalDoses + {count} WHERE VaccineName = '{name}'".format(count= count, name = vaccineName)
  

        try:
            cursor.execute(self.sqltext)
            cursor.connection.commit()
            print("Vaccine updated successfully")
        except pymssql.Error as db_err:
            print("Database Programming Error in SQL Query processing for Adding Vaccines! ")
            print("Exception code: " + str(db_err.args[0]))
            if len(db_err.args) > 1:
                print("Exception message: " + db_err.args[1])
            print("SQL text that resulted in an Error: " + self.sqltext) 
        


    def ReserveDoses(self, vaccineName, cursor):

        sqltext = "SELECT * FROM Vaccines WHERE VaccineName = '{name}'".format(name = vaccineName)
        try:
            cursor.execute(sqltext)
            rows  = cursor.fetchall()
            if len(rows)==0:
                print("Vaccine Not Available")
            elif rows[0]["AvailableDoses"]<rows[0]['DosesPerPatient']:
                print("Vaccine Not Available")
            else:
                doseCount = rows[0]['DosesPerPatient']
                self.sqltext = "UPDATE Vaccines SET AvailableDoses =AvailableDoses-{nums}, ReservedDoses = ReservedDoses+{nums}".format(nums = doseCount)
                cursor.execute(self.sqltext)
                cursor.connection.commit()
                print("Vaccine Reservation Successful")
            
        except pymssql.Error as db_err:
            print("Database Programming Error in SQL Query processing for reserving Vaccines! ")
            print("Exception code: " + str(db_err.args[0]))
            if len(db_err.args) > 1:
                print("Exception message: " + db_err.args[1])
            print("SQL text that resulted in an Error: " + self.sqltext) 
                  
