import numpy as np

b64_corpus = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789+/'
# base_url = "http://mytinyurl.com/"
base_url =''

def get_url():
    rand_num = np.random.randint(0, len(b64_corpus), 6)
    str_ = ''.join([b64_corpus[i] for i in rand_num])
    return base_url+str_

