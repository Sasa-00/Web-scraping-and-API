
from bs4 import BeautifulSoup
import requests
import psycopg2

# Definisanje URL adrese sajta
URL = 'https://www.nekretnine.rs'

BROJEVI = [2, 3, 4, 5]

# Podaci Postgresa
HOSTNAME = 'localhost'
USERNAME = 'postgres'
PASSWORD = 'password'
PORT_ID = 5432

# Konekcija za pravljenje baze
conn = psycopg2.connect(
    host=HOSTNAME,
    user=USERNAME,
    password=PASSWORD,
    port=PORT_ID
)
conn.autocommit = True
# Instanciranje kursora i brisanje tabele ako postoji
cur = conn.cursor()
cur.execute('''DROP DATABASE IF EXISTS nekretnine''')
cur.execute('''CREATE DATABASE nekretnine''')
print("Database created successfully........")
cur.close()
conn.close()

# Konekcija za povezivanje na malopre napravljenu bazu i pravljenje tabele
conn = psycopg2.connect(
    host=HOSTNAME,
    dbname='nekretnine',
    user=USERNAME,
    password=PASSWORD,
    port=PORT_ID
)
conn.autocommit = True
cur = conn.cursor()

cur.execute('DROP TABLE IF EXISTS oglasi')


# Pravljenje tabele
create_table = """
    CREATE TABLE oglasi (
        id                  SERIAL NOT NULL PRIMARY KEY,
        tip                 VARCHAR(255),
        kategorija          VARCHAR(255),
        tip_ponude          VARCHAR(255),
        lokacija            VARCHAR(255),
        stanje              VARCHAR(255),
        kvadratura          VARCHAR(255),
        terasa              VARCHAR(255),
        godina_izgradnje    VARCHAR(255),
        broj_soba           VARCHAR(255),
        broj_spratova       VARCHAR(255),
        broj_kupatila       VARCHAR(255),
        spratnost           VARCHAR(255),
        uknjizeno           VARCHAR(255),
        parking             VARCHAR(255),
        ostava              VARCHAR(255),
        lift                VARCHAR(255),
        balkon              VARCHAR(255),
        cena_po_kvadratu    VARCHAR(255),
        ukupna_cena         VARCHAR(255)
    )
    """
cur.execute(create_table)
print("Table created successfully........")


# Funkcija za parsiranje oglasa
def parser(_link):

    # Definisanje variabli
    kategorija = ''
    stanje_nekretnine = ''
    transakcija = ''
    kvadratura = ''
    ukupan_broj_soba = ''
    godina_izgradnje = ''
    ukupan_broj_spratova = ''
    uknjizeno = ''
    spratnost = ''
    broj_kupatila = ''
    spoljno_parking_mesto = ''
    terasa = ''
    ostava = ''
    lift = ''
    balkon = ''
    lokacija = ''
    tip = ''
    ukupna_cena = ''
    cena_po_kvadratu = ''

    # Smestanje HTML dokumenta sa linka(argumenta) u promenljivu
    html_text2 = requests.get(_link).text
    # Inicijalizacija objekta klase, ciji su argumenti HTML fajl sa kojim radimo i parser metod koji koristimo
    soup2 = BeautifulSoup(html_text2, 'lxml')

    # Definisemo listu gde se tacno vidi kategorija kuce, stana ili zemljista
    objekat = soup2.find('ol', class_='breadcrumb d-none d-md-flex')
    if objekat is not None:
        for li in objekat.find_all('li'):
            # Prolazimo kroz listu svih kategorija, i s obzirom da nemaju sve a tag i tekst unutra, stavljamo try da bi takav slucaj samo preskocio
            try:
                if 'Kuće' in li.a.text.strip():
                    tip = 'Kuca'
                elif 'Stanovi' in li.a.text.strip():
                    tip = 'Stan'
                elif 'Zemljišta' in li.a.text.strip():
                    tip = 'Zemljiste'
            except:
                pass

        if tip != 'Kuca' and tip != 'Stan':
            return False

    # Uzimamo div objekat iz HTML dokumenta, i smestamo ga u promenljivu
    sekcije = soup2.find_all('div', class_='property__amenities')
    if sekcije is not None:
        # Prolazimo kroz sve skecije
        for sekcija in sekcije:
            # Definisemo sekciju koja nam odgovara
            if 'Podaci o nekretnini' in sekcija.h3.text:
                podaci = sekcija.ul
                # Prolazimo kroz listu u odabranoj sekciji
                for li in podaci.find_all("li"):
                    # Proveravamo nazive lista i smestamo podatke u promenljive
                    if 'Kategorija:' in li.text:
                        kategorija = li.strong.text.strip()
                    if 'Stanje nekretnine:' in li.text:
                        stanje_nekretnine = li.strong.text.strip()
                    if 'Transakcija:' in li.text:
                        transakcija = li.strong.text.strip()
                    if 'Kvadratura:' in li.text:
                        kvadratura = li.strong.text.strip()
                    if 'Ukupan broj soba:' in li.text:
                        ukupan_broj_soba = li.strong.text.strip()
                    if 'Godina izgradnje:' in li.text:
                        godina_izgradnje = li.strong.text.strip()
                    if 'Ukupan broj spratova:' in li.text:
                        ukupan_broj_spratova = li.strong.text.strip()
                    if 'Uknjiženo:' in li.text:
                        uknjizeno = li.strong.text.strip()
                    if 'Spratnost:' in li.text:
                        spratnost = li.strong.text.strip()
                    if 'Broj kupatila:' in li.text:
                        broj_kupatila = li.strong.text.strip()

            # Definisemo sekciju koja nam odgovara
            if 'Dodatna opremljenost' in sekcija.h3.text:
                dodatna_opremljenost = sekcija.ul
                for li in dodatna_opremljenost.find_all("li"):
                    # Proveravamo nazive lista i smestamo podatke u promenljive
                    if 'Spoljno parking mesto' in li.text:
                        spoljno_parking_mesto = 'Da'
                    if 'Terasa' in li.text:
                        terasa = 'Da'
                    if 'Ostava' in li.text:
                        ostava = 'Da'
                    if 'Lift' in li.text:
                        lift = 'Da'
                    if 'Balkon' in li.text:
                        balkon = 'Da'

    # Definisiemo mesto gde se nalazi lokacija na HTML stranici
    lok_div = soup2.find('div', class_='property__location')
    if lok_div is not None:
        lok = lok_div.ul
        # Pravimo listu da bi sav tekst iz lista prvo stavili u istu
        lokacija = []
        for li in lok.find_all('li'):
            # Stavljamo tekstove u listu
            lokacija.append(li.text)
        # Pa se lista spaja u string i stavljaju crtice izmedju radi boljeg izgleda
        lokacija = " - ".join(lokacija)

    # Definisemo mesto gde je cena na stranici, i parsiramo ga
    cena_div = soup2.find(
        'h4', class_='stickyBox__price')
    if cena_div is not None:
        # Proveravanje da li cena postoji
        try:
            cena = cena_div.text.split(' EUR ')
            ukupna_cena = cena[0] + " EUR"
            cena_po_kvadratu = cena[1]
        except:
            ukupna_cena = "Cena na upit"

            # print('')
            # print(kategorija)
            # print(stanje_nekretnine)
            # print(transakcija)
            # print(kvadratura)
            # print(ukupan_broj_soba)
            # print(godina_izgradnje)
            # print(ukupan_broj_spratova)
            # print(uknjizeno)
            # print(spratnost)
            # print(broj_kupatila)
            # print(spoljno_parking_mesto)
            # print(terasa)
            # print(ostava)
            # print(lift)
            # print(balkon)
            # print(lokacija)
            # print(tip)
            # print(ukupna_cena)
            # print(cena_po_kvadratu)
            # print('')
            # print('///////////////////////////////////////////////////////////////////////')
            # print('')

            # Ubacivanje podataka u tabelu
    insert_script = """INSERT INTO oglasi (tip, kategorija, tip_ponude, lokacija, stanje, kvadratura,
    terasa, godina_izgradnje, broj_soba, broj_spratova, broj_kupatila, spratnost, uknjizeno, parking, ostava, lift, balkon,
    cena_po_kvadratu, ukupna_cena) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
    insert_value = (tip, kategorija, transakcija, lokacija, stanje_nekretnine, kvadratura, terasa, godina_izgradnje, ukupan_broj_soba,
                    ukupan_broj_spratova, broj_kupatila, spratnost, uknjizeno, spoljno_parking_mesto, ostava, lift, balkon, cena_po_kvadratu, ukupna_cena)
    cur.execute(insert_script, insert_value)


# Smestanje HTML dokumenta sa linka u promenljivu
html_text = requests.get(URL).text
# Inicijalizacija objekta klase, ciji su argumenti HTML fajl sa kojim radimo i parser metod koji koristimo
soup = BeautifulSoup(html_text, 'lxml')
# Definisanje diva i linka gde se nalazi jos oglasa
vise_oglasa_div = soup.find('div', class_='col-sm-4 text-right title-link')
vise_oglasa = vise_oglasa_div.find(
    'a', class_='text-primary ts-small', href=True)['href']
# Pravljenje nove url adrese sa vise oglasa
newURL = URL+vise_oglasa
# Smestanje iste adrese u promenljivu (HTML forma)
html_text = requests.get(newURL).text
# Inicijalizacija objekta klase, ciji su argumenti HTML fajl sa kojim radimo i parser metod koji koristimo
soup = BeautifulSoup(html_text, 'lxml')
# Definisanje sekcije sa oglasima
oglasi = soup.find_all(
    'div', class_='row offer')
# Prolazak kroz sve oglase i pokretanje funkcije parser za svaki pojedinacno
for oglas in oglasi:
    deo_linka = oglas.find('a', href=True)['href']
    link = URL + deo_linka
    parser(link)

# Iteracija kroz stranice
for broj in BROJEVI:
    # Definisanje stranice gde se nalazi jos oglasa
    vise_oglasa_str = soup.find(
        'a', class_='next-number', text=broj, href=True)['href']
    # Pravljenje nove url adrese sa vise oglasa
    newURL = URL+vise_oglasa_str
    # Smestanje iste adrese u promenljivu (HTML forma)
    html_text = requests.get(newURL).text
    # Inicijalizacija objekta klase, ciji su argumenti HTML fajl sa kojim radimo i parser metod koji koristimo
    soup = BeautifulSoup(html_text, 'lxml')
    # Definisanje sekcije sa oglasima
    oglasi = soup.find_all(
        'div', class_='row offer')
    # Prolazak kroz sve oglase i pokretanje funkcije parser za svaki pojedinacno
    for oglas in oglasi:
        deo_linka = oglas.find('a', href=True)['href']
        link = URL + deo_linka
        parser(link)

# Zatvaranje konekcije sa tabelom
cur.close()
conn.close()

print("Citanje i upis u tabelu uspesno zavrseni!")
