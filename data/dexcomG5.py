import sys
sys.path.append("../")
from cgmFlask.models import *

from numpy import genfromtxt, dtype
from time import time
from datetime import datetime
# from sqlalchemy import Column, Integer, Float, Date
import sqlalchemy as db
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

def Load_Data(file_name, dType):
    data = genfromtxt(file_name, delimiter=',', dtype=dType, skip_header=1)
    return data.tolist()

Base = declarative_base()

if __name__ == "__main__":
    engine = create_engine('mysql://sooperAdmin:I<3lambKebabs@localhost/cgmviz')

    session=sessionmaker()
    session.configure(bind=engine)
    s = session()

    try:
        file_name="CLARITY.csv"
        dt = dtype([('index', 'i4'), ('date', 'datetime64[us]'), ('eventType', 'U25'), ('eventSubType', 'U15'), ('patientInfo', 'U20'), ('deviceInfo', 'U50'), ('manufacturerID', 'U10'), ('gluc_value', 'i4'), ('insulin_value', 'i4'), ('carb_value', 'i4'), ('duration', 'm'), ('glucRateChange', 'i4'), ('transmitterTime', 'i8') ])

        data=Load_Data(file_name, dt)
        for i in data:
            print(i)

    except Exception as inst:
        print(type(inst))
        print(inst.args)
        print(inst)
        s.rollback()
    finally:
        s.close()
