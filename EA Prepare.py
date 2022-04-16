################################################################
###############   Written by Dennis Koehler   ##################
###############  https://github.com/KDen404   ##################
###############   Written for Projekt Adler   ##################
###############   https://projekt-adler.eu/   ##################
################################################################

import os.path

fix = True
start_path = ""
search_for = ["using", "namespace"]
not_search_for = ["//using", "//namespace"]
searched_file_ending = ".cs"
backup_file_ending = ".bak"

def get_mode_from_user():
    global fix
    global search_for
    i = input("[prepare/fix]: ")
    if i == "prepare":
        fix = False

    elif i == "fix":
        fix = True

    else:
        print("input nicht erkannt!")
        print()
        print('Bitte "fix" oder "prepare" eingeben!')
        get_mode_from_user()

def get_path_from_user():
    print("Pfad eingeben auf welchen das script angewendet werden soll!")
    global start_path
    i = input("Pfad: ")
    try:
        start_path = str(i)
        if not start_path.endswith(str('\\')):
            start_path += str('\\')
        if not os.path.exists(i):
            raise OSError("Pfad Ungültig!")
    except OSError:
        get_path_from_user()

def parse_all_files(path):
    if fix:
        print("Wiederherstellung der Files wird begonnen!")
        parse_directory(path)
        print("Wiederherstellung erfolgreich beendet!")
    else:
        print("Parsen der Files wird begonnen!")
        parse_directory(path)
        print("Parsen erfolgreich beendet!")

def restore_file(file):
    os.remove(file)
    os.rename(file + str(backup_file_ending), file)

def create_backup(file_path):
    os.rename(file_path, file_path + str('.bak'))

def write_to_new_file(file_path, data):
    new_file = open(file_path, 'a')
    for line in data:
        new_file.write(line + str('\n'))
    new_file.close()

def parse_file(file_path):
    global search_for
    global not_search_for
    file_open_handle = open(file_path, 'r')
    file = file_open_handle.read()[3:].split(str('\n'), -1)
    file_open_handle.close()
    create_backup(file_path)

    linenumber = 0
    new_file_buffer = []

    for line in file:
        linenumber += 1

        if search_for[0] not in line and search_for[1] not in line:
            new_file_buffer.append(line)
        else:
            for i in range(2):
                if line.startswith(search_for[i]):
                    print(str("line ") + str(linenumber) + str(" changed") + str(": ") + line)
                    new_file_buffer.append(line.replace(search_for[i], not_search_for[i]))
                    break
    write_to_new_file(file_path, new_file_buffer)
    print()


#das hier ist der main loop des skripts
# hier wird das vom benutzer eingegebene verzeichnis rekursiv eingelesen
#  es werden entweder die .cs dateien vorbereitet und ein backup erstellt oder aus dem backup (.bak) die ursprüngliche datei wiederhergestellt
#   es werden nur dateien abgeändert welche für Enterprise Architect problematische direktiven enthalten
def parse_directory(current_directory):
    this_directory = os.listdir(current_directory)
    for element in this_directory:
        if os.path.isfile(str(current_directory) + str('\\') + str(element)):
            if element.endswith(searched_file_ending):
                if fix:
                    if os.path.isfile(str(current_directory) + str('\\') + str(element) + str(backup_file_ending)):
                        restore_file(str(current_directory) + str('\\') + str(element))
                else:
                    if not os.path.isfile(str(current_directory) + str('\\') + str(element) + str(backup_file_ending)):
                        file = open(str(current_directory) + str('\\') + str(element), 'r')
                        if "using" in file.read() or "namespace" in file.read():
                            file.close()
                            print(os.path.normpath(str(current_directory) + str('\\') + str(element)) + str(": "))
                            parse_file(str(current_directory) + str('\\') + str(element))
                    else:
                        print(str("File ist bereits vorbereitet: ") + os.path.normpath(str(current_directory) + str("\\") + str(element)))


        elif os.path.isdir(str(current_directory) + str('\\') + str(element)):
            parse_directory(str(current_directory) + str('\\') + str(element))
    return

def main(path):
    parse_all_files(path)


if __name__ == "__main__":
    print("Dieses Skript automatisiert das auskommentieren/einkommentieren von namespaces und using direktiven in C# files")
    print("damit diese in Enterprise Architect automatisch importiert werden können")
    print("NICHT AUF AKTIVE PROJEKTE ANWENDEN VORHER VORSICHTSHALBER EINE KOPIE ANFERTIGEN!!!")
    print()
    print("Auskommentieren = prepare")
    print("Rückgängig machen der Änderungen = fix")
    print()
    get_mode_from_user()
    get_path_from_user()

    print("Bist du dir sicher, dass du das Skript ausführen möchtest?")
    consent = input("[y/n]: ")
    if consent == "y":
        main(start_path)
    elif consent == "n":
        print("Programm abgebrochen!")
    else:
        print("Programm vorsichtshalber abgebrochen!")
