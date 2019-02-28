
import os
from Outlier_detection import scorer_outlierdetection as so

if __name__ == "__main__":
    os.system("cd yoavgo-word2vecf-0d8e19d2f2c6 && ./demo-word-txt.sh")
    so.main('8-8-8_Dataset/', 'vectors.txt')
