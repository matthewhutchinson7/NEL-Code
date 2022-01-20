"""
Created on Wed Jan 19 13:25:22 2022

@author: HutchinsonM
"""
#------------------------------------------------------------------------------

import pandas as pd
import numpy as np
import datetime as dt

#------------------------------------------------------------------------------

#find a random date between a start and end date by finding the timedelta, 
#multiplying this by a rand float between 0-1 and adding it back to the 
#start date
def rand_date(start,end):
    delta = end - start
    multiplier = np.random.rand()
    delta_add = delta * multiplier
    return start + delta_add

#creates lists for the df columns, uses them to build up the dataframe and 
#send to excel file
def generate_dataframe(file_name,column_name,start,end):
    IDList = np.random.choice(100000,100000)
    DiagnosisList = np.random.randint(1,6,100000)
    DateList = []
    for n in range(100000):
        date = rand_date(start,end)
        DateList.append(date)
    data = {'SK_EncounterID': IDList, column_name: DateList,'DiagnosisNumber': 
            DiagnosisList}
    df = pd.DataFrame(data)

    df.to_excel(file_name)
    

#-----------------------------------------------------------------------------

start_date = dt.datetime.strptime('01-04-2018', '%d-%m-%Y').date()
end_date = dt.datetime.strptime('31-03-2021', '%d-%m-%Y').date()

generate_dataframe('RandomDataIP.xlsx','AdmissionDate',start_date, end_date)
generate_dataframe('RandomDataAE.xlsx','StartDate',start_date,end_date)


