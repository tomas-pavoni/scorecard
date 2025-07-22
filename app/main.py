import streamlit as st
import pandas as pd
from utils.config import (
    utilisateurs, business_list, mapping_strategiques,
    mapping_implementation, critiques_strategiques, critiques_implementation, description
)
from utils.charts import generate_bubble_chart
from utils.PDF_generator import create_combined_pdf, save_bubble_chart_to_pdf
from utils.data_processing import prepare_data_for_chart


# Initialisation du session state pour stocker les données des utilisateurs et leurs scores
if 'data_store' not in st.session_state:
    st.session_state['data_store'] = {}
if 'scorecard_data' not in st.session_state:
    st.session_state['scorecard_data'] = {}
if 'current_user' not in st.session_state:
    st.session_state['current_user'] = None


# Page de connexion
def login_page():
    image_path = "RE.png"  # Chemin de votre image
    st.markdown(description, unsafe_allow_html=True)
    st.sidebar.image(image_path)
    st.sidebar.title("Connexion")
    user_input = st.sidebar.selectbox("Sélectionnez votre nom:", utilisateurs)
    user_code = st.sidebar.text_input("Entrez votre code:", value="", type="password")

    if st.sidebar.button("Se connecter"):
        if user_input == user_code:  # Le code doit correspondre au nom d'utilisateur
            st.session_state['current_user'] = user_input
            st.session_state['user_code'] = user_code
            # Initialisation des structures pour stocker les données de scorecard par business
            if user_input not in st.session_state['scorecard_data']:
                st.session_state['scorecard_data'][user_input] = {business: pd.DataFrame() for business in business_list}
            if user_input not in st.session_state['data_store']:
                st.session_state['data_store'][user_input] = {business: {} for business in business_list}
            st.rerun()  # Relance l'application pour refléter l'état connecté
        else:
            st.sidebar.error("Code incorrect. Veuillez réessayer.")

# Log ==================================================================================================================
if st.session_state['current_user'] is None:
    login_page()
else:
    nom_utilisateur = st.session_state['current_user']
    image_path = "RE.png"  # Chemin de votre image
    st.sidebar.image(image_path)

    # Affichage conditionnel des options en fonction de l'utilisateur
    if nom_utilisateur == "Tomas":
        activities = ["Résultats", "Graphes"]
    else:
        activities = ["Remplir les scorecards", "Remplir les critères", "Résultats", "Graphes"]

    activite = st.sidebar.selectbox("Que voulez-vous faire ?", activities)

    if st.sidebar.button("Se déconnecter"):
        # Efface les informations de l'utilisateur courant du session_state
        del st.session_state['current_user']
        if 'user_code' in st.session_state:
            del st.session_state['user_code']
        st.rerun()  # Relance l'application pour refléter l'état non connecté


    # ScoreCards =======================================================================================================
    elif activite == "Remplir les scorecards" and nom_utilisateur != "Tomas":
        # Choix du business pour la scorecard
        st.markdown(
            "<h3 style='font-size:22px;'>Sélectionnez le business pour lequel vous remplissez la scorecard:</h3>",
            unsafe_allow_html=True
        )
        selected_business = st.selectbox("", business_list)
        st.write(f"\nBonjour {nom_utilisateur}, vous remplissez la scorecard pour {selected_business}\n")

        # Structuration des sliders avec des sections explicites
        st.header("Strategic Fit Alignment")
        identity_score = st.slider(
            'CORPORATE IDENTITY : L\'idée/le projet est aligné avec l\'identité de l\'entreprise', 0, 10, 0)
        innovation_guidance_score = st.slider(
            'INNOVATION GUIDANCE : L\'idée/le projet est aligné avec les axes d\'innovation de l\'entreprise', 0, 10, 0)
        leadership_support_score = st.slider(
            'LEADERSHIP SUPPORT : L\'idée/le projet a du support d\'au moins un sponsor clé qui l\'aidera à devenir réalité',
            0, 10, 0)

        st.header("Opportunity Value")
        financial_potential_score = st.slider(
            'FINANCIAL POTENTIAL : Le potentiel financier de l\'idée/du projet est compris', 0, 10, 0)

        st.header("Desirability Evidence & Confidence")
        customer_segment_score = st.slider(
            'CUSTOMER SEGMENT : Nos segments clients critiques ont des besoins, douleurs, et bénéfices pertinents pour vendre notre proposition de valeur',
            0, 10, 0)
        value_proposition_score = st.slider(
            'VALUE PROPOSITION : Notre proposition de valeur résonne avec nos segments clients critiques', 0, 10, 0)
        channels_score = st.slider(
            'CHANNELS : Nous avons trouvé les meilleurs canaux pour atteindre et acquérir nos segments clients critiques',
            0, 10, 0)
        customer_relationship_score = st.slider(
            'CUSTOMER RELATIONSHIP : Nous avons développé les bonnes relations pour retenir les clients et gagner répétitivement',
            0, 10, 0)

        st.header("Feasibility Evidence & Confidence")
        key_resources_score = st.slider(
            'KEY RESOURCES : Nous avons les bonnes technologies et ressources pour créer notre proposition de valeur',
            0, 10, 0)
        key_activities_score = st.slider(
            'KEY ACTIVITIES : Nous avons les capacités requises pour gérer les activités les plus critiques pour créer notre proposition de valeur',
            0, 10, 0)
        key_partners_score = st.slider(
            'KEY PARTNERS : Nous avons trouvé les bons partenaires clés qui sont prêts à travailler avec nous pour créer et livrer notre proposition de valeur',
            0, 10, 0)

        st.header("Viability Evidence & Confidence")
        revenues_score = st.slider(
            'REVENUES : Nous savons combien nos clients sont prêts à nous payer et comment ils vont payer', 0, 10, 0)
        costs_score = st.slider('COSTS : Nous connaissons nos coûts pour créer et livrer la proposition de valeur', 0,
                                10, 0)

        st.header("Adaptability Evidence & Confidence")
        industry_forces_score = st.slider(
            'INDUSTRY FORCES : Notre idée/projet est bien positionné pour réussir face aux concurrents établis et aux nouveaux venus',
            0, 10, 0)
        market_forces_score = st.slider(
            'MARKET FORCES : Notre idée/projet prend en compte les changements de marché connus et émergents', 0, 10, 0)
        key_trends_score = st.slider(
            'KEY TRENDS : Notre idée/projet est bien positionné pour bénéficier des tendances technologiques, réglementaires, culturelles et sociétales clés',
            0, 10, 0)
        macroeconomic_forces_score = st.slider(
            'MACROECONOMIC FORCES : Notre idée/projet est adapté aux tendances macroéconomiques et d\'infrastructure connues et émergentes',
            0, 10, 0)

        # Bouton de soumission pour la Scorecard
        st.header("Valider la Scorecard")
        if st.button('Valider Scorecard'):
            scores = {
                'Strategic Fit Alignment': {
                    'Corporate Identity': identity_score,
                    'Innovation Guidance': innovation_guidance_score,
                    'Leadership Support': leadership_support_score
                },
                'Opportunity Value': {
                    'Financial Potential': financial_potential_score
                },
                'Desirability Evidence & Confidence': {
                    'Customer Segment': customer_segment_score,
                    'Value Proposition': value_proposition_score,
                    'Channels': channels_score,
                    'Customer Relationship': customer_relationship_score
                },
                'Feasibility Evidence & Confidence': {
                    'Key Resources': key_resources_score,
                    'Key Activities': key_activities_score,
                    'Key Partners': key_partners_score
                },
                'Viability Evidence & Confidence': {
                    'Revenues': revenues_score,
                    'Costs': costs_score
                },
                'Adaptability Evidence & Confidence': {
                    'Industry Forces': industry_forces_score,
                    'Market Forces': market_forces_score,
                    'Key Trends': key_trends_score,
                    'Macroeconomic Forces': macroeconomic_forces_score
                }
            }

            # Convertir les scores en DataFrame et stocker dans le session state sous le business sélectionné
            data = []
            for section, section_scores in scores.items():
                for category, value in section_scores.items():
                    data.append({'Section': section, 'Category': category, 'Score': value})

            # Convertir en DataFrame
            scores_df = pd.DataFrame(data)

            # Assurez-vous que le dictionnaire pour l'utilisateur contient un dictionnaire pour les businesses
            if nom_utilisateur not in st.session_state['scorecard_data']:
                st.session_state['scorecard_data'][nom_utilisateur] = {}
            if selected_business not in st.session_state['scorecard_data'][nom_utilisateur]:
                st.session_state['scorecard_data'][nom_utilisateur][selected_business] = pd.DataFrame()

            st.session_state['scorecard_data'][nom_utilisateur][selected_business] = scores_df
            st.success(f"Scorecard for {selected_business} submitted successfully!")
            st.write(f"Your Scorecard Results for {selected_business}:")
            st.table(st.session_state['scorecard_data'][nom_utilisateur][selected_business])


    # Criteres =========================================================================================================
    elif activite == "Remplir les critères" and nom_utilisateur != "Tomas":
        user_data = st.session_state['data_store'][nom_utilisateur]
        scorecard_data = st.session_state['scorecard_data'][nom_utilisateur]

        # Sélection du business
        st.markdown(
            "<h3 style='font-size:22px;'>Sélectionnez le business:</h3>",
            unsafe_allow_html=True
        )
        # Sélection du business
        selected_business = st.selectbox("", business_list)

        st.write(f"\nBonjour {nom_utilisateur}, vous remplissez les critères pour {selected_business}\n")

        if selected_business in user_data:
            df = user_data[selected_business]
            scorecard_df = scorecard_data.get(selected_business, pd.DataFrame())

            if not scorecard_df.empty:
                mean_score = scorecard_df['Score'].mean()
            else:
                mean_score = 0

            st.write(f"Business: {selected_business} (Moyenne: {mean_score:.2f})")

            # Critères de contribution stratégique
            st.header("Critères de contribution stratégique")
            niveaux_strategiques = ["Aucunement", "Faiblement", "Moyennement", "Fortement", "Ne sait pas"]

            for categorie, sous_criteres in critiques_strategiques.items():
                st.subheader(categorie)
                for critere in sous_criteres:
                    valeur_actuelle = df.get(critere, "Moyennement")  # Valeur par défaut : Moyen
                    df[critere] = st.selectbox(f"{critere}", options=niveaux_strategiques,
                                               index=niveaux_strategiques.index(valeur_actuelle))

            # Critères d'implémentation
            st.header("Critères d'implémentation")
            for critere, options in critiques_implementation.items():
                valeur_actuelle = df.get(critere, options[0])  # Par défaut, première option
                df[critere] = st.selectbox(f"{critere} ({selected_business})", options=options,
                                           index=options.index(valeur_actuelle))

            if st.button("Soumettre les critères"):
                st.session_state['data_store'][nom_utilisateur][selected_business] = df
                st.success("Critères soumis avec succès!")
                st.table(df)  # Afficher le tableau mis à jour
        else:
            st.error("Aucune donnée de scorecard disponible pour remplir les critères.")


    # Résultats ========================================================================================================
    elif activite == "Résultats":
        st.title("📊 Résultats des Scorecards et des Critères")

        if nom_utilisateur == "Tomas":
            # ✅ **Téléchargement des résultats en PDF**
            filename = "../Résultats_Scorecards.pdf"
            create_combined_pdf(st.session_state['scorecard_data'], filename)

            with open(filename, "rb") as file:
                pdf_bytes = file.read()

            st.download_button(
                label="📥 Télécharger le PDF des résultats",
                data=pdf_bytes,
                file_name=filename,
                mime="application/pdf"
            )

            # ✅ **Lister les utilisateurs ayant rempli des Scorecards**
            utilisateurs_ayant_saisi = [
                user for user in st.session_state['scorecard_data'] if user != "Tomas"
            ]

            if not utilisateurs_ayant_saisi:
                st.warning("⚠️ Aucun utilisateur n'a encore rempli de Scorecard.")
            else:
                # Dictionnaire pour stocker les scores moyens par section et catégorie
                scorecard_means = {}

                # **Collecter les données pour la moyenne globale**
                for user in utilisateurs_ayant_saisi:
                    for business, df in st.session_state['scorecard_data'][user].items():
                        if not df.empty:
                            for _, row in df.iterrows():
                                section = row["Section"]
                                category = row["Category"]
                                score = row["Score"]

                                if (section, category) not in scorecard_means:
                                    scorecard_means[(section, category)] = []

                                scorecard_means[(section, category)].append(score)

                # ✅ **Construire la Scorecard Moyenne**
                avg_scorecard_data = []

                for (section, category), scores in scorecard_means.items():
                    avg_score = sum(scores) / len(scores)
                    avg_scorecard_data.append({
                        "Section": section,
                        "Category": category,
                        "Score": round(avg_score)  # Arrondi à 2 décimales
                    })

                if avg_scorecard_data:
                    df_avg_scorecard = pd.DataFrame(avg_scorecard_data)

                    # **Afficher en haut la Scorecard Moyenne**
                    st.subheader("📊 Scorecard Moyenne des Utilisateurs")
                    st.table(df_avg_scorecard)

                    # **Afficher en haut la liste des utilisateurs pris en compte**
                    st.subheader("👥 Utilisateurs ayant rempli une Scorecard")
                    st.write(", ".join(utilisateurs_ayant_saisi))

                # ✅ **Afficher la Scorecard pour chaque utilisateur**
                st.subheader("📊 Résultats des Scorecards par utilisateur")

                for user in utilisateurs_ayant_saisi:
                    st.markdown(f"### 📋 Scorecard de {user}")

                    for business, df in st.session_state['scorecard_data'][user].items():
                        if not df.empty:
                            st.write(f"🔹 **{business}**")
                            mean_score = df["Score"].mean()
                            st.write(f"📌 **Moyenne des Scores** : {mean_score:.2f}")
                            st.table(df)


        else:
            # Les autres utilisateurs ne peuvent voir que leurs propres résultats
            st.header(f"Vos résultats de Scorecard")
            user_data = st.session_state['scorecard_data'][nom_utilisateur]

            for business, data in user_data.items():
                if not data.empty:
                    st.write(f"Business : {business}")
                    st.table(data)
                else:
                    st.write(f"Aucune donnée disponible pour {business}.")

            # Affichage des critères remplis par l'utilisateur
            if nom_utilisateur in st.session_state['data_store']:
                st.write(f"📊 **Vos critères renseignés**")
                for business, criteria_data in st.session_state['data_store'][nom_utilisateur].items():
                    if criteria_data:
                        st.write(f"📌 **{business}**")
                        df_criteria = pd.DataFrame(criteria_data.items(), columns=["Critère", "Valeur"])
                        st.table(df_criteria)
                    else:
                        st.write(f"Aucun critère renseigné pour {business}.")


    # Graphes ==========================================================================================================
    elif activite == "Graphes":
        st.title("Graphes des business")

        if nom_utilisateur == "Tomas":
            st.write("📊 **Graphique des moyennes des utilisateurs**")

            df_results = prepare_data_for_chart(nom_utilisateur, st.session_state, business_list, mapping_strategiques,
                                                mapping_implementation)

            # Vérification des utilisateurs inclus dans le calcul
            valid_users = []
            missing_info = {}

            for user, user_data in st.session_state['data_store'].items():
                if user == "Tomas":
                    continue  # Tomas est exclu des données

                user_has_data = False  # Flag pour voir si l'utilisateur a des données valides

                for business in business_list:
                    if business in user_data:
                        df_user = pd.DataFrame(user_data[business], index=[0])  # Convertir en DataFrame
                        if df_user.empty or df_user.isna().any().any():
                            missing_info.setdefault(user, []).append(business)
                        else:
                            user_has_data = True

                if user_has_data:
                    valid_users.append(user)

            # Affichage des utilisateurs inclus dans le graphe
            if valid_users:
                st.success("✅ Utilisateurs pris en compte dans le calcul du graphe :")
                st.write(", ".join(valid_users))
            else:
                st.warning("⚠️ Aucun utilisateur n'a encore rempli toutes les données.")

            # Vérification des données avant d'afficher le graphe
            if df_results.empty or df_results.isna().any().any():
                st.warning(
                    "⚠️ Impossible de générer le graphique : certaines données sont manquantes. Complétez les critères et scorecards.")

                # Affichage des utilisateurs avec des données incomplètes
                if missing_info:
                    st.error("🔍 Données manquantes détectées pour :")
                    for user, businesses in missing_info.items():
                        st.write(f"👤 **{user}** : {', '.join(businesses)}")

            else:
                fig = generate_bubble_chart(df_results, title=f"Priorisation des business pour {nom_utilisateur}")
                if fig:
                    st.pyplot(fig)

                    # Génération et téléchargement du PDF en un seul bouton
                    filename = "../Graphe_Businesses.pdf"

                    # Générer et sauvegarder le PDF
                    save_bubble_chart_to_pdf(fig, filename)

                    # Lire le fichier en binaire
                    with open(filename, "rb") as file:
                        pdf_bytes = file.read()

                    # Un seul bouton qui génère et télécharge en même temps
                    st.download_button(
                        label="📥 Télécharger le graphique en PDF",
                        data=pdf_bytes,
                        file_name=filename,
                        mime="application/pdf"
                    )

        else:
            st.write(f"📊 **Graphique des résultats pour {nom_utilisateur}**")

            df_results = prepare_data_for_chart(nom_utilisateur, st.session_state, business_list, mapping_strategiques,
                                                mapping_implementation)

            if df_results.empty:
                st.warning("Aucune donnée disponible. Remplissez d'abord les critères et les scorecards.")
            else:
                fig = generate_bubble_chart(df_results, title=f"Priorisation des business pour {nom_utilisateur}")
                if fig:
                    st.pyplot(fig)
