# EFREIBOT
Ce projet a été developpé par : `Ilian Bekka`, `AlexandreGomez`,`Eduin Osorio`, `Emeric Bertin`, `Hassan Bachacha`, `Anthony Vong` et `Armand Goubeau`. 
Ce chat bot a été concu dans le but d'un projet scolaire.
  
# Sommaire

1. [Description du projet](#Description-du-projet)
2. [Prérequis](#Prérequis)
3. [Comment lancer l'application](#Comment-lancer-lapp)
4. [Comment le chat bot fonctionne](#Comment-ca-fonctionne)
5. [LICENSE](#LICENSE)

# Description du projet

Ce projet est un chat bot créé pour le site internet de l'EFREI. Le but principal de ce chat bot est d'aider l'utilisateur à trouver ce qu'il recherche d'une façon simple et rapide.

Pour ce projet, nous avons utilisés différentes technologies: Python pour le back-end, du HTML et du CSS pour le frond-end. Nous avons utilisés [Flask](https://flask.palletsprojects.com/en/2.0.x/) afin de réaliser plus facilement le lien entre le Python et le frond-end. Pour parser, nous avons fait l'usage de [NLTK](https://www.nltk.org/)

# Prérequis

Avant toute chose, il faut installer [Python](https://www.python.org/downloads/) sur votre ordinateur.

Ensuite vous pourrez clone ce repo et écrire ces commandes dans votre invité de commande ou votre terminal.

```
$ python -m venv venv
$ venv\Scripts\activate
```

Vous aurez aussi besoin d'installer ces dépendances.

```
pip install -r requirements.txt
pip install textblob
```

# Comment lancer l'application

Faites bien attention d'avoir suivi les étapes et les commandes cités dans le prérequis. Maintenant, vous pouvez lancer l'application grace à cette commande :
```
python app.py
```

Sur votre navigateur web, entrez cet URL : `http://127.0.0.1:5000/`. Vous devriez voir le chat bot en bas à droite de la page.

# Comment le chat bot fonctionne

First we web scrap the efrei website to be able to have every paragraphs of the website. Then we can filter the files we got with the web scrapper and we filter it again and again and we create a dictionnary that will have the top 40 words. Then we create another file where it build knowledge about the related topic.

On utilise un web scrapper afin d'avoir accès a tout les paragraphes du site internet de l'EFREI. Ensuite, nous pouvons filtrer ce que l'on a eu grâce au web scrapper et nous le refiltrons encore. 

# LICENSE

This project is licensed under the `MIT License` - see the LICENSE.md file for details
Ce projet est sous license `MIT License` - voir le fichier LICENSE.md pour plus de détails
