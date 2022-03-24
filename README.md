# EFREIBOT
This project have been designed and developped by : `Yo`
  
# Summary

1. [Global description](#Global)
2. [Prerequisite](#Prerequisite)
3. [How to launch the app](#How-to-launch-the-app)
4. [How the bot works](#How-the-bot-works)
5. [LICENSE](#LICENSE)

# Global description
This project is a chat bot created for the website of EFREI. The main goal of this chat bot is to help the user to find what we want in an easier way. This project is part of a school project.

For this project, we used Python, HTML, CSS. We also used [Flask](https://flask.palletsprojects.com/en/2.0.x/) for the front-end and [NLTK](https://www.nltk.org/) for parsing.

# Prerequisite

First you will need to install [Python](https://www.python.org/downloads/)

Then you can clone this repo and create a virtual environment by writing these commands using your command prompt or the terminal 

```
$ git clone https://github.com/python-engineer/chatbot-deployment.git
$ cd chatbot-deployment
$ python3 -m venv venv
$ . venv/bin/activate
```

You will also need to install dependecies

```
pip install flask
pip install nltk
```

# How to launch the app

Make sure that you have done every command stated in the Prerequisite. Now you can launch the app by writing this command :
```
python3 app.py
```

# How the bot works

First we web scrap the efrei website to be able to have every paragraphs of the website. Then we can filter the files we got with the web scrapper and we filter it again and again and we create a dictionnary that will have the top 40 words. Then we create another file where it build knowledge about the related topic.

# LICENSE

This project is licensed under the `MIT License` - see the LICENSE.md file for details
