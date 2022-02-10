__author__ = 'KevinZhao'
# You can use this to run the CMU Tweet NLP package(http://www.ark.cs.cmu.edu/TweetNLP/)
# First, download the package at https://github.com/brendano/ark-tweet-nlp/
# Second, put everything in the project directory where you are running the python script

import subprocess
import codecs
import os
import psutil
import tempfile
import re
class TweetTagger:
    def runFile(fileName):
        p = subprocess.Popen('java -XX:ParallelGCThreads=2 -Xmx500m -jar D:\\temp20\\ark-tweet-nlp-0.3.2\\ark-tweet-nlp-0.3.2.jar "'+ fileName + '"',stdout=subprocess.PIPE)
        pos_list = []
        while p.poll() is None:
            l = p.stdout.readline()
            pos_list.append(l.decode('utf-8'))
        return pos_list

    def runString(s):
        file_name = 'temp_file_%s.txt' % os.getpid()
        o = codecs.open(file_name,'w','utf-8')
        uniS = s#.decode('utf-8')
        o.write(uniS)
        o.close()
        l = ''
        p = subprocess.Popen('java -XX:ParallelGCThreads=2 -Xmx500m -jar D:\\temp20\\ark-tweet-nlp-0.3.2\\ark-tweet-nlp-0.3.2.jar ' + file_name,stdout=subprocess.PIPE)

        while p.poll() is None:
            l = p.stdout.readline()
            break

        p.kill()
        psutil.pids()

        os.remove(file_name)
        #Running one tweet at a time takes much longer time because of restarting the tagger
        #we recommend putting all sentences into one file and then tag the whole file, use the runFile method shown above
        return l

    if __name__ == "__main__":
        pos_dict = dict()
        split_list = list()

        heyvar = runString("Xe went to the store. Zhey saw a big chungus. It was xim who saw it.").decode("utf-8")
        if heyvar != "":
            formatted_tags = re.split(r'\t+', heyvar.rstrip('\t'))
            print(formatted_tags)
            keys = formatted_tags[1].strip().split(" ")
            values = formatted_tags[0].strip().split(" ")
            split_list.append(values)
            for i in range(len(values)):
                pos_dict.setdefault(keys[i], {})[values[i]] = 1
        print(pos_dict)
        print("\n\n")
        print(split_list)