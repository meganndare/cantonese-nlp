# cantonese-nlp
cantonese-mandarin unsupervised neural translation for sw project

To map embeddings to a shared space, apply https://github.com/artetxem/vecmap to the seperately learned embeddings

# BPE
I used this https://github.com/rsennrich/subword-nmt for BPE

Cantonese/Mandarin corpora: https://drive.google.com/drive/folders/13tWHQkv3MOxVZnz8bMhDOfl6OPSBI6rn?usp=sharing (train: monolingual, dev/test parallel)

Binarized training data: https://drive.google.com/drive/folders/1KCvj5UQmaLW7YgkLJQ-KCVoFTWMO7im6?usp=sharing

Pre-trained model: https://drive.google.com/drive/folders/1XUOht0kdUJPf3byd_5ODLyAhPEEAvvep?usp=sharing

To obtain the pretrained model, run:

 python3 main.py --exp_name test --transformer True --n_enc_layers 4 --n_dec_layers 4 --share_enc 3 --share_dec 3 --share_lang_emb True --share_output_emb True --langs 'can,man' --n_mono -1 --mono_dataset 'can:data_bin/mono/can.char.pth,,;man:data_bin/mono/man.char.pth,,' --para_dataset 'can-man:,data_bin/para/dev/dev.XX.pth,data_bin/para/test/test.XX.pth' --mono_directions 'can,man' --word_shuffle 3 --word_dropout 0.1 --word_blank 0.2 --pivo_directions 'man-can-man,can-man-can' --pretrained_emb 'data_bin/all.vec' --pretrained_out True --lambda_xe_mono '0:1,100000:0.1,300000:0' --lambda_xe_otfd 1 --otf_num_processes 30 --otf_sync_params_every 1000 --enc_optimizer adam,lr=0.0001 --epoch_size 500000 --stopping_criterion bleu_can_man_valid,10
 
 on https://github.com/facebookresearch/UnsupervisedMT (NMT)
