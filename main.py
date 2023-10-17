from machine import *
from thingz import *
import network
import utime
import urequests

station = None
accessPoint = None

def connect_station(ssid='', password='', ip='', mask='', gateway=''):
  global station
  station = network.WLAN(network.STA_IF)
  if station.isconnected():
    if station.config('essid') is ssid:
      print("Already connected on ssid: '%s'" % station.config('essid'))
      return
    else:
      disconnect_station()
  print("\nTrying to connect to '%s' ..." % ssid)
  if len(ip) is not 0:
    if len(gateway) == 0:
      gateway = ip.split('.')[0] + '.' + ip.split('.')[1] + '.' + ip.split('.')[2] + '.1'
    if len(mask) == 0:
      mask = '255.255.255.0'
    station.ifconfig([ip, mask, gateway, gateway])
  if not station.active():
    station.active(True)
  station.connect(ssid, password)
  while not station.isconnected():
    pass
  print("Station connected !")

def disconnect_station():
  if station is not None and station.isconnected():
    ssid = station.config('essid')
    station.disconnect()
    for retry in range(100):
      connected = station.isconnected()
      if not connected:
        break
      utime.sleep(0.1)
    if not connected:
      station.active(False)
      utime.sleep(0.2)
      print("Disconnected from '%s'\n" %ssid)
    else:
      print("Disconnection from '%s' failed.\n" %ssid)
  else:
    print("Station already disconnected.\n")

identifiant_capteur = '17173'
connect_station(ssid='RiboulonEtCiboulette', password='0686226329')

while True:
  sensor_json = urequests.request(method='GET', url=("{}" * 3).format("http://data.sensor.community/airrohr/v1/sensor/", identifiant_capteur, "/")).json()
  pm25_value = float(sensor_json[0].get('sensordatavalues')[1].get('value'))
  
  print("\n\n\n\n\n\n\n\n")
  print("PM2.5: {}ug/m3\n\n\n\n\n\n\n\n".format(pm25_value))
  
  if pm25_value < 20:
      led.set_colors(60, 100, 60)
  elif pm25_value < 40:
     led.set_colors(100, 80, 40)
  elif pm25_value < 60:
    led.set_colors(100, 20, 20)
  else:
    led.set_colors(80, 20, 80)
  utime.sleep(10)

