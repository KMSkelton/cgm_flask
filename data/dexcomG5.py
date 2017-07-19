import sys
sys.path.append("../")
# from cgmFlask.models import *
import cgmFlask.models as m

from numpy import genfromtxt, dtype
import pandas as pd
from time import time
from datetime import datetime
from sqlalchemy import Column, Integer, Float, Date
import sqlalchemy as db
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

def load_data(file_name, dType):
    # data = genfromtxt(file_name, delimiter=',', dtype=dType, names = None, missing_values = '', filling_values = 0 )
    # data = genfromtxt(file_name, delimiter=',', dtype=dType, skip_header=1)
    data = pd.read_table(file_name, sep=',')
    return data

def create_meas_record(opts):
    ''' options for create measurement require measuremant date, glucose value, insulin value, carbohydrate value, event type, manufacturerID, device_id and user_id '''


def create_user_record(name, userName):
    ''' options for create user require name and username '''
    print('User Created: ', name, userName)
    record = m.User(**{
        'username': userName,
        'name': name
    })
    print(record)
    return record


def create_device_record(opts):
    ''' options for create device require model, manufacturerID and user_id '''


Base = declarative_base()

if __name__ == "__main__":
    engine = create_engine('mysql://sooperAdmin:I<3lambKebabs@localhost/cgmviz')

    session=sessionmaker()
    session.configure(bind=engine)
    s = session()

    try:
        file_name="CLARITY.csv"
        dt = dtype([('index', 'i4'), ('date', 'datetime64[us]'), ('eventType', 'U25'), ('eventSubType', 'U15'), ('patientInfo', 'U20'), ('deviceInfo', 'U50'), ('manufacturerID', 'U10'), ('gluc_value', 'i4'), ('insulin_value', 'i4'), ('carb_value', 'i4'), ('duration', 'm'), ('glucRateChange', 'i4'), ('transmitterTime', 'i8') ])

        data=load_data(file_name, dt)
        ''' pandas loads all that data into memory but the trade off is we can access dict locations more than once, and we can go back to before where we are accessing '''
        # I'm going to create a user by passing in databse locations that correspond to the needed information
        # will getting the first and last names together in the same "name" field be tricky?
        firstName = data.loc[data['Event Type'] == 'FirstName']['Patient Info'].iloc[0]
        print(firstName)
        lastName = data.loc[data['Event Type'] == 'LastName']['Patient Info'].iloc[0]
        userName = firstName[:4] + lastName[-4:]
        name = firstName + ' ' + lastName
        record = create_user_record(name, userName)
        s.add(record)
        # commit should be moved to the end of try, to capture all the changes made to the database
        s.commit()
        print("Done creating user")

        # I'm also going to create a device entry the same way I am making user entries.

        # PANDAS DATAFRAME RELATED:
        # This gets the Event Type column then gets the 0th row of that. This will get more info from the column.
        # print(data['Event Type'].iloc[0])

        # This gets the 0th row, then gets the 'event type' column. This will get more info from the row.
        # print(data.iloc[0]['Event Type'])

        for i in data:
            print(i)
            if i[2] == 'EGV':
                create_meas_record(i[1] + i[2] + i[6] + i[7])

    except Exception as inst:
        print(type(inst))
        print(inst.args)
        print(inst)
        s.rollback()
    finally:
        s.close()
