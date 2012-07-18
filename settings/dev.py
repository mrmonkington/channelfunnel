from defaults import *

DEBUG = True
TEMPLATE_DEBUG = DEBUG
MEDIA_DEV_MODE = DEBUG

# Make this unique, and don't share it with anybody.
SECRET_KEY = '_swm&p9m^07^c&z6b_x9o71cuttp%)*4!nqplkgsm3q4(6s68e'

ADMINS = (
    ('Mark Kennedy', 'mark@eurogamer.net'),
)

MANAGERS = ADMINS

class CIDR_LIST(list):
    def __init__(self, cidrs):
        self.cidrs = []
        try:
            #http://cheeseshop.python.org/pypi/IPv4_Utils/0.35
            import ipv4
            for cidr in cidrs:
                self.cidrs.append(ipv4.CIDR(cidr))
        except ImportError:
            pass
    def __contains__(self, ip):
        import ipv4
        try:
            for cidr in self.cidrs:
                if ipv4.CIDR(ip) in cidr:
                    return True
        except:
            pass
        return False

INTERNAL_IPS = (
    '10.0.0.0/16',
    '192.168.0.0/16',
)

