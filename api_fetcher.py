"""
 Program to load the entries from Oracle DB and display it in GUI
"""
from fastapi import FastAPI, File, Form, UploadFile
import csv, ast
from sshtunnel import SSHTunnelForwarder, open_tunnel
#import paramiko
#from flask import send_file
from starlette.responses import FileResponse
import cx_Oracle
import pandas as pd
import sys
import datetime
import tabtocsv as tb
import insert_to_oracle_erp as insr

app = FastAPI(title="Anylogic Results in Transfact ERP", description="Retrieve Anylogic Model results stored in Oracle Database of Transfact ERP System")

# ssh variables
host = 'pps03.hs-el.de'
#host = 'pps03.hs-emden-leer.de'
localhost = '127.0.0.1'
ssh_username = 'oracle'
#ssh_private_key = 'D:\HariMasters\SIMPROD\ERP\pps06.ppk'
ssh_private_key = 'pps06_rsa'

# database variables
user='tfweb'
password='tfweb'
database='grerp'

# port=server.local_bind_port,
UPLOAD_FOLDER = 'D:/HariMasters/SIMPROD/uploads'
EXCEL_PATH = 'D:/HariMasters/SIMPROD/GenericSimulationproject/ERP/TransfactAPP/'

@app.post("/files/")
async def upload_result(
    fileb: UploadFile = File(...)
):
    """
     Upload a file with the extension of .tab which will be converted to a .csv file
     and used for insertion to the Oracle Database of the Transfact System
     [Note]: A new table will be created with the filename of the uploaded .tab file
    """
    # tb.convert_file(file,fileb.filename)
    tb.convert_file(fileb.file, fileb.filename)
    insr.query(fileb.filename)
    return {
        # "file_size": len(fileb.file.read()),
        "fileb_content_type": fileb.content_type,
    }
@app.delete("/files/{table}")
def remove_table(table: str):
    """
    Delete the table which was created in the ERP system with the name of the .tab file
    """
    q = "DROP TABLE " + table + " PURGE";
    with SSHTunnelForwarder(
            (host, 24226),
            ssh_username=ssh_username,
            ssh_pkey=ssh_private_key,
            remote_bind_address=(localhost, 1521),
            local_bind_address=(localhost, 1563)
    ) as server:
        dsn_tns = cx_Oracle.makedsn(localhost, 1563,
                                    service_name=database)
        conn = cx_Oracle.connect(user=user, password=password,
                                 dsn=dsn_tns)

        c = conn.cursor()
        print(q)
        try:
            c.execute(q)
            #res = c.fetchall()
            c.close()
            conn.close()
        except:
            c.execute(q)
            #res = c.fetchall()
            c.close()
            conn.close()
        return {"Table Removed Successfully !": table}
    #return {"Hello": table}

@app.get("/")
def read_root():
    """
    Random test function xD
    """
    return {"Hello": "World"}

# @app.get("/items/{item_id}")
# def read_item(item_id: int, q: str = None):
#     return {"item_id": item_id, "q": q}

@app.get("/erp/latest/{table}")
def get_latest_simulation_result(table: str):
    """
    Search for the latest simulation record in the table and returns it to the User
    """
    q = "select * from "+ table +" where Timestamp = (select max(Timestamp) from "+ table +" )";
    with SSHTunnelForwarder(
            (host, 24226),
            ssh_username=ssh_username,
            ssh_pkey=ssh_private_key,
            remote_bind_address=(localhost, 1521),
            local_bind_address=(localhost, 1563)
    ) as server:
        # client = paramiko.SSHClient()
        # client.connect(localhost, 1521)
        dsn_tns = cx_Oracle.makedsn(localhost, 1563,
                                    service_name=database)
        conn = cx_Oracle.connect(user=user, password=password,
                                 dsn=dsn_tns)

        c = conn.cursor()
        print(q)
        try:
            c.execute(q)
            res = c.fetchall()
            # res = c
            # val["Output"] = c
            c.close()
            conn.close()
        except:
            c.execute(q)
            res = c.fetchall()
            c.close()
            conn.close()
        return res


@app.get("/erp/{table}")
def query(table: str,filter_time: str = None):
    """
    Queries and returns the value of the records of the simulation from the database.
    [Note]: If timestamp is not included it fetches all the records from the table
    """
    if filter_time == None:
        q = "select * from "+ table +" ";
    else:
        q = "select * from "+ table +" where Timestamp = '"+filter_time+"'";

    with SSHTunnelForwarder(
            (host, 24226),
            ssh_username=ssh_username,
            ssh_pkey=ssh_private_key,
            remote_bind_address=(localhost, 1521),
            local_bind_address=(localhost, 1563)
    ) as server:
        dsn_tns = cx_Oracle.makedsn(localhost, 1563,
                                    service_name=database)
        conn = cx_Oracle.connect(user=user, password=password,
                                 dsn=dsn_tns)

        c = conn.cursor()
        print(q)
        try:
            c.execute(q)
            res = c.fetchall()
            #res = c
            #val["Output"] = c
            c.close()
            conn.close()
        except:
            c.execute(q)
            res = c.fetchall()
            c.close()
            conn.close()
        return res
        # for row in c:
        #     print(row)

@app.get("/download/{table}")
def download_table_as_excel(table: str, filter_time: str = None):
    """
    Downloads the entire data from the database as an excel file
    [Note]: If timestamp is not included it fetches all the records from the table
    """
    if filter_time == None:
        q = "select * from " + table + " ";
    else:
        q = "select * from " + table + " where Timestamp = '" + filter_time + "'";

    with SSHTunnelForwarder(
            (host, 24226),
            ssh_username=ssh_username,
            ssh_pkey=ssh_private_key,
            remote_bind_address=(localhost, 1521),
            local_bind_address=(localhost, 1563)
    ) as server:
        dsn_tns = cx_Oracle.makedsn(localhost, 1563,
                                    service_name=database)
        conn = cx_Oracle.connect(user=user, password=password,
                                 dsn=dsn_tns)

        c = conn.cursor()
        print(q)
        try:
            # c.execute(q)
            # res = c.fetchall()
            # c.close()
            data = pd.read_sql(q, conn)
            print(data.head())
            data.to_excel(table+'.xlsx')
            conn.close()
        except:
            data = pd.read_sql(q, conn)
            print(data.head())
            data.to_excel(table + '.xlsx')
            conn.close()
        #return data.to_excel(table + '.xlsx')
        return FileResponse(EXCEL_PATH+table+'.xlsx',media_type='application/octet-stream')
        #return send_file(EXCEL_PATH+table+'.xlsx', as_attachment=True)



