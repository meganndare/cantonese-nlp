# cantonese-nlp
cantonese-mandarin unsupervised neural translation for sw project


# Running your own model

#### 1. RNN and Transformer Models leveraged the following repositories. For a step-by-step pipeline for running the RNN model in your own environment, see [this google doc](https://docs.google.com/document/d/1hlBGubStfdLhES_RppezuPCXex6Z98QuzQwxIzIjm7Q/edit).

##### RNN
https://github.com/artetxem/undreamt

##### Transformer
https://github.com/facebookresearch/UnsupervisedMT


#### 2. Note that there are several components required to train a model for unsupervised machine translation, as detailed in our paper. Below are some components we used for various models, such as a BPE vocabulary generator and repository for training cross-lingual embeddings. Depending on which model configuartion you would like to run, they may be useful:

##### Vecmap for mapping-based cross-lingual embeddings
To map embeddings to a shared space, apply https://github.com/artetxem/vecmap to the seperately learned embeddings

##### BPE
This [Github repository](https://github.com/rsennrich/subword-nmt) was used for generating BPE vocabulary.



# Information about the Cantonese Dataset 

We collected 910k monolingual Cantonese data, in addition to some parallel datasets. The scraping script can be found in `crawl.py` and an example can be found in `crawling_demo.py`. 
| Domain  | Source | Number of lines | Parallel|
| --------| ------ | --------------- |---------|
| wikipedia|Wikipedia|689234|NO|
|articles|handstopmouthstop.com|6531|NO|
|corpus|UD / John Lee corpus|c:1004 / m:1004|YES|
||HKCanCor|10801|NO|
||tatoeba|6244|NO|
|dictionary|kaifangcidian 開放詞典|c:13004 / m:13004|YES|
|reviews|openrice|78761|NO|
|subtitles|kongjisubtitles|77479|YES|
||youtube subtitles|1620|NO|

For data extracted from Instagram (all monolingual) via imginn.org: 
| Domain  | Source | Number of lines | Number of comments|
| --------| ------ | --------------- |-------------------|
|instagram non-news|afcdgovhk|698|255|
||cfs.hk1|2103|77|
||connect.card_hk|617|160|
||govnews.hk|1429|1113|
||hk.observatory|72|208|
||likemagazinehk|10031|3267|
||moov_music|9689|3333|
||t.expert|320|57|
||touchwoodtv|4752|1304|
|instagram news|smartpost hk|5026|4971|
||as1.entertainment|13784|20680|
||100most|37996|73102|
||nownewshk|369|40|
||onepao.hk|1719|33|

# Data and Pre-trained model:

Cantonese/Mandarin corpora: https://drive.google.com/drive/folders/13tWHQkv3MOxVZnz8bMhDOfl6OPSBI6rn?usp=sharing (train: monolingual, dev/test parallel)

Binarized training data: https://drive.google.com/drive/folders/1KCvj5UQmaLW7YgkLJQ-KCVoFTWMO7im6?usp=sharing

Pre-trained model: https://drive.google.com/drive/folders/1XUOht0kdUJPf3byd_5ODLyAhPEEAvvep?usp=sharing

To obtain the pretrained model, run:

```
 python3 main.py --exp_name test --transformer True --n_enc_layers 4 --n_dec_layers 4 --share_enc 3 --share_dec 3 --share_lang_emb True --share_output_emb True --langs 'can,man' --n_mono -1 --mono_dataset 'can:data_bin/mono/can.char.pth,,;man:data_bin/mono/man.char.pth,,' --para_dataset 'can-man:,data_bin/para/dev/dev.XX.pth,data_bin/para/test/test.XX.pth' --mono_directions 'can,man' --word_shuffle 3 --word_dropout 0.1 --word_blank 0.2 --pivo_directions 'man-can-man,can-man-can' --pretrained_emb 'data_bin/all.vec' --pretrained_out True --lambda_xe_mono '0:1,100000:0.1,300000:0' --lambda_xe_otfd 1 --otf_num_processes 30 --otf_sync_params_every 1000 --enc_optimizer adam,lr=0.0001 --epoch_size 500000 --stopping_criterion bleu_can_man_valid,10
 ```
 
 on https://github.com/facebookresearch/UnsupervisedMT (NMT)
