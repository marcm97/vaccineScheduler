def clear_tables(client):
    # sqlQuery = '''
    #            Truncate Table CareGiverSchedule
    #            DBCC CHECKIDENT ('CareGiverSchedule', RESEED, 0)
    #            Delete From Caregivers
    #            DBCC CHECKIDENT ('Caregivers', RESEED, 0)
    #            '''
    # client.cursor().execute(sqlQuery)
    # client.commit()

    sqlQuery = '''
               Truncate Table VaccineAppointments
Truncate Table Vaccines
Truncate Table CareGiverSchedule
Delete From Patients
Delete From Caregivers
               '''
    client.cursor().execute(sqlQuery)
    client.commit()
