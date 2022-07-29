import csv
from datetime import datetime as dt
from fileinput import close
import PySimpleGUI as sg

import ctypes

WINDOW_TITLE = 'Banking parser'
#DEFAULT_PATH = 'C:/'
DEFAULT_PATH = 'E:/Projekte/BankingAtEase/resources/Umsatzanzeige_DE97500105175425638062_20220728.csv'
ROW_SKIP_DEFAULT = 14

# Datum Buchung:    0
# Auftraggeber:     2
# Buchungstext:     3
# Verwendungszweck: 5
# Betrag:           8
# Saldo:            6

def read_csv(file_path, rows_to_skip):
    if file_path == '':
        raise ValueError('File path is empty')

    data = []
    
    with open(file_path, 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=';')

        for i in range(rows_to_skip):
            next(reader)

        for row in reader:
            date_entry = dt.strptime(row[0], '%d.%m.%Y')
            client = row[2].lower()
            text = row[3].lower()
            purpose = row[5].lower()
            balance = float(row[6].replace('.', '').replace(',', '.'))
            amount = float(row[8].replace('.', '').replace(',', '.'))

            data.append([date_entry, client, text, purpose, balance, amount])
        
        close()
    
    data.sort(key=lambda x: x[0])

    return data


def save_to_xlsm(data):
    for row in data:
        print(row)


def main():
    ctypes.windll.shcore.SetProcessDpiAwareness(True)

    layout = [
        [sg.Text('Select file for parsing')],
        [
            sg.In(key='file_path', size=(40, 1), default_text=DEFAULT_PATH),
            sg.FileBrowse(file_types=(('CSV files', '*.csv'), ('All files', '*.*')))
        ],
        [
            sg.Text('Rows to skip'),
            sg.In(key='skip_count', size=(5, 1), default_text=ROW_SKIP_DEFAULT, enable_events=True)
        ],
        [
            sg.Button(button_text='Parse', key='-PARSE-'), 
            sg.Button(button_text='Exit', key='-EXIT-')
        ]
    ]

    window = sg.Window(WINDOW_TITLE).Layout(layout)

    while True:
        event, values = window.Read()

        if event == 'skip_count' and values['skip_count'] and values['skip_count'][-1] not in ('0123456789'):
            window['skip_count'].Update(values['skip_count'][:-1])

        if event == "-EXIT-" or event == sg.WIN_CLOSED:
            break

        if event == "-PARSE-":
            file_path = values['file_path']
            rows_to_skip = int(values['skip_count'])

            data = read_csv(file_path, rows_to_skip)
            save_to_xlsm(data)
    
    window.Close()
    


if __name__ == "__main__":
    main()