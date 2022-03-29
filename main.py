import ScannerService
from ScannerService.GPSAPI import GPSAPI
import os

keys = []
with open(os.path.join(os.getcwd(),"gps_keys.txt")) as f:
    for line in f:
        keys.append(line.strip())

gps = GPSAPI(keys)
res = gps.scanAppData(['net.osmand'])
print(res)


