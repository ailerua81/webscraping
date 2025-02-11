import dash
import dash_bootstrap_components as dbc
from dash import dcc, html, dash_table
import pandas as pd
import pymongo
import plotly.express as px
from elasticsearch import Elasticsearch
import os
import subprocess
import logging
import time

# Configuration MongoDB et Elasticsearch
MONGO_URI = os.getenv("MONGO_URI", "mongodb://mongodb_projetDE:27017/projetDE")
# ES_HOST = os.getenv("ELASTICSEARCH_HOST", "http://elasticsearch:9200")


# Vérification de MongoDB
def wait_for_mongo():
    print("Vérification de la connexion à MongoDB...")
    for _ in range(10):  # Essaye pendant 10 secondes
        try:
            client = pymongo.MongoClient(MONGO_URI, serverSelectionTimeoutMS=2000)
            client.admin.command("ping")
            print("MongoDB est accessible !")
            return True
        except Exception as e:
            print(f"MongoDB pas encore prêt : {e}")
            time.sleep(2)
    return False


client = pymongo.MongoClient(MONGO_URI)
db = client.get_database()  # ou db = client['nom_de_votre_db']
collection = db["books"]


# Connexion à Elasticsearch
#es_host = os.getenv("ELASTICSEARCH_HOST", "http://elasticsearch:9200")  # Utilise le hostname Docker
#es = Elasticsearch(es_host)


# def create_index_if_not_exists():
#     if not es.indices.exists(index="books"):
#         print("Index 'books' non trouvé, création en cours...")
#         es.indices.create(index="books", body={
#             "settings": {
#                 "number_of_shards": 1,
#                 "number_of_replicas": 1
#             },
#             "mappings": {
#                 "properties": {
#                     "titre": { "type": "text" },
#                     "auteur": { "type": "text" },
#                     "editeur": { "type": "text" },
#                     "prix": { "type": "float" }
#                 }
#             }
#         })
#         print("Index 'books' créé avec succès !")

# Vérifie et crée l'index avant d'exécuter des recherches
# create_index_if_not_exists()



# Initialisation de l'application Dash avec Bootstrap
dash_app = dash.Dash(__name__, external_stylesheets=[dbc.themes.LUX])

# Récupérer les données de MongoDB
def fetch_data():
    logging.info(" Récupération des données depuis MongoDB...")
    data = list(collection.find({}, {"_id": 0}))
    logging.info(f"Données récupérées : {data}")

    db = pd.DataFrame(data)

    # Vérifier que la colonne "date_edition" existe
    if "date_edition" not in db.columns:
        db["date_edition"] = "Unknown"  # Valeur par défaut si la colonne manque
    else:
        db["date_edition"] = db["date_edition"].astype(str)  # Convertir en texte

    
    # Convertir les listes en chaînes de caractères pour éviter les erreurs dans Dash DataTable
    if "categories" in db.columns:
        db["categories"] = db["categories"].apply(lambda x: ", ".join(x) if isinstance(x, list) else x)

    return db



# Mise en page du Dashboard
dash_app.layout = dbc.Container([

    dbc.Row([
        dbc.Col(html.H1("📚 Dashboard - L'occasion de lire", className="text-center my-3"), width=12)
    ]),

    # html.H4(" 🔍 Recherche : "),
    # dbc.Row([
    #     dbc.Col(dcc.Input(id="search-bar", type="text", className="form-control", placeholder="Rechercher un livre..."), width=8),
    #     dbc.Col(dbc.Button("🔍 Rechercher", id="search-button", color="#52e6f7", className="w-100"), width=4),
    # ], className="mb-4"),

    # dbc.Row([
    #     dcc.Store(id="search-results"),  # Pour stocker les résultats
    #     dbc.Col(html.Div(id="results-display"), width=12)  # Pour afficher les résultats
    # ]),

    html.H4("📋 Liste des livres"),

    # Tableau des livres
    dbc.Row([
        dcc.Interval(id="interval-update", interval=10000, n_intervals=0),  # Mise à jour auto toutes les 10s
        dbc.Col(dash_table.DataTable(
            id="data-table",
            columns=[{"name": i, "id": i} for i in ["titre", "auteur", "editeur", "date_edition", "prix", "categories", "etat"]],
            data=fetch_data().to_dict("records"),
            page_size=10,
            style_table={"overflowX": "auto"},
            style_cell={"textAlign": "left", "padding": "5px"},
        ), width=12)
    ]),


    dbc.Row([
        dbc.Col(html.Img(id="book-image", src="", style={"max-width": "300px", "margin-top": "20px"}), width=6),
        dbc.Col(html.P(id="book-summary", children="Sélectionnez un livre pour voir son résumé.", 
                    style={"margin-top": "20px", "font-style": "italic"}), width=6)
    ], className="text-center"),



    html.H4("📊 Visualisation des données"),

    dbc.Row([
        dbc.Col(dcc.Graph(id="category-pie"), width=6),
        dbc.Col(dcc.Graph(id="price-histogram"), width=6),
    ], className="mt-4"),

    dbc.Row([
        dbc.Col(dcc.Graph(id="edition-bar"), width=6),
        dbc.Col(dcc.Graph(id="top-authors"), width=6),
    ], className="mt-4"),

    dbc.Row([
        dbc.Col(dcc.Graph(id="editor-donut"), width=6),
        dbc.Col(dcc.Graph(id="price-by-category"), width=6),
    ], className="mt-4"),
], fluid=True)



# Callbacks pour mise à jour en temps réel des graphiques
@dash_app.callback(
    [
        dash.Output("data-table", "data"),
        dash.Output("editor-donut", "figure"),
        dash.Output("price-histogram", "figure"),
        dash.Output("edition-bar", "figure"),
        dash.Output("top-authors", "figure"),
        dash.Output("category-pie", "figure"),
        dash.Output("price-by-category", "figure"),
    ],
    [dash.Input("interval-update", "n_intervals")],
)
def update_dashboard(n):
    df = fetch_data()

    # Gérer les éditions manquantes
    if "date_edition" not in df.columns:
        df["date_edition"] = "Unknown"

    # Convertir en numérique (remplace "Unknown" par NaN)
    df["date_edition"] = pd.to_numeric(df["date_edition"], errors="coerce")


    # 📊 Graphique 1 : Répartition des catégories
    category_counts = df.explode("categories")["categories"].value_counts().reset_index()
    category_counts.columns = ["Category", "Nombre"]
    category_pie = px.pie(category_counts, names="Category", values="Nombre", title="Répartition des catégories")

    # 📈 Graphique 2 : Distribution des prix
    df["prix"] = df["prix"].str.replace("€", "").str.replace(",", ".").astype(float)  # Convertir prix en float
    price_hist = px.histogram(df, x="prix", nbins=20, title="Distribution des prix (€)")

    # 📅 Graphique 3 : Nombre de livres par année d'édition
    edition_counts = df["date_edition"].dropna().value_counts().reset_index()
    edition_counts.columns = ["Year", "Nombre"]
    edition_bar = px.bar(edition_counts, x="Year", y="Nombre", title="Livres par année d'édition")

    # 🏆 Graphique 4 : Top 10 auteurs les plus présents
    top_authors = df["auteur"].value_counts().nlargest(10).reset_index()
    top_authors.columns = ["Auteur", "Nombre"]
    author_bar = px.bar(top_authors, x="Auteur", y="Nombre", title="Top 10 Auteurs les Plus Présents")

    # 🌍 Graphique 5 : Répartition des éditeurs (Graphique en anneau)
    editor_counts = df["editeur"].value_counts().reset_index()
    editor_counts.columns = ["Editeur", "Nombre"]
    editor_donut = px.pie(editor_counts, names="Editeur", values="Nombre", title="Répartition des Éditeurs", hole=0.4)


    # 📏 Comparaison des prix moyens par catégorie (Boxplot)
    price_category_box = px.box(df.explode("categories"), x="categories", y="prix", title="Comparaison des Prix par Catégorie")


    return (df.to_dict("records"), category_pie, price_hist, edition_bar, author_bar, editor_donut, price_category_box)



# # Callback pour lancer la recherche dans Elasticsearch
# @dash_app.callback(
#     dash.Output("search-results", "data"),
#     [dash.Input("search-bar", "value"),
#      dash.Input("search-button", "n_clicks")]
# )
# def search_books(query, n_clicks):
#     # On effectue la recherche seulement si la requête est présente et que le bouton a été cliqué
#     if not query or not n_clicks:
#         return []

#     response = es.search(index="books", body={"query": {"match_all": {}}})
#     print(response)    

    
#     try:
#         # Exécuter une recherche (notez que la syntaxe peut varier selon la version de votre client Elasticsearch)
#         response = es.search(
#             index="books",
#             body={
#                 "query": {
#                     "multi_match": {
#                         "query": query,
#                         "fields": ["titre", "auteur", "editeur"]
#                     }
#                 }
#             }
#         )
#     except Exception as e:
#         print("Erreur lors de la recherche :", e)
#         return []
    
#     # Formater les résultats pour l'affichage
#     results = [
#         {
#             "titre": hit["_source"].get("titre"),
#             "auteur": hit["_source"].get("auteur"),
#             "editeur": hit["_source"].get("editeur")
#         }
#         for hit in response.get("hits", {}).get("hits", [])
#     ]
    
#     return results

# # Callback pour afficher les résultats sur le dashboard
# @dash_app.callback(
#     dash.Output("results-display", "children"),
#     [dash.Input("search-results", "data")]
# )
# def display_results(data):
#     if not data:
#         return "Aucun résultat."
    
#     # Exemple simple d'affichage sous forme de liste
#     return html.Ul([
#         html.Li(f"{result['titre']} par {result['auteur']} (Éditeur: {result['editeur']})")
#         for result in data
#     ])




@dash_app.callback(
    [dash.Output("book-image", "src"),
     dash.Output("book-summary", "children")],
    [dash.Input("data-table", "active_cell")],
    [dash.State("data-table", "data"),
     dash.State("data-table", "page_current"),
     dash.State("data-table", "page_size")]
)
def display_book_info(active_cell, data, page_current, page_size):
    if active_cell is None:
        return "", "Sélectionnez un livre pour voir son résumé."

    # Définir des valeurs par défaut pour éviter les erreurs
    page_current = page_current if page_current is not None else 0
    page_size = page_size if page_size is not None else 10

    # Calculer l'index absolu du livre sélectionné
    relative_row = active_cell["row"]
    absolute_row = page_current * page_size + relative_row

    if absolute_row >= len(data):  # Vérifier que l'index est valide
        return "", "Sélectionnez un livre pour voir son résumé."

    # Récupérer la photo et le résumé du livre
    book_photo = data[absolute_row].get("photo", "")
    book_summary = data[absolute_row].get("resume", "Résumé non disponible.")

    return book_photo, book_summary


if __name__ == "__main__":
    dash_app.run_server(debug=True, host="0.0.0.0", port=8050)  
