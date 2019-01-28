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

    if message.content.startswith("!syn"):
        syn = []
        for ss in wordnet.synsets(word):
            for lemma in ss.lemmas():
                syn.append(lemma.name()) #add the synonyms to syn

        syn = remove(syn)



        print(syn)


def remove(array): 
    final_list = [] 
    for num in array: 
        if num not in final_list: 
            final_list.append(num) 
    return final_list


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

client.run(token)