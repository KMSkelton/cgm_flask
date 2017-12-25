import sys
sys.path.append("../")
# from models import *
import models as m

from numpy import genfromtxt, dtype
import pandas as pd
from time import time
from datetime import datetime
from sqlalchemy import Column, Integer, Float, Date
import sqlalchemy as db
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import NoResultFound

def load_data(file_name, dType):
    # data = genfromtxt(file_name, delimiter=',', dtype=dType, names = None, missing_values = '', filling_values = 0 )
    # data = genfromtxt(file_name, delimiter=',', dtype=dType, skip_header=1)
    data = pd.read_table(file_name, sep=',')
    #print("data in load data", data)
    data.fillna(0, inplace=True)
    #print("data after fillna", data)
    return data

def create_meas_record(meas_date, event_type, manufacturerID, gluc_value, insulin_value, carb, userRecord, deviceRecord ):
    ''' options for create measurement require measurement date, glucose value, insulin value, carbohydrate value, event type, manufacturerID, device_id and user_id '''
    print('Measurement Record Created: ', meas_date, event_type, manufacturerID, gluc_value, insulin_value, carb, deviceRecord.id )
    measVars = {
        'meas_date': meas_date,
        'event_type': event_type,
        'manufacturerID': manufacturerID,
        'gluc_value': gluc_value,
        'insulin_value': insulin_value,
        'carb': carb,
        'user_id': userRecord.id,
        'device_id': deviceRecord.id
    }
    try:
        return s.query(m.Measurement).filter_by(**measVars).one()
    except NoResultFound:
        record = m.Measurement(**measVars)
        print("Create Meas record record: ", record, record.__dict__, dir(record))
    return record

def create_user_record(name, userName):
    ''' options for create user require name and username '''
    print('Attempting to create user: ', name, userName)
    userVars = {
        'username': userName,
        'name': name
    }
    try:
        return s.query(m.User).filter_by(**userVars).one()
    except NoResultFound:
        userRecord = m.User(**userVars)
        print("Create User userRecord userRecord: ", userRecord, userRecord.__dict__, dir(userRecord))
        return userRecord


def create_device_record(model, manufacturerID, userRecord):
    ''' options for create device require model, manufacturerID and user_id '''
    print('Device Created: ', model, manufacturerID, userRecord.id)

    deviceVars = {
            'model': model,
            'manufacturerID': manufacturerID,
            'user_id': userRecord.id
    }
    try:
        return s.query(m.Device).filter_by(**deviceVars).one()
    except NoResultFound:
        deviceRecord = m.Device(**deviceVars)
        print("Device Record record: ", deviceRecord.id, userRecord.id)
        return deviceRecord


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

        # I'm going to CREATE A USER by passing in databse locations that correspond to the needed information
        # will getting the first and last names together in the same "name" field be tricky?
        firstName = data.loc[data['Event Type'] == 'FirstName']['Patient Info'].iloc[0]
        # print(firstName)
        lastName = data.loc[data['Event Type'] == 'LastName']['Patient Info'].iloc[0]
        userName = firstName[:4] + lastName[-4:]
        name = firstName + ' ' + lastName
        userRecord = create_user_record(name, userName)
        s.add(userRecord)
        s.commit()
        # commit should be moved to the end of try, to capture all the changes made to the database
        print("Done creating user", userRecord.id)

        # I'm also going to CREATE A DEVICE entry the same way I am making user entries.
        deviceData = data[data['Event Type'] == 'Device']
        for (i, row) in deviceData.iterrows():
            model = row[5]
            manufacturerID = row[6]
            userRecordID = userRecord
            print("mod, manuf, userRecID: ", model, manufacturerID, userRecordID)
            deviceRecord = create_device_record(model, manufacturerID, userRecordID)
            print("record: ", deviceRecord, userRecord.id)
            s.add(deviceRecord)

        s.commit()
        # PANDAS DATAFRAME RELATED:
        # This gets the Event Type column then gets the 0th row of that. This will get more info from the column.
        # print(data['Event Type'].iloc[0])

        # This gets the 0th row, then gets the 'event type' column. This will get more info from the row.
        # print(data.iloc[0]['Event Type'])
        measData = data
        for (i, row) in data.iterrows():
            if row[2] == 'EGV':
                print("what is this?", i, row.iloc[6])
                measDeviceID = s.query(m.Device).filter_by(**{'manufacturerID': row[6]}).one()
                print('MEASDEVICEID:  ', measDeviceID)
                measRecord = create_meas_record(row[1], row[2], row[6], row[7], row[8], row[9], userRecord, deviceRecord)
                print(measRecord)
                s.add(measRecord)
        s.commit()




    except Exception as inst:
        print(type(inst))
        print(inst.args)
        print(inst)
        s.rollback()
    finally:
        s.close()
