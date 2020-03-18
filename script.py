import os
import time
import sys

import telepot
from telepot.loop import MessageLoop

from subprocess import Popen
from pythonping import ping

devnull = open(os.devnull, 'wb')

p = []
active = []
not_responding = 0
failed = 0

chat_ids = []

def handle(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    print(content_type, chat_type, chat_id)

    if content_type != 'text':
        return

    command = msg['text'][1:].lower()

    if command == 'start':
        chat_ids.append(chat_id)
        bot.sendMessage(chat_id, 'You will now receive notification if you are lagging')


TOKEN = sys.argv[1]  # get token from command-line
bot = telepot.Bot(TOKEN)
MessageLoop(bot, handle).run_as_thread()
print ('Listening ...')

# Keep the program running.
while 1:
    response_list = ping('8.8.8.8', size=40, count=10)
    if response_list.rtt_avg_ms > 300:
        for chat_id in chat_ids:
            bot.sendMessage(chat_id, 'Yes, you are, your ping is ' + str(response_list.rtt_avg_ms) + 'ms')
    time.sleep(10)

"""start = time.time()

for ping in range(1,255):
    address = '192.168.1.' + str(ping)
    p.append((address, Popen(['ping', '-c', '3', address], stdout=devnull)))

while p:
    for i, (address, proc) in enumerate(p[:]):
        if proc.poll() is not None:
            p.remove((address, proc))
            if proc.returncode == 0:
                print( "ping to", address, "OK")
                active.append(address)
            elif proc.returncode == 2:
                #print("no response from", address)
                not_responding += 1
            else:
                #print("ping to", address, "failed!")
                failed += 1

end = time.time()"""

devnull.close()

print("Scan time: " + str(end - start) + "s")
