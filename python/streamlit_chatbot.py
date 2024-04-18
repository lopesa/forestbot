import streamlit as st

def get_response(user_input):
    # Ceci est une fonction de réponse très basique. Vous pouvez intégrer un modèle de NLP ici.
    responses = {
        "bonjour": "Bonjour! Comment puis-je vous aider aujourd'hui?",
        "comment vas-tu": "Je vais bien, merci! Et vous?",
        "au revoir": "Au revoir! Bonne journée!"
    }
    # Retourne une réponse basée sur l'entrée de l'utilisateur, ou une réponse par défaut.
    return responses.get(user_input.lower(), "Désolé, je n'ai pas compris votre question.")

# Création de l'interface utilisateur avec Streamlit
st.title("Chatbot Simple")

# Champ de texte pour l'entrée de l'utilisateur
user_input = st.text_input("Dites quelque chose au chatbot:")

if user_input:
    # Obtention de la réponse du chatbot
    response = get_response(user_input)
    # Affichage de la réponse du chatbot
    st.text_area("Réponse du chatbot:", value=response, height=200, max_chars=None, key=None)
