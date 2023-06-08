Named Entity Recognition for BeCoRe project
===

As part of the [BeCoRe project](https://drd.hypotheses.org/anr-fwf-becore), we tried to create a script that would automatically identify the issuers of acts on the basis of their regeste.

## Setting up

Runs with python 3.10 and packages listed in requirements.txt

## Using language model

This script is based on the spacy package and requires the installation of the language models that will be used: https://spacy.io/usage/models/

Please note: we have only used the 'lg' versions of the language models proposed by spacy, which are very heavy.

## Results

This script was used with two corpora: 1 - the acts of the abbey of Fontenay (encoded by Dominique Stutzmann) with regests in French 2 - the acts of the abbey of Gottweig (whose issuers are encoded by Jacqueline Schindler) with regests in German.

Several trials were carried out and their results are stored in eponymous files. The current .csv files are the results of the last test with the Gottweig acts.

## Multilingual

The script is able to detect the language of the source file, but the current version only runs on French and German files.

## Command line

You can use this script on command line with regests contained in a cei file:

```shell
python main.py "cei-file.xml" 
```

The result is contained in 2 files: 1 - "results.csv" containing the regests with the issuer in a dedicated column and a comparison with the issuer already encoded if applicable 2 - "unused.csv" containing the regests that have been detected as unusable for the script.
