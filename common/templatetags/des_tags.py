# coding=utf-8
from common.des_tool import get_decode_num, get_encode_num
from django import template

register = template.Library()

@register.filter(name='get_encode_id')
def get_encode_id(id):
    return get_encode_num(id)

@register.filter(name='get_decode_id')
def get_decode_id(encode_str):
    return get_decode_num(encode_str)