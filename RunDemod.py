#!/usr/bin/env python

from datetime import datetime
from time import sleep
import sys, time
from Demon import Daemon
 
class MyDaemon(Daemon):
        def run(self):
            while(1):
                f = open('info.log', 'a')
                f.write(str(datetime.today()))
                f.write('\n')
                f.close()

            
 
if __name__ == "__main__":
        daemon = MyDaemon('/tmp/daemon-example.pid')
        # daemon.start()

        if len(sys.argv) == 2:
                if 'start' == sys.argv[1]:
                        daemon.start()
                elif 'stop' == sys.argv[1]:
                        daemon.stop()
                elif 'restart' == sys.argv[1]:
                        daemon.restart()
                else:
                        print("Unknown command")
                        sys.exit(2)
                sys.exit(0)
        else:
                print("usage: %s start|stop|restart" % sys.argv[0])
                sys.exit(2)