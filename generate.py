import argparse
import random
import numpy as np
import pdb
import re
import importlib


def train(text):
    words = text.split()

    words = filter_words(words)#[w for w in ["".join(filter(lambda x: x.isalpha(), word)).lower() for word in words] if w]
    transitions = {}
    for i in range(len(words) - 2):
        word = words[i]
        next_word = words[i + 1]
        sec_word = words[i + 2]
        word_pair = (next_word, sec_word)

        if word not in transitions:
            transitions[word] = {}

        if word in transitions:
            next_words = transitions[word]
            if word_pair in next_words:
                next_words[word_pair] += 1
            else:
                next_words[word_pair] = 1
    return transitions


def filter_words(words):
    res = []
    for word in words:
        if word in ':P:D:):(':
            res += [word]
            continue

        new_words = ['']
        curr_i = 0
        for c in word:
            if c in '.,!?':
                curr_i += 2
                new_words.append(c)
                new_words.append('')
            elif c.isalpha():
                new_words[curr_i] += c.lower()
        res += [w for w in new_words if w]
    return res

            


def convert_to_probabilities(transitions):
    probabilities = {}
    for next_word, next_words in transitions.items():
        total = sum(next_words.values())
        if total > 0:
            new_next_words = {}
            for w, freq in next_words.items():
                new_next_words[w] = freq/total
            probabilities[next_word] = new_next_words
    return probabilities


def generate(probabilities, length):
    current_word = random.choice(list(probabilities.keys()))
    text = [current_word.capitalize()]
    capitalize = True
    for _ in range(length):
        if current_word in probabilities:
            next_words = probabilities[current_word]
            words, probs = _get_probabilities_list(next_words)

            index = np.random.choice(range(len(words)), 1, p=probs)[0]
            next_word1, next_word2 = words[index]
            if next_word1 in '.!?':
                text[-1] += next_word1
                text.append(next_word2.capitalize())
                capitalize = False
            elif next_word1 == ',':
                text[-1] += next_word1
                text.append(next_word2)
                capitalize = next_word2 in '.!?'
            elif next_word2 in '.!?':
                text.append(next_word1.capitalize() if capitalize else next_word1)
                text[-1] += next_word2
                capitalize = True
            elif next_word2 == ',':
                text.append(next_word1)
                text[-1] += next_word2
                capitalize = False
            else:
                text.append(next_word1.capitalize() if capitalize else next_word1)
                text.append(next_word2)
                capitalize = False
            current_word = next_word2
        else:
            text[-1] += '.'
            current_word = random.choice(list(probabilities.keys()))
            capitalize = True
    return " ".join(text)
        

def _get_probabilities_list(next_words):
    probabilities = []
    words = []
    for word, prob in next_words.items():
        probabilities.append(prob)
        words.append(word)
    return words, probabilities


def generate_from(training_data, word_amount):
    probabilities = convert_to_probabilities(training_data)
    return generate(probabilities, word_amount)


def main():
    parser = argparse.ArgumentParser(description="Din mamma.")

    parser.add_argument('file', nargs=1, type=str, help="Text file containing training text.")
    parser.add_argument('-l', '--length', help='Number of words in output',
                        type=int, default=100)

    args = parser.parse_args()

    text = None
    with open(args.file[0]) as f:
        text = f.read()

    text = generate_from(train(text), args.length)
    print(text)


def train_from_messages_file(module_name):
    module = importlib.import_module(module_name)

    total_messages_training = {}
    for m in module.messages:
        train_result = train(m)

        for word, next_words in train_result.items():
            if word not in total_messages_training:
                total_messages_training[word] = next_words
            else:
                existing_next_words = total_messages_training[word]
                for w in next_words:
                    if w not in existing_next_words:
                        existing_next_words[w] = next_words[w]
                    else:
                        existing_next_words[w] += next_words[w]

    return total_messages_training

def get_random_user():
    users = [
        'Emil',
        'Malcolm',
        'Robin',
        'David',
        'Olav',
        'Hannes',
        'Frans'
    ]
    return random.choice(users)


if __name__ == '__main__':
    main()

