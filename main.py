import streamlit as st
from pyzbar.pyzbar import decode
from PIL import Image
import pandas as pd
import io
import base64
from datetime import datetime


# Fonction pour extraire les informations Wi-Fi
def extract_wifi_info(qr_data):
    wifi_info = {}
    if qr_data.startswith('WIFI:'):
        data = qr_data[5:]
        params = data.split(';')
        for param in params:
            if param and ':' in param:
                key, value = param.split(':', 1)
                wifi_info[key] = value
    return wifi_info


# Fonction pour décoder le QR Code
def get_qr_info(image):
    try:
        decoded_objects = decode(image)
        qr_data = []
        for obj in decoded_objects:
            if obj.type == 'QRCODE':
                data = obj.data.decode('utf-8')
                entry = {
                    "Type": obj.type,
                    "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "Data": data
                }
                if data.startswith('WIFI:'):
                    wifi_info = extract_wifi_info(data)
                    entry.update({
                        "SSID": wifi_info.get('S', 'N/A'),
                        "Password": wifi_info.get('P', 'N/A'),
                        "Security": wifi_info.get('T', 'N/A'),
                        "Hidden": wifi_info.get('H', 'false')
                    })
                qr_data.append(entry)
        return qr_data
    except Exception as e:
        st.error(f"Erreur: {str(e)}")
        return []


# Fonction pour le lien de téléchargement CSV
def get_csv_download_link(df, filename="qr_data.csv"):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    return f'<a href="data:file/csv;base64,{b64}" download="{filename}">Télécharger en CSV</a>'


# Tutoriel interactif
def show_tutorial():
    with st.expander("📚 Comment utiliser cette application ?", expanded=False):
        st.markdown("""
        ### Bienvenue dans l'Analyseur de QR Code !
        Voici un guide rapide pour commencer :

        1. **Choisir une méthode** :
           - **Télécharger une image** : Cliquez sur "Téléchargez une image" pour sélectionner un fichier.
           - **Utiliser la webcam** : Cliquez sur "Utiliser la webcam" pour prendre une photo.

        2. **Analyser le QR Code** :
           - Une fois l'image chargée, les résultats s'affichent automatiquement.
           - Pour les QR Codes Wi-Fi, vous verrez les détails comme le SSID et le mot de passe.

        3. **Options utiles** :
           - **Historique** : Cochez "Afficher l'historique" dans la barre latérale pour voir vos scans précédents.
           - **Télécharger** : Cliquez sur le lien CSV pour sauvegarder les résultats.

        4. **Besoin d'aide ?** :
           - Utilisez les info-bulles (ℹ️) pour des explications rapides.
        """)
        st.success("Astuce : Essayez avec un QR Code Wi-Fi pour voir toutes les fonctionnalités !")


# Interface principale
def main():
    # Style CSS pour une interface fluide
    st.markdown("""
        <style>
        .stApp {max-width: 1200px; margin: 0 auto;}
        .wifi-box {background-color: #f0f2f6; padding: 15px; border-radius: 10px; margin: 10px 0;}
        .stButton>button {width: 100%; border-radius: 5px;}
        .stDataFrame {width: 100% !important;}
        </style>
    """, unsafe_allow_html=True)

    # Titre et introduction
    st.title("Analyseur de QR Code Facile")
    st.write("Scannez vos QR Codes en toute simplicité !")

    # Afficher le tutoriel
    show_tutorial()

    # Sidebar simplifiée
    with st.sidebar:
        st.header("Options")
        analyze_wifi = st.checkbox("Analyser Wi-Fi", value=True, help="Décoder les détails des QR Codes Wi-Fi")
        show_history = st.checkbox("Voir l'historique", value=False, help="Afficher tous vos scans précédents")

    # Initialisation de l'historique
    if 'qr_history' not in st.session_state:
        st.session_state.qr_history = []

    # Section principale avec tabs pour une navigation fluide
    tab1, tab2 = st.tabs(["Scanner un QR Code", "Résultats"])

    with tab1:
        st.subheader("1. Chargez votre QR Code")
        col1, col2 = st.columns(2)
        with col1:
            uploaded_file = st.file_uploader(
                "Téléchargez une image",
                type=["png", "jpg", "jpeg"],
                help="Sélectionnez une image contenant un QR Code"
            )
        with col2:
            webcam_img = st.camera_input(
                "Ou utilisez votre webcam",
                help="Prenez une photo d'un QR Code avec votre caméra"
            )

        # Traitement de l'image
        img = None
        if uploaded_file:
            img = Image.open(uploaded_file)
            st.image(img, caption="Image téléchargée", use_column_width=True)
        elif webcam_img:
            img = webcam_img
            st.image(img, caption="Photo prise", use_column_width=True)

    with tab2:
        if img:
            with st.spinner("Analyse en cours..."):
                qr_info = get_qr_info(img)

                if qr_info:
                    st.session_state.qr_history.extend(qr_info)
                    st.subheader("2. Résultats")

                    # Tableau structuré
                    df = pd.DataFrame(qr_info)
                    columns_order = ['Type', 'Timestamp', 'Data']
                    if analyze_wifi and any('SSID' in entry for entry in qr_info):
                        columns_order.extend(['SSID', 'Password', 'Security', 'Hidden'])
                    df = df.reindex(columns=columns_order).fillna('N/A')

                    st.dataframe(
                        df.style.set_properties(**{
                            'text-align': 'left',
                            'border': '1px solid #ddd',
                            'padding': '5px'
                        }).set_table_styles([
                            {'selector': 'th', 'props': [('background-color', '#e6f3ff'), ('font-weight', 'bold')]}
                        ]),
                        use_container_width=True
                    )

                    # Détails Wi-Fi
                    if analyze_wifi and any('SSID' in entry for entry in qr_info):
                        st.markdown('<div class="wifi-box">', unsafe_allow_html=True)
                        st.subheader("Connexion Wi-Fi")
                        st.write(f"**Nom du réseau (SSID):** {qr_info[0].get('SSID', 'N/A')}")
                        st.write(f"**Mot de passe:** {qr_info[0].get('Password', 'N/A')}")
                        st.write(f"**Sécurité:** {qr_info[0].get('Security', 'N/A')}")
                        st.write(f"**Caché:** {'Oui' if qr_info[0].get('Hidden', 'false') == 'true' else 'Non'}")
                        st.markdown('</div>', unsafe_allow_html=True)

                    st.markdown(get_csv_download_link(df), unsafe_allow_html=True)
                else:
                    st.warning("Aucun QR Code détecté. Essayez une autre image !")

        # Historique
        if show_history and st.session_state.qr_history:
            st.subheader("Historique des scans")
            history_df = pd.DataFrame(st.session_state.qr_history)
            columns_order = ['Type', 'Timestamp', 'Data', 'SSID', 'Password', 'Security', 'Hidden']
            history_df = history_df.reindex(columns=columns_order).fillna('N/A')
            st.dataframe(history_df, use_container_width=True)
            if st.button("Effacer l'historique", help="Supprimer tous les scans précédents"):
                st.session_state.qr_history = []
                st.success("Historique effacé !")


if __name__ == "__main__":
    main()