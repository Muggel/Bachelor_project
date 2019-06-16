""" Script for creating the second testset for task 2 """

import os


def create_copy_without_dublicates(syntax_type, syntax_testset_folder):
    """ Creates a copy of 'parsed_syntax_file' but without words already in 'syntax_testset' 
        Even though lower case and upper case words aren't the same vector, we still choses to
        remove both if one of them has been seen. (To get a completely different test set)."""
    already_used_words = set()
    for filename in os.listdir(syntax_testset_folder):
        with open(syntax_testset_folder + "/" + filename, "r") as f:
            for line in f:
                already_used_words.add(line.strip().lower())

    cleaned_parsed_syntax_file = "cleaned_words_and_pos_{}.txt".format(syntax_type)
    parsed_syntax_file = "parsed_syntax_data/cleaned_parsed_syntax_data_ALL_FILES/cleaned_words_and_pos_{}.txt".format(syntax_type)
    with open(cleaned_parsed_syntax_file, "w") as w:
        with open(parsed_syntax_file, "r") as f:
            for line in f:
                if line.split()[0].lower() not in already_used_words:
                    w.write(line)

if __name__ == "__main__":
    syntax_types = ["IN", "JJ", "JJR", "MD", "NN", "NNS", "RB", "VB"]
    for syntax_type in syntax_types:
        create_copy_without_dublicates(syntax_type, "Outlier_detection/8-8-8_syntax_Dataset_2")