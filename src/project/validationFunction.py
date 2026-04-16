import re
import datetime as datetimeModule


# ===================== VALIDATION BASIQUE =====================

def isCodeValid(code):
    """AAA000"""
    return bool(re.match(r'^[A-Z]{3}\d{3}$', str(code).strip()))


def isNumeroValid(numero):
    """7 caractères alphanumériques"""
    return bool(re.match(r'^[A-Z0-9]{7}$', str(numero).strip()))


def isPrenomValid(prenom):
    """Min 3 lettres"""
    return bool(re.match(r'^[A-Za-z]{3,}$', str(prenom).strip()))


def isNomValid(nom):
    """Min 2 lettres"""
    return bool(re.match(r'^[A-Za-z]{2,}$', str(nom).strip()))


# ===================== DATE =====================

def isDateValid(dateString):
    """Format YYYY-MM-DD"""
    try:
        datetimeModule.datetime.strptime(dateString, '%Y-%m-%d')
        return True
    except:
        return False


# ===================== CLASSE =====================

def isClasseValidFormat(classeString):
    """
    Formats acceptés après nettoyage :
    6A, 5B, 4C, 3D
    """
    if not classeString:
        return False

    classe = str(classeString).upper().replace(" ", "")

    return bool(re.match(r'^[3-6][ABCD]$', classe))


# ===================== NOTES =====================

def isNoteValidFormat(noteString):
    """
    Vérifie structure globale :
    Math[12|11:13]#Francais[4|11:13]
    """
    if not noteString or not isinstance(noteString, str):
        return False

    pattern = r'^([A-Za-z]+\[[^\]]+\])(#[A-Za-z]+\[[^\]]+\])*$'
    return bool(re.match(pattern, noteString.strip()))


def isNoteValuesValid(noteString):
    """
    Vérifie que les valeurs sont entre 0 et 20
    """
    try:
        subjects = noteString.split("#")

        for subject in subjects:
            _, content = subject.split("[")
            content = content.rstrip("]")

            parts = content.split("|")

            # examen
            examen = float(parts[0].replace(",", "."))
            if not (0 <= examen <= 20):
                return False

            # devoirs
            if len(parts) > 1:
                devoirs = parts[1].split(":")
                for note in devoirs:
                    val = float(note.replace(",", "."))
                    if not (0 <= val <= 20):
                        return False

        return True

    except:
        return False


# ===================== VALIDATION GLOBALE =====================

def validateRow(row):
    errors = {}

    if not isCodeValid(row.get("CODE", "")):
        errors["CODE"] = "Format AAA000 attendu"

    if not isNumeroValid(row.get("NUMERO", "")):
        errors["NUMERO"] = "7 caractères alphanumériques attendus"

    if not isPrenomValid(row.get("PRÉNOM", "")):
        errors["PRÉNOM"] = "Minimum 3 lettres"

    if not isNomValid(row.get("NOM", "")):
        errors["NOM"] = "Minimum 2 lettres"

    if not isDateValid(row.get("DATE_DE_NAISSANCE", "")):
        errors["DATE"] = "Format YYYY-MM-DD invalide"

    if not isClasseValidFormat(row.get("CLASSE", "")):
        errors["CLASSE"] = "Format attendu : 6A, 5B, 4C, 3D"

    note = row.get("NOTE", "")

    if not isNoteValidFormat(note):
        errors["NOTE"] = "Format invalide"
    elif not isNoteValuesValid(note):
        errors["NOTE_VALUES"] = "Notes doivent être entre 0 et 20"

    return errors