import sys
if sys.prefix == '/usr':
    sys.real_prefix = sys.prefix
    sys.prefix = sys.exec_prefix = '/home/strazi/FAKS/3.letnik/RINS/workspace/install/dis_tutorial2'
