import pathlib
import yaml
import pandas as pd
import csv
import os
import json
import re

import validationFunction as validation


# =========================================================
# CONFIG
# =========================================================

BASE_DIR = pathlib.Path(__file__).resolve().parent.parent.parent
pathConfig = BASE_DIR / "src" / "config" / "config.yaml"

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)


# =========================================================
# CONFIG FILE
# =========================================================

def read_configFile():
    with open(pathConfig, "r", encoding="utf-8") as file:
        return yaml.safe_load(file)


def get_paths():
    config = read_configFile()
    pathFileData = BASE_DIR / config["paths"]["inputBrutFile"]["path"]
    pathFileCSV = BASE_DIR / config["paths"]["outputBrutFile"]["path"]
    return pathFileData, pathFileCSV


# =========================================================
# CONVERSION EXCEL → CSV
# =========================================================

def convert_excel_to_csv(pathFileCSV, pathFileData):
    df = pd.read_excel(pathFileData)
    df.to_csv(pathFileCSV, index=False)


# =========================================================
# LECTURE CSV
# =========================================================

def traitementDataCsv():
    pathFileData, pathFileCSV = get_paths()

    if not os.path.exists(pathFileCSV) and os.path.exists(pathFileData):
        convert_excel_to_csv(pathFileCSV, pathFileData)

    listItemsCsv = []

    with open(pathFileCSV, "r", encoding="utf-8") as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            listItemsCsv.append(row)

    return listItemsCsv


# =========================================================
# NETTOYAGE
# =========================================================

def removeVoidLinesFromCsv(listDictData):
    return [item for item in listDictData if not item["isContentVoidCell"]]


# =========================================================
# FORMATAGE
# =========================================================

def formatateDate(dateString):
    try:
        date = pd.to_datetime(dateString, errors='coerce')
        if pd.isna(date):
            return dateString
        return date.strftime('%Y-%m-%d')
    except:
        return dateString


def formatatNotes(columnValue, sep="#", sepExam="|", sepDevoir=":"):
    result = {}

    if not columnValue or not isinstance(columnValue, str):
        return None

    try:
        subjects = columnValue.split(sep)

        for subject in subjects:
            matiere, content = subject.split("[")
            content = content.rstrip("]")

            parts = content.split(sepExam)

            examen = float(parts[0].replace(",", "."))

            devoirs = []
            if len(parts) > 1:
                devoirs = [
                    float(x.replace(",", "."))
                    for x in parts[1].split(sepDevoir)
                    if x.strip()
                ]

            moyenne = examen
            if devoirs:
                moyenne = (sum(devoirs)/len(devoirs) + 2*examen) / 3

            result[matiere.strip().upper()] = {
                "examen": examen,
                "devoirs": devoirs,
                "moyenne": round(moyenne, 2)
            }

        return result

    except:
        return None


# =========================================================
# NORMALISATION
# =========================================================

def normalizeClasse(classe):
    if not classe:
        return classe

    c = str(classe).upper().replace(" ", "")
    match = re.match(r'([3-6]).*?([ABCD])$', c)
    return match.group(1) + match.group(2) if match else c


def normalizeText(text):
    return str(text).strip().title() if text else text


def normalizeNumero(numero):
    return str(numero).strip().upper() if numero else numero


# =========================================================
# AFFICHAGE UNIQUE
# =========================================================

def displayData(data, title="DATA", pageSize=5):
    print(f"\n===== {title} =====")

    if not data:
        print("Aucune donnée")
        return

    for i in range(0, len(data), pageSize):
        print(f"\n--- PAGE {i//pageSize + 1} ---\n")
        for item in data[i:i+pageSize]:
            print(json.dumps(item, indent=4, ensure_ascii=False))
        input("Entrée pour continuer...")


# =========================================================
# RECHERCHE UNIQUE
# =========================================================

def searchByNumero(numero, validData, invalidData, correctedData):
    numero = normalizeNumero(numero)
    found = False

    def search(data, label):
        nonlocal found
        for item in data:
            ref = item.get("NUMERO") or item.get("data", {}).get("NUMERO")
            if ref == numero:
                print(f"\n✔ Trouvé dans {label}")
                print(json.dumps(item, indent=4, ensure_ascii=False))
                found = True

    search(validData, "VALIDES")
    search(invalidData, "INVALIDES")
    search(correctedData, "CORRIGÉES")

    if not found:
        print("❌ Aucun résultat")


# =========================================================
# CORRECTION CELLULE
# =========================================================

def correctCell(data, config):
    corrected = data.copy()

    corrected["CLASSE"] = normalizeClasse(corrected.get("CLASSE"))
    corrected["NOM"] = normalizeText(corrected.get("NOM"))
    corrected["PRENOM"] = normalizeText(corrected.get("PRENOM"))
    corrected["NUMERO"] = normalizeNumero(corrected.get("NUMERO"))

    try:
        from validationFunction import formatatNotes

        corrected["NOTE_DETAILS"] = formatatNotes(
            corrected["NOTE"],
            config["separators"]["subject_sep"],
            config["separators"]["value_sep"],
            config["separators"]["exam_sep"]
        )

    except:
        corrected["NOTE_DETAILS"] = None

    return corrected


# =========================================================
# VALIDATION PIPELINE
# =========================================================

def processData(validData, invalidData, config):
    correctedData = []
    newInvalid = []

    for item in invalidData:

        corrected = correctCell(item["data"], config)

        try:
            from validationFunction import validateRow

            if validateRow(corrected):
                validData.append(corrected)
                correctedData.append(corrected)
            else:
                newInvalid.append({"data": corrected, "errors": item.get("errors")})

        except:
            newInvalid.append(item)

    return validData, newInvalid, correctedData


# =========================================================
# MENU
# =========================================================

def menu(validData, invalidData, config):

    correctedData = []

    while True:

        print("\n===== MENU =====")
        print("1. Valides")
        print("2. Invalides")
        print("3. Corrigés")
        print("4. Recherche")
        print("5. Correction")
        print("6. Quitter")

        choice = input("Choix : ")

        if choice == "1":
            displayData(validData, "VALIDES")

        elif choice == "2":
            displayData(invalidData, "INVALIDES")

        elif choice == "3":
            displayData(correctedData, "CORRIGÉS")

        elif choice == "4":
            numero = input("Numéro : ")
            searchByNumero(numero, validData, invalidData, correctedData)

        elif choice == "5":
            validData, invalidData, correctedData = processData(
                validData, invalidData, config
            )

        elif choice == "6":
            break

        else:
            print("❌ Choix invalide")


# =========================================================
# MAIN
# =========================================================

if __name__ == "__main__":

    data = traitementDataCsv()
    config = read_configFile()["grades"]

    header = data[0]
    rows = data[1:]

    listDictCsv = [
        {
            "INDEX": i,
            "isContentVoidCell": any(cell.strip() == "" for cell in rows[i]),
            **{
                header[j].upper().replace(" ", "_"): rows[i][j]
                for j in range(len(header))
            }
        }
        for i in range(len(rows))
    ]

    listDictCsv = removeVoidLinesFromCsv(listDictCsv)

    validData = []
    invalidData = []
    correctedData = []

    # for row in listDictCsv:
    #     errors = validation.validateRow(row)

    #     if not errors:
    #         row["NOTE_DETAILS"] = formatatNotes(row["NOTE"])
    #         validData.append(row)
    #     else:
    #         invalidData.append({"data": row, "errors": errors})

    for row in listDictCsv:

        errors = validation.validateRow(row)

        # =========================
        # ✔ CAS 1 : VALIDE DIRECT
        # =========================
        if not errors:
            row["NOTE_DETAILS"] = formatatNotes(row["NOTE"])
            validData.append(row)
            correctedData.append(row)  # 🔥 on garde aussi dans corrigé

        # =========================
        # ❌ CAS 2 : INVALID → tentative correction
        # =========================
        else:
            corrected = correctCell(row, config)

            # 🔁 revalidation après correction
            try:
                if not validation.validateRow(corrected):
                    invalidData.append({"data": row, "errors": errors})
                else:
                    corrected["NOTE_DETAILS"] = formatatNotes(corrected["NOTE"])
                    validData.append(corrected)
                    correctedData.append(corrected)

            except:
                invalidData.append({"data": row, "errors": errors})


    print(f"VALIDES: {len(validData)}")
    print(f"INVALIDES: {len(invalidData)}")

    displayData(validData, "VALIDES")