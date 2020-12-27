import numpy as np
b62_corpus = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
# base_url = "http://mytinyurl.com/"
base_url =''

def get_url():
    rand_num = np.random.randint(0, len(b62_corpus), 6)
    str_ = ''.join([b62_corpus[i] for i in rand_num])
    return base_url+str_

