import sys
if sys.prefix == '/usr':
    sys.real_prefix = sys.prefix
    sys.prefix = sys.exec_prefix = '/home/thelegend442/faxic/RINS-kappa/install/dis_tutorial2'
