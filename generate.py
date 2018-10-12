import argparse
import random
import numpy as np
import pdb


def train(text):
    words = text.split()

    words = [w for w in ["".join(filter(lambda x: x.isalpha(), word)).lower() for word in words] if w]
    transitions = {}
    for i in range(len(words) - 1):
        word = words[i]
        next_word = words[i + 1]

        if word in transitions:
            next_words = transitions[word]
            if next_word in next_words:
                next_words[next_word] += 1
            else:
                next_words[next_word] = 1
        else:
            transitions[word] = {}
    return transitions


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
    text = [current_word]
    for _ in range(length):
        if current_word in probabilities:
            next_words = probabilities[current_word]
            words, probs = _get_probabilities_list(next_words)
            next_word = str(np.random.choice(words, 1, p=probs)[0])
            text.append(next_word)
            current_word = next_word
        else:
            text[-1] += random.choice(['.', '.', '.', ',', '!', '?'])
            current_word = random.choice(list(probabilities.keys()))
    return " ".join(text)
        

def _get_probabilities_list(next_words):
    probabilities = []
    words = []
    for word, prob in next_words.items():
        probabilities.append(prob)
        words.append(word)
    return words, probabilities


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

    probabilities = convert_to_probabilities(train(text))
    text = generate(probabilities, args.length)
    print(text)


if __name__ == '__main__':
    main()

