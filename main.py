from flask import Flask, request, render_template

app = Flask(__name__)
#poid est = a l'ipacte final sur  le score de la voiture
#fonction pur calculer le score sur 40 de la voiture
def calculer_score_véhicule(type_véhicule, énergie, année_fabrication, kilométrage):
    # Poids pour le type de véhicule
    poids_type = 0
    if type_véhicule == "Citadine":
        poids_type = 8
    elif type_véhicule == "Cabriolet":
        poids_type = 6
    elif type_véhicule == "Berline":
        poids_type = 6.5
    elif type_véhicule == "SUV / 4x4":
        poids_type = 4

    # Poids pour le type d'énergie
    poids_énergie = 5
    if énergie == "Electrique":
        poids_énergie = 9
    elif énergie == "Gaz":
        poids_énergie = 6
    elif énergie == "Hybride":
        poids_énergie = 7
    elif énergie == "Diesel":
        poids_énergie = 4
    elif énergie == "Essence":          
        poids_énergie = 5

    année_fabrication = int(année_fabrication)

    # Poids pour l'année de fabrication
    poids_année = 1
    if 1960 < année_fabrication < 1970:
        poids_année = 1
    elif année_fabrication >= 1970 and année_fabrication < 1980:
        poids_année = 2
    elif année_fabrication >= 1980 and année_fabrication < 1990:
        poids_année = 2
    elif année_fabrication >= 1990 and année_fabrication < 2000:
        poids_année = 4
    elif année_fabrication >= 2000 and année_fabrication <= 2010:
        poids_année = 5
    elif année_fabrication > 2010:
        poids_année = 7

    kilométrage = int(kilométrage)

    # Poids pour le kilométrage
    
    if kilométrage >= 5000 and kilométrage < 10000:
        poids_kilométrage = 9
    elif kilométrage >= 10000 and kilométrage < 15000:
        poids_kilométrage = 7
    elif kilométrage >= 15000 and kilométrage < 20000:
        poids_kilométrage = 5
    elif kilométrage >= 20000 and kilométrage < 25000:
        poids_kilométrage = 3
    elif kilométrage >= 25000 and kilométrage < 30000:
        poids_kilométrage = 1

    score = (poids_type + poids_énergie + poids_année + poids_kilométrage)  # Somme des poids
    return score

# Fonction pour calculer le taux d'emprunt en fonction du score du véhicule et du nombre de passagers
def calculer_taux_emprunt(score, passagers):
    taux_base = 0  # Taux d'emprunt de base
    
    if 0 <= score <= 10:
        taux = taux_base + 3
    elif 11 <= score <= 15:
        taux = taux_base + 2.74
    elif 16 <= score <= 25:
        taux = taux_base + 2.52
    elif 26 <= score <= 33:
        taux = taux_base + 2.10
    else:
        taux = taux_base + 1.85
    
    if passagers == 1:
        taux = taux + 0.11
    elif passagers == 2:
        taux = taux - 0.17
    elif passagers == 3:
        taux = taux - 0.29
    else:
        taux = taux - 0.53 
    taux = round(taux, 2)
    return taux
#demarage de l'app et mise en relation avec index.html
@app.route("/", methods=["GET", "POST"])
def calcul_emprunt():
    score_véhicule = None
    taux_emprunt = None

    if request.method == "POST":
        type_véhicule = request.form["type_véhicule"]
        énergie = request.form["énergie"]
        année_fabrication = request.form["année_fabrication"]
        kilométrage = request.form["kilométrage"]
        passagers = int(request.form["passagers"])

        score_véhicule = calculer_score_véhicule(type_véhicule, énergie, année_fabrication, kilométrage)
        taux_emprunt = calculer_taux_emprunt(score_véhicule, passagers)

    return render_template("index.html", score_véhicule=score_véhicule, taux_emprunt=taux_emprunt)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)