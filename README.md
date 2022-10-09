# cantonese-nlp
cantonese-mandarin unsupervised neural translation for sw project

# REMEMBER TO "git pull" BEFORE "git push" PLZ

To map embeddings to a shared space, apply https://github.com/artetxem/vecmap to the seperately learned embeddings

# BPE
I used this [Github repository](https://github.com/rsennrich/subword-nmt) for BPE

# Cantonese data 

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

