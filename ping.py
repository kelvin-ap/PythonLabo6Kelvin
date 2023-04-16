import subprocess
import platform 

class Ping:
    def __init__(self, host):
        self.host = host

    def do_ping(self):
        parameter = '-n' if platform.system().lower()=='windows' else '-c'
        command = ['ping', parameter, '3', self.host]
        response = subprocess.call(command)
        return response == 0
