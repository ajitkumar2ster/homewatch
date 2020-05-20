#Author: Maninder Singh Bhogal
#Contact: maninder.bhogal@gmail.com

import RPi.GPIO as GPIO
import time
import telepot
import _thread
import configparser
import urllib3
import telepot.api
from urllib3.contrib.socks import SOCKSProxyManager

proxy_url = 'socks5://192.168.1.64:9050'
telepot.api._pools = {'default': SOCKSProxyManager(proxy_url=proxy_url, num_pools=3, maxsize=10, retries=False, timeout=30),}
telepot.api._onetime_pool_spec = (SOCKSProxyManager, dict(proxy_url=proxy_url, num_pools=1, maxsize=1, retries=False, timeout=30))

cf = configparser.ConfigParser()
cf.read('homewatch.conf')

bot = telepot.Bot('1220821606:AAGa_uLYxAZuebphG2MxTXHnlpjdSYOM7EQ')
homemembers = [537452059, 1224139768]

try:
    need_clean = False

    MSG_TYPE = {True:'OPENED', False:'CLOSED'}

    def send_msg(opened:bool, pin:int):
        str_print =''.join([PIN_MSG[pin], MSG_TYPE[opened], ' on ',
                            time.strftime('%m/%d/%Y at %I:%M:%S %p')])
        print(str_print)
        for chat_id in homemembers:
            bot.sendMessage(chat_id, str_print)


    #Initializing GPIO Pins
    print('Setting up hardware...')
    PIN_foyerwindow = int(cf.get('PIN', 'foyerwindow'))
    PIN_livingwindow = int(cf.get('PIN', 'livingwindow'))
    PIN_diningwindow = int(cf.get('PIN', 'diningwindow'))
    PIN_backdoor = int(cf.get('PIN', 'backdoor'))
    PIN_maingaragedoor = int(cf.get('PIN', 'maingaragedoor'))
    PIN_MSG = {PIN_foyerwindow:'Foyer Window was ', PIN_livingwindow:'Living Room Window was ', PIN_diningwindow:'Dining Room Window was '
               , PIN_backdoor:'Back Door was ', PIN_maingaragedoor:'Main or Garage Door was '}

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(PIN_foyerwindow, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(PIN_livingwindow, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(PIN_diningwindow, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(PIN_backdoor, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(PIN_maingaragedoor, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    #next_state to check for to send message
    PIN_foyerwindow_next_state = True
    PIN_livingwindow_next_state = True
    PIN_diningwindow_next_state = True
    PIN_backdoor_next_state = True
    PIN_maingaragedoor_next_state = True

    need_clean = True

    print('Security System is Ready!')
    #Run infinitely
    while True:
        #Check for next state
        if GPIO.input(PIN_foyerwindow) == PIN_foyerwindow_next_state:
            #Send message on different thread
            _thread.start_new_thread(send_msg, (PIN_foyerwindow_next_state,PIN_foyerwindow))
            #Negate next_state
            PIN_foyerwindow_next_state = not PIN_foyerwindow_next_state
        time.sleep(0.3)
        if GPIO.input(PIN_livingwindow) == PIN_livingwindow_next_state:
            #Send message on different thread
            _thread.start_new_thread(send_msg, (PIN_livingwindow_next_state,PIN_livingwindow))
            #Negate next_state
            PIN_livingwindow_next_state = not PIN_livingwindow_next_state
        time.sleep(0.3)
        if GPIO.input(PIN_backdoor) == PIN_backdoor_next_state:
            #Send message on different thread
            _thread.start_new_thread(send_msg, (PIN_backdoor_next_state,PIN_backdoor))
            #Negate next_state
            PIN_backdoor_next_state = not PIN_backdoor_next_state
        time.sleep(0.3)
        if GPIO.input(PIN_diningwindow) == PIN_diningwindow_next_state:
            #Send message on different thread
            _thread.start_new_thread(send_msg, (PIN_diningwindow_next_state,PIN_diningwindow))
            #Negate next_state
            PIN_diningwindow_next_state = not PIN_diningwindow_next_state
        time.sleep(0.3)
        if GPIO.input(PIN_maingaragedoor) == PIN_maingaragedoor_next_state:
            #Send message on different thread
            _thread.start_new_thread(send_msg, (PIN_maingaragedoor_next_state,PIN_maingaragedoor))
            #Negate next_state
            PIN_maingaragedoor_next_state = not PIN_maingaragedoor_next_state
        time.sleep(0.3)

except KeyboardInterrupt:
    GPIO.cleanup() #For Keyboard Interrupt exit
    need_clean = False

if need_clean:
    GPIO.cleanup() #For normal exit
print('\nEnd!')
