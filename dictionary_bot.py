# Work with Python 3.6
import discord
from nltk.corpus import wordnet
from PyDictionary import PyDictionary

f = open("data/token.txt")
token = f.readline()
f.close()

client = discord.Client()
 

@client.event
async def on_message(message):
    # we do not want the bot to reply to itself
    if message.author == client.user:
        return

    msg = message.content
    response = ""
        
    commands = msg.split(" ")

    try:
        word = commands[1]
        print(word)
    except:
        response = "Enter a word ya dingus"
        await client.send_message(message.channel, response)

    dictionary = PyDictionary()

#############################################################################################

    #TODO: Migrate '!define' from PyDictionary to wordnet
    if message.content.startswith('!define'):
        #get definition
        definition = dictionary.meaning(word) #returns a dictionary in the form {'Part of Speech': ['definition(s)']}

        #getting the parts of speech in a list
        
        parts_of_speech = []

        try:
            parts_of_speech = list(definition.keys())
            defNum = 0

            for i in parts_of_speech:
                #state the part of speech
                response += i + ": \n"
                #Loop through each definition per part of speech
                for defin in definition[i]:
                    #make it so we don't output a bunch of definitions/spam chat
                    defNum += 1
                    if(defNum <= 3):
                        #Tack on another definition plus a \n
                        response += defin + "\n"
                    else:
                        break
                #Space the parts of speech accordingly
                response += "\n"
                defNum = 0
                #definition[i] is an array of definitions, so what we want to do is loop through each definition[i] and print out those definitions
        except:
            response = "Sorry! For some reason we can't find this definition."

        await client.send_message(message.channel, response)

#############################################################################################

    if message.content.startswith("!syn"):
        response += "Synonyms of " + word + ":\n"
        syn = []
        synNum = 0
        for ss in wordnet.synsets(word):
            for lemma in ss.lemmas():
                word = lemma.name()
                if('_' in lemma.name()):
                    word = word.replace('_', " ")
                syn.append(word) #add the synonyms to syn

        syn = set(syn) #use a set to get rid of duplicates

        if(word in syn): #a word being its own synonym is redundant
            syn.remove(word)

        for synonym in syn:
            synNum += 1
            if(synNum <= 5):
                #Tack on another synonym plus a \n
                response += synonym + "\n"
            else:
                break

        try: #make sure we dont have an empty message to send (ie. no synonyms/not a word)
            await client.send_message(message.channel, response)
        except:
            response = "Sorry, we couldn't find that word!"
            await client.send_message(message.channel, response)

#############################################################################################

    if message.content.startswith("!ant"):
        response += "Antonyms of " + word + ":\n"
        ant = []
        antNum = 0
        for ss in wordnet.synsets(word):
            for lemma in ss.lemmas():
                word = lemma.name()
                if('_' in lemma.name()):
                    word = word.replace('_', " ")
                
                if lemma.antonyms():
                    ant.append(lemma.antonyms()[0].name()) #add the synonyms to syn

        ant = set(ant) #use a set to get rid of duplicates

        if(word in ant): #a word being its own antonym is redundant
            ant.remove(word)

        for antonym in ant:
            antNum += 1
            if(antNum <= 5):
                #Tack on another synonym plus a \n
                response += antonym + "\n"
            else:
                break

        try: #make sure we dont have an empty message to send (ie. no ants/not a word)
            await client.send_message(message.channel, response)
        except:
            response = "Sorry, we couldn't find that word!"
            await client.send_message(message.channel, response)

#############################################################################################

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

client.run(token)