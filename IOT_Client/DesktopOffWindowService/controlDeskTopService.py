import win32service
import win32serviceutil
import win32event
import servicemanager
import controlDeskTop as condesk
import socket
import sys

class controlService(win32serviceutil.ServiceFramework):
    _svc_name_ = "DeskTopControl"
    _svc_display_name_ = 'Remote Control Desktop Service'

    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
        socket.setdefaulttimeout(60)



    def SvcStop(self):

        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.hWaitStop)

    def SvcDoRun(self):

        servicemanager.LogMsg(servicemanager.EVENTLOG_INFORMATION_TYPE,
                              servicemanager.PYS_SERVICE_STARTED,
                              (self._svc_name_, ''))
        self.main()


    def main(self):
        print('Start Service')
        condesk.serviceRun()
        #win32event.WaitForSingleObject(self.hWaitStop,
        #                              win32event.INFINITE)


if __name__ == "__main__":

    if len(sys.argv) == 1:
        servicemanager.Initialize()
        servicemanager.PrepareToHostSingle(controlService)
        servicemanager.StartServiceCtrlDispatcher()
    else:
        win32serviceutil.HandleCommandLine(controlService)