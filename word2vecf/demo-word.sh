make
if [ ! -e text8 ]; then
  curl http://mattmahoney.net/dc/text8.zip -O
  unzip -a text8.zip
fi
time ./word2vec -train text8 -output vectors.bin -cbow 0 -size 200 -window 5 -negative 0 -hs 1 -sample 1e-3 -threads 12 -binary 1
./distance vectors.bin
