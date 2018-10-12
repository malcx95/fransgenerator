import argparse
import random
import numpy


def train(text):
    words = text.split(' ')
    total = len(words)

    words = [w for w in ["".split(filter(lambda x: x.isalpha(), word)).lower() for word in words] if w]
    transitions = {}
    for i in range(total - 1):
        word = words[i]
        next_word = words[i + 1]

        if word in transitions:
            next_words, freq = transitions[word]
            if next_word in next_words:
                next_words[next_word] += 1
            else:
                next_words[next_word] = 0
        else:
            transitions[word] = {}
    return transitions


def convert_to_probabilities(transitions):
    probabilities = {}
    for next_word, next_words in transitions.items():
        total = sum(next_words.values())
        new_next_words = {}
        for w, freq in next_words.items():
            new_next_words[w] = freq/total
        probabilities[next_word] = new_next_words
    return probabilities


def generate(probabilities, length):
    current_word = random.choice(list(probabilities.keys()))
    text = [current_word]
    for _ in range(length):
        next_words = probabilities[current_word]
        words_list = list(next_words.keys())
        probs = list(next_words.values())
        # TODO create a function that matches probabilities with the words
        

def main():
    parser = argparse.ArgumentParser(description="Din mamma.")

    parser.add_argument('-f', '--file', type=str,
                        help="Text file containing training text.",
                        required=True)
    parser.add_argument('-l', '--length', help='Number of words in output',
                        type=int, default=100)

    args = parser.parse_args()

    text = None
    with open(args.file) as f:
        text = f.read()


if __name__ == '__main__':
    main()

