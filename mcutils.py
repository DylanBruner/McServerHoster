import json, os, random, string, time
import urllib.request

def getAvaliableServers() -> list:
    return [f.name for f in os.scandir('data/servers') if f.is_dir()]
def getAvaliableVersions() -> list:
    with open('config/downloadurls.json', 'r') as f:
        return list(json.load(f).keys())
def getVersionTypes(version) -> list:
    with open('config/downloadurls.json', 'r') as f:
        return list(json.load(f)[version.strip()].keys())


def getRandString(length: int) -> str:
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(length))

def getDownloadUrl(version: str, serverType: str) -> str:
    with open('config/downloadurls.json', 'r') as f:
        return json.load(f)[version.strip()][serverType.strip().lower()]

def runServer(serverName):
    os.chdir(f'data/servers/{serverName}')
    os.system('java -jar server.jar --nogui')
    os.chdir('../../..')

def startServerWServerRunner(serverName):
    print("[Info] Starting server...")
    os.system(f'python serverrunner.py "{os.getcwd()}/data/servers/{serverName}" "{serverName}"')
    print("[Info] Server started!")

def createNewServer(serverName, serverVersion, serverType):
    print("Creating new server...")
    if not os.path.exists(f'data/servers/{serverName}'):
        os.mkdir(f'data/servers/{serverName}')
        with open(f'data/servers/{serverName}/config.json', 'w') as f:
            f.write(json.dumps({
                'name': serverName,
                'version': serverVersion,
                'type': serverType,
                'downloadUrl': getDownloadUrl(serverVersion, serverType)
            }))
    print("Downloading server...")
    urllib.request.urlretrieve(getDownloadUrl(serverVersion, serverType), f'data/servers/{serverName}/server.jar')

def modifyPropertiesFile(serverName, setting, newValue):
    with open(f'data/servers/{serverName}/server.properties', 'r') as f:
        lines = f.readlines()
    with open(f'data/servers/{serverName}/server.properties', 'w') as f:
        for line in lines:
            if line.startswith(setting):
                line = f'{setting}={newValue}\n'
            f.write(line)

def getPropertyValue(serverName, serverValue) -> str:
    with open(f'data/servers/{serverName}/server.properties', 'r') as f: lines = f.readlines()
    return next((line.split('=')[1].strip() for line in lines if line.startswith(serverValue)), None)

def setupServerToBeManaged(serverName):
    print("[Info] Initializing server...")
    if os.path.exists(f'data/servers/{serverName}') and not os.path.exists(f'data/servers/{serverName}/eula.txt'):
        print('[Info] Eula not found, doing first time run...')
        runServer(serverName)

        print("[Info] Eula created, modifying server...")

    print(os.getcwd())
    with open(f'data/servers/{serverName}/eula.txt', 'w') as f: f.write('eula=true')
    print("[Info] EULA accepted")

    #Apply server property changes
    print("[Info] Modifying server properties...")
    modifyPropertiesFile(serverName, 'broadcast-rcon-to-ops', 'false')
    modifyPropertiesFile(serverName, 'broadcast-console-to-ops', 'false')
    modifyPropertiesFile(serverName, 'enable-rcon', 'true')
    modifyPropertiesFile(serverName, 'rcon.password', getRandString(12))

    print("[Info] Server is ready to be managed!")