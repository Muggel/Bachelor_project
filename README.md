# Bachelor_project

This is the source code for our bachelor project (2019).

SKRIV HVOR DE FORSKELLIGE STYKKER KODE ER FRA

SKRIV HVORDAN MAN KØRER DE FORSKELLIGE TING

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
