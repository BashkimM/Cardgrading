import cv2
import numpy as np
import os
from ultralytics import YOLO
from ultralytics.utils.plotting import Annotator  # ultralytics.yolo.utils.plotting is deprecated

model = YOLO('runs/detect/train19/weights/best.pt')

def analyze_centering(bild_pfad):

    # Lade das Bild
    display_bild = cv2.imread(bild_pfad)
   
    # rotate picture
    # https://stackoverflow.com/questions/57713358/how-to-rotate-skewed-fingerprint-image-to-vertical-upright-position
    gray = cv2.cvtColor(display_bild, cv2.COLOR_BGR2GRAY)
    gray = 255 - gray + 60
    thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

    # Compute rotated bounding box
    coords = np.column_stack(np.where(thresh > 0))
    angle = cv2.minAreaRect(coords)[-1] 

    print("PRE:" + str(angle))

    if angle < 45:
        angle = -angle
    else:
        angle = 90 - angle

    print("POST:" + str(angle))

    # Rotate image to deskew
    (h, w) = display_bild.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    rotated = cv2.warpAffine(display_bild, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)

    # Run YOLOv8 tracking on the frame, persisting tracks between frames
    results = model.track(rotated)

    # Visualize the results on the frame
    annotated_frame = results[0].plot()

    #move windows
    #https://stackoverflow.com/questions/62450255/can-you-display-an-image-at-specific-screen-coordinates-with-opencv
    # Make your windows
    cv2.namedWindow('Raw Image', cv2.WINDOW_NORMAL)
    cv2.namedWindow('Inverted Image', cv2.WINDOW_NORMAL)
    cv2.namedWindow('Rotated Image', cv2.WINDOW_NORMAL)
    cv2.namedWindow('YOLOv8 Tracking', cv2.WINDOW_NORMAL)

    if display_bild is None:
        print(f"Fehler: Bild {bild_pfad} konnte nicht geladen werden.")
    else:
        # Zeigen Sie das Bild an (z.B., in einem separaten Fenster)
        cv2.imshow('Raw Image', display_bild)
        cv2.imshow('Inverted Image', thresh)
        cv2.imshow('Rotated Image', rotated)
        cv2.imshow('YOLOv8 Tracking', annotated_frame)

        # Then move your windows to where you want them
        cv2.moveWindow('Raw Image', 100, 50)
        cv2.moveWindow('Inverted Image', 1400, 50)
        cv2.moveWindow('Rotated Image', 2700, 50)
        cv2.moveWindow('YOLOv8 Tracking', 4000, 50)

        cv2.waitKey(0)  # Warten auf eine Taste, bevor das Fenster geschlossen wird
        cv2.destroyAllWindows()  # Schließen Sie alle offenen OpenCV-Fenster
    
    analyse_ergebnis = 10

    return analyse_ergebnis

if __name__ == "__main__":
    # Beispielverwendung der Funktion
    bild_pfad = "pfad_zum_bild.jpg"
    mitte_x, mitte_y = analyze_centering(bild_pfad)
    print("Zentrum des Bildes (X, Y):", mitte_x, mitte_y)
