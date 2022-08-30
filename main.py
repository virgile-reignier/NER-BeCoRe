from lxml import etree as ET
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
            spamwriter.writerow(list(analyse))


def extract_regeste(fichier_cei):
    """
    :param fichier_cei: path for xml file
    :return: dictionnaries with regestes contains in that file and issuer balised
    """
    NAMESPACES = {
        "cei": "http://www.monasterium.net/NS/cei"
    }
    xml_doc = ET.parse(fichier_cei)
    regestes = xml_doc.xpath("//cei:abstract", namespaces=NAMESPACES)
    regestes_plein, regestes_inutilisables, issuer_balised = {}, {}, {}
    for r in regestes:
        balise_id = r.xpath('./parent::cei:chDesc/preceding-sibling::cei:idno', namespaces=NAMESPACES)
        id = balise_id[0].xpath("./@id")[0]
        issuer = r.xpath('./cei:issuer', namespaces=NAMESPACES)
        if issuer:
            issuer_balised[id] = issuer[0].xpath("normalize-space()")
        else:
            issuer_balised[id] = ""
        text = r.xpath("normalize-space()").replace("Régeste", "")
        if text and text[0] in [" ", "."]:
            text = text[1:]
        if text and "Chirographe" not in text:
            regestes_plein[id] = text
        else:
            regestes_inutilisables[id] = [r.xpath("normalize-space()"), issuer]
    return regestes_plein, regestes_inutilisables, issuer_balised


import spacy


def nlp_regestes(regestes):
    """
    :param regestes: list of regestes
    :return: entities and part of speech
    """
    nlp = spacy.load("de_core_news_lg")
    trial_with_identity, trial_with_part_of_speech, regestes_inutilisables = {}, {}, {}
    for id_regeste in regestes:
        regeste = regeste_original = regestes[id_regeste]
        while "[" in regeste:
            crochet, i = "[", 1
            if regeste[0] != crochet:
                while regeste.split("[", 1)[0][-i] == " ":
                    crochet = " " + crochet
                    i += 1
            regeste = regeste.split(crochet, 1)[0] + regeste.split("]", 1)[1]
        text = nlp(regeste)
        if "VERB" in [tok.pos_ for tok in text] and text.ents: # and (text[0].pos_ == "PROPN" or len(str(text[0])) == 1)
            trial_with_identity[id_regeste] = [regeste_original, text.ents[0].text, text.ents[0].label_]
            i = 0
            while text[i].pos_ != "VERB" or i == 0:
                i += 1
            premier_groupe_mot = regeste_original.split(str(text[i]))[0]
            while premier_groupe_mot[-1] in [" ", ","]:
                premier_groupe_mot = premier_groupe_mot[:-1]
            trial_with_part_of_speech[id_regeste] = [regeste_original, premier_groupe_mot]
        else:
            regestes_inutilisables[id_regeste] = [regeste_original]
    return regestes_inutilisables, trial_with_identity, trial_with_part_of_speech


if __name__ == '__main__':
    file = 'goettweig_corpus_saved.xml'
    result_unused, result_ents, result_pos = 'unused.csv', 'results_with_entities.csv', 'results_with_pos.csv'
    list_regestes, no_regeste, balises = extract_regeste(file)
    unusables_regestes, regestes_ents, regestes_pos = nlp_regestes(list_regestes)
    for result in regestes_pos:
        balise = balises[result]
        if regestes_pos[result][1] == balise:
            yf = "Same"
        else:
            yf = "Not_same"
        regestes_pos[result] += [balise, yf]
    save_list(list(no_regeste.items()) + list(unusables_regestes.items()), result_unused)
    save_list([["id", "regeste", "first_ent", "first_ent_label"]] +
              [[key] + values for key, values in regestes_ents.items()], result_ents)
    save_list([["id", "regeste", "string_before_first_verb", "issuer_jacky", "is_same"]] +
              [[key] + values for key, values in regestes_pos.items()], result_pos)

    # TODO : prendre en compte les fonctionalités de https://spacy.io/usage/linguistic-features#dependency-parse