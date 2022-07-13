import json
import mcutils, mcapi, os, time

IP_BINDS = {
    '192.168.50.170': 19186,
    '192.168.50.49': 25564
}

def ManageServer(serverName):
    ServerIp       = mcutils.getPropertyValue(serverName, 'server-ip')
    ServerPassword = mcutils.getPropertyValue(serverName, 'rcon.password')
    ServerPort     = mcutils.getPropertyValue(serverName, 'rcon.port')

    Server = mcapi.Server(ServerIp, ServerPassword, int(ServerPort))

    os.system('cls')
    os.system(f'title {serverName}:{ServerIp}')
    print("1. Restart server")
    print("2. Stop server")
    print("3. Save all")
    print("4. Ban player")
    print("5. Ban ip")
    print("6. Pardon player")
    print("7. Pardon ip")
    print("8. Say in chat")
    print("9. Exit")

    while True:
        choice = input("Enter your choice: ")
        if choice == "1":
            print(f"Stopping {serverName}...")
            Server.stop()
            input("Press enter when server is stops...")
            mcutils.startServerWServerRunner(serverName)
            input("Press enter when server is running...")
            ManageServer(serverName)
        elif choice == "2": print(f"Stopping {serverName}..."); Server.stop()
        elif choice == "3": print("Saving all..."); Server.saveAll()
        elif choice == "4": player2ban = input("Player to ban: "); Server.ban(player2ban)
        elif choice == "5": ip2ban = input("Ip to ban: "); Server.banIp(ip2ban)
        elif choice == "6": player2pardon = input("Player to pardon: "); Server.pardon(player2pardon)
        elif choice == "7": ip2pardon = input("Ip to pardon: "); Server.pardonIp(ip2pardon)
        elif choice == "8": text = input("Text to say: "); Server.say(text)
        elif choice == "9": exit()

def MainMenu():
    # sourcery skip: extract-duplicate-method, inline-immediately-returned-variable, low-code-quality, remove-redundant-fstring
    print("1. Create new server")
    print("2. Start server")
    print("3. Manage existing server")
    print("4. Manage global connect")
    print("5. Exit")

    choice = input("Enter your choice: ")

    if choice == "1":
        ServerVersion = input("Server Version [1.19, 1.18](default=1.19): ").strip()
        if ServerVersion == "": ServerVersion = '1.19'

        ServerType = input("Server Type [vanilla, paper](default=paper): ").strip()
        if ServerType == "": ServerType = 'paper'
        ServerName = input("Server Name (default=none): ").strip()
        IpToRunOn = input("Ip to run on [hint your ipv4 local](default=localhost): ").strip()
        if IpToRunOn == "": IpToRunOn = 'localhost'
 
        print(f"Creating a {ServerVersion} {ServerType} server...")
        mcutils.createNewServer(ServerName, ServerVersion, ServerType)
        print(f"Server {ServerName} created, getting it ready to be managed...")
        mcutils.setupServerToBeManaged(ServerName)
        print(f"Server {ServerName} ready to be managed")

        mcutils.modifyPropertiesFile(ServerName, 'server-ip', IpToRunOn)

        print(f"Starting {ServerName}...")
        mcutils.startServerWServerRunner(ServerName)
    
    elif choice == "2":
        for server in mcutils.getAvaliableServers(): print(server)
        ServerName = input("Server Name (default=none): ").strip()
        print(f"Starting {ServerName}...")
        mcutils.startServerWServerRunner(ServerName)

        if os.path.exists(f"data/servers/{ServerName}/globalconnect.json"):
            with open(f"data/servers/{ServerName}/globalconnect.json", 'r') as f:
                data = json.load(f)
                if data['enabled']:
                    print("Global connect is enabled, launching...\n")
                    os.system(f"start cmd /k python globalconnectserver.py {data['listen_ip']} {data['listen_port']} {data['connect_ip']} {data['connect_port']} && exit")


    elif choice == "3":
        for server in mcutils.getAvaliableServers(): print(server)

        ManageServer(input("Server Name (default=none): ").strip())
    
    elif choice == "4":
        os.system('cls')
        os.system(f'title Global Connect')
        print('=====[Global Connect]=====')
        print("1. Setup global connect for server")
        print("2. Launch global connect")

        choice = input("Enter your choice: ")
        if choice == "1":
            for server in mcutils.getAvaliableServers(): print(server)

            ServerName = input("Server Name (default=none): ").strip()
            print()
            if mcutils.getPropertyValue(ServerName, 'server-ip').strip() in ['localhost','','127.0.0.1']:
                print("You can't setup global connect for localhost server")
                ServerIp = input("Server Ip (default=none): ").strip()
                if ServerIp in ['localhost','','127.0.0.1']:
                    print("You can't setup global connect for localhost server"); return

                print("Setting up global connect...\n")


                mcutils.modifyPropertiesFile(ServerName, 'server-ip', ServerIp)
                print(f"Server {ServerName} ip set to {ServerIp}")
            else:
                ServerIp = mcutils.getPropertyValue(ServerName, 'server-ip').strip()

            try:
                ServerGlobalPort = IP_BINDS[ServerIp]
            except Exception:
                print("No ip binding found for this server ip")
                return

            print("Writing global connect config...")
            with open(f"data/servers/{ServerName}/globalconnect.json", 'w') as f:
                f.write(json.dumps({
                    'enabled': True,
                    'listen_ip': ServerIp,
                    'listen_port': ServerGlobalPort,
                    'connect_ip': ServerIp,
                    'connect_port': 25565
                }))
            
            print(f"Global connect setup for server use {ServerGlobalPort} to connect non-locally")
            print()
        
        elif choice == "2":
            ServerName = input("Server Name (default=none): ").strip()
            print("Launching global connect...")
            if os.path.exists(f"data/servers/{ServerName}/globalconnect.json"):
                with open(f"data/servers/{ServerName}/globalconnect.json", 'r') as f:
                    data = json.load(f)
                    os.system(f"start cmd /k python globalconnectserver.py {data['listen_ip']} {data['listen_port']} {data['connect_ip']} {data['connect_port']} && exit")
            else:
                print("No global connect setup for this server")
                return


    elif choice == "5":
        exit()
    
    MainMenu()

MainMenu()