import os
import argparse
from Outlier_detection import scorer_outlierdetection as so
from conllu import parse_incr
from collections import OrderedDict

# create a file (dep.contexts) where each line is: word context
def create_word_and_context_file_word2vecf(conllu_file):
    with open("dep.contexts", "w") as parsed_conllu_file:
        with open(conllu_file, "r") as data_file:
            for tokenlist in parse_incr(data_file):
                for bigram in tokenlist[0].items():
                    # TODO: Fix nested OrderedDicts
                    #if not isinstance(bigram[1], OrderedDict):
                    parsed_conllu_file.write("%s %s\n" % (bigram[0], bigram[1]))

# create word and context vocabularies (cv and wv)
def create_vocabs_word2vecf(path_to_word2vecf_folder):
    os.system("%s/count_and_filter \
        -train dep.contexts \
        -cvocab cv \
        -wvocab wv \
        -min-count 100" % path_to_word2vecf_folder)

# trains the word embedding vectors with word2vecf
# both the word vectors and the context vectors
def train_word_embedding_vectors_word2vecf(path_to_word2vecf_folder, path_to_conllu_file):
    create_word_and_context_file_word2vecf(path_to_conllu_file)
    create_vocabs_word2vecf("./%s" % path_to_word2vecf_folder)
    os.system("%s/word2vecf \
        -train dep.contexts \
        -wvocab wv \
        -cvocab cv \
        -output vectors.txt \
        -size 200 \
        -negative 15 \
        -threads 10 \
        -dumpcv dim200context-vecs" % path_to_word2vecf_folder)    

# trains the word embedding vectors with word2vec 
def train_word_embedding_vectors(path_to_word2vecf_folder, path_to_dataset):
    os.system("%s/word2vec \
        -train %s \
        -output ../vectors.txt \
        -cbow 0 \
        -size 200 \
        -window 5 \
        -negative 0 \
        -hs 1 \
        -sample 1e-3 \
        -threads 12" % (path_to_word2vecf_folder, path_to_dataset))    

# runs the outlier detection script from the outlier detection paper
# on the word embedding vectors created from either word2vec or word2vecf
def run_outlier_detection():
    # os.system("cd Outlier_detection && python3 scorer_outlierdetection.py 8-8-8_Dataset/ ../vectors.txt")
    so.main('Outlier_detection/8-8-8_Dataset/', 'vectors.txt')

class Args:
    pass

class Vectorize(argparse.Action):
    def __init__(self, choices, dest, option_strings, nargs=None, **kwargs):
        if nargs is not None:
            raise ValueError('nargs not allowed')
        super(Vectorize, self).__init__(option_strings, dest, **kwargs)

    
    def getConfirmation(self, values):
        answer = input('Do you want to train the Word Embeddings with {} \n\
This might take some time [Y/n]:'.format(values)).lower()
        while answer not in ['y', 'n']:
            answer = input('[Y/n]: ')
        
        return (True if answer == 'y' else False)
    
    
    def __call__(self, parser, namespace, values, option_string=None):
        if not self.getConfirmation(values):
            return

        print('Vectorizing with method: {}'.format(values))

        if values in ['word2vec', 'w2v']:
            train_word_embedding_vectors("yoavgo-word2vecf-0d8e19d2f2c6", "en_ewt-ud-train.txt") 
        elif values in ['word2vecf', 'w2vf']: 
            train_word_embedding_vectors_word2vecf("yoavgo-word2vecf-0d8e19d2f2c6", "en_ewt-ud-train.conllu")


class Task(argparse.Action):
    def __init__(self, choices, dest, option_strings, nargs=None, **kwargs):
        if nargs is not None:
            raise ValueError('nargs not allowed')
        super(Task, self).__init__(option_strings, dest, **kwargs)

    def __call__(self, parser, namespace, values, option_string=None):
        print('Running task: {}'.format(values))
        if values in ['outlier', 'o', 'task1', '1']:
            run_outlier_detection()


if __name__ == "__main__":
    args = Args()
    parser = argparse.ArgumentParser()
    parser.add_argument('-vectorize', '-v', 
                        choices=['word2vec', 'w2v', 'word2vecf', 'w2vf'], 
                        help='If you want to vectorize a corpus used \"-v=\" \
                              followed by the method you want to use.',
                        action=Vectorize)
    parser.add_argument('-task', '-t',
                        choices=['outlier', 'o', 'task1', '1'],
                        action=Task)
    parser.parse_args(namespace=args)