# Evaluation of Word Embeddings for Natural Language Processing Tasks, and a Proposal for Dependency Based Contexts

This is the source code for our bachelor project (2019).

The word2vecf folder is from the official repository for Word2VecF: https://bitbucket.org/yoavgo/word2vecf/src/default/
The Outlier_detection folder is from official repository for the 'Find the word that does not belong' paper: ?????

* To train a either CBOW or Skip-gram use: `python3 pipeline.py -v [MODEL_TYPE] -tokenized [PATH_TO_TOKENIZED_FILE] -train`
* To train a Word2VecF or Word2VecFix use: `python3 pipeline.py -v [MODEL_TYPE] -parsed [PATH_TO_PARSED_FILE] -train`
* To run task 1 or 2 on one of the trained models use: `python3 pipeline.py -v [MODEL_TYPE] -t [TASK]`
* To run task 3 on one of the trained models use: `python3 pipeline.py -v [MODEL_TYPE] -t [TASK] -questions [PATH_TO_QUESIONS]`

The models and task:  
* MODEL_TYPE: skipgram, cbow, w2vf, w2vfix
* TASK: semant, syntax, syntax2, analogy

## Word2Vec args
* train \<file\>: Dataset to train the model.
* output \<file\>: Output file for the resulting word vectors.
* size \<int\>: Size of word vectors (default 100).
* window \<int\>: Max skip length between words.
* sample \<float\>: Threshold for occurrence of words. Those that appear with higher frequency in the training data will be randomly down-sampled (default 1e-3).
* hs \<int\>: Hierarchical Softmax on or off.
* negative \<int\>: Amount of negative samples. Default is 5, common values are 3 - 10 (0 = not used).
* threads \<int\>: Amount of threads to be used.
* iter \<int\>: Amount of iterations (default 5).
* min-count \<int\>: Discard words that occur less than min-count times (default 5).
* alpha \<float\>: Set the starting learning rate (default 0.025 for skip-gram and 0.05 for CBOW).
* classes \<int\>: Output word classes rather than word vectors if 1.
* debug \<int\>: Set the debug mode (default = 2 = more info during training).
* binary \<int\> Type of output file, binary 0 = txt and binary 1 = bin (default 0).
* save-vocab \<file\>: Save the vocabulary to file.
* read-vocab \<file\>: Read vocabulary from file instead of constructing from the training data.
* cbow \<int\>: cbow 1 = CBOW and cbow 0 = Skip-Gram.

## Word2VecF args
* train \<file\>: Dataset to train the model.
* output \<file\>: Output file for the resulting word vectors / word clusters.
* size \<int\>: Size of word vectors (default 100).
* negative \<int\>: Amount of negative samples. Default is 15, common values are 5 - 10 (0 = not used).
* threads \<int\>: Amount of threads to be used.
* sample \<float\>: Threshold for occurrence of words and contexts. Those that appear with higher frequency in the training data will be randomly down-sampled (default 0 = off).
* alpha \<float\>: Set the starting learning rate (default 0.025).
* iter \<int\>: Amount of iterations (default 1).
* binary \<int\>: Type of output file, binary 0 = txt and binary 1 = bin (default 0).
* dumpcv \<file\>: Dump the context vectors in file.
* wvocab \<file\>: Word vocabulary file.
* cvocab \<file\>: Context vocabulary file.
