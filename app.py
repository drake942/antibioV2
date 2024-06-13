import streamlit as st
import pandas as pd

# Charger le nouveau fichier Excel
file_path = "exemple_3_antibio.xlsx"  # Assurez-vous que le fichier est dans le même répertoire que le script
data = pd.read_excel(file_path, engine='openpyxl')

# Vérifier que les colonnes attendues sont présentes
required_columns = [
    'Spécialité chirurgicale', 'Chirurgie Spécifique', 'Antibioprophylaxie',
    'Réinjection', 'Note', 'Allergie', 'Réinjection allergie'
]
for col in required_columns:
    if col not in data.columns:
        st.error(f"La colonne '{col}' est manquante dans le fichier Excel.")
        st.stop()

# Page d'accueil
if "page" not in st.session_state:
    st.session_state.page = "Accueil"
if "allergie_selected" not in st.session_state:
    st.session_state.allergie_selected = False
if "chirurgie_specifique" not in st.session_state:
    st.session_state.chirurgie_specifique = ""

if st.session_state.page == "Accueil":
    st.title("Antibioprophylaxie en chirurgie et médecine interventionnelle")
    st.header("Bienvenue")
    if st.button("Recherche par intitulé opératoire"):
        st.session_state.page = "Recherche par intitulé opératoire"
        st.experimental_rerun()
    if st.button("Recherche par catégorie"):
        st.session_state.page = "Recherche par catégorie"
        st.experimental_rerun()

elif st.session_state.page == "Recherche par intitulé opératoire":
    if st.button("Retour"):
        st.session_state.page = "Accueil"
        st.experimental_rerun()

    if not st.session_state.allergie_selected:
        st.title("Antibioprophylaxie en chirurgie et médecine interventionnelle")
        # Recherche globale pour la chirurgie spécifique
        chirurgie_specifique_search = st.text_input("Recherche", key="global_search")
        chirurgies_specifiques = data['Chirurgie Spécifique'].unique()
        filtered_chirurgies_specifiques = [option for option in chirurgies_specifiques if chirurgie_specifique_search.lower() in option.lower()]

        # Sélection de la chirurgie spécifique avec recherche
        chirurgie_specifique = st.selectbox("Chirurgie Spécifique", filtered_chirurgies_specifiques)

        # Obtenir la spécialité chirurgicale correspondant à la chirurgie spécifique sélectionnée
        if chirurgie_specifique:
            type_chirurgie = data[data['Chirurgie Spécifique'] == chirurgie_specifique]['Spécialité chirurgicale'].values[0]
            st.markdown(f"### Spécialité Chirurgicale: {type_chirurgie}")

            # Indiquer si le patient a une allergie
            st.markdown("Le patient a-t-il une allergie aux antibiotiques ?")
            col1, col2 = st.columns(2)
            with col1:
                if st.button("Non", key="non_allergie", help="Cliquer pour afficher les antibioprophylaxies sans allergie"):
                    st.session_state.allergie_selected = True
                    st.session_state.chirurgie_specifique = chirurgie_specifique
                    st.session_state.allergie = False
                    st.experimental_rerun()

            with col2:
                if st.button("Oui", key="oui_allergie", help="Cliquer pour afficher les antibioprophylaxies avec allergie"):
                    st.session_state.allergie_selected = True
                    st.session_state.chirurgie_specifique = chirurgie_specifique
                    st.session_state.allergie = True
                    st.experimental_rerun()
    else:
        chirurgie_specifique = st.session_state.chirurgie_specifique
        allergie = st.session_state.allergie
        result = data[data['Chirurgie Spécifique'] == chirurgie_specifique]

        st.markdown(f"## {chirurgie_specifique}")

        if not result.empty:
            if not allergie:
                antibioprophylaxie = result.iloc[0]['Antibioprophylaxie']
                reinjection = result.iloc[0]['Réinjection']
                note = result.iloc[0]['Note']
                st.markdown("### Antibioprophylaxie")
                st.write(antibioprophylaxie)
                st.markdown("### Réinjection")
                st.write(reinjection)
                st.markdown("### Note")
                st.write(note)
            else:
                antibioprophylaxie_allergie = result.iloc[0]['Allergie']
                reinjection_allergie = result.iloc[0]['Réinjection allergie']
                st.markdown("### Antibioprophylaxie allergie")
                st.write(antibioprophylaxie_allergie)
                st.markdown("### Réinjection allergie")
                st.write(reinjection_allergie)
        else:
            st.markdown("<span style='color: red; font-size: 20px;'>Aucune antibioprophylaxie recommandée trouvée pour cette combinaison.</span>", unsafe_allow_html=True)

        if st.button("Retour"):
            st.session_state.allergie_selected = False
            st.experimental_rerun()

elif st.session_state.page == "Recherche par catégorie":
    if st.button("Retour"):
        st.session_state.page = "Accueil"
        st.experimental_rerun()

    if not st.session_state.allergie_selected:
        st.title("Antibioprophylaxie en chirurgie et médecine interventionnelle")
        # Sélection du type de chirurgie avec menu déroulant
        type_chirurgie_selection = st.selectbox("Type de Chirurgie", data['Spécialité chirurgicale'].unique())

        # Filtrer les chirurgies spécifiques basées sur le type de chirurgie sélectionné
        chirurgies_specifiques_selection = data[data['Spécialité chirurgicale'] == type_chirurgie_selection]['Chirurgie Spécifique'].unique()

        # Sélection de la chirurgie spécifique avec menu déroulant
        chirurgie_specifique_selection = st.selectbox("Chirurgie Spécifique", chirurgies_specifiques_selection)

        if chirurgie_specifique_selection:
            result = data[(data['Spécialité chirurgicale'] == type_chirurgie_selection) & (data['Chirurgie Spécifique'] == chirurgie_specifique_selection)]

            if not result.empty:
                # Indiquer si le patient a une allergie
                st.markdown("Le patient a-t-il une allergie aux antibiotiques ?")
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("Non", key="non_allergie_cat", help="Cliquer pour afficher les antibioprophylaxies sans allergie"):
                        st.session_state.allergie_selected = True
                        st.session_state.chirurgie_specifique = chirurgie_specifique_selection
                        st.session_state.allergie = False
                        st.experimental_rerun()

                with col2:
                    if st.button("Oui", key="oui_allergie_cat", help="Cliquer pour afficher les antibioprophylaxies avec allergie"):
                        st.session_state.allergie_selected = True
                        st.session_state.chirurgie_specifique = chirurgie_specifique_selection
                        st.session_state.allergie = True
                        st.experimental_rerun()
    else:
        chirurgie_specifique = st.session_state.chirurgie_specifique
        allergie = st.session_state.allergie
        result = data[data['Chirurgie Spécifique'] == chirurgie_specifique]

        st.markdown(f"## {chirurgie_specifique}")

        if not result.empty:
            if not allergie:
                antibioprophylaxie = result.iloc[0]['Antibioprophylaxie']
                reinjection = result.iloc[0]['Réinjection']
                note = result.iloc[0]['Note']
                st.markdown("### Antibioprophylaxie")
                st.write(antibioprophylaxie)
                st.markdown("### Réinjection")
                st.write(reinjection)
                st.markdown("### Note")
                st.write(note)
            else:
                antibioprophylaxie_allergie = result.iloc[0]['Allergie']
                reinjection_allergie = result.iloc[0]['Réinjection allergie']
                st.markdown("### Antibioprophylaxie allergie")
                st.write(antibioprophylaxie_allergie)
                st.markdown("### Réinjection allergie")
                st.write(reinjection_allergie)
        else:
            st.markdown("<span style='color: red; font-size: 20px;'>Aucune antibioprophylaxie recommandée trouvée pour cette combinaison.</span>", unsafe_allow_html=True)

        if st.button("Retour"):
            st.session_state.allergie_selected = False
            st.experimental_rerun()

# Ajouter la mention en bas de l'écran
st.markdown("<div style='position: fixed; bottom: 0; width: 100%; text-align: center; padding: 10px 0; background-color: #f8f9fa; color: #333; font-size: 14px;'>Recommandations d'antibioprophylaxie de la SFAR, au jour du 13/06/2024</div>", unsafe_allow_html=True)
