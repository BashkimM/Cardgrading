import os
import time
import shutil
import zipfile
import json

# Importieren Sie die Funktionen oder Klassen aus den Analyse-Skripten
from analyze_centering import analyze_centering
from analyze_edge import analyse_edge
from analyze_corner import analyse_corner

# Das Verzeichnis, das Sie überwachen möchten
verzeichnis_pfad = 'sourceDirectory'

# Das Verzeichnis, in das die Auswertungsdateien verschoben werden sollen
ziel_verzeichnis = 'destinationDirectory'

# Das Verzeichnis, in dem die Auswertungen gespeichert werden sollen
auswertungs_verzeichnis = 'gradedCardsDirectory'

# Entpacken Sie die Zip-Datei in ein temporäres Verzeichnis
temp_verzeichnis = 'tempDirectory'

# Initialisiere eine Liste der bereits verarbeiteten Dateien
verarbeitete_dateien = set()

def analyse_json(json_pfad):
    # Hier können Sie die Verarbeitung des JSON-Objekts durchführen
    with open(os.path.join(temp_verzeichnis, json_pfad), 'r') as json_datei:
        json_inhalt = json.load(json_datei)
        # Hier können Sie mit den JSON-Daten arbeiten
        return json_inhalt

def verarbeite_bild(bild_pfad):
    # Hier können Sie die Verarbeitung des Bildes unter Verwendung des JSON-Arrays durchführen
    bearbeitetes_array = []
    
    # Rufen Sie die entsprechenden Funktionen oder Klassen aus den Analyse-Skripten auf
    bearbeitetes_array_centering = analyze_centering(bild_pfad)
    bearbeitetes_array_edge = analyse_edge(bild_pfad)
    bearbeitetes_array_corner = analyse_corner(bild_pfad)
    
    # Fügen Sie die Ergebnisse der Analysen dem bearbeiteten Array hinzu oder verarbeiten Sie sie
    # bearbeitetes_array.extend(bearbeitetes_array_centering)
    # bearbeitetes_array.extend(bearbeitetes_array_edge)
    # bearbeitetes_array.extend(bearbeitetes_array_corner)
    
    return bearbeitetes_array

while True:
    # Liste der Dateien im Verzeichnis abrufen
    dateien = os.listdir(verzeichnis_pfad)
    
    # Überprüfen Sie, ob neue Dateien hinzugefügt wurden
    neue_dateien = [datei for datei in dateien if datei not in verarbeitete_dateien]
    
    if neue_dateien:
        print(f'Neue Dateien gefunden: {neue_dateien}')
        
        # Hier können Sie die Verarbeitung der Dateien durchführen
        
        for datei in neue_dateien:
            quelle = os.path.join(verzeichnis_pfad, datei)
            
            # Überprüfen, ob es sich um eine Zip-Datei handelt
            if datei.endswith('.zip'):
                with zipfile.ZipFile(quelle, 'r') as zip_datei:
                    print(f'Inhalt:{datei} verschoben nach {temp_verzeichnis}')
                    zip_datei.extractall(temp_verzeichnis)
                
                # Hier können Sie die JSON-Datei verarbeiten und das JSON-Array erhalten
                json_array = None
                
                # Überprüfen Sie den Inhalt des temporären Verzeichnisses (Analyse JSON)
                temp_dateien = os.listdir(temp_verzeichnis)
                for temp_datei in temp_dateien:
                    temp_pfad = os.path.join(temp_verzeichnis, temp_datei)
                    if temp_datei.endswith('.json'):
                        json_array = analyse_json(temp_datei)
                
                # Überprüfen Sie den Inhalt des temporären Verzeichnisses (Analyse Bild)
                temp_dateien = os.listdir(temp_verzeichnis)
                for temp_datei in temp_dateien:
                    temp_pfad = os.path.join(temp_verzeichnis, temp_datei)
                    if temp_datei.endswith('.jpg') or temp_datei.endswith('.png'):
                        # Verarbeiten Sie das Bild unter Verwendung des JSON-Arrays
                        bearbeitetes_array = verarbeite_bild(temp_pfad)
                
                # Speichern Sie das bearbeitete Array in einer separaten Textdatei im Auswertungsverzeichnis
                auswertungs_datei = os.path.splitext(datei)[0] + '_auswertung.txt'
                auswertungs_pfad = os.path.join(auswertungs_verzeichnis, auswertungs_datei)
                
                with open(auswertungs_pfad, 'w') as auswertungsdatei:
                    auswertungsdatei.write(json.dumps(bearbeitetes_array))  # Schreiben Sie das Array als JSON in die Datei
                
                # Verschieben Sie die verarbeiteten Dateien in das Zielverzeichnis
                #ziel = os.path.join(ziel_verzeichnis, datei)
                #shutil.move(quelle, ziel)
                #print(f'Datei verschoben nach {ziel}')
                
            # Löschen Sie das temporäre Verzeichnis
            for temp_datei in temp_dateien:
                if temp_datei.endswith('.jpg') or temp_datei.endswith('.png'):
                    print(temp_verzeichnis + temp_datei )
                    try:
                        os.remove(temp_verzeichnis+ "/" +temp_datei)
                    except:
                        print("FileNotFoundError:Errno 2] No such file or directory: '" + temp_datei + "")
        
        # Fügen Sie die neu verarbeiteten Dateien zur Liste der verarbeiteten Dateien hinzu 
        verarbeitete_dateien.update(neue_dateien)
    
    # Warten Sie eine Weile, bevor Sie erneut nach neuen Dateien suchen
    time.sleep(5)  # Hier wird alle 5 Sekunden überprüft, Sie können dies anpassen
