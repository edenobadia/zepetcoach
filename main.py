import json
import time
import pandas as pd
from datetime import datetime
from openai import OpenAI
import warnings
import re
warnings.filterwarnings("ignore", category=DeprecationWarning)


# Configuration API



# Historique des interactions
log_file = "conversation_log.json"


def analyse_intention(user_input):
    rules = [
        {
            "motifs": [r"\bgratte\b", r"\bdémange\b"],
            "reponse": "Est-ce que votre chien a des rougeurs, des croûtes ou perd ses poils ? 🐶"
        },
        {
            "motifs": [r"\bvomit\b", r"\bvomissement\b"],
            "reponse": "Depuis quand votre animal vomit-il ? A-t-il changé d’alimentation récemment ? 🍽️"
        },
        {
            "motifs": [r"\bMerci\b", r"\bBye\b",r"\bEnrevoir\b"],
            "reponse": "Avec plaisir, si tu as d'autres questions, n'hésite pas! 🐶"
        },
        {
            "motifs": [r"\burgent\b", r"\bsang\b",r"\bmort\b",r"\bconvulsion\b" ],
            "reponse": "Nous te conseillons de consulter au plus rapidement un de nos expert vétérinaire pour avoir un avis plus précis sur la situation!"
        }
        # ➕ Ajoute autant de règles que tu veux
    ]

    for rule in rules:
        for motif in rule["motifs"]:
            if re.search(motif, user_input.lower()):
                return rule["reponse"]
    return None

# Fonction personnalisée
def rechercher_produit_medvet(espece, indication=None):
    df = pd.read_csv("medvet.csv")
    filt = df["espèce_cible"].str.lower() == espece.lower()
    if indication:
        filt &= df["indication"].str.contains(indication, case=False, na=False)
    resultats = df[filt][["nom_commercial", "substance_active", "forme"]].head(3)
    return resultats.to_dict(orient="records")

# Initialisation du thread
thread = client.beta.threads.create()
print("🎉 Bienvenue sur l'assistant PetCoach !\nComment puis-je vous aider ? 🐶😺 (Tapez 'exit' pour quitter)\n")
print("🤖 Tapez 'exit' pour quitter.")

# Boucle principale
while True:
    user_input = input("Vous : ").strip()
    if user_input == "":
        continue  # Ignore les entrées vides
    if user_input.lower() in ["exit", "quit"]:
        print("Fin de la session.")
        break

    custom_response = analyse_intention(user_input)
    if custom_response:
        print("Assistant :", custom_response)
        continue  # ↪️ On saute l'appel OpenAI si c'était une commande simple

    # Envoie du message utilisateur
    client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=user_input
    )

    # Création d'un run pour générer une réponse
    run = client.beta.threads.runs.create(thread_id=thread.id, assistant_id=assistant_id)

    # Attente du traitement ou d'une action à exécuter
    while True:
        run_status = client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)

        if run_status.status == "completed":
            break

        elif run_status.status == "requires_action":
            tool_outputs = []
            for call in run_status.required_action.submit_tool_outputs.tool_calls:
                fn_name = call.function.name
                args = json.loads(call.function.arguments)
                if fn_name == "rechercher_produit_medvet":
                    result = rechercher_produit_medvet(args["espece"], args.get("indication"))
                    tool_outputs.append({
                        "tool_call_id": call.id,
                        "output": json.dumps(result)
                    })
            client.beta.threads.runs.submit_tool_outputs(
                thread_id=thread.id,
                run_id=run.id,
                tool_outputs=tool_outputs
            )

        time.sleep(1)

    # Récupère uniquement le dernier message assistant
    messages = client.beta.threads.messages.list(thread_id=thread.id, order="desc", limit=1)
    assistant_response = messages.data[0].content[0].text.value
    print("Assistant :", assistant_response)

    # Enregistre l'échange dans un journal
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "user_message": user_input,
        "assistant_response": assistant_response
    }

    try:
        with open(log_file, "r", encoding="utf-8") as f:
            history = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        history = []

    history.append(log_entry)

    with open(log_file, "w", encoding="utf-8") as f:
        json.dump(history, f, indent=2, ensure_ascii=False)