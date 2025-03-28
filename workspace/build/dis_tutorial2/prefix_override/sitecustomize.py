import sys
if sys.prefix == '/usr':
    sys.real_prefix = sys.prefix
    sys.prefix = sys.exec_prefix = '/home/kappa/RINS-kappa/workspace/install/dis_tutorial2'
