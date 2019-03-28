import os

def read_file(dest):
    print(dest)
    with open(dest, 'r', encoding='utf-8', errors='ignore') as file:
        text = file.read()
        return list(map(lambda x: x.split("_") if len(x.split('_')) == 2 else [x, 'error'], text.split()))

def create_map(file_list):
    word_to_pos = {}
    for curr_file in file_list:
        list_of_words = read_file(path + curr_file)
        for word, tag in list_of_words:
            if tag == 'error':
                continue
            current = word_to_pos.get(word)
            if current == None:
                word_to_pos[word] = [tag, 1]
            elif not current[0]:
                continue
            elif tag == current[0]:
                word_to_pos[word] = [tag, current[1] + 1]
            else:
                word_to_pos[word][0] = False
    return word_to_pos


def write_to_file(file, word_to_pos):
    for key, value in word_to_pos.items():
        if value[0] == pos_type and value[1] >= 50:
            file.write('{} {}\n'.format(key, value[0]))


if __name__ == "__main__":
    global path, pos_type
    path = 'temp/'
    pos_type = 'JJ'
    with open('words_and_pos_{}.txt'.format(pos_type), 'w') as dest:
        word_to_pos = create_map(os.listdir(path))
        write_to_file(dest, word_to_pos)
