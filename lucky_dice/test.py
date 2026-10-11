import socket
import re

input_stage = 1 # This variable is just to maintain the "round" that we are in. a value of 1, indicates, the rounds haven't started yet.

def round_handler(stage: int, lines: list) -> int:
    """
    # Essentially, in this function, we capture the lines starting with "Player <n>: <die roll list>"
    # split the line so that we get the die roll(s) as a list
    # store the sum of the die rolls in a variable and look for max. 
    # The delimiter is obviously the space, " "
    """
    player_select = 0 # the final value that needs to be returned to user
    max_ = 0
    if stage == 1:
        return 1
    else:
        for i in range(len(lines)-1,0,-1):
            if re.search("Player [0-9]", lines[i]):
                print(lines[i])
                els = lines[i].split(" ")
                rols = [int(roll) for roll in els[2:]]
                player_sum = sum(rols)
                if player_sum>max_:
                    max_ = player_sum
                    player_select = int(els[1].split(":")[0])
        return player_select

target_ip = "154.57.164.82" # Please change these values as provided by your target.
target_port = 37383

target = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
target.settimeout(20)

try:
    target.connect((target_ip, target_port))
except Exception as e:
    print(f"An error occured: {e}")

lines = []
running = True
while running:
    try:
        raw_data = target.recv(4096)
        if not raw_data:
            running = False
            break
        mod_data = raw_data.decode("utf-8")
        lines += mod_data.split("\n")
        print(mod_data, end="")
        if mod_data.endswith("> "):
            cmd = round_handler(input_stage, lines)
            target.sendall((str(cmd)+"\n").encode("utf-8"))
            input_stage+=1
            print(cmd)
            lines = []
    except Exception as e:
        print(f"Error occurred: {e}")
        running = False

target.close()

print("Program run completed!")
