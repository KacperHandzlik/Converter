import sys
sys.path.append('../')
from src.convertion import line_to_list, csv_to_mt940
import PySimpleGUI as sg

if __name__ == "__main__":

    file_browsing = [[sg.Input(key="file_name"), sg.FileBrowse(button_text="Search")]
    ]
    name_of_file = [[sg.Input(key="mt940_name")]
    ]
    path_to_mt940 = [[sg.Input(key="mt_path"), sg.FolderBrowse(button_text="Search")]
    ]
    layout = [
        [sg.Text(text="choose file .csv")],
        [file_browsing],
        [sg.Text(text="file name .mt940")],
        [name_of_file],
        [sg.Text(text="file directory .mt940")],
        [path_to_mt940],
        [sg.Button(button_text="Convert", key="-CLICKED-", enable_events=True)]
    ]

    window = sg.Window("File converter from csv to mt940", layout)

    while True:
        event, values = window.read()

        if event == "Exit" or event == sg.WIN_CLOSED:
            break

        if event == "-CLICKED-":
            file_name = values["file_name"]
            mt_path = values["mt_path"]
            mt_name = values["mt940_name"]
            if mt_name == "":
                mt_name = file_name.split('/')[-1][:-4]
            try:
                csv_file = open(file_name, "r", encoding="utf-8")
            except UnicodeEncodeError:
                csv_file = open(file_name, "r", encoding="CP852")
            except FileNotFoundError:
                sg.Popup("Choose file .csv", keep_on_top=True)
                continue
            try:
                mt940_file = open(mt_path + "/" + mt_name + ".mt940", "w")

            except PermissionError:
                sg.Popup("Choose terget directory", keep_on_top=True)
                continue
            csv_list = []

            for line in csv_file:
                row = line_to_list(line)
                csv_list.append(row)
            csv_to_mt940(mt940_file, csv_list)
    window.close()
