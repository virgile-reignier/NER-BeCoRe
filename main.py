from bs4 import BeautifulSoup
import lxml


def extract_regeste(fichier_cei):
    """
    :param fichier_cei: path for xml file
    :return: liste of regeste contains in that file
    """
    with open(fichier_cei, 'r', encoding="utf-8") as f:
        xml_doc = f.read()
    soup = BeautifulSoup(xml_doc, 'xml')
    regestes = soup.find_all('cei:abstract')
    regestes_plein = []
    for r in regestes:
        text = r.get_text().replace("Régeste", "").replace("\n", " ")
        while "  " in text:
            text = text.replace("  ", " ")
        if text and text[0] in [" ", "."]:
            text = text[1:]
        if text and "Chirographe" not in text:
            regestes_plein.append(text)
    return regestes_plein

import spacy

def nlp(regestes):

# Blabla bla maintenant j'ai des regestes propres, faudra juste que je les trie en fonction de critères. Mais on passe à l'étape suivante
# TODO : NLP with spacy !

if __name__ == '__main__':
    file = 'cei_complete.xml'
    list_regestes = extract_regeste(file)
    nlp(list_regestes)
