# domoticz-apc-ups-plugin
Domoticz APC UPS plugin

This plugin retrieves data from the APC UPS. It uses `apcaccess` to retrieve the details.

**Installation**

On your machine with USB or connectivity to the APC UPS:

```apt-get install apcupsd ```

And configure it to be able to retrieve the APC UPS data

If domoticz runs on another machine, install it again there so the `apcaccess` executable exists.
