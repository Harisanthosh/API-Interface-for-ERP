:: This batch is used to store the results from csv into Database for further analysis
@ECHO OFF
ECHO ON
ECHO Result Extraction from Anylogic
ECHO Converting the results to csv...
python tabtocsv.py
:: SET tb_created=No
ECHO Press any key to enter values to DB
:: csvcut sir_output.csv --delete-empty-rows >> sir_output_edited.csv
PAUSE
:: csvsql --db "postgresql://localhost:5432/postgres?user=postgres&password=harisan" --insert --no-create sir_output_edited.csv
csvsql --db "postgresql://localhost:5432/postgres?user=postgres&password=harisan" --insert sir_output.csv

IF %ERRORLEVEL% NEQ 0 ( 
   csvsql --db "postgresql://localhost:5432/postgres?user=postgres&password=harisan" --insert --no-create sir_output.csv
)

:: csvsql --db "tfweb@//127.0.0.1:1563/grerp?user=tfweb&password=tfweb" --insert sir_output_edited.csv
:: csvsql --db "oracle+cx_oracle://tfweb:tfweb@127.0.0.1:1563/grerp" --insert sir_output_edited.csv
ECHO Insertion into DB Complete
PAUSE