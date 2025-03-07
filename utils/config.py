# 📌 config.py – Stocke les configurations et constantes globales

# Liste des noms des utilisateurs prédéfinis
utilisateurs = ["Alexandre", "Aline", "Damien", "David", "Franck", "Giulio",
                "John", "Olivier", "Oliviero", "Philippe", "Thierry", "Urs", "Tomas"]

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
    "Expertise dans le domaine": {"Aucune": 0, "Faible": 1, "Moyenne": 2, "Élevée": 3, "Ne sait pas": 1.5},
    "Projet pilote": {"Non": 0, "À définir": 1, "En cours": 2, "Oui": 3, "Ne sait pas": 1.5},
    "Compétences internes": {"Aucune": 0, "Oui légèrement": 1, "Oui partiellement": 2, "Oui entièrement": 3, "Ne sait pas": 1.5}
}

# Critères stratégiques
critiques_strategiques = {
    "Excellence opérationnelle": ["Contribue à la rénovation énergétique du parc romand", "Contribue à l'assainissement énergétique du parc romand"],
    "Développement du digital dans nos métiers": ["Contribue à la digitalisation et automatisation des processus"],
    "Décarbonation et nouvelles technologies": ["Contribue au développement de solutions innovantes", "Contribue à la réduction des émissions carbones"],
    "Rénovation énergétique immobilière": ["Contribue à la simplification des échanges d'affaires"],
    "Croissance et optimisation des revenus": ["Contribue à la croissance du chiffre d’affaires"]
}

# Critères d'implémentation
critiques_implementation = {
    "Expertise dans le domaine": ["Aucune", "Faible", "Moyenne", "Élevée", "Ne sait pas"],
    "Projet pilote": ["Non", "À définir", "En cours", "Oui", "Ne sait pas"],
    "Compétences internes": ["Aucune", "Oui légèrement", "Oui partiellement", "Oui entièrement", "Ne sait pas"]
}

description = """
### 🚀 Bienvenue sur la plateforme de priorisation des initiatives stratégiques 📊

Cette application vous permet **d’évaluer et comparer différents projets** en fonction de leur **pertinence stratégique**, de leur **faisabilité** et de leur **impact potentiel**.  

Grâce aux **scorecards et aux graphiques interactifs**, vous pouvez analyser les résultats et **faciliter la prise de décision**. 📈  

---

## 🎯 Objectif de l’application  
Cette plateforme vous aide à :  
✔ **Évaluer** la pertinence et la faisabilité des projets.  
✔ **Prioriser** les initiatives selon des critères stratégiques.  
✔ **Visualiser** les résultats sous forme de graphes interactifs.  
✔ **Faciliter** le suivi des projets à fort impact.  

---

## 📝 Fonctionnement des Scorecards  
Chaque projet est évalué selon plusieurs dimensions :  

### **1️⃣ Contribution Stratégique (Vision) 🌍**  
➡️ Évalue **l’alignement du projet avec les objectifs stratégiques**.  
➡️ Notation basée sur **son impact sur la digitalisation, la décarbonation, la croissance, etc.**  

### **2️⃣ Faisabilité & Implémentation 🛠**  
➡️ Analyse de la **facilité de mise en œuvre** du projet.  
➡️ Critères : **expertise requise, état du projet pilote, compétences internes disponibles**.  

### **3️⃣ Scorecard détaillée 🎯**  
➡️ Notation de **0 à 10** sur : potentiel financier, valeur client, faisabilité technique, viabilité économique, etc.  

---

## 📊 Visualisation et Priorisation des Business  
Les résultats sont représentés sous forme de **graphique en bulles** :  

🔵 **Chaque bulle représente un projet**.  
🔵 **La taille** de la bulle correspond au **score moyen** du projet.  
🔵 **L’axe X** = **Alignement stratégique (vision)**.  
🔵 **L’axe Y** = **Facilité d’implémentation (réalisation)**.  

### **📌 Interprétation des résultats :**  
✅ **En haut à droite (💎 Prioritaires)** : Projets à fort impact stratégique et faciles à implémenter.  
🔄 **Au centre (⚖ Zone d’arbitrage)** : Projets nécessitant une discussion approfondie.  
❌ **En bas à gauche (📉 Risqués)** : Projets difficiles à mettre en œuvre avec un faible impact stratégique.  

---

## 📄 Exportation et Partage des Résultats  
Les résultats peuvent être **générés en PDF** pour partage et analyse ultérieure.  

📥 **Options disponibles** :  
- Télécharger **les résultats des scorecards** pour chaque projet.  
- Exporter **le graphe global des projets**.  
- Générer **un PDF unique contenant toutes les analyses**.  

---

## 🚀 Conclusion  
Cette plateforme vous aide à **structurer, analyser et prioriser vos projets d’innovation** pour maximiser leur succès.  

🔍 **À vous de jouer !** 💡  

---

💬 **En cas de question, contactez Tomas Pavoni ou Philippe Chollet.**
"""