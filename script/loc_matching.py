# -*- coding: utf-8 -*-
"""
Created on Mon Apr 21 17:12:14 2014

@author: zhengchen
"""
import logging
import os
import re
import chinese_clean as cc
import time


logging.basicConfig(filename = os.path.join(os.getcwd(), 'log.'+time.strftime('%Y%m%d%H%M%S',time.localtime(time.time()))), level = logging.DEBUG,\
    filemode = 'w', format = '%(asctime)s - %(levelname)s: %(message)s') 

#dong = re.compile(ur"[\u680b\u5e62']")
dong = re.compile(ur"[栋幢]+")
brackets = re.compile(ur"(\(|（).+(\)|）)")
digit = re.compile(ur"[零一二三四五六七八九十百千万０１２３４５６７８９壹贰叁肆伍陆柒捌玖拾佰仟萬亿]+")


def load_jd_dict(filename):
    # county_id : addr
    result = {}
    # prov, city, district, county_id
    for line in open(filename).readlines():
        prov_id, prov, city_id, city, county_id, county, district_id, district = line.split('\t')
        result[county_id] = prov + city + county 
    return result


def load_yx_dict(filename):
    # sysno : county_id
    result = {}
    for line in open(filename).readlines():
        cons = line.strip().split('\t')
        if len(cons) == 7:
            result[cons[0]] = cons[6] 
        else:
            result[cons[0]] = 'cannot_find_countyid'
    return result


def extract_jd_user_loc(addr, county_id, jd_dict):
    county = jd_dict[county_id]
    if addr.startswith(county):
        addr = addr.decode('utf-8')[len(county.decode('utf-8')):]
    return addr

    
def split_locfile_2_idfile(filename, dim_dict, type):
    if type == 'jd':
        file_dict = dict([(key, open(type+'/'+key, 'a')) for key in dim_dict])
    elif type == 'yx':
        file_dict = dict([(key, open(type+'/'+dim_dict[key], 'a')) for key in dim_dict])
    # uid, addr, prov, city, county
    no_county_set = set()
    for line in open(filename).readlines():        
        uid, addr, phone, county_id = line.strip().split('\t')
        if county_id not in dim_dict: 
            no_county_set.add(county_id)
        else:
            if type == 'jd':
                addr = extract_jd_user_loc(addr, county_id, dim_dict)
            file_dict[county_id].write(uid+'\t'+clean(addr).encode('utf-8')+'\t'+phone+'\n')
    
    for key in file_dict: file_dict[key].close()
    # DEBUG 
    if len(no_county_set) > 0:
        _log_set(no_county_set)
        

def _log_set(id_set):
    logging.debug("The unmatched countyids: ")
    ids = ''
    for x in id_set: 
        ids += x
        ids += ' ' 
    logging.debug(ids)


def clean(line):
    if isinstance(line, str):
        line = line.decode('utf-8')
    # remove brackets
    line = brackets.sub('', line)
    # replace 栋 幢 by -
    line = dong.sub('-',line)   
    # replace Chinese numerals by Arabic numerals
    line = digit.sub(lambda m: cc.getResultForDigit(m.group(0)), line)
    
    return line


def split_loc(addr):
    addr = addr.strip(' ').decode('utf-8')
    key_words = [u'省',u'市',u'区',u'县',u'道',u'镇',u'乡',u'村',\
    u'庙',u'寺',u'苑',u'厦',u'里',u'弄',u'园',u'路',u'街',u'巷']#,u'号']
    # key_words + suffix
    key_words_num = len(key_words)
    # the value is '' if there is no keywords matching it.
    result = ['' for i in range(key_words_num + 1)]
    # [(key_words_index, addr_index)]
    index_list = []
    for key_words_index in range(key_words_num):
        addr_index = addr.find(key_words[key_words_index])
        # if the addr_index is the last word in addr, we will not put it into
        # the index_list. We consider the last part a particuler loc to match.
        if addr_index != -1 and addr_index != len(addr):
            index_list.append((key_words_index, addr_index))
    # sort by addr index
    index_list.sort(cmp=lambda x,y: x[1]-y[1])
    list_length = len(index_list)
    
    if list_length > 0:
        # the first keywords index map the 0 to the first addr index 
        result[index_list[0][0]] = addr[:index_list[0][1]+1]
        # the last keywords index map to the last addr index to end
        result[len(result)-1] = addr[index_list[list_length-1][1]+1:]
        for i in range(1, list_length):
            result[index_list[i][0]] = addr[index_list[i-1][1]+1:index_list[i][1]+1]
    return result
    
    
def is_same_loc(a, b):
    result = True
    flag = False
    la = len(a)
    a_num, b_num, same = 0, 0, 0
    for i in range(la):
        if a[i] != '': a_num += 1
        if b[i] != '': b_num += 1
        if a[i] != '' and b[i] !='' and i != la-1 and is_same_detail_loc(a[i], b[i]):
            flag = True 
            same += 1
        elif i == la-1: 
            if a[i] != '' and b[i] != '' and is_same_detail_loc(a[i], b[i]):
                same += 1
            else:
                result = False
        elif a[i] != '' and b[i] != '': 
            result = False
    num = a_num < b_num and a_num or b_num
    if num > 1 and same < int(num/2):
        result = False
    return result and flag

    
def is_same_detail_loc(a, b):
    # if a contains b or b contains a, then they are the same loc.
    la, lb = len(a), len(b)
    if la == lb:
        return a == b
    elif la > lb:
        return a.startswith(b)
    else:
        return b.startswith(a)
        

def _log_loc(x, type, cons):
    # just for debug
    logging.debug('======== '+type+' ==========')
    for r in x: 
        if r != '': logging.debug(r.encode('utf-8'))
    for c in cons:
        logging.debug(c)
 

def _log_loc_flag(x, type, cons, flag):
    # just for debug
    logging.debug('======== '+type+' ==========' + flag)
    for r in x: 
        if r != '': logging.debug(r.encode('utf-8'))
    for c in cons:
        logging.debug(c)
 
    
def match_loc(filename):
    jd, yx = [], []
    for line in open('jd/'+filename).readlines():
        cons = line.strip().split('\t')
        if len(cons) > 2:
            uid, addr, phone = cons[0], cons[1], cons[2]
            jd.append((uid, split_loc(addr), addr, phone))
    for line in open('yx/'+filename).readlines():
        cons = line.strip().split('\t')
        if len(cons) > 2:
            uid, addr, phone = cons[0], cons[1], cons[2]
            yx.append((uid, split_loc(addr), addr, phone))
    same = 0
    phone_num = 0
    logging.debug(' jd num: ' + str(len(jd)) + ' yx num: ' + str(len(yx)))
    for x in jd:
        for y in yx:         
            #'''
            if is_same_loc(x[1], y[1]):
                same += 1
                _log_loc(x[1],'jd', (x[2], x[3]))
                _log_loc(y[1],'yx', (y[2], y[3]))
                yx.remove(y)
                if x[3] == y[3]: phone_num += 1
                break
            '''
            if x[3] == y[3]:
                same += 1
                if is_same_loc(x[1], y[1]): 
                    phone_num += 1 
                    _log_loc_flag(x[1],'jd', (x[2], x[3]), 'locsame ')
                    _log_loc_flag(y[1],'yx', (y[2], y[3]), 'locsame ')
                else:
                    _log_loc(x[1],'jd', (x[2], x[3]))
                    _log_loc(y[1],'yx', (y[2], y[3]))
                yx.remove(y)
                break
            '''
    #logging.debug('match num: ' + str(same) + ' same phone in matched locs:' + str(phone_num))
    logging.debug('match num: ' + str(same) + ' same loc in matched phones:' + str(phone_num))


if __name__ == '__main__':
    ''' 
    logging.info('loading jd dim dict')
    jddim_dict = load_jd_dict('/data1/data/tmp/jddim.data')
    logging.info('loading yx dim dict')
    yxdim_dict = load_yx_dict('/data1/data/tmp/yxdim.data')
    logging.info('spliting jd loc files')
    split_locfile_2_idfile('/data1/data/tmp/jdloc.data', jddim_dict, 'jd')
    logging.info('spliting yx loc files')
    split_locfile_2_idfile('/data1/data/tmp/yxloc.data', yxdim_dict, 'yx')
    ''' 
    match_loc('893')
    #match_loc('2383')
