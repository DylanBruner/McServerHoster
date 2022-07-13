import mcrcon

class Server(object):
    def __init__(self, rconIp, rconPassword, rconPort = 25575):
        self.rconIp       = rconIp
        self.rconPort     = rconPort
        self.rconPassword = rconPassword

        self.rconClient = mcrcon.MCRcon(self.rconIp, self.rconPassword, self.rconPort)
        self.rconClient.connect()
    
    def ban(self, username: str): self.rconClient.command(f'ban {username}')
    def banIp(self, ip: str): self.rconClient.command(f'ban-ip {ip}')
    def pardon(self, username: str): self.rconClient.command(f'pardon {username}')
    def pardonIp(self, ip: str): self.rconClient.command(f'pardon-ip {ip}')
    def restart(self): self.rconClient.command('restart')
    def stop(self): self.rconClient.command('stop')
    def saveAll(self): self.rconClient.command('save-all')
    def say(self, text): self.rconClient.command(f'say {text}')