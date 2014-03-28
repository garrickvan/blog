#coding=utf-8
from common.des import DES

DES_KEY = '$aekx,a&'
des = DES()
des.input_key(DES_KEY)

def get_encode_num(num_str):
    '''
    Use DES to encode the db num
    '''
    return des.encode(str(num_str))

def get_decode_num(encode_str):
    '''
    Use Des to decode the encode num
    '''
    num = -1
    try:
        str = des.decode(encode_str)
        num = int(str)
    except :
        print encode_str + " is not the correct int."
    return num