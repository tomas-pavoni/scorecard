import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from utils import description, calculate_means, generate_bubble_chart, create_combined_pdf, save_bubble_chart_to_pdf


# Initialisation du session state pour stocker les données des utilisateurs et leurs scores
if 'data_store' not in st.session_state:
    st.session_state['data_store'] = {}
if 'scorecard_data' not in st.session_state:
    st.session_state['scorecard_data'] = {}
if 'current_user' not in st.session_state:
    st.session_state['current_user'] = None

# Liste des noms des utilisateurs prédéfinis
utilisateurs = ["Alexandre", "Aline", "Damien", "David", "Franck", "Giulio", "John", "Olivier", "Oliviero", "Philippe", "Thierry", "Urs", "Tomas"]

# Liste prédéfinie des business pour la scorecard
business_list = ["Calculateur réno", "Comptabilité carbone"]

# Correspondance des valeurs numériques pour les critères
mapping_strategiques = {
    "Aucunement": 0,
    "Faiblement": 1,
    "Moyennement": 2,
    "Fortement": 3,
    "Ne sait pas": 1.5
}

mapping_implementation = {
    "Expertise dans le domaine": {
        "Aucune": 0,
        "Faible": 1,
        "Moyenne": 2,
        "Élevée": 3,
        "Ne sait pas": 1.5
    },
    "Projet pilote": {
        "Non": 0,
        "À définir": 1,
        "En cours": 2,
        "Oui": 3,
        "Ne sait pas": 1.5
    },
    "Compétences internes": {
        "Aucune": 0,
        "Oui légèrement": 1,
        "Oui partiellement": 2,
        "Oui entièrement": 3,
        "Ne sait pas": 1.5
    }
}

# Critères stratégiques
critiques_strategiques = {
    "Excellence opérationnelle": [
        "Contribue à la rénovation énergétique du parc romand",
        "Contribue à l'assainissement énergétique du parc romand"
    ],
    "Développement du digital dans nos métiers": [
        "Contribue à la digitalisation, automatisation ou simplification de nos processus métiers afin d'en améliorer le fonctionnement et l'efficacité"
    ],
    "Décarbonation et nouvelles technologies": [
        "Contribue au développement de solutions innovantes qui nous permettent de nous démarquer de la concurrence",
        "Contribue à l’essor et au développement de nouvelles technologies telles que l'IA, le machine learning ou la digitalisation au sein de l'entreprise",
        "Contribue à la réduction des émissions carbones liées à nos activités"
    ],
    "Rénovation énergétique immobilière": [
        "Contribue à la simplification des échanges d'affaires entre RES et IDGO"
    ],
    "Croissance et optimisation des revenus": [
        "Contribue à la croissance du chiffre d’affaires, de l’EBIT et du chiffre d’affaires récurrent"
    ]
}

# Critères d'implémentation
critiques_implementation = {
    "Expertise dans le domaine": ["Aucune", "Faible", "Moyenne", "Élevée", "Ne sait pas"],
    "Projet pilote": ["Non", "À définir", "En cours", "Oui", "Ne sait pas"],
    "Compétences internes": ["Aucune", "Oui légèrement", "Oui partiellement", "Oui entièrement", "Ne sait pas"]
}


# Fonction pour générer le graphique en bulles
def generate_bubble_chart(data, title="Priorisation des nouveaux business"):
    if data.empty:
        st.warning("Aucune donnée disponible pour afficher le graphique.")
        return None

    fig, ax = plt.subplots(figsize=(12, 6))

    # Définition des couleurs pour chaque business
    colors = plt.cm.get_cmap("tab10", len(data))

    # Création des bulles
    for i, row in data.iterrows():
        x = row["Moyenne Contribution Stratégique"]
        y = row["Moyenne Implémentation"]
        size = row["Score moyen Scorecard"] * 100  # Ajustement de la taille
        label = row["Business"]

        bubble = ax.scatter(x, y, s=size, color=colors(i), alpha=0.6, edgecolors='k')
        ax.annotate(label, (x, y), textcoords="offset points", xytext=(0, 10), ha='center')

    # Configuration du graphique
    ax.set_xlabel("Contribution stratégique (vision)")
    ax.set_ylabel("Facilité d'implémentation (réalisation)")
    ax.set_title(title, fontsize=14, fontweight='bold')

    plt.grid(True, linestyle="--", alpha=0.6)
    return fig


# Fonction pour préparer les données pour le graphique
def prepare_data_for_chart(nom_utilisateur):
    all_data = []

    if nom_utilisateur == "Tomas":
        # Calcul de la moyenne des résultats pour tous les utilisateurs
        aggregated_data = {}
        user_count = 0  # Nombre d'utilisateurs ayant des données valides

        for user, user_data in st.session_state['data_store'].items():
            if user != "Tomas":  # On exclut Tomas lui-même
                user_count += 1
                for business in business_list:
                    if business in user_data:
                        data = user_data[business]

                        # Calcul des moyennes par business
                        mean_strategic = np.mean(
                            [mapping_strategiques.get(val, 0) for val in data.values() if val in mapping_strategiques]
                        )
                        mean_implementation = np.mean([
                            mapping_implementation[key].get(val, 0)
                            for key, val in data.items()
                            if key in mapping_implementation and val in mapping_implementation[key]
                        ])
                        mean_score = st.session_state['scorecard_data'].get(user, {}).get(business, pd.DataFrame()).get(
                            "Score", pd.Series()).mean()

                        # Agrégation des résultats
                        if business not in aggregated_data:
                            aggregated_data[business] = {
                                "Moyenne Contribution Stratégique": mean_strategic,
                                "Moyenne Implémentation": mean_implementation,
                                "Score moyen Scorecard": mean_score
                            }
                        else:
                            aggregated_data[business]["Moyenne Contribution Stratégique"] += mean_strategic
                            aggregated_data[business]["Moyenne Implémentation"] += mean_implementation
                            aggregated_data[business]["Score moyen Scorecard"] += mean_score

        # Moyenne des valeurs pour tous les utilisateurs
        if user_count > 0:
            for business in aggregated_data:
                aggregated_data[business]["Moyenne Contribution Stratégique"] /= user_count
                aggregated_data[business]["Moyenne Implémentation"] /= user_count
                aggregated_data[business]["Score moyen Scorecard"] /= user_count

        # Convertir en DataFrame
        all_data = [{"Business": business, **values} for business, values in aggregated_data.items()]

    else:
        # Si l'utilisateur n'est pas Tomas, calcul normal
        for business in business_list:
            if business in st.session_state['data_store'].get(nom_utilisateur, {}):
                data = st.session_state['data_store'][nom_utilisateur][business]

                mean_strategic = np.mean(
                    [mapping_strategiques.get(val, 0) for val in data.values() if val in mapping_strategiques]
                )
                mean_implementation = np.mean([
                    mapping_implementation[key].get(val, 0)
                    for key, val in data.items()
                    if key in mapping_implementation and val in mapping_implementation[key]
                ])
                mean_score = st.session_state['scorecard_data'].get(nom_utilisateur, {}).get(business,
                                                                                             pd.DataFrame()).get(
                    "Score", pd.Series()).mean()

                all_data.append({
                    "Business": business,
                    "Moyenne Contribution Stratégique": mean_strategic,
                    "Moyenne Implémentation": mean_implementation,
                    "Score moyen Scorecard": mean_score
                })

    return pd.DataFrame(all_data)


# Page de connexion
def login_page():
    image_path = "./RE.png"  # Chemin de votre image
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
            st.experimental_rerun()  # Relance l'application pour refléter l'état connecté
        else:
            st.sidebar.error("Code incorrect. Veuillez réessayer.")

# Log ==================================================================================================================
if st.session_state['current_user'] is None:
    login_page()
else:
    nom_utilisateur = st.session_state['current_user']
    image_path = "./RE.png"  # Chemin de votre image
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
        st.experimental_rerun()  # Relance l'application pour refléter l'état non connecté


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
        st.title("Résultats des Scorecards")
        if nom_utilisateur == "Tomas":
            # Génération et téléchargement du PDF en un seul bouton
            filename = "Résultats_Scorecards.pdf"

            # Générer et sauvegarder le PDF
            create_combined_pdf(st.session_state['scorecard_data'], filename)

            # Lire le fichier en binaire
            with open(filename, "rb") as file:
                pdf_bytes = file.read()

            # Un seul bouton qui génère et télécharge en même temps
            st.download_button(
                label="📥 Télécharger le PDF des résultats",
                data=pdf_bytes,
                file_name=filename,
                mime="application/pdf"
            )

            for user, user_data in st.session_state['scorecard_data'].items():
                if user != "Tomas":  # S'assurer que Tomas ne voit pas ses propres résultats
                    st.subheader(f"Résultats pour l'utilisateur : {user}")
                    for business, data in user_data.items():
                        if not data.empty:
                            st.write(f"Business : {business}")
                            st.table(data)
                        else:
                            st.write(f"Business : {business} - Aucune donnée disponible")
        else:
            # Les autres utilisateurs ne peuvent pas générer de PDF, ils ne voient que leurs résultats.
            st.header(f"Vos résultats de Scorecard")
            user_data = st.session_state['scorecard_data'][nom_utilisateur]
            for business, data in user_data.items():
                if not data.empty:
                    st.write(f"Business : {business}")
                    st.table(data)
                else:
                    st.write(f"Aucune donnée disponible pour {business}.")


    # Graphes ==========================================================================================================
    elif activite == "Graphes":
        st.title("Graphes des business")

        if nom_utilisateur == "Tomas":
            st.write("📊 **Graphique des moyennes des utilisateurs**")

            df_results = prepare_data_for_chart(nom_utilisateur)

            if df_results.empty:
                st.warning("Aucune donnée disponible. Remplissez d'abord les critères et les scorecards.")
            else:
                fig = generate_bubble_chart(df_results, title="Moyenne des business - Tous utilisateurs")
                if fig:
                    st.pyplot(fig)

                    # Génération et téléchargement du PDF en un seul bouton
                    filename = "Moyenne_Businesses.pdf"

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

            df_results = prepare_data_for_chart(nom_utilisateur)

            if df_results.empty:
                st.warning("Aucune donnée disponible. Remplissez d'abord les critères et les scorecards.")
            else:
                fig = generate_bubble_chart(df_results, title=f"Priorisation des business pour {nom_utilisateur}")
                if fig:
                    st.pyplot(fig)


