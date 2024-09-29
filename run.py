import aiohttp
import asyncio
import requests
import json
import time
from datetime import datetime
from itertools import cycle
from colorama import init, Fore, Style
from random import randint

# Initialize colorama
init(autoreset=True)

def load_tokens(filename):
    with open(filename, 'r') as file:
        return [line.strip() for line in file]

def get_headers(query):
   # query_id, cookie = query.strip().split('|')
    
    return {
        'Accept': '*/*',
        'Accept-Language': 'en-US,en;q=0.9',
        'X-Telegram-Web-App-Init-Data' : f'{query}',
    #    'Cookie' : f'{cookie}',
        'Connection': 'keep-alive',
        'Origin' : 'https://www.vanadatahero.com',
        'cache-control' : 'cache-control',
        'Referer': 'https://www.vanadatahero.com/home?tgWebAppStartParam=1232432698',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-site',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.0',
        'Content-Type': 'application/json'
   
    }

def getUser(token):
    url = 'https://www.vanadatahero.com/api/player'
    headers = get_headers(token)
    response = requests.post(url, headers=headers)
    return response

def getTask(token):
    url = 'https://www.vanadatahero.com/api/tasks'
    headers = get_headers(token)
    response = requests.post(url, headers=headers)
    return response

def tap(token):
    url = 'https://www.vanadatahero.com/api/tasks/1'
    headers = get_headers(token)
    headers['content-type'] = "application/json"
    points = randint(50,150)
    payload = {
        "status": "completed",
        "points": int(points)
    }
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    return response, points


# MAIN CODE
cek_task = False
def main():
    global cek_task
    print(Fore.GREEN + Style.BRIGHT + "Starting Vana ....\n\n")
    
    init_data = load_tokens('initdata.txt')
    token_cycle = cycle(init_data)

    token_dict = {}  # Dictionary to store successful tokens
    while True:
        init_data_raw = next(token_cycle)
       # print(Fore.GREEN + Style.BRIGHT + f"{get_headers(init_data_raw)}\n\n")

        token = token_dict.get(init_data_raw)
        if token:
            print(Fore.GREEN + Style.BRIGHT + f"\rMenggunakan token yang sudah ada...", end="", flush=True)
        else:
            print(Fore.GREEN + Style.BRIGHT + f"\rMendapatkan token...", end="", flush=True)

        response = getUser(init_data_raw)
   
        ## TOKEN AMAN
        if response.status_code == 200:

            data_user = response.json()
            username = data_user['tgUsername']
            nametg = data_user['tgFirstName']
            print(Fore.GREEN + Style.BRIGHT + f"\r\n======[{Fore.WHITE + Style.BRIGHT} {username} || {nametg} {Fore.GREEN + Style.BRIGHT}]======")

            # Sync Clicker
          # print(Fore.GREEN + f"\r\nGetting info user...", end="", flush=True)
            response = getUser(init_data_raw)
            print(Fore.YELLOW + Style.BRIGHT + f"[ Total Points ] : {int(data_user['points'])}")
            print(Fore.CYAN + Style.BRIGHT + f"[ Multiplier ] : {int(data_user['multiplier'])}")
            print(Fore.CYAN + Style.BRIGHT + f"[ Created At ] : {data_user['createdAt']}")
            print(Fore.CYAN + Style.BRIGHT + f"[ Update At ] : {data_user['updatedAt']}")
            print(Fore.GREEN + f"\r[ Tap Status ] : Tapping ...", end="", flush=True)
            response, points = tap(init_data_raw)
            if response.status_code == 200:
                print(Fore.GREEN + Style.BRIGHT + f"\r[ Tap Status ] : Tapped get {points} points                        ", flush=True)
                time.sleep(2)
            else:
                print(Fore.GREEN + Style.BRIGHT + f"\r[ Tap Status ] : {response}                         ", flush=True)
                if(response.json()['message'] == "Internal Server Error" ):
                    print(Fore.RED + Style.BRIGHT + f"\r[ Tap Status ] : Gagal Tap     ", flush=True)
                    time.sleep(5)
                    tap(init_data_raw)
                elif(response.json()['message'] == "Points limit exceeded" ):
                    print(Fore.RED + Style.BRIGHT + f"\r[ Tap Status ] : Points Limit ", flush=True)
                else:
                    print(Fore.RED + Style.BRIGHT + f"\r[ Tap Status ] : Gagal Tap  {response.json()}    ", flush=True)
                    break 
                
 
            time.sleep(5)
                # Check Task
            
        ## TOKEN MATI        
        elif response.status_code == 401:
            error_data = response.json()
            if error_data.get("error_code") == "NotFound_Session":
                print(Fore.RED + Style.BRIGHT + f"=== [ Token Invalid {token} ] ===")
                token_dict.pop(init_data_raw, None)  # Remove invalid token
                token = None  # Set token ke None untuk mendapatkan token baru di iterasi berikutnya
            else:
                print(Fore.RED + Style.BRIGHT + "Authentication failed with unknown error")
        else:
            print(Fore.RED + Style.BRIGHT + f"Error with status code: {response.status_code}")
            token = None  # Set token ke None jika terjadi error lain
            
        time.sleep(1)



if __name__ == "__main__":
    main()
