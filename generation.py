#from ark-tweet-nlp-master import CMUTweetTaggerWindows 
#import ark-tweet-nlp-0.3.2
#CMUTweetTaggerWindows.run
from asyncio.windows_events import NULL
import re
from JavaTweetFiles.CMUTweetTaggerWindows import TweetTagger
from storing import Storage
from filedata import FileInteraction
import asyncio
import time
import random
class Generate():

    def make_markov(corpus):
        markov_list = {}
        for chunk in corpus:
            for i in range(len(chunk)):
                current_word = chunk[i]
                previous_words = ' '.join(chunk[i-1:i])
                if previous_words in markov_list:
                    markov_list[previous_words].append(current_word)
                else:
                    markov_list[previous_words] = [current_word]
        return markov_list

    async def unroll_message(client, line):
        message = await client.get_channel(line[1]).fetch_message(line[0])
        return message.content        

    async def tag_and_split(serverID):
        pos_dict = dict()
        markov_dict = dict()
        split_list = list()
        pos_pattern = None
        first_item = True
        file_name = FileInteraction.get_file_path()
        pos_list = TweetTagger.runFile(file_name + str(serverID) + "\\" + "temporary_generation_file.txt")
        for item in pos_list:
            if item != "":
                formatted_tags = re.split(r'\t+', item.rstrip('\t'))
                keys = formatted_tags[1].strip().split(" ")
                if first_item:
                    pos_pattern = keys
                    first_item = False

                values = formatted_tags[0].strip().split(" ")
                split_list.append(values)
                for i in range(len(values)):
                    pos_dict.setdefault(keys[i], {})[values[i]] = 1

        markov_dict = Generate.make_markov(split_list)
        return pos_dict, markov_dict, pos_pattern