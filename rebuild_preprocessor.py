"""
Run this script to rebuild feature_extractor.pkl from scratch.
Use Python 3.12 (matching HF Space environment).
"""
import joblib
import pandas as pd
from feature_extraction import NIDSFeaturePreprocessor

preprocessor = NIDSFeaturePreprocessor()

# All known values from UNSW-NB15 dataset for proto, service, state
protos = [
    'tcp', 'udp', 'arp', 'ospf', 'icmp', 'igmp', 'rtp', 'ddp',
    'ipv6-frag', 'cftp', 'wsn', 'pvp', 'wb-expak', 'mtp', 'pri-enc',
    'sat-expak', 'idrp', 'zero', 'netblt', 'mfe-nsp', 'merit-inp',
    'dccp', 'rsvp', '3pc', 'idpr', 'xtp', 'rdp', 'irtp', 'iso-tp4',
    'sctp', 'swipe', 'narp', 'mobile', 'tlsp', 'skip', 'ipv6-nonxt',
    'ipv6-opts', 'any', 'unas', 'pim', 'ipcomp', 'vrrp', 'l2tp',
    'isis', 'etherip', 'encap', 'aris', 'fcoe', 'udt'
]

services = [
    '-', 'http', 'ftp', 'smtp', 'ssh', 'dns', 'ftp-data', 'irc',
    'pop3', 'snmp', 'ssl', 'dhcp', 'radius', 'vnc', 'bgp', 'mdns',
    'kerberos', 'sip', 'ldap', 'mysql', 'mssql', 'rdp'
]

states = [
    'FIN', 'INT', 'CON', 'REQ', 'RST', 'CLO', 'ECO', 'URN',
    'no', 'ACC', 'NRS', 'STA', 'TST', 'MAS', 'TXD', 'PAR', 'URP'
]

# Pad all lists to the same length
max_len = max(len(protos), len(services), len(states))
protos   += [protos[-1]]   * (max_len - len(protos))
services += [services[-1]] * (max_len - len(services))
states   += [states[-1]]   * (max_len - len(states))

sample_data = pd.DataFrame({
    'proto':   protos,
    'service': services,
    'state':   states
})

preprocessor.fit(sample_data)
joblib.dump(preprocessor, 'feature_extractor.pkl')

print('feature_extractor.pkl rebuilt successfully')
print('proto categories: ', list(preprocessor.encoder.categories_[0]))
print('service categories:', list(preprocessor.encoder.categories_[1]))
print('state categories:  ', list(preprocessor.encoder.categories_[2]))
