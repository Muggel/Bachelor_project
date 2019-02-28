# Bachelor_project

This is the source code for our bachelor project (2019).

## Word2Vec args
* train &ltfile&gt: Dataset to train the model.
* output &ltfile&gt: Output file for the resulting word vectors.
* size &ltint&gt: Size of word vectors (default 100).
* window &ltint&gt: Max skip length between words.
* sample &ltfloat&gt: Threshold for occurrence of words. Those that appear with higher frequency in the training data will be randomly down-sampled (default 1e-3).
* hs &ltint&gt: Hierarchical Softmax on or off.
* negative &ltint&gt: Amount of negative samples. Default is 5, common values are 3 - 10 (0 = not used).
* threads &ltint&gt: Amount of threads to be used.
* iter &ltint&gt: Amount of iterations (default 5).
* min-count &ltint&gt: Discard words that occur less than min-count times (default 5).
* alpha &ltfloat&gt: Set the starting learning rate (default 0.025 for skip-gram and 0.05 for CBOW).
* classes &ltint&gt: Output word classes rather than word vectors if 1.
* debug &ltint&gt: Set the debug mode (default = 2 = more info during training).
* binary &ltint&gt Type of output file, binary 0 = txt and binary 1 = bin (default 0).
* save-vocab &ltfile&gt: Save the vocabulary to file.
* read-vocab &ltfile&gt: Read vocabulary from file instead of constructing from the training data.
* cbow &ltint&gt: cbow 0 = CBOW and cbow 1 = Skip-Gram.

## Word2VecF args
* train &ltfile&gt: Dataset to train the model.
* output &ltfile&gt: Output file for the resulting word vectors / word clusters.
* size &ltint&gt: Size of word vectors (default 100).
* negative &ltint&gt: Amount of negative samples. Default is 15, common values are 5 - 10 (0 = not used).
* threads &ltint&gt: Amount of threads to be used.
* sample &ltfloat&gt: Threshold for occurrence of words and contexts. Those that appear with higher frequency in the training data will be randomly down-sampled (default 0 = off).
* alpha &ltfloat&gt: Set the starting learning rate (default 0.025).
* iter &ltint&gt: Amount of iterations (default 1).
* binary &ltint&gt: Type of output file, binary 0 = txt and binary 1 = bin (default 0).
* dumpcv &ltfile&gt: Dump the context vectors in file.
* wvocab &ltfile&gt: Word vocabulary file.
* cvocab &ltfile&gt: Context vocabulary file.
