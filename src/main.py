import csv
import PySimpleGUI as sg

import ctypes

WINDOW_TITLE = 'Banking parser'
DEFAULT_PATH = 'C:/'
   
def read_csv(file_path):
    if file_path == '':
        raise ValueError('File path is empty')
    
    with open(file_path, 'r') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            print(row)


def main():
    ctypes.windll.shcore.SetProcessDpiAwareness(True)
    layout = [
        [sg.Text('Select file for parsing')],
        [
            sg.In(key='file_path', size=(40, 1), default_text=DEFAULT_PATH),
            sg.FileBrowse(file_types=(('CSV files', '*.csv'), ('All files', '*.*')))
        ],
        [sg.Button(button_text='Parse', key='-PARSE-'), sg.Button(button_text='Exit', key='-EXIT-')]
    ]
    window = sg.Window(WINDOW_TITLE).Layout(layout)

    while True:
        event, values = window.Read()
        if event == "-EXIT-" or event == sg.WIN_CLOSED:
            break
        elif event == "-PARSE-":
            file_path = values['file_path']
            read_csv(file_path)
    
    window.Close()
    


if __name__ == "__main__":
    main()