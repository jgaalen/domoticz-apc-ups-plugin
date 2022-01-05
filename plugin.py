#!/usr/bin/env python
"""
APC UPS Monitoring
"""
"""
<plugin key="APCUPS" name="APC UPS" version="0.1" author="Joerek van Gaalen">
    <params>
        <param field="Address" label="Your APC UPS Address" width="200px" required="true" default="127.0.0.1"/>
        <param field="Port" label="Port" width="40px" required="true" default="3551"/>
        <param field="Mode1" label="Reading Interval (sec)" width="40px" required="true" default="10" />
        <param field="Mode2" label="apcaccess path" width="200px" required="true" default="/sbin/apcaccess" />
    </params>
</plugin>
"""

import Domoticz
import subprocess	#For OS calls

values = {
    'STATUS': {'dname': 'Status', 'dunit': 1, 'dtype':243, 'dsubtype':19},
    'LINEV': {'dname': 'Line voltage', 'dunit': 2, 'dtype':243, 'dsubtype':8},
    'LOADPCT': {'dname': 'Load percentage', 'dunit': 3, 'dtype':243, 'dsubtype':6},
    'BCHARGE': {'dname': 'Battery charge level', 'dunit': 4, 'dtype':243, 'dsubtype':6},
}

def onStart():
    Domoticz.Log("Domoticz APC UPS plugin start")

    if len(Devices) == 0:
        for key in values:
            Domoticz.Device(Name=values[key]['dname'], Unit=values[key]['dunit'], Type=values[key]['dtype'], Subtype=values[key]['dsubtype'], Used=1).Create()

    Domoticz.Heartbeat(int(Parameters["Mode1"]))

def onHeartbeat():
    try:
        res = str(subprocess.check_output([Parameters["Mode2"], '-u', '-h', Parameters["Address"] + ':' + Parameters["Port"]]))
        for line in res.split('\\n'):
            (key,spl,val) = line.partition(': ')
            key = key.rstrip()			#Strip spaces right of text
            val = val.strip()			#Remove outside spaces
            if key in values:
                Devices[values[key]['dunit']].Update(0, str(val))
    except Exception as err:
        Domoticz.Error("APC UPS Error: " + str(err))
