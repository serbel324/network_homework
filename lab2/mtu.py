import subprocess
import socket
import sys
import traceback
import logging
import platform
import argparse
import time

IP_HEADER_SIZE = 20
ICMP_HEADER_SIZE = 8

def do_ping_with_payload(host: str, payload_size: int, is_verbose: bool):
    tries_number_key = '-n' if platform.system().lower()=='windows' else '-c'
    payload_size_key = '-l' if platform.system().lower()=='windows' else '-s'
    no_fragmentation=['-f'] if platform.system().lower()=='windows' else ['-M', 'do']
    try:
        ping_result = subprocess.run(['ping', host, tries_number_key, '1'] + no_fragmentation + [payload_size_key, str(payload_size)], 
                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except Exception as e:
        return None

    if is_verbose:
        print(f'Ping host# {host} with payload_size# {payload_size}, returncode={ping_result.returncode}')
    return ping_result.returncode == 0

def main():
    parser = argparse.ArgumentParser(description='Discover MTU to host.')

    parser.add_argument('host', help='host to determine MTU to')
    parser.add_argument('-v', '--verbose', help='print intermediate steps', action='store_true')

    args = parser.parse_args()
    host = args.host
    is_verbose = args.verbose

    try:
        socket.gethostbyname(host)
    except socket.error:
        print(f'Host name {host} cannot be resolved')
        return 1
    
    try:
        if subprocess.run(['ping', '-c', '1', host], 
                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).returncode != 0:
            print(f'Host {host} is unreachable')
            return 1
    except Exception as e:
        print('Unexpected exception raised while initial ping')
        logging.error(traceback.format_exc())
        return 1

    left_bound = 1
    right_bound = 2000

    while right_bound - left_bound > 1:
        try_mtu = (left_bound + right_bound) // 2
        try_result = do_ping_with_payload(host, try_mtu, is_verbose)
        if try_result is None:
            print('Unexpected exception raised while trying to discover MTU')
            logging.error(traceback.format_exc())
            return 1
        elif try_result == True:
            left_bound = try_mtu
            time.sleep(0.5)
        else:
            right_bound = try_mtu

    print(f'MTU to host# {host} = {left_bound} bytes, '\
          f'packet size with headers = {left_bound + IP_HEADER_SIZE + ICMP_HEADER_SIZE} bytes')

if __name__ == '__main__':
    main()

