# D-codage-des-QR-codes-Wi-Fi
--------------------------------------------------------
    Analyseur de QR Code Facile - README
--------------------------------------------------------

Description :
-------------
Ce projet est une application Streamlit qui vous permet de scanner des QR codes contenant des informations Wi-Fi. L'application analyse le QR code, extrait les données et les affiche sous forme de tableau. Elle permet aussi de télécharger les résultats au format CSV.

Fonctionnalités :
-----------------
- Décodage des QR codes Wi-Fi.
- Affichage structuré des informations extraites (SSID, mot de passe, sécurité, etc.).
- Sauvegarde des résultats sous forme de fichier CSV.
- Historique des scans pour consulter les QR codes précédemment analysés.
- Interface simple avec Streamlit pour télécharger des images ou prendre des photos via la webcam.

Prérequis :
-----------
- Python 3.x
- Bibliothèques : Streamlit, pyzbar, Pillow, pandas

Installation :
-------------
1. Clonez ce dépôt sur votre machine :
   git clone https://github.com/votre-nom/votre-repo.git

2. Allez dans le répertoire du projet :
   cd votre-repo

3. Créez un environnement virtuel (facultatif mais recommandé) :
   python -m venv venv

4. Activez l'environnement virtuel :
   - Sur Windows : venv\Scripts\activate
   - Sur macOS/Linux : source venv/bin/activate

5. Installez les dépendances :
   pip install -r requirements.txt

Utilisation :
-------------
1. Lancez l'application Streamlit avec la commande suivante :
   streamlit run qr_wifi_streamlit.py

2. Ouvrez votre navigateur à l'adresse suivante :
   http://localhost:8501

3. Téléchargez une image contenant un QR Code ou utilisez la webcam pour scanner un QR Code en temps réel.

4. Les résultats seront affichés sous forme de tableau. Si le QR Code contient des informations Wi-Fi, vous verrez le SSID, le mot de passe, la sécurité, etc.

5. Vous pouvez télécharger les résultats sous forme de fichier CSV en cliquant sur le lien fourni.

Historique des scans :
-----------------------
Tous les QR codes scannés sont enregistrés dans l'historique de l'application et peuvent être consultés dans l'onglet "Historique". Vous pouvez également effacer l'historique en cliquant sur le bouton prévu à cet effet.

Crédits :
---------
- Développé par : Issa Bathily
- Basé sur : pyzbar (https://github.com/mchehab/pyzbar), Streamlit (https://streamlit.io/), Pillow (https://pillow.readthedocs.io/), pandas (https://pandas.pydata.org/)

--------------------------------------------------------
