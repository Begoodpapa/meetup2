import os

from comm.communication.helper import CommonItem, CommonDict
from ilcallmgmt_subsystem_lib import library
#### OS Env 
ENV = CommonItem()

ENV.HOSTIP = os.getenv('HOSTIP', '')
ENV.SRNC = os.getenv('HOSTIP', '')
ENV.DRNC = os.getenv('FGW2IP', '')
ENV.USERNAME = os.getenv('USERNAME', '')
ENV.PASSWD = os.getenv('PASSWD', '')
ENV.PORT = os.getenv('PORT', '')
ENV.FPCIP = os.getenv('FPCIP', '')
ENV.NODEBIP = os.getenv('FPCIP_ETH1', '')

ENV.RNC_IUB_IP = os.getenv('DSP0_IUB_IP', '')
ENV.RNC_IUR_IP = os.getenv('DSP0_IUR_IP', '')
ENV.RNC_IUCS_IP = os.getenv('DSP0_IUCS_IP', '')
ENV.RNC_IUPS_IP = os.getenv('DSP0_IUPS_IP', '')

#print 'ENV={%s}' % ENV
###########################################################################################
#### CM CALL MODEL ########################################################################
# CM VAR
CM_VAR = CommonItem()
CM_VAR.TESTDATA_PATH = '/home/public/SS_ILFT/TestData/NODEB'
#CM_VAR.USCP0 = os.getenv('USCP_TYPE_NAME', '') + '-' + os.getenv('USUP_0_INDEX', '')
#CM_VAR.CSCP0 = os.getenv('CSCP_TYPE_NAME', '') + '-' + os.getenv('CSUP_0_INDEX', '')
CM_VAR.USCP0 = 'USCP-0'
CM_VAR.CSCP0 = 'CSCP-0'

# CALL_MINIMAL
CALL_MIN = CommonItem()
CALL_MIN.comp = CM_VAR.USCP0
CALL_MIN.call_id = '0'
CALL_MIN.hand_id = '0'
CALL_MIN.subnet_id = ''
CALL_MIN.user_id = ''
CALL_MIN.legs = {}

# CALL_AMR
CALL_AMR = CALL_MIN
CALL_AMR.nodeb_ip = ENV.NODEBIP
CALL_AMR.nodeb_ip_hex = library.display_ipaddress(ENV.NODEBIP, 'dec2hex')
CALL_AMR.nodeb_port = '50000'
CALL_AMR.nodeb_port_hex = 'C350'
CALL_AMR.cn_ip = ENV.NODEBIP
CALL_AMR.cn_ip_hex = library.display_ipaddress(ENV.NODEBIP, 'dec2hex')
CALL_AMR.cn_port = '60000'
CALL_AMR.cn_port_hex = 'EA60'
CALL_AMR.rnc_ip_hex = ''
CALL_AMR.hsdpa_port = '10000'
CALL_AMR.hsdpa_port_hex = '2710'

# CALL_PS
CALL_PS = CALL_MIN
CALL_PS.nodeb_ip = ENV.NODEBIP
CALL_PS.nodeb_ip_hex = library.display_ipaddress(ENV.NODEBIP, 'dec2hex')
CALL_PS.nodeb_port = '50000'
CALL_PS.nodeb_port_hex = 'C350'
CALL_PS.cn_ip = ENV.NODEBIP
CALL_PS.cn_ip_hex = library.display_ipaddress(ENV.NODEBIP, 'dec2hex')
CALL_PS.cn_port = '60000'
CALL_PS.cn_port_hex = 'EA60'
CALL_PS.rnc_ip_hex = ''
CALL_PS.hsdpa_port = '10000'
CALL_PS.hsdpa_port_hex = '2710'

# CALL_MODEL
CM_MODEL = CommonItem()
CM_MODEL.comp = CM_VAR.USCP0
CM_MODEL.call_id = '0'
CM_MODEL.hand_id = '0'
CM_MODEL.subnet_id = ''
CM_MODEL.user_id = ''
CM_MODEL.nodeb_ip = ENV.NODEBIP
CM_MODEL.nodeb_ip_hex = library.display_ipaddress(ENV.NODEBIP, 'dec2hex')
CM_MODEL.nodeb_port = '50000'
CM_MODEL.nodeb_port_hex = 'C350'
CM_MODEL.cn_ip = ENV.NODEBIP
CM_MODEL.cn_ip_hex = library.display_ipaddress(ENV.NODEBIP, 'dec2hex')
CM_MODEL.cn_port = '60000'
CM_MODEL.cn_port_hex = 'EA60'
CM_MODEL.rnc_ip_hex = ''
CM_MODEL.hsdpa_port = '10000'
CM_MODEL.hsdpa_port_hex = '2710'

CM_MODEL.legs = {}


# CALL
CM_BASE_CALL = CommonItem()
CM_BASE_CALL.comp = CM_VAR.USCP0
CM_BASE_CALL.call_id = '0'
CM_BASE_CALL.hand_id = '0'
CM_BASE_CALL.subnet_id = ''
CM_BASE_CALL.user_id = ''
CM_BASE_CALL.nodeb_ip = ENV.NODEBIP
CM_BASE_CALL.nodeb_ip_hex = library.display_ipaddress(ENV.NODEBIP, 'dec2hex')
CM_BASE_CALL.nodeb_port = '50000'
CM_BASE_CALL.nodeb_port_hex = 'C350'
CM_BASE_CALL.cn_ip = ENV.NODEBIP
CM_BASE_CALL.cn_ip_hex = library.display_ipaddress(ENV.NODEBIP, 'dec2hex')
CM_BASE_CALL.cn_port = '60000'
CM_BASE_CALL.cn_port_hex = 'EA60'
#CM_BASE_CALL.rnc_ip = library.get_interface_ip('ether1_1', )
CM_BASE_CALL.rnc_ip_hex = ''
CM_BASE_CALL.hsdpa_port = '10000'
CM_BASE_CALL.hsdpa_port_hex = '2710'
CM_BASE_CALL.dsp = ''

CM_BASE_CALL.legs = {}

CM_VAR.CM_BASE_CALL = CM_BASE_CALL
#print 'CM_BASE_CALL={%s}' % CM_BASE_CALL

# TRAFFIC
CM_BASE_TRAFFIC = CM_BASE_CALL
CM_BASE_TRAFFIC.reply_ip = ENV.NODEBIP
CM_BASE_TRAFFIC.reply_port = '30000'
CM_BASE_TRAFFIC.src_file = CM_VAR.TESTDATA_PATH + '/udp_src'
CM_BASE_TRAFFIC.dst_file = CM_VAR.TESTDATA_PATH + '/udp_recvfile'

CM_BASE_TRAFFIC.drnc_ip = ENV.DRNC
CM_BASE_TRAFFIC.drnc_ip_hex = ''
CM_BASE_TRAFFIC.drnc_port = ''
CM_BASE_TRAFFIC.drnc_port_hex = ''

CM_VAR.CM_BASE_TRAFFIC = CM_BASE_TRAFFIC
#print 'CM_VAR.CM_BASE_TRAFFIC={%s}' % CM_BASE_TRAFFIC

CM_BASE_HSDPA = CM_BASE_CALL
CM_BASE_HSDPA.sgsn_ip = ENV.NODEBIP
CM_BASE_HSDPA.sgsn_ip_hex = library.display_ipaddress(ENV.NODEBIP, 'dec2hex')
CM_BASE_HSDPA.sgsn_port = '2152'
CM_BASE_HSDPA.sgsn_port_hex = '868'
CM_BASE_HSDPA.teid = '8'
CM_BASE_HSDPA.dl_udp_port = '2459'
CM_BASE_HSDPA.dl_udp_port_hex = '99b'
CM_BASE_HSDPA.ul_udp_port = '2459'
CM_BASE_HSDPA.ul_udp_port_hex = '99b'

CM_BASE_HSDPA.drnc_ip = ENV.DRNC
CM_BASE_HSDPA.drnc_ip_hex = ''
CM_BASE_HSDPA.drnc_port = ''
CM_BASE_HSDPA.drnc_port_hex = ''

CM_BASE_HSDPA.serv_id = '0'

CM_VAR.CM_BASE_HSDPA = CM_BASE_HSDPA

#HSUPA

CM_VAR.CM_BASE_HSUPA = CM_BASE_HSDPA
CM_VAR.CM_PS_CALL = CM_BASE_HSDPA

#HSUPA

CM_VAR.CM_BASE_HSUPA = CM_BASE_HSDPA
###########################################################################################

#Standard Definition
SRB_STANDARD = CommonItem()
SRB_STANDARD.leg_num = '1'
SRB_STANDARD.service_num = '1'
SRB_STANDARD.conn_num = '1'
CM_VAR.SRB_STANDARD = SRB_STANDARD

AMR_STANDARD = CommonItem()
AMR_STANDARD.leg_num = '2'
AMR_STANDARD.service_num = '1'
AMR_STANDARD.conn_num = '2'
CM_VAR.AMR_STANDARD = AMR_STANDARD

#/proc/dmxmsg/comp_addr_tbl 
comp_addr_tbl = {
'OMU': ['0002', '4002', '8003', '0010', '1FFF'],
'CFCP': ['0147', '444C', '8004', '0110', '1FFF'],
'CSCP_GROUP': ['0149', '444E', '8009', '1FFF', '1FFF'],
'CSCP_UNIT': ['0149', '444F', '0210', '0210', '1FFF'],
'CSUP_GROUP': ['0124', '4AAD', '800A', '1FFF', '1FFF'],
'CSUP_UNIT': ['0124', '4AAE', '1310', '1310', '1FFF'],
'USCP_GROUP': ['0125', '4ADA', '800B', '1FFF', '1FFF'],
'USCP_UNIT': ['0125', '4ADB', '0410', '0410', '1FFF'],
'USUP_GROUP': ['0126', '4B1B', '800C', '1FFF', '1FFF'],
'USUP_UNIT': ['0126', '4B1C', '1510', '1510', '1FFF'],
'EITP': ['0127', '4B5D', '800D', '1710', '1FFF'],
'EITPProxy': ['0128', '4B6E', '800F', '0910', '1FFF'],
'NONE': ['00FD', '4FFE', '0E10', '0E10', '1FFF']
}

#Stubs
STUB = CommonItem()
STUB.path = "/home/public/SS_ILFT/Testenv/FPC/"
STUB.udp_recv = STUB.path + "udpreceive"
STUB.udp_send = STUB.path + "udpsend"
STUB.gtp_recv = STUB.path + "udpreceive"
STUB.gtp_send = STUB.path + "udpsend"

STUB.udp_temp_files = "/home/public/SS_ILFT/TestData/NODEB/udp_recvfile*"
STUB.src_file = "/home/public/SS_ILFT/TestData/NODEB/udp_src"

STUB.gtp_nodeb_src_file = "/home/public/SS_ILFT/TestData/NODEB/gtpu"
STUB.gtp_nodeb_recv_path = "/home/public/SS_ILFT/TestData/NODEB/fp_recv_file/"
STUB.gtp_nodeb_temp_files = "/home/public/SS_ILFT/TestData/NODEB/fp_recv_file/*"
STUB.gtp_nodeb_svn_temp_files = "/home/public/SS_ILFT/TestData/NODEB/fp_recv_file/.svn"

STUB.gtp_sgsn_src_file = "/home/public/SS_ILFT/TestData/SGSN/gtpu"
STUB.gtp_sgsn_recv_path = "/home/public/SS_ILFT/TestData/SGSN/gtp_recv_file/"
STUB.gtp_sgsn_temp_files = "/home/public/SS_ILFT/TestData/SGSN/gtp_recv_file/*"
STUB.gtp_sgsn_svn_temp_files = "/home/public/SS_ILFT/TestData/SGSN/gtp_recv_file/.svn"
