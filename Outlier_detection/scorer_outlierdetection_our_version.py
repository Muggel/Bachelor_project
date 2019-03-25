# -*- coding: utf-8 -*-

### Author: Jose Camacho Collados


### Changes made:
# We have taken the original scorer_outlierdetection.py and made some changes:
# - Instead of setting the outlier position to 8/8 by default if the outlier vector isn't known,
#   we set the position to 0/8. This way, your score get punished by not knowing a vector
#   instead of gaining from it.
# - Used the package 'black' to format the code according to PEP8.
# - Used 2to3 to convert the code (which was python2) into python3 code.
# - In the computation of accuracy_cluster, we changed what we divide with
#   from count_total_outliers to len(cluster.outliers). We did this because,
#   count_total_outliers is growing for each new cluster (8, 16, 24, ...), but we
#   only want to divide by the size of the cluster (8).

import os
import fileinput
from math import sqrt
import operator
import sys


class OutlierDetectionCluster:
    # Class modeling a cluster of the dataset, composed of its topic name,
    # its corresponding elements and the outliers to be detected
    def __init__(self, elements, outliers, topic=""):
        self.elements = elements
        self.outliers = outliers
        self.topic = topic


class OutlierDetectionDataset:
    # Class modeling a whole outlier detection dataset composed of various topics or clusters
    def __init__(self, path):
        self.path = path
        self.setWords = set()
        self.clusters = set()

    def read_dataset(self):
        print("\nReading outlier detection dataset...")

        listing = os.listdir(self.path)
        for in_file in listing:
            if in_file.endswith(".txt"):
                cluster_file = open(self.path + in_file).readlines()
                cluster_name = in_file.replace(".txt", "")
                set_elements = set()
                set_outliers = set()
                cluster_boolean = True
                for line in cluster_file:
                    if cluster_boolean:
                        if line != "\n":
                            word = line.strip().replace(
                                " ", "_"
                            )  # removed .decode('utf-8') when changing to python3
                            set_elements.add(word)
                            self.setWords.add(word)
                            if "_" in word:
                                for unigram in word.split("_"):
                                    self.setWords.add(unigram)
                        else:
                            cluster_boolean = False
                    else:
                        if line != "\n":
                            word = line.strip().replace(
                                " ", "_"
                            )  # removed .decode('utf-8') when changing to python3
                            set_outliers.add(word)
                            self.setWords.add(word)
                            if "_" in word:
                                for unigram in word.split("_"):
                                    self.setWords.add(unigram)
                self.clusters.add(
                    OutlierDetectionCluster(set_elements, set_outliers, cluster_name)
                )


def boolean_answer(answer):
    if answer.lower() == "y" or answer.lower() == "yes":
        return True
    elif answer.lower() == "n" or answer.lower() == "no":
        return False
    else:
        new_answer = input('Please answer "Yes" or "No"')
        return boolean_answer(new_answer)


def module(vector):
    # Module of a vector
    suma = 0.0
    for dimension in vector:
        suma += dimension * dimension
    return sqrt(suma)


def scalar_prod(vector1, vector2):
    # Scalar product between two vectors
    prod = 0.0
    for i in range(len(vector1)):
        dimension_1 = vector1[i]
        dimension_2 = vector2[i]
        prod += dimension_1 * dimension_2
    return prod


def cosine(vector1, vector2):
    # Cosine similarity between two vectors
    module_vector_1 = module(vector1)
    if module_vector_1 == 0.0:
        return 0.0
    module_vector_2 = module(vector2)
    if module_vector_2 == 0.0:
        return 0.0
    return scalar_prod(vector1, vector2) / (module(vector1) * module(vector2))


def pairwisesimilarities_cluster(set_elements_cluster, input_vectors):
    # This function calculates all pair-wise similarities between the elements
    # of a cluster and stores them in a dictionary
    dict_sim = {}
    for element_1 in set_elements_cluster:
        for element_2 in set_elements_cluster:
            if element_1 != element_2:
                dict_sim[element_1 + " " + element_2] = cosine(
                    input_vectors[element_1], input_vectors[element_2]
                )
    return dict_sim


def compose_vectors_multiword(multiword, input_vectors, dimensions):
    # Given an OOV word as input, this function either returns a vector by averaging
    # the vectors of each token composing a multiword expression or a zero vector
    vector_multiword = [0.0] * dimensions
    cont_unigram_in_vectors = 0
    for unigram in multiword.split("_"):
        if unigram in input_vectors:
            cont_unigram_in_vectors += 1
            vector_unigram = input_vectors[unigram]
            for i in range(dimensions):
                vector_multiword[i] += vector_unigram[i]
    if cont_unigram_in_vectors > 0:
        for j in range(dimensions):
            vector_multiword[j] = vector_multiword[j] / cont_unigram_in_vectors
    return vector_multiword


def getting_vectors(path_vectors, set_words):
    # Reads input vectors file and stores the vectors of the words occurring in the dataset in a dictionary
    print("Loading word vectors...")
    dimensions = -1
    vectors = {}
    # vectors_file = fileinput.FileInput(path_vectors)
    with open(path_vectors, "r", encoding="utf-8", errors="ignore") as vectors_file:
        for line in vectors_file:
            word = line.split(" ", 1)[
                0
            ]  # removed .decode('utf-8') when changing to python3
            if word in set_words:
                linesplit = line.strip().split(" ")
                if dimensions != len(linesplit) - 1:
                    if dimensions == -1:
                        dimensions = len(linesplit) - 1
                    else:
                        print("WARNING! One line with a different number of dimensions")
                vectors[word] = []
                for i in range(dimensions):
                    vectors[word].append(float(linesplit[i + 1]))
    print(("Number of vector dimensions: " + str(dimensions)))
    for word in set_words:
        if word not in vectors:
            vectors[word] = compose_vectors_multiword(word, vectors, dimensions)
    print("Vectors already loaded")
    return vectors, dimensions


def main(path_dataset, path_vectors):

    dataset = OutlierDetectionDataset(path_dataset)
    dataset.read_dataset()
    input_vectors, dimensions = getting_vectors(path_vectors, dataset.setWords)

    dict_compactness = {}
    count_total_outliers = 0
    num_outliers_detected = 0
    sum_positions_percentage = 0
    detailed_results_string = ""
    results_by_cluster_string = ""
    for cluster in dataset.clusters:
        results_by_cluster_string += (
            "\n\n -- " + cluster.topic + " --"
        )  # removed .decode('utf-8') when changing to python3
        detailed_results_string += (
            "\n\n -- " + cluster.topic + " --\n"
        )  # removed .decode('utf-8') when changing to python3
        # create dict where keys are [element_cluster_1+" "+element_cluster_2] and the values are the similarities
        dict_sim = pairwisesimilarities_cluster(cluster.elements, input_vectors)
        num_outliers_detected_cluster = 0
        sum_positions_cluster = 0
        count_total_outliers += len(cluster.outliers)
        for outlier in cluster.outliers:
            # This makes sure that the score doesn't get better, if we don't know the vector for the outlier.
            if module(input_vectors[outlier]) == 0.0:
                print("No vector found for the outlier: ", outlier)
                continue

            comp_score_outlier = 0.0
            dict_compactness.clear()
            for element_cluster_1 in cluster.elements:
                # calculate the similarities of the current element and the outlier
                sim_outlier_element = cosine(
                    input_vectors[element_cluster_1], input_vectors[outlier]
                )

                comp_score_element = sim_outlier_element
                comp_score_outlier += sim_outlier_element
                # Sum the similarities between the elements in the cluster
                for element_cluster_2 in cluster.elements:
                    if element_cluster_1 != element_cluster_2:
                        comp_score_element += dict_sim[
                            element_cluster_1 + " " + element_cluster_2
                        ]
                # Set the compactness of the current element equal to the sum of how
                # similar it is to all other elements in the cluster
                dict_compactness[element_cluster_1] = comp_score_element

                # The "P-compactness" is the average of the comp_score_element
                detailed_results_string += (
                    "\nP-compactness "
                    + element_cluster_1
                    + " : "
                    + str(comp_score_element / len(cluster.elements))
                )  # removed .decode('utf-8') when changing to python3
            dict_compactness[outlier] = comp_score_outlier
            detailed_results_string += (
                "\nP-compactness "
                + outlier
                + " : "
                + str(comp_score_outlier / len(cluster.elements))
            )  # removed .decode('utf-8') when changing to python3

            # Gets a list of tuples: (<element>, compactness), sorted after the compactness
            # in decreasing order.
            sorted_list_compactness = sorted(
                iter(dict_compactness.items()), key=operator.itemgetter(1), reverse=True
            )

            # Runs through the sorted list of tuples to find the position
            # of the outlier.
            position_of_outlier = 0
            for position, element_score in enumerate(sorted_list_compactness):
                element = element_score[0]
                if element == outlier:
                    sum_positions_cluster += position
                    position_of_outlier = position
                    # if position==number_of_elements then we know we classified it correctly
                    if position == len(cluster.elements):
                        num_outliers_detected_cluster += 1
                    break
            print()
            detailed_results_string += (
                "\nPosition outlier "
                + outlier
                + " : "
                + str(position_of_outlier)
                + "/"
                + str(len(cluster.elements))
                + "\n"
            )  # removed .decode('utf-8') when changing to python3

        num_outliers_detected += num_outliers_detected_cluster
        sum_positions_percentage += (sum_positions_cluster * 1.0) / len(
            cluster.elements
        )

        score_opp_cluster = (
            ((sum_positions_cluster * 1.0) / len(cluster.elements))
            / len(cluster.outliers)
        ) * 100
        accuracy_cluster = (
            (num_outliers_detected_cluster * 1.0) / len(cluster.outliers)
        ) * 100.0

        results_by_cluster_string += "\nAverage outlier position in this topic: " + str(
            score_opp_cluster
        )
        results_by_cluster_string += (
            "\nOutliers detected percentage in this topic: " + str(accuracy_cluster)
        )
        results_by_cluster_string += "\nNumber of outliers in this topic: " + str(
            len(cluster.outliers)
        )

    score_opp = ((sum_positions_percentage * 1.0) / count_total_outliers) * 100
    accuracy = ((num_outliers_detected * 1.0) / count_total_outliers) * 100.0
    print("\n\n ---- OVERALL RESULTS ----\n")
    print(("OPP score: " + str(score_opp)))
    print(("Accuracy: " + str(accuracy)))
    print(("\nTotal number of outliers: " + str(count_total_outliers)))

    answer = input("\n\nWould you like to see the results by topic? [Y|N]")
    boolean = boolean_answer(answer)
    if boolean:
        print(results_by_cluster_string)
        answer_2 = input("\n\nWould you like to see a more detailed summary? [Y|N]")
        boolean_2 = boolean_answer(answer_2)
        if boolean_2:
            print(detailed_results_string)


if __name__ == "__main__":

    args = sys.argv[1:]

    if len(args) == 2:

        path_dataset = args[0]
        path_vectors = args[1]

        main(path_dataset, path_vectors)

    else:
        sys.exit(
            """
            Requires:
            path_dataset -> Path of the outlier detection directory
            path_vectors -> Path of the input word vectors
            """
        )