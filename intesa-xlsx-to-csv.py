import pandas
import sys
import datetime
import csv
import sqlite3

## converte il file xlsx in csv
x = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
file = sys.argv[1]
excelFile = pandas.read_excel (file)
excelFile.to_csv (x, index = None, header=True,sep=';', quoting=csv.QUOTE_NONE)

try:
    with open(x, 'r') as fr:
        lines = fr.readlines()
        with open(x, 'w') as fw:
            for line in lines:
               

                if  line.startswith('2') :
                    print("non rimossa")
                    fw.write(line)
                else :
                    print("Deleted")
except:
    print("Oops! something error")
    exit()


## rimuovere tutte le righe prima dei dati prima di importarlo su mariadb
# rimuovere fino a data;descrizione, ecc.. riga compresa

## mi connetto al db e inserisco quelle non già presenti
connection = sqlite3.connect('database.db')
connection.row_factory = sqlite3.Row
connection.execute('CREATE TABLE IF NOT EXISTS dati_xlsx_to_csv (id integer primary key autoincrement not null,Data varchar(19) NOT NULL,Operazione varchar(73) NOT NULL,Dettagli varchar(267) NOT NULL,ContoOcarta varchar(47) NOT NULL,Contabilizzazione varchar(18) NOT NULL,Categoria varchar(41) NOT NULL,Valuta varchar(3) NOT NULL,Importo decimal(7,2) NOT NULL,UNIQUE(Data,Operazione,Dettagli,ContoOcarta,Contabilizzazione,Categoria,Valuta,Importo))')
connection.commit()

sum=0
err=0

with open(x,'r') as file2:
     for row in file2:
         #print(row)
         try:
            connection.execute('INSERT INTO dati_xlsx_to_csv (Data,Operazione,Dettagli,ContoOcarta,Contabilizzazione,Categoria,Valuta,Importo) VALUES ( ?, ?, ?, ?, ?, ?, ?, ?)',row.split(";"))            # Floor Division : Gives only Fractional Part as Answer
            #connection.commit()
            # commit commentato per vedere come andrebbe ad operare      
            sum=sum+1
            print(row)
         except :
            err=err+1

connection.close()

print("Righe inserite: ")
print(sum)
print("Righe già presenti: ")
print(err)
