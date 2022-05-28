import fasttext
import argparse
import sys


def learn_embeddings():
    parser = argparse.ArgumentParser()
    parser.add_argument("--corpus", type=str, help="Corpus used for learning embeddings")
    parser.add_argument("--write_path", type=str)
    parser.add_argument("--embedding_dim", type=int)
    parser.add_argument("--model", default="skipgram")

    args = parser.parse_args()

    model = fasttext.train_unsupervised(args.corpus, dim=args.embedding_dim, model=args.model)

    # format requirement: first line [vocabulary_size embedding_dimension]
    # word and each entry in embedding are split using whitespace (not \t)
    with open(args.write_path, 'w') as f:
        f.write(str(len(model.words)))
        f.write(' ')
        f.write(str(args.embedding_dim))
        f.write('\n')
        for word in model.words:
            vec = model[word]
            f.write(word)
            f.write(' ')
            for entry in vec:
                f.write(str(entry))
                f.write(' ')
            f.write('\n')

    sys.stdout.write("Embedding trained and saved.\n")


if __name__ == "__main__":
     learn_embeddings()
