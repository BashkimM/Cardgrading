import cv2

class analyze_centering:
    def __init__(self, bild_pfad):
        self.bild_pfad = bild_pfad
    
    def analyze(self):
        # Lade das Bild
        bild = cv2.imread(self.bild_pfad)
        
        if bild is None:
            print("Fehler: Bild konnte nicht geladen werden.")
            return None
        
        # Führen Sie hier Ihre Zentrierungsanalyse durch
        # Zum Beispiel, ermitteln Sie das Zentrum des Bildes oder prüfen Sie, ob das Bild zentriert ist
        
        # Beispiel: Berechnen Sie die Mitte des Bildes
        höhe, breite, _ = bild.shape
        mitte_x = breite // 2
        mitte_y = höhe // 2
        
        # Beispiel: Überprüfen Sie, ob die Mitte des Bildes nahe am tatsächlichen Zentrum ist
        toleranz = 10
        ist_zentriert = abs(mitte_x - breite/2) <= toleranz and abs(mitte_y - höhe/2) <= toleranz
        
        # Hier können Sie weitere Analysen und Berechnungen durchführen
        
        # Geben Sie das Analyseergebnis als Tupel zurück (ohne "ist_zentriert")
        analyse_ergebnis = (mitte_x, mitte_y)
        
        return analyse_ergebnis

if __name__ == "__main__":
    # Beispielverwendung der Klasse
    bild_pfad = "pfad_zum_bild.jpg"
    analyzer = analyze_centering(bild_pfad)
    mitte_x, mitte_y = analyzer.analyze()
    print("Zentrum des Bildes (X, Y):", mitte_x, mitte_y)
