
"""
 Program to load and store the entries from csv file to Oracle DB
"""

import csv, ast
from sshtunnel import SSHTunnelForwarder
import cx_Oracle
import pandas as pd
import sys
import datetime


def dataType(val, current_type):
    try:
        if isinstance(val, datetime.date):
            return 'date'
        # Evaluates numbers to an appropriate type, and strings an error
        t = ast.literal_eval(val)
    except ValueError:
        return 'varchar'
    except SyntaxError:
        return 'varchar'
    if type(t) in [int, float]:
       if (type(t) in [int]) and current_type not in ['float', 'varchar']:
           # Use smallest possible int type
           if (-32768 < t < 32767) and current_type not in ['int', 'bigint']:
               return 'smallint'
           elif (-2147483648 < t < 2147483647) and current_type not in ['bigint']:
               return 'int'
           else:
               return 'bigint'
       if type(t) is float and current_type not in ['varchar']:
           return 'decimal'
    else:
        return 'varchar'



# ssh variables
host = 'pps03.hs-el.de'
localhost = '127.0.0.1'
ssh_username = 'oracle'
#ssh_private_key = 'D:\HariMasters\SIMPROD\ERP\pps06.ppk'
ssh_private_key = 'pps06_rsa'

# database variables
user='tfweb'
password='tfweb'
database='grerp'

# port=server.local_bind_port,

def query(fi=sys.argv[1]):
    csv_file = fi.split('.')[0] + '.csv'
    #csv_file = namea + '.csv'
    print(csv_file)
    f = open(csv_file, 'r')
    reader = csv.reader(f)
    longest, headers, type_list = [], [], []
    lines = []
    for row in reader:
        try:
            lines.append(row)
            if len(headers) == 0:
                headers = row
                for col in row:
                    longest.append(0)
                    type_list.append('')
            else:
                for i in range(len(row)):
                    # NA is the csv null value
                    if type_list[i] == 'varchar' or type_list[i] == 'date' or row[i] == 'NA':
                        pass
                    else:
                        var_type = dataType(row[i], type_list[i])
                        type_list[i] = var_type

                    try:
                        if len(row[i]) > longest[i]:
                            longest[i] = len(row[i])
                    except IndexError:
                        longest[i] = len(row[i])
        except IndexError:
            print("List out of range")

    f.close()

    q = 'create table ' + csv_file.split('.')[0] + ' ( '

    for i in range(len(headers)):
        if type_list[i] == 'varchar':
            q = (q + '{} varchar({}),').format(headers[i].lower(), str(longest[i]))
        else:
            q = (q + '{} {}' + ',').format(headers[i].lower(), type_list[i])

    q = q[:-1] + ')'

    print(q)

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
            c.execute(q)  # use triple quotes if you want to spread your query across multiple lines
            nlines = lines[1:]
            # c.executemany("insert into sir_output(location,infectedpeople) values (:1, :2)", nlines)
            c.executemany("insert into " + csv_file.split('.')[0] + " values (:1, :2, :3)", nlines)
            conn.commit()
            c.close()
            conn.close()
        except:
            nlines = lines[1:]
            c.executemany("insert into " + csv_file.split('.')[0] + " values (:1, :2, :3)", nlines)
            conn.commit()
            c.close()
            conn.close()
        # for row in c:
        #     print(row)
        # conn.close()


#query("select * from ARTIKEL where ART_NR LIKE '5312%'")
if __name__ == "__main__":
    query()

