import sys, os

ServerLocation = sys.argv[1]
ServerName     = sys.argv[2]

print(f"[Info] Starting {ServerName}")

os.system('start cmd /k "cd ' + ServerLocation + ' && java -jar server.jar --nogui && exit"')