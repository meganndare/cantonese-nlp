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

We collected 910k monolingual Cantonese data, in addition to some parallel datasets. 
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

