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
    'MODEL': {'dname': 'Model', 'dunit': 5, 'dtype':243, 'dsubtype':19},
    'SERIALNO': {'dname': 'Serial Number', 'dunit': 6, 'dtype':243, 'dsubtype':19},
    'BATTV': {'dname': 'Battery voltage', 'dunit': 7, 'dtype':243, 'dsubtype':8},
    'NOMBATTV': {'dname': 'Nominal battery voltage', 'dunit': 8, 'dtype':243, 'dsubtype':8},
    'BATTDATE': {'dname': 'Battery date', 'dunit': 9, 'dtype':243, 'dsubtype':19},
    'SELFTEST': {'dname': 'Date of last self test', 'dunit': 10, 'dtype':243, 'dsubtype':19},
    'LASTXFER': {'dname': 'Reason for last transfer to battery', 'dunit': 11, 'dtype':243, 'dsubtype':19},
    'NOMPOWER': {'dname': 'Nominal UPS power output', 'dunit': 12, 'dtype':243, 'dsubtype':31, 'options':'1;Watt'},
    'TIMELEFT': {'dname': 'Time left on battery', 'dunit': 13, 'dtype':243, 'dsubtype':31, 'options':'1;minutes'},
    'NUMXFERS': {'dname': 'Number of transfers to battery', 'dunit': 14, 'dtype':243, 'dsubtype':31, 'options':'1;times'},
    'TONBATT': {'dname': 'Time on battery', 'dunit': 15, 'dtype':243, 'dsubtype':31, 'options':'1;minutes'},
    'CUMONBATT': {'dname': 'Cumulative time on battery', 'dunit': 16, 'dtype':243, 'dsubtype':31, 'options':'1;minutes'},
}

def onStart():
    Domoticz.Log("Domoticz APC UPS plugin start")

    if len(Devices) != len(values):
        for key in values:
            try:
                Domoticz.Device(Name=values[key]['dname'], Unit=values[key]['dunit'], Type=values[key]['dtype'], Subtype=values[key]['dsubtype'], Used=1, Options=values[key]['options']).Create()
            except:
                Domoticz.Device(Name=values[key]['dname'], Unit=values[key]['dunit'], Type=values[key]['dtype'], Subtype=values[key]['dsubtype'], Used=1).Create()

    Domoticz.Heartbeat(int(Parameters["Mode1"]))

def onHeartbeat():
    try:
        res = str(subprocess.check_output([Parameters["Mode2"], '-u', '-h', Parameters["Address"] + ':' + Parameters["Port"]]))

        battery_values = {}

        for line in res.strip().split('\\n'):
            (key,spl,val) = line.partition(': ')
            key = key.rstrip()			#Strip spaces right of text
            val = val.strip()			#Remove outside spaces
            battery_values[key] = float(val) if val.replace('.', '', 1).isdigit() else val

        batterylevel = int(str(battery_values.get('BCHARGE', -1)).split('.')[0])

        for key, val in battery_values.items():
            if key in values:
                #Domoticz.Log("{} {}".format(key,val))
                iUnit = values[key]['dunit']
                curval = Devices[iUnit].sValue

                if ( str(val) != curval ):
                    if batterylevel >= 0:
                        Devices[iUnit].Update(nValue=0, sValue=str(val), BatteryLevel=batterylevel)
                    else:
                        Devices[iUnit].Update(0, str(val))

    except Exception as err:
        Domoticz.Error("APC UPS Error: " + str(err))
