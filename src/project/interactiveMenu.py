

"""
    Fonction de presentation à l'ecrande sortie de l'utilisateur 
"""
def line_graphic(char='-',length=80):
    """Affiche une ligne de séparation pour le menu ou l'affichage."""
    if not isinstance(char, str) or len(char) == 0:
        char = '-'
    try:
        length = int(length)
    except (TypeError, ValueError):
        length = 80
    print((char * length)[:length])


def _split_line(line, max_len):
    """Coupe une ligne en segments de taille max_len."""
    words = str(line).split()
    if not words:
        return ['']
    chunks = []
    current = words[0]
    for w in words[1:]:
        if len(current) + 1 + len(w) <= max_len:
            current += ' ' + w
        else:
            chunks.append(current)
            current = w
    chunks.append(current)
    return chunks


def presentation(title='', subtitle='', lines=None, width=80):
    """Affiche un en-tête de menu réutilisable et responsive."""
    width = max(40, int(width))
    border = '+' + '-' * (width - 2) + '+'

    def centered(text):
        text = str(text) if text is not None else ''
        if len(text) >= width - 4:
            return '| ' + text[:width - 4] + ' |'
        padding = width - 4 - len(text)
        left = padding // 2
        right = padding - left
        return '| ' + ' ' * left + text + ' ' * right + ' |'

    print(border)
    if title:
        print(centered(title))
    if subtitle:
        print(centered(subtitle))
    if title or subtitle:
        print('|' + ' ' * (width - 2) + '|')
    if lines:
        for line in lines:
            for chunk in _split_line(line, width - 4):
                print(centered(chunk))
    print(border)


def show_menu(options, title='Menu', prompt='Votre choix', width=80, allow_quit=True):
    """Affiche un menu interactif et demande la sélection utilisateur."""
    if not options:
        raise ValueError('La liste des options ne peut pas être vide')

    width = max(40, int(width))
    presentation(title=title, lines=options, width=width)
    for idx, option in enumerate(options, start=1):
        print(f'{idx}. {option}')
    if allow_quit:
        print('Q. Quitter')

    while True:
        choix = input(f'{prompt} : ').strip()
        if allow_quit and choix.lower() in ('q', 'quit', 'exit'):
            return None
        if choix.isdigit():
            idx = int(choix)
            if 1 <= idx <= len(options):
                return idx
        print('Choix invalide. Réessayez.')


def input_int(prompt='Entrez un nombre entier', default=None, min=None, max=None):
    """Demande et valide un entier."""
    while True:
        raw = input(f'{prompt}{f' [{default}]' if default is not None else ''} : ').strip()
        if raw == '' and default is not None:
            return default
        try:
            val = int(raw)
            if min is not None and val < min:
                print(f'Doit être >= {min}')
                continue
            if max is not None and val > max:
                print(f'Doit être <= {max}')
                continue
            return val
        except ValueError:
            print('Entrez un entier valide.')


def input_float(prompt='Entrez un nombre', default=None, min=None, max=None):
    """Demande et valide un flottant."""
    while True:
        raw = input(f'{prompt}{f' [{default}]' if default is not None else ''} : ').strip()
        if raw == '' and default is not None:
            return default
        try:
            val = float(raw)
            if min is not None and val < min:
                print(f'Doit être >= {min}')
                continue
            if max is not None and val > max:
                print(f'Doit être <= {max}')
                continue
            return val
        except ValueError:
            print('Entrez un nombre valide.')


def input_text(prompt='Entrez du texte', default=None, allow_empty=False):
    """Demande et valide une entrée texte."""
    while True:
        raw = input(f'{prompt}{f' [{default}]' if default is not None else ''} : ').strip()
        if raw == '':
            if default is not None:
                return default
            if allow_empty:
                return ''
            print('La valeur ne peut pas être vide.')
        else:
            return raw
        
"""
    Fonction de presentation de Menu ou pour indiquer un message
"""






def demo():
    """Démonstration rapide du menu interactif."""
    presentation(
        title='Mon programme interactif',
        subtitle='Choisissez une option',
        lines=['Menu principal de gestion', 'Saisie sécurisée et claire'],
        width=80,
    )

    option = show_menu(['Ajouter', 'Modifier', 'Supprimer', 'Afficher'], title='Menu principal', prompt='Sélectionnez (1-4)')
    if option is None:
        print('Fin du programme.')
        return

    print(f'Vous avez sélectionné l’option {option}')
    qte = input_int('Saisissez une quantité', default=1, min=1)
    nom = input_text('Saisissez un nom', default='Sans nom')

    print(f'Option choisie : {option}, Nom : {nom}, Quantité : {qte}')
    line_graphic('=', 80)


if __name__ == "__main__":
    demo()