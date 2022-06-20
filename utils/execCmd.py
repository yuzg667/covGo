import os
import sys
from utils.logs import MyLog

def execCmd(cmd):
    MyLog.info(f"ExecCmd start: {cmd}")
    pingaling = os.popen(cmd,"r")
    while 1:
        line = pingaling.readline()
        if not line: break
        MyLog.info(line)
        sys.stdout.flush()
        # pingaling.close()
    MyLog.info(f"ExecCmd end: {cmd}")

# os.chdir("D:\work_space\simple-go-server")
# execCmd("diff-cover merge.xml --compare-branch=ae4b318d245d7fe463f3e69f9a866c47cab0db44 --html-report report33.html")


