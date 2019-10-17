

import csv
import os
from datetime import datetime
txt_file = "D:\HariMasters\SIMPROD\GenericSimulationproject\ERP\TransfactAPP\sir_output.tab"
csv_file = os.path.splitext(txt_file)[0] + ".csv"

def convert():
    with open(txt_file, "r") as in_text:
        in_reader = csv.reader(in_text, delimiter='\t')
        now = datetime.now()
        with open(csv_file, "w", newline='') as out_csv:
            out_writer = csv.writer(out_csv)
            row = next(in_reader)
            row.append('Timestamp')
            out_writer.writerow(row)
            for row in in_reader:
                # line = next(in_reader)
                if not ''.join(row).strip():
                    pass
                else:
                    row.append(str(now))
                    out_writer.writerow(row)
                # row = row.append('\t' + str(now))
def convert_file(file_par, namef):
    namea = namef.split('.')[0] + '.csv'
    csv_file = os.getcwd() + '\\' +namea
    #csv_file = "D:\Anylogic\AnyLogic 8.4 Personal Learning Edition\plugins\com.anylogic.examples_8.4.0.201903191549\models\SIR Agent Based Calibration\sir_output.csv"
    in_reader = csv.reader(file_par.read().decode('utf-8').splitlines(), delimiter='\t')
    now = datetime.now()
    with open(csv_file, "w", newline='') as out_csv:
        out_writer = csv.writer(out_csv)
        row = next(in_reader)
        row.append('Timestamp')
        out_writer.writerow(row)
        for row in in_reader:
            # line = next(in_reader)
            if not ''.join(row).strip():
                pass
            else:
                row.append(str(now))
                out_writer.writerow(row)
            # row = row.append('\t' + str(now))
    #with open(file_par.read(), "rb") as in_text:


convert()

