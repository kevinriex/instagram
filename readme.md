# Instagram Abo Filter (Followings Review)

Dieses kleine Tool hilft dir dabei, deine Instagram-„Followings“ aus dem offiziellen Instagram-Datenexport zu extrahieren und interaktiv zu entscheiden, ob du Accounts behalten möchtest (ja/nein).  
Die Entscheidungen werden **fortlaufend** in `edited_followings.csv` gespeichert, sodass du nach einem Abbruch später **genau dort weitermachen** kannst.

## Voraussetzungen

- Python 3.10+ (geht meistens auch mit 3.8+, aber empfohlen 3.10+)
- Kein zusätzliches Paket nötig (nur Standardbibliothek)

## 1) Instagram-Daten herunterladen

Instagram/Meta hat die Funktion in den **Kontenübersicht / Accounts Center** verschoben.  
Der Menüpfad ist je nach App-Version leicht unterschiedlich, typischerweise:

- Instagram App öffnen → Profil
- Menü (≡) → **Kontenübersicht** (Accounts Center)
- **Deine Informationen und Berechtigungen**
- **Deine Informationen herunterladen** / **Export your information**
- „Herunterladen“ bzw. „Dateien erstellen“ und warten, bis der Download bereit ist

Quellen: Instagram-Hilfe und Schritt-für-Schritt-Anleitungen. :contentReference[oaicite:0]{index=0}

Am Ende erhältst du eine **ZIP-Datei** (z.B. `instagram-data.zip`).

## 2) ZIP entpacken + following.json extrahieren

Im Instagram-Export liegt die Datei normalerweise hier:

`connections/followers_and_following/following.json`

Nutze dafür das Script `prepare.py` (siehe unten).  
Das Script entpackt die ZIP in einen Ordner und kopiert die `following.json` in dein Arbeitsverzeichnis, z.B. als `following.json`.

### Beispiel

```bash
python3 extract_following_json.py instagram-data.zip --outdir export --dest following.json
