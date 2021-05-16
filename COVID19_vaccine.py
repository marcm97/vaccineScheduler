import pymssql

class COVID19Vaccine:

    def __init__(self,name,doses,cursor):
        self.sqltext = "INSERT INTO Vaccine (VaccineName, Reserved,Used, Available,DoseCount) VALUES ('" + name + "','0','0','0',{doses})".format(doses =doses)
        self.vaccineId = 0
        try: 
            cursor.execute(self.sqltext)
            cursor.connection.commit()
            cursor.execute("SELECT @@IDENTITY AS 'Identity'; ")
            _identityRow = cursor.fetchone()
            self.vaccineId = _identityRow['Identity']
            # cursor.connection.commit()
            print('Query executed successfully. Vaccine: ' + name 
            +  ' added to the database using Vaccine ID = ' + str(self.vaccineId))
        except pymssql.Error as db_err:
            print("Database Programming Error in SQL Query processing for Vaccine! ")
            print("Exception code: " + str(db_err.args[0]))
            if len(db_err.args) > 1:
                print("Exception message: " + db_err.args[1])
            print("SQL text that resulted in an Error: " + self.sqltext)

    def AddDoses(self,vaccineName,count,cursor):

        
        self.sqltext = "UPDATE Vaccine SET Available =Available + {count} WHERE VaccineName = '{name}'".format(count= count, name = vaccineName)
  

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

        sqltext = "SELECT * FROM Vaccine WHERE VaccineName = '{name}'".format(name = vaccineName)
        try:
            cursor.execute(sqltext)
            rows  = cursor.fetchall()
            if len(rows)==0:
                print("Vaccine Not Available")
            elif rows[0]["Available"]<rows[0]['DoseCount']:
                print("Vaccine Not Available")
            else:
                doseCount = rows[0]['DoseCount']
                self.sqltext = "UPDATE Vaccine SET Available =Available-{nums}, Reserved = Reserved+{nums}".format(nums = doseCount)
                cursor.execute(self.sqltext)
                cursor.connection.commit()
                print("Vaccine Reservation Successful")
            
        except pymssql.Error as db_err:
            print("Database Programming Error in SQL Query processing for reserving Vaccines! ")
            print("Exception code: " + str(db_err.args[0]))
            if len(db_err.args) > 1:
                print("Exception message: " + db_err.args[1])
            print("SQL text that resulted in an Error: " + self.sqltext) 
                  
