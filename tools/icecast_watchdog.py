#!python

import yaml
import sys
import argparse
from time import sleep
from icecast.iceserver import IceServer
import dbus

parser = argparse.ArgumentParser(description="Monitor an Icecast stream and restart")

parser.add_argument('-c', '--config-file',
                    default='../web/app/djrq/config.yaml',
                    help='The DJRQ2 config file to use for site information')
parser.add_argument('--ice-server',
                    #default='192.168.68.114',
                    default="eldrad.local",
                    help='The Icecast server to watch')
parser.add_argument('--ice-relay-port',
                    default='8000',
                    help='Icecast relay port')
parser.add_argument('--autodj-mount-point', default='autodj',
                    help='The AutoDJ mount point')
parser.add_argument('-p', '--listen-mount-points', default='listen',
                    help='Comma separated list of DJ mount points to watch')

args = parser.parse_args()

sysbus = dbus.SystemBus()
systemd1 = sysbus.get_object('org.freedesktop.systemd1', '/org/freedesktop/systemd1')
manager = dbus.Interface(systemd1, 'org.freedesktop.systemd1.Manager')

with open(args.config_file) as f:
    config = yaml.safe_load(f)

iceuri = f"http://{args.ice_server}:{args.ice_port}/status-json.xsl"
errorlog = "errors.txt"
djlist = DJList(config, args.site, args.use_ssl)
le = LocaleExtension() # For now, default to english
djlist.close_db()
le.prepare(djlist.context)
djs = djlist.djs

iserv = IceServer(args=args)
try:
    iserv.get()
except:
    print('Unable to contact the IceCast server')

while True:
    active_source = iserv.now_playing()
    if active_source is None:
        print('Restart AutoDJ')
    sleep(10)
