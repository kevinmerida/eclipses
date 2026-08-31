import cv2
import numpy as np


def eclipse_orth(vid_ent="anim2d-380.mp4", vid_sor="pce2orth_opencv.mp4", lambda0=-51 + 25, phi0=14 + 50 / 60, sig_theta=1, T=380):

    # --- INITIALISATION ET PRÉ-CALCULS GÉOMÉTRIQUES ---
    cap = cv2.VideoCapture(vid_ent)
    fps = cap.get(cv2.CAP_PROP_FPS)

    # Lecture d'une frame pilote pour obtenir les dimensions d'origine
    ret, first_frame = cap.read()
    if not ret:
        raise ValueError("Impossible de lire la vidéo")

    Y, X, _ = first_frame.shape

    # Paramètres astrophysiques / géométriques
    delta_az = 15 / 60
    inclinaison = 23.44
    theta0 = sig_theta*180*np.arctan(np.sqrt(np.sin(np.pi * inclinaison / 180)**2 -
                                             np.sin(np.pi * phi0 / 180)**2)/np.cos(np.pi * inclinaison / 180))/np.pi

    # Conversion des angles de référence en radians
    phi0_rad = np.pi * phi0 / 180
    theta0_rad = np.pi * theta0 / 180

    # Génération de la grille cible (Meshgrid standard)
    xf, yf = np.meshgrid(np.linspace(-1, 1, T), np.linspace(1, -1, T))

    # Application de la rotation statique (theta0)
    xrot = xf * np.cos(theta0_rad) + yf * np.sin(theta0_rad)
    yrot = -xf * np.sin(theta0_rad) + yf * np.cos(theta0_rad)

    # Calcul des coordonnées sphériques sur le disque (rho <= 1)
    rho = np.sqrt(xrot**2 + yrot**2)
    mask = rho <= 1

    c = np.arcsin(rho[mask])
    phi = np.arcsin(np.cos(c) * np.sin(phi0_rad) +
                    yrot[mask] * np.sin(c) * np.cos(phi0_rad) / rho[mask])

    # Pré-calcul partiel de la longitude (sans lambda0 qui varie)
    lamb_base = np.arctan2(xrot[mask] * np.sin(c), (rho[mask] * np.cos(
        phi0_rad) * np.cos(c) - yrot[mask] * np.sin(phi0_rad) * np.sin(c)))

    # --- PRÉPARATION DES ENREGISTREURS ---
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(vid_sor, fourcc, fps, (T, T))

    # Pré-allocation des matrices de mapping pour cv2.remap
    # OpenCV requiert des matrices au format float32
    map_x = np.zeros((T, T), dtype=np.float32)
    map_y = np.zeros((T, T), dtype=np.float32)

    # Conversion de la latitude (phi) en indices de pixels Y (Statique : ne change jamais)
    # Formule inverse de : y = np.linspace(np.pi/2, -np.pi/2, Y)
    # y_pixel = (phi - (pi/2)) / (-pi / (Y - 1))
    map_y[mask] = (phi - np.pi / 2) * (1 - Y) / np.pi

    # Traitement de la première frame
    RGB = first_frame

    # --- BOUCLE PRINCIPALE ULTRA-RAPIDE ---
    while ret:
        # 1. Ajout de la colonne de rebouclage (continuité circulaire)
        # Remplacement de concatenate par une affectation directe (plus rapide)
        RGB_extended = np.empty((Y, X + 1, 3), dtype=np.uint8)
        RGB_extended[:, :X, :] = RGB
        RGB_extended[:, X, :] = RGB[:, 0, :]

        # Injection des repères visuels demandés dans votre code d'origine
        RGB_extended[0, 0, :] = [255, 255, 255]
        RGB_extended[int(Y / 2), :, :] = [0, 255, 0]
        RGB_extended = cv2.putText(RGB_extended, "Equateur", (int(
            0.25*X), int(0.49*Y)), cv2.FONT_HERSHEY_SCRIPT_SIMPLEX, 0.4, (0, 128, 0), 1)
        RGB_extended = cv2.putText(RGB_extended, "Equateur", (int(
            0.5*X), int(0.49*Y)), cv2.FONT_HERSHEY_SCRIPT_SIMPLEX, 0.4, (0, 128, 0), 1)
        RGB_extended = cv2.putText(RGB_extended, "Equateur", (int(
            0.75*X), int(0.49*Y)), cv2.FONT_HERSHEY_SCRIPT_SIMPLEX, 0.4, (0, 128, 0), 1)

        # 2. Calcul de la longitude dynamique (dépend de lambda0)
        lambda0_rad = np.pi * lambda0 / 180
        lamb = lamb_base + lambda0_rad
        lamb = np.remainder(lamb + 3 * np.pi, 2 * np.pi) - np.pi

        # 3. Conversion de la longitude (lamb) en indices de pixels X
        # Formule inverse de : x = np.linspace(-np.pi, np.pi, X+1)
        map_x[mask] = (lamb + np.pi) * X / (2 * np.pi)

        # Gestion des pixels hors du disque (rho > 1) -> pointent vers un pixel neutre (ex: 0,0)
        map_x[~mask] = 0
        map_y[~mask] = 0

        # 4. L'INTERPOLATION MAGIQUE D'OPENCV (Bilinéraire par défaut)
        RGBout = cv2.remap(RGB_extended, map_x, map_y, interpolation=cv2.INTER_LINEAR,
                           borderMode=cv2.BORDER_CONSTANT, borderValue=(0, 0, 0))

        # Ligne noire centrale
        RGBout[int(T / 2), :, :] = [0, 0, 0]
        RGBout = cv2.putText(RGBout, "Plan de l'Ecliptique", (int(
            0.05*T), int(0.49*T)), cv2.FONT_HERSHEY_SCRIPT_SIMPLEX, 0.75, (64, 64, 64), 1)

        # Écriture et affichage
        out.write(RGBout)
        cv2.imshow('RGBout', RGBout)

        # Passage à l'image suivante
        lambda0 -= delta_az
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        ret, RGB = cap.read()

    cap.release()
    out.release()
    cv2.destroyAllWindows()
