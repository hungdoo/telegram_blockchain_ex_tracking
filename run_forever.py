#!/usr/bin/python
# 

from subprocess import Popen
import sys, time
from logger import get_logger
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--py", type=str, help="Python application file")
parser.add_argument("--go", type=str, help="Golang application file")
parser.add_argument("-i", "--interval", type=int, default=5, help="Wait interval before restarting")
args = parser.parse_args()

logg = get_logger('ws_trade')

try:
    logg.info("Run Forever: Starting {} and {}".format(args.py, args.go))
    p_go = Popen("./" + args.go, shell=True)
    time.sleep(2)
    p_py = Popen("python " + args.py, shell=True)
    while True:
        if p_py.poll():
            logg.info('Restart Python app')
            p_py = Popen("python " + args.py, shell=True)
        if p_go.poll():
            logg.info('Restart Go app')
            p_go = Popen("./" + args.go, shell=True)

        time.sleep(args.interval)

except KeyboardInterrupt as e:
    logg.warning('Run Forever: KeyboardInterrupt. Terminate proc {} & {}'.format(p_py.pid, p_go.pid))
    p_py.kill()
    p_py.terminate()
    p_py.wait()
    p_go.kill()
    p_go.terminate()
    p_go.wait()
    logg.warning('Run Forever: KeyboardInterrupt. Proc terminated {} & {}'.format(p_py.pid, p_go.pid))

    sys.exit(0)