# Preprocess data for word2vec and word2vecf
import subprocess
import os
from nltk.tokenize import word_tokenize, sent_tokenize

def tokenize_and_write_to_tokenresult(text):
    tokens = word_tokenize(text)
    with open('tokenized_data_set.txt', 'a') as dest:
        for token in tokens:
            if token == '.':
                dest.write(token.lower() + '\n')   
            else:
                dest.write(token.lower() + ' ')
    

def append_to_conll(part):
    # Write next part of source to temp file
    with open('temp_file', 'w') as temp_file:
        for sentence in part:
            temp_file.write(sentence + "\n")
    
    # call java
    subprocess.run("java -Xmx12g -cp 'stanford-corenlp/*' edu.stanford.nlp.pipeline.StanfordCoreNLP -annotators tokenize,ssplit,pos,depparse -file temp_file  -outputFormat conllu", shell=True)
    # write result from tmp_file into conllu_result

    with open('temp_file.conllu', 'r') as from_file:
        with open('conll_data_set.conllu', 'a') as dest_file:
            dest_file.write(from_file.read())

def make_conll_and_write_to_conllresult(text, threshhold):
    sentences = sent_tokenize(text)
    
    temp_arr = []
    temp_file_len = 0
    for sentence in sentences:
        if temp_file_len >= threshhold: 
            append_to_conll(temp_arr)
            temp_arr = []
            temp_file_len = 0
        
        temp_arr.append(sentence)
        temp_file_len += len(sentence)
    
    append_to_conll(temp_arr)
        

def create_conll_file_and_tokenized_file(source):
    with open(source, 'r') as input:
        inp = input.read()
        #make_conll_and_write_to_conllresult(inp, )
        tokenize_and_write_to_tokenresult(inp)
        

# split alle filer op i mindre filer på størrelsen okring 3mb
def process_all_files_in_folder(path_to_folder):
    pass

if __name__ == "__main__":
    create_conll_file_and_tokenized_file("test_file.txt")
