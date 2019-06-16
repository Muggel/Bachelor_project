""" This script is for analysing the output of multiple models in task 1 and 2 """

def average_topics(file_path, no_of_topics):
    """ Takes the result from all 10 models of the same kind and
        outputs the average result of each topic (Months, Big_cats, etc.) """

    score_dict = {}

    result_file = open(file_path)
    reading_mode = False
    line = result_file.readline()
    counter = 0
    while line != "":
        #print(line)
        if "Would you like to see the results by topic" in line:
            reading_mode = True

        if reading_mode:
            if line.startswith(" -- "):
                topic = line.strip()
                opp = result_file.readline().split()[-1]
                acc = result_file.readline().split()[-1]

                if topic in score_dict:
                    t_opp, t_acc = score_dict[topic]
                    score_dict[topic] = (t_opp + float(opp), t_acc + float(acc))
                else:
                    score_dict[topic] = (float(opp), float(acc))

                counter += 1

        if counter == no_of_topics:
            counter = 0
            reading_mode = False

        line = result_file.readline()

    for topic, scores in score_dict.items():
        print(topic)
        print("Mean OPP:", scores[0]/10)
        print("Mean Accuracy:", scores[1]/10)
        print()


def make_results_summary(file_path, model_type):
    result_file = open(file_path)
    reading_mode = False
    line = result_file.readline()
    counter = 0
    while line != "":
        #print(line)
        if "OPP score:" in line:
            print(model_type + " " + str(counter))
            print(line.strip("\n"))
            line = result_file.readline()
            print(line)
            counter += 1

        line = result_file.readline()


make_results_summary("result_file.txt", "Word2VecFix")
average_topics("result_file.txt", 8)

