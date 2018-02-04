#!/usr/bin/python

import re
from string import atoi
from robot.libraries.BuiltIn import BuiltIn

msg_re = re.compile('MONITOR.*?\n\n', re.M|re.S)

recv_name_list = ['computer', 'family', 'process']
bottom_name_list = ['computer', 'family', 'process', 'focus', 'control', 'hop_count', 'error_code', 'sequence_number', 'phys_computer', 'trace_hop_limit', 'bottom_flag', 'filler', 'filler2']
msg_name_list = ['length', 'computer', 'family', 'process', 'focus', 'attributes', 'group', 'number', 'phys_computer']
msg_data_list = ['data0', 'data1', 'data2', 'data3', 'data5']
msg_time_list = ['date', 'time', 'date_time']
recv_re = re.compile("MONITORING TIME: (\S+)    (\S+).*?\nRECEIVED BY: (\S+) (\S+) (\S+)\nBOTTOM: (\S+) (\S+) (\S+) (\S+) (\S+) (\S+) (\S+) (\S+) (\S+) (\S+) (\S+) (\S+) (\S+)\nMONITORED MESSAGE: (\S+) (\S+) (\S+) (\S+) (\S+) (\S+) (\S+) (\S+) (\S+)\n(.*)")
sent_re = re.compile("MONITORING TIME: (\S+)    (\S+).*?\nSENT BY: (\S+) (\S+) (\S+)\nBOTTOM: (\S+) (\S+) (\S+) (\S+) (\S+) (\S+) (\S+) (\S+) (\S+) (\S+) (\S+) (\S+) (\S+)\nMONITORED MESSAGE: (\S+) (\S+) (\S+) (\S+) (\S+) (\S+) (\S+) (\S+) (\S+)\n(.*)")
arrv_re = re.compile("MONITORING TIME: (\S+)    (\S+).*?\nARRIVED TO: (\S+) (\S+) (\S+)\nBOTTOM: (\S+) (\S+) (\S+) (\S+) (\S+) (\S+) (\S+) (\S+) (\S+) (\S+) (\S+) (\S+) (\S+)\nMONITORED MESSAGE: (\S+) (\S+) (\S+) (\S+) (\S+) (\S+) (\S+) (\S+) (\S+)\n(.*)")
enter_int_re   = re.compile("MONITORING TIME: (\S+)    (\S+).*?\nENTER INT: (\S+) (\S+) (\S+)\nBOTTOM: (\S+) (\S+) (\S+) (\S+) (\S+) (\S+) (\S+) (\S+) (\S+) (\S+) (\S+) (\S+) (\S+)\nMONITORED MESSAGE: (\S+) (\S+) (\S+) (\S+) (\S+) (\S+) (\S+) (\S+) (\S+)\n(.*)")
enter_ioctl_re = re.compile("MONITORING TIME: (\S+)    (\S+).*?\nENTER IOCTL: (\S+) (\S+) (\S+)\nBOTTOM: (\S+) (\S+) (\S+) (\S+) (\S+) (\S+) (\S+) (\S+) (\S+) (\S+) (\S+) (\S+) (\S+)\nMONITORED MESSAGE: (\S+) (\S+) (\S+) (\S+) (\S+) (\S+) (\S+) (\S+) (\S+)\n(.*)")
exit_ioctl_re  = re.compile("MONITORING TIME: (\S+)    (\S+).*?\nEXIT IOCTL: (\S+) (\S+) (\S+)\nBOTTOM: (\S+) (\S+) (\S+) (\S+) (\S+) (\S+) (\S+) (\S+) (\S+) (\S+) (\S+) (\S+) (\S+)\nMONITORED MESSAGE: (\S+) (\S+) (\S+) (\S+) (\S+) (\S+) (\S+) (\S+) (\S+)\n(.*)")
data_re = re.compile("(\S+) (\S+) (\S+) (\S+) (.*)")
# sample msg
sample_msg = {'bottom': {'bottom_flag': 0,
            'computer': 49152,
            'control': 0,
            'error_code': 0,
            'family': 41000,
            'filler': 0,
            'filler2': 0,
            'focus': 0,
            'hop_count': 0,
            'phys_computer': 1792,
            'process': 0,
            'sequence_number': 20835,
            'trace_hop_limit': 0},
 'data': '00 0F 00 00 00 00',
 'msg': {'attributes': 19,
         'computer': 49152,
         'family': 160,
         'focus': 0,
         'group': 0,
         'length': 22,
         'number': 1,
         'phys_computer': 1792,
         'process': 1},
 'recv': {'family': 41000, 'process': 0, 'focus': 0},
 'time': {'date':'2012-04-18', 'time':'17:29:16.171185', 'date_time': '2012-04-18 17:29:16.171185'},
 'type': 'recv'}


def _convert_number(number):
    if type(number) != type(100):
        if number.lower().count('0x') == 1:
            num = int(number,16)
        else:
            num = int(number)
    else:
        num = number
    print number, num
    return num

def convert_time(date,time):
    """This keyword is to convert time from string date and time

    #COMMAND: convert_time(date, time)
    | Parameters        | Man. | Description                       |
    | date              | Yes  | date string like 2012-04-20       |
    | time              | Yes  | time string like 07:53:14.953785     |
       
    | Return value | command execution result |
    
    Example 
    | ${result} | convert time | date | time |
    """
    t = time.split('.')
    print 't=',t
    import time, datetime
    time_list = list(time.strptime(date + ' ' + t[0], '%Y-%m-%d %H:%M:%S')[0:6])
    print 'time_list1=',time_list
    time_list.append(int(t[1][0:6]))
    print 'time_list2=',time_list
    print 'time_list[0:7]',time_list[0:7]
    dtime = datetime.datetime(*time_list[0:7])
    return dtime

def get_msg_from_buf(buf):
    buf = buf+"\n\n"
    return msg_re.findall(buf.replace('\r\n', '\n'))

# This function will parse only one msg from raw input string.
def parse_msg(raw):
    type = ''
    m1 = sent_re.match(raw)
    if type == '' and m1:
        type = 'sent'
        m = m1
    if type == '':
        m1 = recv_re.match(raw)
        if m1:
            type = 'recv'
            m = m1
    if type == '':
        m1 = arrv_re.match(raw)
        if m1:
            type = 'arrv'
            m = m1
    if type == '':
        m1 = enter_int_re.match(raw)
        if m1:
            type = 'enter_int'
            m = m1
    if type == '':
        m1 = enter_ioctl_re.match(raw)
        if m1:
            type = 'enter_ioctl'
            m = m1
    if type == '':
        m1 = exit_ioctl_re.match(raw)
        if m1:
            type = 'exit_ioctl'
            m = m1
    
    if type == '':
        return None
    
    l = m.groups()
    mon_msg = {'type' : type}
    d = {}
    offset = 0
    for i in range(len(msg_time_list)):
        if i == len(msg_time_list) - 1:
            d[msg_time_list[i]] = convert_time(l[offset + i - 2], l[offset + i - 1])
        else:
            d[msg_time_list[i]] = l[offset + i]
 
    mon_msg['time'] = d

    d = {}
    offset += len(msg_time_list) - 1
    for i in range(len(recv_name_list)):
        d[recv_name_list[i]] = int(l[offset + i], base=16)
    mon_msg[type] = d

    d = {}
    offset += len(recv_name_list)
    for i in range(len(bottom_name_list)):
        d[bottom_name_list[i]] = int(l[offset + i], base=16)
    mon_msg['bottom'] = d

    d = {}
    offset += len(bottom_name_list)
    for i in range(len(msg_name_list)):
        d[msg_name_list[i]] = int(l[offset + i], base=16)
    mon_msg['msg'] = d
      
    offset += len(msg_name_list)
    mon_msg['data'] = l[offset]
    
    return mon_msg

def get_msg_list(msg_buf):
    l = get_msg_from_buf(msg_buf)
    msg_list = [parse_msg(i) for i in l]
    return msg_list

def get_msgs_by_id(msg_list, number, type='all'):
    l = []
    num = _convert_number(number)
    print num
    for msg in msg_list:
        if msg is None:
            continue
        if msg['msg']['number'] == num:
            if type == 'all':
                l.append(msg)
            elif msg['type'] == type:
                l.append(msg)
    return l

def get_msgs_by_type(msg_list, type):
    l = []
    for msg in msg_list:
        if msg['type'] == type:
            l.append(msg)
    return l
	
#===================================add for monster testing===================
	
def get_msgs_by_family(msg_list, family,type):
    l = []
    family_id = _convert_number(family)
    for msg in msg_list:
        if msg['msg']['family'] == family_id:
            if type == 'all':
                l.append(msg)
            elif msg['type'] == type:
                l.append(msg)
    return l

def get_msgs_by_family_with_type(msg_list, family,type):
    l = []
    for msg in msg_list:
        if msg['type'] == type:
            if msg['bottom']['family'] == atoi(family):
                l.append(msg)
        elif type == 'all':
            if msg['msg']['family'] == atoi(family) or msg['bottom']['family'] == atoi(family):
                l.append(msg)
    return l

def get_msgs_by_id_and_family(msg_list, number, family, type):
    l = []
    num = _convert_number(number)
    family_id = _convert_number(family)
    for msg in msg_list:
        if msg['msg']['number'] == num:
            if msg['msg']['family'] == family_id:
                if type == 'all':
                    l.append(msg)
                elif msg['type'] == type:
                    l.append(msg)
    return l


def get_msgs_by_data(msg_list, data, type):
    l = []
    i=0
    data_tmp = data.split()
    for msg in msg_list:
        str1 = msg['data']
        result = str1.split()
        if len(result) > 1:
            if msg['type'] == type:
                if result[1] == data_tmp[1]:
                    print result[1]
                    print i
                    i=i+1
                    l.append(msg)
    return l


#=============================================================================

def check_message_data_equal(msg_list1, msg_list2):
    for i in range(len(msg_list1)):
         if msg_list1[i]['data'] != msg_list2[i]['data']:
            print msg_list1[i]['data']+'!='+msg_list2[i]['data']
            return 'failure'
    return 'success'
	
def check_msg(sample, target):
    if type(sample) != dict or type(target) != dict:
        return False
    
    for s_key in sample:
        if s_key not in target:
            return False
        if type(sample[s_key]) != type(target[s_key]):
            return False
        
        if type(sample[s_key]) != dict:
            return sample[s_key] == target[s_key]
        
        for i_key in sample[s_key]:
            if i_key not in target[s_key]:
                return False
            if sample[s_key][i_key] != target[s_key][i_key]:
                return False
            
    return True

if __name__ == '__main__':
    print 'Do unit test for parse monster msg script.'
    raw = '''MONITORING TIME: 2010-04-01    14:57:48.909322    000DE00A 4BB4B460
RECEIVED BY: 0391 0000 00
BOTTOM: C000 0391 0000 00 00 00 00 B95B 0700 00 00 0000 00000000
MONITORED MESSAGE: 0016 C000 00A0 0001 00 13 0000 0001 0700
00 0F 00 00 00 00 

MONITORING TIME: 2010-04-01    14:57:48.910125    000DE32D 4BB4B460
SENT BY: 0391 0000 00
BOTTOM: C000 0391 0000 00 00 00 00 B95B 0700 00 00 0000 00000000
MONITORED MESSAGE: 0016 C000 00A0 0001 00 11 0000 0002 0700
00 0F 00 00 00 00

MONITORING TIME: 2010-04-01    14:57:48.920125    000DE32D 4BB4B462
ENTER_INT: 0391 0000 00
BOTTOM: C000 0391 0000 00 00 00 00 B95B 0700 00 00 0000 00000000
MONITORED MESSAGE: 0016 C000 00A0 0001 00 11 0000 0002 0700
00 0F 00 00 00 00

MONITORING TIME: 2010-04-01    14:57:48.922125    000DE32D 4BB4B46A
ENTER_IOCTL: 0391 0000 00
BOTTOM: C000 0391 0000 00 00 00 00 B95B 0700 00 00 0000 00000000
MONITORED MESSAGE: 0016 C000 00A0 0001 00 11 0000 0002 0700
00 0F 00 00 00 00

MONITORING TIME: 2010-04-01    14:57:48.930125    000DE32D 4BB4B46A
EXIT_IOCTL: 0391 0000 00
BOTTOM: C000 0391 0000 00 00 00 00 B95B 0700 00 00 0000 00000000
MONITORED MESSAGE: 0016 C000 00A0 0001 00 11 0000 0002 0700
00 0F 00 00 00 00



MONITORING TIME: 2010-04-01    14:57:51.933285    000E3DA5 4BB4B46F
RECEIVED BY: 0391 0000 00
BOTTOM: C000 0391 0000 00 00 00 00 B98A 0700 00 00 0000 00000000
MONITORED MESSAGE: 0016 C000 00A0 0001 00 13 0000 0001 0700
00 0F 00 00 00 00 

MONITORING TIME: 2010-04-01    14:57:51.934091    000E40CB 4BB4B46F
SENT BY: 0391 0000 00
BOTTOM: C000 0391 0000 00 00 00 00 B98A 0700 00 00 0000 00000000
MONITORED MESSAGE: 0016 C000 00A0 0001 00 11 0000 0002 0700
00 0F 00 00 00 00 

MONITORING TIME: 2010-04-01    14:57:54.957225    000E9B29 4BB4B472
RECEIVED BY: 0391 0000 00
BOTTOM: C000 0391 0000 00 00 00 00 B9BC 0700 00 00 0000 00000000
MONITORED MESSAGE: 0016 C000 00A0 0001 00 13 0000 0001 0700
00 0F 00 00 00 00 

MONITORING TIME: 2010-04-01    14:57:54.958025    000E9E49 4BB4B472
SENT BY: 0391 0000 00
BOTTOM: C000 0391 0000 00 00 00 00 B9BC 0700 00 00 0000 00000000
MONITORED MESSAGE: 0016 C000 00A0 0001 00 11 0000 0002 0700
00 0F 00 00 00 00 
'''

    l = get_msg_from_buf(raw)
    print len(l)
    
    #assert len(l) == 6
    m_l = [parse_msg(i) for i in l]
    #assert len(m_l) == 6
    #assert len(get_msgs_by_family(m_l,0x00A0,type='all'))==6
    assert len(get_msgs_by_family(m_l,0x00A0,type='recv')) == 3
    assert len(get_msgs_by_id_and_family(m_l,1,0x00A0,type='recv')) == 3
    assert len(get_msgs_by_data(m_l,'00 0F 00 00 00 00','recv')) == 3
    assert len(get_msgs_by_id(m_l,2)) == 3
    assert len(get_msgs_by_family(m_l, 160)) >= 0
    assert len(get_msgs_by_id(m_l, 1)) == 3
    assert len(get_msgs_by_id(m_l, 2, type='recv')) == 0
    assert len(get_msgs_by_id(m_l, 2, type='sent')) == 3
    assert len(get_msgs_by_id(m_l, 1, type='sent')) == 0
    assert len(get_msgs_by_id(m_l, 1, type='recv')) == 3
    assert len(get_msgs_by_id(m_l, 2, type='enter_int')) == 1
    assert len(get_msgs_by_id(m_l, 2, type='enter_ioctl')) == 1
    assert len(get_msgs_by_id(m_l, 2, type='exit_ioctl')) == 1

    msg = m_l[0]
    assert check_msg({'msg': {'number': 1}}, msg) == True
    assert check_msg({'msg': {'number': 111}}, msg) == False
    assert check_msg({'msg': {'number': 1, 'computer': 0xC000, 'family': 0xA0},
                      'bottom': {'phys_computer': 0x0700}}, msg) == True
    
    print 'Unit test case passed.'
    
