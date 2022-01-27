import gpt_2_simple as gpt2
from datetime import datetime

#1 RUN THIS LINE FIRST AND ONCE TO DOWNLOAD THE 355M MODEL
#gpt2.download_gpt2(model_name="355M")

#2 RUN THIS CODE AFTER TO TRAIN YOUR MODEL
file_name = "train.txt"
sess = gpt2.start_tf_sess()

gpt2.finetune(sess,
              dataset=file_name,
              model_name='355M',
              steps=-1,
              restore_from='fresh',
              run_name='doppelganger',
              print_every=10,
              sample_every=500,
              save_every=500
              )