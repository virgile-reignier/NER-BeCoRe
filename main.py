from bs4 import BeautifulSoup
import lxml
import csv


def save_list(regestes, csv_file):
    """
    :param regestes: List or regestes
    :param csv_file: file to save that list
    :return: file csv with regeste by row
    """
    with open(csv_file, 'w', encoding="utf-8", newline='') as f:
        spamwriter = csv.writer(f, delimiter='\t')
        for analyse in regestes:
            spamwriter.writerow(analyse)


def extract_regeste(fichier_cei):
    """
    :param fichier_cei: path for xml file
    :return: liste of regeste contains in that file
    """
    with open(fichier_cei, 'r', encoding="utf-8") as f:
        xml_doc = f.read()
    soup = BeautifulSoup(xml_doc, 'xml')
    regestes = soup.find_all('cei:abstract')
    regestes_plein, regestes_inutilisables = [], []
    for r in regestes:
        text = r.get_text().replace("Régeste", "").replace("\n", " ")
        while "  " in text:
            text = text.replace("  ", " ")
        if text and text[0] in [" ", "."]:
            text = text[1:]
        if text and "Chirographe" not in text:
            regestes_plein.append(text)
        else:
            regestes_inutilisables.append([r.get_text()])
    return regestes_plein, regestes_inutilisables


import spacy


def nlp(regestes):
    nlp = spacy.load("fr_core_news_lg")
    trial_with_identity, trial_with_part_of_speech, regestes_inutilisables = [], [], []
    for regeste_original in regestes:
        regeste = regeste_original
        while "[" in regeste:
            crochet, i = "[", 1
            while regeste.split("[", 1)[0][-i] == " ":
                crochet = " " + crochet
                i += 1
            regeste = regeste.split(crochet, 1)[0] + regeste.split("]", 1)[1]
        text = nlp(regeste)
        if "VERB" in [tok.pos_ for tok in text] and text.ents and (text[0].pos_ == "PROPN" or len(str(text[0])) == 1):
            trial_with_identity.append([regeste_original, text.ents[0].text, text.ents[0].label_])
            i = 0
            while text[i].pos_ != "VERB":
                i += 1
            premier_groupe_mot = regeste_original.split(str(text[i]))[0]
            while premier_groupe_mot[-1] in [" ", ","]:
                premier_groupe_mot = premier_groupe_mot[:-1]
            trial_with_part_of_speech.append([regeste_original, premier_groupe_mot])
        else:
            regestes_inutilisables.append([regeste_original])
    return regestes_inutilisables, trial_with_identity, trial_with_part_of_speech

# TODO : Améliorer encore le modèle en virant tout ce qui ne commence pas par un nom !


if __name__ == '__main__':
    file = 'cei_complete.xml'
    result_unused, result_ents, result_pos = 'unused.csv', 'results_with_entities.csv', 'results_with_pos.csv'
    list_regestes, no_regeste = extract_regeste(file)
    unusables_regestes, regestes_ents, regestes_pos = nlp(list_regestes)
    save_list(no_regeste + unusables_regestes, result_unused)
    save_list([["regeste", "first_ent", "first_ent_label"]] + regestes_ents, result_ents)
    save_list([["regeste", "string_before_first_verb"]] + regestes_pos, result_pos)
