import fasttext
import argparse
import sys


def learn_embeddings(parser=None):
    if parser:
        parser = parser
    else:
        parser = argparse.ArgumentParser()
        parser.add_argument("src_input", type=str, help="Corpus used for learning embeddings")
        parser.add_argument("tgt_input", type=str, help="Corpus used for learning embeddings")
        parser.add_argument("src_output", type=str)
        parser.add_argument("tgt_output", type=str)
        parser.add_argument("--shared_input", type=str, help="Concatenated src + tgt corpora")
        parser.add_argument("--shared_output", type=str)
        parser.add_argument("--embedding_dim", type=int, default=512)
        parser.add_argument("--model", default="skipgram")

    args = parser.parse_args()

    src_model = fasttext.train_unsupervised(args.src_input, dim=args.embedding_dim, model=args.model)

    # format requirement: first line [vocabulary_size embedding_dimension]
    # word and each entry in embedding are split using whitespace (not \t)

    with open(args.src_output, 'w', encoding='utf-8') as f:
        f.write(str(len(src_model.words)))
        f.write(' ')
        f.write(str(args.embedding_dim))
        f.write('\n')
        for word in src_model.words:
            vec = src_model[word]
            f.write(word)
            f.write(' ')
            for entry in vec:
                f.write(str(entry))
                f.write(' ')
            f.write('\n')

    tgt_model = fasttext.train_unsupervised(args.tgt_input, dim=args.embedding_dim, model=args.model)

    # format requirement: first line [vocabulary_size embedding_dimension]
    # word and each entry in embedding are split using whitespace (not \t)

    with open(args.tgt_output, 'w', encoding='utf-8') as f:
        f.write(str(len(tgt_model.words)))
        f.write(' ')
        f.write(str(args.embedding_dim))
        f.write('\n')
        for word in tgt_model.words:
            vec = tgt_model[word]
            f.write(word)
            f.write(' ')
            for entry in vec:
                f.write(str(entry))
                f.write(' ')
            f.write('\n')

    if args.shared_input and args.shared_output:
        shared_model = fasttext.train_unsupervised(args.shared_input, dim=args.embedding_dim, model=args.model)

        # format requirement: first line [vocabulary_size embedding_dimension]
        # word and each entry in embedding are split using whitespace (not \t)

        with open(args.shared_output, 'w', encoding='utf-8') as f:
            f.write(str(len(shared_model.words)))
            f.write(' ')
            f.write(str(args.embedding_dim))
            f.write('\n')
            for word in shared_model.words:
                vec = shared_model[word]
                f.write(word)
                f.write(' ')
                for entry in vec:
                    f.write(str(entry))
                    f.write(' ')
                f.write('\n')

    sys.stdout.write("Embedding trained and saved.\n")


if __name__ == "__main__":
    learn_embeddings()
