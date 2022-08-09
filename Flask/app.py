from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

# Instanciranje klase Flask
app = Flask(__name__)
# Povezivanje sa bazom
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:password@localhost/nekretnine'
SQLALCHEMY_TRACK_MODIFICATIONS = False

db = SQLAlchemy(app)

# Citanje postojece baze podataka i smestanje u promenljivu
oglasi = db.Table('oglasi', db.metadata, autoload=True,
                  autoload_with=db.engine)


# pretrazivanje po Id-u
@app.route('/nekretnine_id/<id>')
def pretrazi_po_id(id):
    results = db.session.query(oglasi).all()
    for oglas in results:
        if oglas.id == int(id):
            return {"result": {
                oglas.id: {
                    'id': oglas.id,
                    'tip': oglas.tip,
                    'kategorija': oglas.kategorija,
                    'tip ponude': oglas.tip_ponude,
                    'lokacija': oglas.lokacija,
                    'stanje': oglas.stanje,
                    'kvadratura': oglas.kvadratura,
                    'terasa': oglas.terasa,
                    'godina izgradnje': oglas.godina_izgradnje,
                    'broj soba': oglas.broj_soba,
                    'broj spratova': oglas.broj_spratova,
                    'broj kupatila': oglas.broj_kupatila,
                    'spratnost': oglas.spratnost,
                    'uknjizeno': oglas.uknjizeno,
                    'parking': oglas.parking,
                    'ostava': oglas.ostava,
                    'lift': oglas.lift,
                    'balkon': oglas.balkon,
                    'cena po kvadratu': oglas.cena_po_kvadratu,
                    'ukupna cena': oglas.ukupna_cena
                }}}


# Pretrazivanje po parametrima
@app.route('/nekretnine/')
def pretrazi():

    # Smestanje parametara u promenljive
    try:
        tip = request.args.get('tip').lower()
    except AttributeError:
        tip = None
    minkv = request.args.get('minkv')
    maxkv = request.args.get('maxkv')
    try:
        parking = request.args.get('parking').lower()
    except AttributeError:
        parking = None

    lst = []
    # Selektovanje svih elemenata baze
    results = db.session.query(oglasi).all()
    # Prolazak kroz svaki oglas u bazi
    for oglas in results:

        # Funkcija ispisivanja json-a u listu
        def ispisivanje(lista):
            lista.append({
                'tip': oglas.tip,
                'kategorija': oglas.kategorija,
                'tip ponude': oglas.tip_ponude,
                'lokacija': oglas.lokacija,
                'stanje': oglas.stanje,
                'kvadratura': oglas.kvadratura,
                'terasa': oglas.terasa,
                'godina izgradnje': oglas.godina_izgradnje,
                'broj soba': oglas.broj_soba,
                'broj spratova': oglas.broj_spratova,
                'broj kupatila': oglas.broj_kupatila,
                'spratnost': oglas.spratnost,
                'uknjizeno': oglas.uknjizeno,
                'parking': oglas.parking,
                'ostava': oglas.ostava,
                'lift': oglas.lift,
                'balkon': oglas.balkon,
                'cena po kvadratu': oglas.cena_po_kvadratu,
                'ukupna cena': oglas.ukupna_cena
            })

        # Smestanje vrednosti kolona u variable, koje cesto koristimo
        tipOglas = oglas.tip.lower()
        parkingOglas = oglas.parking.lower()
        kvadratura = int(oglas.kvadratura.split(" ")[0])

        # Odavnde pa na dole su sve kombinacije za pretrazi
        # Prvo proveravanje, ako parametri ne postoje, sve se salje
        if tip == None and minkv == None and maxkv == None and parking == None:
            ispisivanje(lst)

        # Ako svi parametri postoje
        elif tip == tipOglas and minkv != None and maxkv != None and parking == parkingOglas:
            minkvadratura = int(minkv)
            maxkvadratura = int(maxkv)
            if minkvadratura < kvadratura < maxkvadratura:
                ispisivanje(lst)

        # Ako samo nema parking parametra
        elif tip == tipOglas and minkv != None and maxkv != None and parking == None:
            minkvadratura = int(minkv)
            maxkvadratura = int(maxkv)
            if minkvadratura < kvadratura < maxkvadratura:
                ispisivanje(lst)

        # Ako samo nema parametra minimalne kvadrature
        elif tip == tipOglas and minkv == None and maxkv != None and parking == parkingOglas:
            maxkvadratura = int(maxkv)
            if kvadratura < maxkvadratura:
                ispisivanje(lst)

        # Ako samo nema parametra maksimalne kvadrature
        elif tip == tipOglas and minkv != None and maxkv == None and parking == parkingOglas:
            minkvadratura = int(minkv)
            if kvadratura > minkvadratura:
                ispisivanje(lst)

        # Ako samo nema tip nekretnine
        elif tip == None and minkv != None and maxkv != None and parking == parkingOglas:
            minkvadratura = int(minkv)
            maxkvadratura = int(maxkv)
            if minkvadratura < kvadratura < maxkvadratura:
                ispisivanje(lst)

        # Ako samo ima tip nekretnine
        elif tip == tipOglas and minkv == None and maxkv == None and parking == None:
            ispisivanje(lst)

        # Ako samo ima parametar minimalne kvadrature
        elif tip == None and minkv != None and maxkv == None and parking == None:
            minkvadratura = int(minkv)
            if kvadratura > minkvadratura:
                ispisivanje(lst)

        # Ako samo ima parametar maksimalne kvadrature
        elif tip == None and minkv == None and maxkv != None and parking == None:
            maxkvadratura = int(maxkv)
            if kvadratura < maxkvadratura:
                ispisivanje(lst)

        # Ako samo ima parking parametar
        elif tip == None and minkv == None and maxkv == None and parking == parkingOglas:
            ispisivanje(lst)

        # Ako samo imaju parametri kvadrature
        elif tip == None and minkv != None and maxkv != None and parking == None:
            minkvadratura = int(minkv)
            maxkvadratura = int(maxkv)
            if minkvadratura < kvadratura < maxkvadratura:
                ispisivanje(lst)

        # Samo tip i minimalna krvadratura
        elif tip == tipOglas and minkv != None and maxkv == None and parking == None:
            minkvadratura = int(minkv)
            if kvadratura > minkvadratura:
                ispisivanje(lst)

        # Samo tip i maksimalna krvadratura
        elif tip == tipOglas and minkv == None and maxkv != None and parking == None:
            maxkvadratura = int(maxkv)
            if kvadratura < maxkvadratura:
                ispisivanje(lst)

        # Samo tim i parking
        elif tip == tipOglas and minkv == None and maxkv == None and parking == parkingOglas:
            ispisivanje(lst)

         # Ako ima minimalnu kvadraturu i parking
        elif tip == None and minkv != None and maxkv == None and parking == parkingOglas:
            minkvadratura = int(minkv)
            if kvadratura > minkvadratura:
                ispisivanje(lst)

        # Ako ima maksimalnu kvadraturu i parking
        elif tip == None and minkv == None and maxkv != None and parking == parkingOglas:
            maxkvadratura = int(maxkv)
            if kvadratura < maxkvadratura:
                ispisivanje(lst)

        # else:
        #     return {'result': 'Not found'}, 404

    lst2 = []
    [lst2.append(item) for item in lst if item not in lst2]

    return {'result': lst2}


if __name__ == '__main__':
    app.run(debug=True, port=5000)
