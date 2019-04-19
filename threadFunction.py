# -*- coding: utf-8 -*-
#!/usr/bin/env python
import threading
import logging
import Queue
import bluetooth
import time
import sys

bt_q = Queue.Queue()
conn_check_q = Queue.Queue()

RECONNECTION_TIME = 30 #재연결 시간
BT_CONN_MSG_SEND_TIME = 240 #주기적으로 Bluetooth 살아 있는지 확인 하는 시간


HC_06_com_addr = "20:14:04:11:22:37"
HC_06_com_port = 1

root = logging.getLogger()
root.setLevel(logging.DEBUG)
logging.basicConfig(filename= 'echo_mqtt.log', level=logging.DEBUG)

handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)
root.addHandler(handler)


TimerDic = {}
ThreadList = []
BTCycle = "BTCycle"
# thread
class MThread(threading.Thread):
    def __init__(self, ID, name, function, *args):
        threading.Thread.__init__(self)
        self.ID = ID
        self.name = name
        self.function = function
        self.input_tuple = tuple(value for _, value in enumerate(args))

        self.stop_flag = threading.Event()
        self.stop_flag.set()
        self.input_tuple = self.input_tuple + (self.stop_flag,)

    def run(self):
        logging.debug("starting " + self.name)
        # LedJarThreadLock.acquire()
        self.function(*self.input_tuple)
        # LedJarThreadLock.release()
        logging.debug("ending " + self.name)

# timer
class MTimer:
    kill_evt = 0
    def __init__(self,name,delay,count,fuction,*args):
        self.name = name
        #if name
        self.delay = delay
        self.count = count
        self.fuction = fuction
        self.args = tuple(value for _, value in enumerate(args))
        self.thread = threading.Timer(self.delay, self.handle_function)

    def handle_function(self):
        if self.count != -1:
            self.count -= 1

        self.fuction(*self.args)
        self.thread = threading.Timer(self.delay, self.handle_function)
        self.thread.start()

        if self.kill_evt == 1 or self.count == 0:
            logging.debug ('[%s]timer kill len  kill = %d, count = %d ' %  (self.name, self.kill_evt, self.count))
            self.thread.cancel()

    def start(self):
        logging.debug ('[%s]timer start !'%self.name)
        self.thread.start()

    def cancel(self):
        logging.debug ('[%s]timer stop !'%self.name)
        self.kill_evt = 1

        self.thread.cancel()

    def isAlive(self):
        val = self.thread.isAlive()
        logging.debug ('[%s]timer status %d !'% (self.name, val))
        return val


# bluetooth ------------------------------------

def connectBluetooth(adress, port):
    try:
        sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
        sock.connect((adress, port))
        sock.settimeout(2)

        logging.debug("Bluetooth Connected !")
        # TX Thread 생성
        bt_tx = MThread(1, "SendBT", sendDataToBT, sock)
        bt_tx.start()
        ThreadList.append(bt_tx)


        sendFunction(sock, 'B_Start')

        # 블루투스 Check Timer 생성
        bt_cycle = MTimer(BTCycle, BT_CONN_MSG_SEND_TIME, -1, sendFunction, sock, 'B_Start')
        bt_cycle.start()
        TimerDic[BTCycle] = bt_cycle

        # Queue를 비워 줌
        while True:
            try:
                para = conn_check_q.get_nowait()
                logging.debug('Flush Q:', str(para))
            except Queue.Empty:
                break;

    except Exception, e:
        logging.debug("Bluetooth error Occured ! ! " + str(e))
        conn_check_q.put_nowait(1)

# bluetooth 데이터 Sends 함수
def sendFunction(bt_sock, data):
    try:
        strs = "msg send : " + str(data)
        logging.debug(strs)
        bt_sock.send(data)
    except:
        logging.debug("Bluetooth socket send error")
        conn_check_q.put_nowait(1)
        pass

def sendDataToBT(sock, t_event):
    while t_event.is_set():
        try:
            data = bt_q.get_nowait()
            sendFunction(sock, data)
        except Queue.Empty:
            pass
        except Exception, e:
            logging.debug(str(e))
        time.sleep(0.1)
    logging.debug('sendDataToBT Thread Kill !')
    sock.close()


def recoveryProcess(adress, port, t_event):
    while t_event.is_set():
        try:
            para = conn_check_q.get_nowait()
            #thread_list_mutex.acquire()
            if para == 1:
                try:

                    #logging.debug('Thread list ' + str(len(ThreadList)))
                    while len(ThreadList) >0:

                        thread = ThreadList.pop()
                        logging.debug('Get Thread Name :' + thread.name + ' kill by Recovery Proc')
                        thread.stop_flag.clear()

                except:
                    logging.debug('Thread kill error')
                try:
                    #logging.debug('Timer Dic ' + str(len(TimerDic)))
                    for key, value in TimerDic.iteritems():
                        logging.debug('Timer Kill :' + 'kill by Recovery Proc')
                        value.kill_evt = 1

                    TimerDic.clear()

                except:
                    logging.debug('Timer kill error')
                time.sleep(RECONNECTION_TIME)

                connectBluetooth(adress, port)

        except Queue.Empty:
            pass
        except Exception, e:
            print 'RecoveryProcess error' + str(e)
        time.sleep(0.1)


if __name__ == "__main__":

    pass
