#!/bin/bash

while getopts 's:t:h' opt; do
  case "$opt" in

    s)
      SRC_TOK="$OPTARG"
      echo "Processing option 's' with '${OPTARG}' argument"
      ;;

    t)
      TGT_TOK="$OPTARG"
      echo "Processing option 't' with '${OPTARG}' argument"
      ;;

    ?|h)
      echo "Usage: $(basename $0) [-s <tokenized_source_data_path>] [-t <tokenized_target_data_path]"
      exit 1
      ;;
  esac
done

shift "$(($OPTIND -1))"

set -e

echo $SRC_TOK
echo $TGT_TOK

TOOLS_PATH=$PWD/tools
DATA_PATH=$PWD/data
mkdir -p $TOOLS_PATH
mkdir -p $DATA_PATH

SRC_VOCAB=$DATA_PATH/vocab.yue
TGT_VOCAB=$DATA_PATH/vocab.zh
FULL_VOCAB=$DATA_PATH/vocab.yue-zh

# fastBPE dir
FASTBPE_DIR=$TOOLS_PATH/fastBPE
FASTBPE=$FASTBPE_DIR/fast

# Download fastBPE
cd $TOOLS_PATH
if [ ! -d "$FASTBPE_DIR" ]; then
  echo "Cloning fastBPE from GitHub repository..."
  git clone https://github.com/glample/fastBPE
fi
echo "fastBPE found in: $FASTBPE_DIR"

# Compile fastBPE
cd $TOOLS_PATH
if [ ! -f "$FASTBPE" ]; then
  echo "Compiling fastBPE..."
  cd $FASTBPE_DIR
  g++ -std=c++11 -pthread -O3 fastBPE/main.cc -IfastBPE -o fast
fi
echo "fastBPE compiled in: $FASTBPE"

# extract vocabulary
# if this fails, it can be run manually after the code above has successfully completed
if ! [[ -f "$SRC_VOCAB" && -f "$TGT_VOCAB" && -f "$FULL_VOCAB" ]]; then
  echo "Extracting vocabulary..."
  $FASTBPE getvocab $SRC_TOK > $SRC_VOCAB
  $FASTBPE getvocab $TGT_TOK > $TGT_VOCAB
  $FASTBPE getvocab $SRC_TOK $TGT_TOK > $FULL_VOCAB
fi
echo "YUE vocab in: $SRC_VOCAB"
echo "ZH vocab in: $TGT_VOCAB"
echo "Full vocab in: $FULL_VOCAB"