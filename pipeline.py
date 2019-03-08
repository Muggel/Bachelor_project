import os
import argparse
from Outlier_detection import scorer_outlierdetection as so
from conllu import parse_incr
from collections import OrderedDict

# convert files with: cat PATH_TO_CONLLU_FILE | perl conllu_to_conllx.pl  > PATH_TO_WHERE_CONVERTED_FILE_IS_SAVED
# get it by cloning: https://github.com/UniversalDependencies/tools

def create_word_and_context_file_word2vecf(path_to_conllu_file):
    """ Create a file with words and their context.

    This function create a file (dep.contexts) where
    each line is on the form: <word> <context>.

    Args:
        path_to_conllu_file: The path to the conllu file that
        contains the information about the words in the
        corpus and their corresponding data
    """

    os.system("cut -f 2 %s | python yoavgo-word2vecf-0d8e19d2f2c6/scripts/vocab.py 50 > counted_vocabulary" % path_to_conllu_file) 
    os.system("cat %s | python yoavgo-word2vecf-0d8e19d2f2c6/scripts/extract_deps.py counted_vocabulary  100 > dep.contexts" % path_to_conllu_file)
    

def create_vocabs_word2vecf(path_to_word2vecf_folder):
    """ Create word and context vocabularies.

    This function creates a word vocabulary (wv) and 
    a context vocabularie (cv), based on the dep.contexts
    file.

    Args:
        path_to_word2vecf_folder: The path to the
        folder where the executable count_and_filer file 
        is located.
    """

    os.system("%s/count_and_filter \
        -train dep.contexts \
        -cvocab cv \
        -wvocab wv \
        -min-count 50" % path_to_word2vecf_folder) 


def train_word_embedding_vectors_word2vecf(path_to_word2vecf_folder, path_to_conllu_file):
    """ Trains the word embedding vectors with word2vecf.
        
    This function creates the file vectors.txt 
    containing the word embedding vectors for the 
    words in the corpus, and the vectors for the
    context.

    Args:
        path_to_word2vecf_folder: The path to the
        folder where the executable word2vecf file 
        is located.
        path_to_conllu_file: The path to the conllu file that
        contains the information about the words in the
        corpus and their corresponding data
    """

    create_word_and_context_file_word2vecf(path_to_conllu_file)
    create_vocabs_word2vecf("./%s" % path_to_word2vecf_folder)
    os.system("%s/word2vecf \
        -train dep.contexts \
        -wvocab wv \
        -cvocab cv \
        -output vectors.txt \
        -size 200 \
        -negative 1 \
        -threads 12 \
        -dumpcv dim200context-vecs" % path_to_word2vecf_folder)

 
def train_word_embedding_vectors(path_to_word2vecf_folder, path_to_dataset):
    """Trains the word embedding vectors with word2vec.
    
    The vectors generated from running this function
    is outputted to the file vectors.txt.

    Args:
        path_to_word2vecf_folder: The path to the
        folder where the executable word2vec file 
        is located. (It is not a mistake it is to the 
        word2vecf folder. This folder also contains
        an implementation of word2vec).
        path_to_dataset: The path to the dataset that
        should be used to extract word embeddings from.
    """
    
    os.system("%s/word2vec \
        -train %s \
        -output vectors.txt \
        -cbow 0 \
        -size 200 \
        -window 5 \
        -negative 15 \
        -hs 0 \
        -sample 1e-3 \
        -threads 12" % (path_to_word2vecf_folder, path_to_dataset))    

def run_outlier_detection():
    """Runs the outlier detection script from the outlier detection paper
    on the word embedding vectors in the file vectors.txt"""
    
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
        
        return answer == 'y'
    
    
    def __call__(self, parser, namespace, values, option_string=None):
        if not self.getConfirmation(values):
            return

        print('Vectorizing with method: {}'.format(values))

        if values in ['word2vec', 'w2v']:
            train_word_embedding_vectors("yoavgo-word2vecf-0d8e19d2f2c6", "datasets/combined_English_text.txt") 
        elif values in ['word2vecf', 'w2vf']: 
            train_word_embedding_vectors_word2vecf("yoavgo-word2vecf-0d8e19d2f2c6", "datasets/Converted_combined_english_text.conllu")


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