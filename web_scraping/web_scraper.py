import sys
import os
import re
import string
import requests
import nltk
import data_extraction
import json
from nltk import tokenize
from nltk.corpus import stopwords
from bs4 import BeautifulSoup

# Web scraper that finds URL's related to artist Frank Ocean starting from his wikipedia page. 
# Every relevant URL found on the page is then scraped and saved to a text file. These files are
# later cleaned up to find the top 40 most frequent terms found accross all pages scraped. 
# 
# The initial scrape takes a little bit as some of the pages take a little while to be loaded
#
# Needs to be optimized. Each function was created as a separate file during 
# development so I wouldn't have to run the entire program each time I was testing.
# 


# GLOBALS
current_working_dir: str = os.getcwd()

# Creates a dictionary of the most frequently used terms in the clean files
# accross all of the files
def term_extraction():

    #current_working_dir: str = os.getcwd()
    path = os.path.join(current_working_dir, "clean_files\\")
    stop = set(stopwords.words("french"))
    term_dict = {}

    # Iterates through each file and processes them further before
    # creating a dictionary with all of the terms and their frequency

    for file in os.listdir(path):
        file_read = path + "\\" + os.fsdecode(file)
        with open(file_read, "r", encoding='utf-8') as f_in:
            text = f_in.read()
            # I noticed an issue with some of the punctuation not having a space after it,
            # leading to two words getting combined. This line fixes most of those issues
            text = text.replace(".", ". ")
            text = text.replace('“', " ")
            text = text.replace('”', "")
            text = text.replace('-', " ")
            text = text.replace('_', " ")
            text = text.replace(',', " ")
            #text = text.replace('\u00e9n\u00e9', "é")

            text = text.translate(str.maketrans('','',string.punctuation))
            tokens = nltk.word_tokenize(text)
            tokens = [w for w in tokens if not w in stop]
            # Creates a dictionary of the terms found in the text
            for word in tokens:
                if word in term_dict:
                    term_dict[word] += 1
                else:
                    term_dict[word] = 1

    # Sorts the dictionary and outputs the top 40 most frequent words
    sorted_dict = sorted(term_dict.items(), key=lambda kv: kv[1], reverse=True)
    for x in range(40):
        print(str(x+1) + ": " + str(sorted_dict[x]))

# Takes the files from the web scraping and cleans them up and splits them into sentences.
# The sentences from each file are output to a new file
def file_cleanup():

    path = os.path.join(current_working_dir, "raw_files\\")

    # Iterates through each file and cleans them up, saving the sentences
    # in the text to new files in a new directory.
    for file in os.listdir(path):
        file_read = path + "\\" + os.fsdecode(file)
        file_write = os.path.join(current_working_dir, "clean_files")
        filename = file[:-4] + "_clean.txt"
        file_write = os.path.join(file_write, filename)
        os.makedirs(os.path.dirname(file_write), exist_ok=True)
        with open(file_read, 'r', encoding='utf-8') as f_in:
            text = f_in.read()
            text = text.lower()
            text = text.replace('"', '')
            text = text.replace('“', "")
            text = text.replace('”', "")
            text =  re.sub(r'\[.*\]', '', text)
            text = ' '.join(text.split())
            tokens = nltk.sent_tokenize(text)
            with open(file_write, 'w', encoding='utf-8') as f_out:
                 for token in tokens:
                    #token = token.translate(str.maketrans('','',string.punctuation))
                    f_out.write(token + '\n')

# Takes a starter URL, and finds more URLs related to the topic
# These URL's are stored in a list, and the first 15
# have the text from them scraped and output to files
def web(page,WebUrl):

    if(page>0):
        url = WebUrl
        code = requests.get(url)
        plain = code.text
        s = BeautifulSoup(plain, "html.parser")
        links = []
        links.append(WebUrl) #adds starter link to links

        # Words to search for in the URLs that relate to the topic
        topic_words = [
        #"programme-grande-ecole","le-cycle-ingenieur","cursus-programme-ingenieur","cycle-ingenieur-1re-annee"
        "ingenieur-software-engineering",
        "ingenieur-business-intelligence"
        "ingenieur-cloud","ingenieur-securite-systeme-information","cybersecurite-infrastructure-logiciels","ingenieur-big-data","master-data-engineering","ingenieur-network-virtualisation","ingenieur-it-for-finance","ingenieur-bio-informatique","ingenieur-droides-et-drones","majeure-transports-intelligents-efrei-paris","ingenieur-imagerie-et-realite-virtuelle"
        #"les-prepas",
        #"prepa-classique","prepa-renforcee","section-internationale","prepa-integree-bio-et-numerique","rentree-decalee",
        #"international","efrei-paris-integre-le-campus-cyber",
        #"classements", "ecole-ingenieur", "programmes-experts","lefrei-sassocie-a-luniversite-paris-pantheon-assas","clap-de-fin-pour-la-journee-de-la-technologie-au-service-de-lhumain",
        #"cybernight-efrei-2021-2",
        #"nous-rencontrer", 
        #"portes-ouvertes", "preparer-son-concours-puissance-alpha", "participer-au-projette-toi","ateliers-decouverte",
        #"atelier-ux-design","preparer-son-bac-avec-efrei-paris","participer-a-lescape-game","visite-du-campus-efrei-paris","rdv-personnalise",
        
        #"associations",
        #"association-bde","professionnelles","media","internationales","cultures-loisirs","sportives","evenementielles","technologiques","humanitaires",
        
        #"carriere-et-entreprise/devenir-partenaire-efrei-paris","etudier-international/licence-3-international",
        
        ]

        for link in s.findAll('a', attrs={'href': re.compile("^http://")}):
            link_url = link.get('href')
            if any(substring in link_url for substring in topic_words):
                if link_url not in links:
                    links.append(link_url)

        # The links that pointed to another wiki page were not a full URL,
        # so searching for "http://" didn't work to get them.
        for link in s.findAll('a', attrs={'href': re.compile("efrei.fr/")}):
            link_url = link.get('href')

            if any(substring in link_url.lower() for substring in topic_words):
                # It was pulling image URLs, this skips them
                if "File:" in link_url:
                    continue
                #  Makes each wiki link into a proper URL
                if link_url.startswith('efrei.fr/'):
                    link_url = "https://www.efrei.fr/" + link_url
                if "efrei" in link_url and not link_url.startswith('https://www'):
                    continue
                if link_url not in links:
                    links.append(link_url)

        # Outputs text from URL into a file 
        for x in range(len(links)):
            # Tries to get a response from url, if no response is received (dead link etc.)
            # then it is ignored and execution continues
            try:
                link_code = requests.get(links[x])
            except:
                continue
            # Psk il prends aussi l'url efrei.net sans rien derriere ptn g capté du coup on doit dodge le 0
            print("link : " + str(links[x]) + " x : " + str(x))
            if(x>0):
                soup2 = BeautifulSoup(link_code.content, 'html.parser')
                file_write = os.path.join(current_working_dir, "raw_files")
                #filename = "test" + majeure + ".txt"
                filename = str(x) + ".txt"
                file_write = os.path.join(file_write, filename)
                os.makedirs(os.path.dirname(file_write), exist_ok=True)
                intro = soup2.find("div", {"class": "intro"})
                #print("yo " + str(intro))
                majeure = intro.findChildren("h1" , recursive=False)
                # Le 1 de tier-content contient TOUJOURS le responsable de la majeure
                equipe = soup2.find_all("div", {"class": "tier-content" })[1]
                description = soup2.find_all("div", {"class": "description"})
                presentation = soup2.find_all("div", {"class": "column small-12"})[1]
                if(x!=1):
                    debouche = soup2.find_all("div", {"class": "column small-12"})[3]
                else:
                    debouche = soup2.find_all("div", {"class": "column small-12"})[6]
                for text in majeure: # NOM DE LA MAJEURE
                    maj = re.sub(r'[\ \n]{2,}', '', text.getText())
                majTag = re.sub("\n", "", re.sub(" " , "_" , re.sub('é',  'e', maj)))
                nomMaj =  re.sub("\n", "", re.sub("Majeure" , "Majeure " , re.sub('é',  'e', maj)))
                for text in soup2.find_all("div", {"class": "description"}): # DESCRIPTION
                    write_json({"tag" : majTag + "_description", "patterns" : [nomMaj + " description"], "responses": [re.sub("\n", "", re.sub("à", "a", re.sub( "'", "" , re.sub('[éè]', 'e', text.getText()))))]  , "context": ""})
                for text in soup2.find_all("div", {"class": "column small-12"})[1].find("p"): # PRESENTATION
                    if(str(re.sub("à", "a", re.sub( "'", "" , re.sub('[éè]', 'e', text.getText()))))!="\n" and str(re.sub("à", "a", re.sub( "'", "" , re.sub('[éè]', 'e', text.getText()))))!=""):
                        write_json({"tag" : majTag + " presentation", "patterns" : [nomMaj + " presentation"], "responses":  [re.sub("\n", "", re.sub("à", "a", re.sub( "'", "" , re.sub('[éè]', 'e', text.getText()))))] , "context": ""})
                i = 0
                for text in equipe: # EQUIPE
                    if(str(re.sub("à", "a", re.sub( "'", "" , re.sub('[éè]', 'e', text.getText()))))!="\n" and str(re.sub("à", "a", re.sub( "'", "" , re.sub('[éè]', 'e', text.getText()))))!=""):
                        write_json({"tag" : majTag  + "_equipe", "patterns" : [nomMaj + " equipe"], "responses":  [re.sub("\n", "", re.sub("à", "a", re.sub( "'", "" , re.sub('[éè]', 'e', text.getText()))))] , "context": ""})
                if(x!=1): # DEBOUCHES
                    for text in soup2.find_all("div", {"class": "column small-12"})[3]:
                        if(str(re.sub("à", "a", re.sub( "'", "" , re.sub('[éè]', 'e', text.getText()))))!="\n" and str(re.sub("à", "a", re.sub( "'", "" , re.sub('[éè]', 'e', text.getText()))))!=""):
                            write_json({"tag" : majTag + "_debouche", "patterns" : [nomMaj + " debouche"], "responses":  [re.sub("\n", "", re.sub("à", "a", re.sub( "'", "" , re.sub('[éè]', 'e', text.getText()))))] , "context": ""})
                else:
                    for text in soup2.find_all("div", {"class": "column small-12"})[6]:
                        if(str(re.sub("à", "a", re.sub( "'", "" , re.sub('[éè]', 'e', text.getText()))))!="\n" and str(re.sub("à", "a", re.sub( "'", "" , re.sub('[éè]', 'e', text.getText()))))!=""):
                            write_json({"tag" : majTag + "_debouche", "patterns" : [nomMaj + " debouche"], "responses":  [re.sub("\n", "", re.sub("à", "a", re.sub( "'", "" , re.sub('[éè]', 'e', text.getText()))))] , "context": ""})                
                #equipeclean = equipe.find('p')[1].text
                #majeure_cleaned = list(majeure.stripped_strings)
                #maj = "\n\n".join(majeure_cleaned) if majeure_cleaned else ""
                with open(file_write, 'w', encoding='utf-8') as f_out:
                    #for text in soup2.findAll('p'):
                    for text in majeure:
                        f_out.write(text.getText())
                    f_out.write("\nDESCRIPTION : ")
                    for text in soup2.find_all("div", {"class": "description"}):
                        f_out.write(text.getText())
                    f_out.write("\nPRESENTATION : ")
                    #for text in soup2.find_all("div", {"class": "column small-12 txtpres"}):
                    #    f_out.write(text.getText())
                    # ca et le for au dessus c les meme en fait la presentation est tjrs [1]
                    for text in soup2.find_all("div", {"class": "column small-12"})[1]:
                        f_out.write(text.getText())
                    f_out.write("\nEQUIPE : " + equipe.getText())
                    f_out.write("\nDEBOUCHES : " + text.getText())
                    if(x!=1):
                        for text in soup2.find_all("div", {"class": "column small-12"})[3]:
                            f_out.write(text.getText())
                    else:
                        for text in soup2.find_all("div", {"class": "column small-12"})[6]:
                            f_out.write(text.getText())


"""         # Outputs text from URL into a file 
        for x in range(len(links)):
            # Tries to get a response from url, if no response is received (dead link etc.)
            # then it is ignored and execution continues
            try:
                link_code = requests.get(links[x])
            except:
                continue
            # Psk il prends aussi l'url efrei.net sans rien derriere ptn g capté du coup on doit dodge le 0
            print("link : " + str(links[x]) + " x : " + str(x))
            if(x>0):
                soup2 = BeautifulSoup(link_code.content, 'html.parser')
                file_write = os.path.join(current_working_dir, "raw_files")
                filename = str(x) + ".txt"
                file_write = os.path.join(file_write, filename)
                os.makedirs(os.path.dirname(file_write), exist_ok=True)
                intro = soup2.find("div", {"class": "intro"})
                majeure = intro.findChildren("h1" , recursive=False)
                equipe = soup2.find_all("div", {"class": "tier-content" })[1]
                description = soup2.find_all("div", {"class": "description"})
                presentation = soup2.find_all("div", {"class": "column small-12"})[1]
                if(x!=1):
                    debouche = soup2.find_all("div", {"class": "column small-12"})[3]
                else:
                    debouche = soup2.find_all("div", {"class": "column small-12"})[6]
                # ajouter la description de la majeure dans le json
                write_json({"tag" : majeure, "patterns" : majeure + " description", "responses": description, "context": ""})
                # ajouter la présentation de la majeure dans le json
                write_json({"tag" : majeure, "patterns" : majeure + " presentation", "responses": presentation, "context": ""})
                # ajouter l'équipe de la majeure dans le json    
                write_json({"tag" : majeure, "patterns" : majeure + " equipe", "responses": equipe, "context": ""})
                # ajouter les débouchés de la majeure dans le json
                write_json({"tag" : majeure, "patterns" : majeure + " debouche", "responses": debouche, "context": ""}) """

def write_json(new_data, filename='intents.json'):
    with open(filename,'r+', encoding='utf8') as file:
          # First we load existing data into a dict.
        file_data = json.load(file)
        # Join new_data with file_data inside emp_details
        file_data["intents"].append(new_data)
        # Sets file's current position at offset.
        file.seek(0)
        # convert back to json.
        json.dump(file_data, file, indent = 4)

# Just calls all the other functions, I'm sure this can be improved
def main():

    web(1, 'https://www.efrei.fr/')
    file_cleanup()
    term_extraction()
    data_extraction.knowledge_base_creator()
    data_extraction.fact_curator()


if __name__ == "__main__":
    main()
print("The program has executed fully.")