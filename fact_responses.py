import os
import random

def create_facts_dict():
    
    current_dir: str = os.getcwd()
    parent_directory = os.path.split(current_dir)[0]
    dir_path = 'python_chatbot/files'
    filename = 'facts.txt'
    file_path = os.path.join(parent_directory, dir_path)
    file_path = os.path.join(file_path, filename)

    f = open(file_path, 'r', encoding='utf-8')

    text = f.read()
    text = text[:-2]
    text = text.lower()
    text = text.split('*')
    facts = {}
    
    for x in text:
        x = x.split('\n')
        if '' in x:
            x.remove('')
        if x[0] not in facts:
            facts[x[0]] = x[1:len(x)-1]
    return facts

facts = create_facts_dict()

# If one of the topic words was in the question posed by the user, 
# it pulls facts about that topic and creates a dictionary
def specific_facts(topic, sentence, noun, adjective, verb):
    topic = topic.lower()
    # Weird case where I have to add a space after 'blonde'. Without it, my fact picker would include
    # facts about blonded radio, which is not the same topic
    if topic == "blonde":
        topic = "blonde "
   
    topic_facts = facts[topic]
    
    # Essentially goes through the whole dictionary of facts to find a potential match using 
    # the POS found within the sentence given by the user 
    for x in range(len(topic_facts)):
        #It tries to match all three if it can, if not then it tries matching two before going to just one
        if noun is not None and verb is not None and adjective is not None:
            if (noun in topic_facts[x]) and (verb in topic_facts[x]) and (adjective in topic_facts[x]):
                resp = topic_facts[x]
                return resp
        elif noun is not None and verb is not None:
            if (noun in topic_facts[x]) and (verb in topic_facts[x]):
                resp = topic_facts[x]
                return resp
        elif noun is not None and adjective is not None:
            if (noun in topic_facts[x]) and (adjective in topic_facts[x]):
                resp = topic_facts[x]
                return resp
        elif verb is not None and adjective is not None:
            if (verb in topic_facts[x]) and (adjective in topic_facts[x]):
                resp = topic_facts[x]
                return resp
        elif noun is not None:
            if noun in topic_facts[x]:
                resp = topic_facts[x]
                return resp
        elif verb is not None:
            if verb in topic_facts[x]:
                resp = topic_facts[x]
                return resp
        elif adjective is not None:
            if adjective in topic_facts[x]:
                resp = topic_facts[x]
                return resp

    #If the user just wants a random fact, it is selected here
    if "random" in sentence.lower():
        num_facts = len(topic_facts)
        resp = "Here's a random fact about " + topic + ": " + topic_facts[random.randrange(num_facts-1)] 
    else:
        resp = "I couldn't find that, sorry"

    return resp