import os
import argparse
import subprocess 
import itertools
#from Outlier_detection import scorer_outlierdetection as so
from Outlier_detection import scorer_outlierdetection_our_version as so
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

    os.system("cut -f 2 {} | python yoavgo-word2vecf-0d8e19d2f2c6/scripts/vocab.py 50 > counted_vocabulary".format(path_to_conllu_file))
    os.system("cat {} | python yoavgo-word2vecf-0d8e19d2f2c6/scripts/extract_deps.py counted_vocabulary  100 > dep.contexts".format(path_to_conllu_file))
    

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

    os.system("{}/count_and_filter \
        -train dep.contexts \
        -cvocab cv \
        -wvocab wv \
        -min-count 50".format(path_to_word2vecf_folder))


def train_word_embedding_vectors_word2vecf(path_to_word2vecf_folder, path_to_conllu_file, outputfile, negative):
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
    create_vocabs_word2vecf("./{}".format(path_to_word2vecf_folder))
    os.system("{}/word2vecf \
        -train dep.contexts \
        -wvocab wv \
        -cvocab cv \
        -output {} \
        -size 300 \
        -negative {} \
        -threads 12 \
        -dumpcv dim200context-vecs".format(path_to_word2vecf_folder, outputfile, negative))

def train_word_embedding_vectors(path_to_word2vecf_folder, path_to_dataset, outputfile, cbow_or_skipgram, window, negative, hs):
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
        cbow_or_skipgram: If 0 run cbow. If 1 run skip-gram
    """

    os.system("{}/word2vec \
        -train {} \
        -output {} \
        -cbow {} \
        -size 300 \
        -window {} \
        -negative {} \
        -hs {} \
        -sample 1e-3 \
        -threads 12".format(path_to_word2vecf_folder, path_to_dataset, outputfile, cbow_or_skipgram, window, negative, hs))    

def run_outlier_detection(path_to_dataset, vectors):
    """Runs the outlier detection script from the outlier detection paper
    on the word embedding vectors in the file vectors.txt"""
    
    so.main(path_to_dataset, vectors)

class Args:
    pass

if __name__ == "__main__":
    args = Args()
    parser = argparse.ArgumentParser()
    parser.add_argument('-vectorize', '-v', 
                        choices=['skipgram', 'cbow', 'w2vf'],
                        help='The vectorizing methods used in the given task. It is required to give at least one',
                        nargs='+',
                        required=True)
    parser.add_argument('-tasks', '-t',
                        choices=['semant', 'syntax'],
                        help='The task that is to be run with the vectorizing methods.',
                        nargs='+')
    parser.add_argument('-train',
                        action='store_true',
                        help='If set, the vectorze methods will train again.')
    parser.add_argument('-tokenized',
                        default='tokenized_dataset.txt',
                        help='Path to the tokenized dataset. Default is ./tokenized_dataset.txt.')
    parser.add_argument('-parsed',
                        default='parsed_dataset.conllu',
                        help='Path to the parsed dataset. Default is ./parsed_dataset.conllu.')
    parser.add_argument('-iter',
                        default="1",
                        help='number of iterations the pipeline should be run. Default is 1')
    parser.parse_args(namespace=args)
    
    args = parser.parse_args()


    for i in range(int(args.iter)):
        vec_func_dict = {'skipgram': lambda: train_word_embedding_vectors("yoavgo-word2vecf-0d8e19d2f2c6", args.tokenized, "vectors_skipgram{}.txt".format(i), 0, 10, 15, 0),
                        'cbow': lambda: train_word_embedding_vectors("yoavgo-word2vecf-0d8e19d2f2c6", args.tokenized, "vectors_cbow{}.txt".format(i), 1, 5, 0, 1),
                        'w2vf': lambda: train_word_embedding_vectors_word2vecf("yoavgo-word2vecf-0d8e19d2f2c6", args.parsed, "vectors_w2vf{}.txt".format(i), 15)}

        task_func_dict = {'semant': lambda x: run_outlier_detection('Outlier_detection/8-8-8_Dataset/', x),
                        'syntax': lambda x: run_outlier_detection('Outlier_detection/8-8-8_syntax_Dataset/', x)}

        vector_file_dict = {'skipgram': "vectors_skipgram{}.txt".format(i),
                            'cbow': "vectors_cbow{}.txt".format(i),
                            'w2vf': "vectors_w2vf{}.txt".format(i)}

        if args.train: [vec_func_dict[x]() for x in set(args.vectorize)]

        if args.tasks:
            task_set = {task_func_dict[x] for x in args.tasks}

            for task, vectors in itertools.product(task_set, args.vectorize):
                task(vector_file_dict[vectors])
