#!/usr/bin/env python3

import asyncio
import argparse
import sys
import os
import signal

sys.path.append(os.path.dirname(__file__))

from constants import *

DEFAULT_HOST_ALL_INTERFACES = '0.0.0.0'
DEFAULT_HOST_LOCALHOST = 'localhost'
DEFAULT_HOST_LOOPBACK = '127.0.0.1'
ARG_VALIDATION_EXIT_SUCCESS = 0
ARG_VALIDATION_EXIT_ERROR = 1
SIGNAL_SIGINT = signal.SIGINT
SIGNAL_SIGTERM = signal.SIGTERM
USER_INPUT_YES = 's'

class SimpleServer:
    def __init__(self, host='0.0.0.0', port=DEFAULT_SERVER_PORT):
        self.host = host
        self.port = port
        self.running = False

    async def start(self):
        self.running = True
        
        try:
            await self._start_battleship_server()
        except OSError as e:
            self._handle_os_error(e)
        except KeyboardInterrupt:
            pass
        except Exception as e:
            self._handle_unexpected_error(e)
        finally:
            self._cleanup_server()
            
    async def _start_battleship_server(self):
        from server import BattleshipServer
        server = BattleshipServer(host=self.host, port=self.port)
        await server.start_server()
        
    def _handle_os_error(self, error):
        # Error de red; finalizar con código de error
        sys.exit(ARG_VALIDATION_EXIT_ERROR)
        
    def _handle_unexpected_error(self, error):
        sys.exit(ARG_VALIDATION_EXIT_ERROR)
        
    def _cleanup_server(self):
        self.running = False

def setup_signal_handlers(server_instance):
    def signal_handler(signum, frame):
        _handle_shutdown_signal(signum, server_instance)
    
    signal.signal(SIGNAL_SIGINT, signal_handler)
    signal.signal(SIGNAL_SIGTERM, signal_handler)
    
def _handle_shutdown_signal(signal_number, server_instance):
    server_instance.running = False
    sys.exit(ARG_VALIDATION_EXIT_SUCCESS)

def validate_args(args):
    _validate_port_range(args.port)
    _validate_host_format(args.host)
    
def _validate_port_range(port):
    if not (MIN_PORT_NUMBER <= port <= MAX_PORT_NUMBER):
        sys.exit(ARG_VALIDATION_EXIT_ERROR)
        
def _validate_host_format(host):
    valid_hosts = [DEFAULT_HOST_ALL_INTERFACES, DEFAULT_HOST_LOCALHOST, DEFAULT_HOST_LOOPBACK]
    if host not in valid_hosts and not _is_valid_ip_format(host):
        _prompt_host_confirmation(host)
        
def _is_valid_ip_format(host):
    return host.replace('.', '').isdigit()
    
def _prompt_host_confirmation(host):
    response = input("¿Continuar de todos modos? (s/N): ").strip().lower()
    if response != USER_INPUT_YES:
        sys.exit(ARG_VALIDATION_EXIT_SUCCESS)

def main():
    parser = _create_argument_parser()
    args = parser.parse_args()
    
    validate_args(args)
    server = SimpleServer(host=args.host, port=args.port)
    setup_signal_handlers(server)
    
    _run_server_with_error_handling(server)
    
def _create_argument_parser():
    parser = argparse.ArgumentParser(
        description='Servidor de Batalla Naval sin ngrok',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    _add_parser_arguments(parser)
    return parser
  
def _add_parser_arguments(parser):
    parser.add_argument(
        '--host', 
        default=DEFAULT_HOST_ALL_INTERFACES,
        help=f'Host/IP en la que escuchar (default: {DEFAULT_HOST_ALL_INTERFACES} para todas las interfaces)'
    )
    parser.add_argument(
        '--port', 
        type=int, 
        default=DEFAULT_SERVER_PORT,
        help=f'Puerto en el que escuchar (default: {DEFAULT_SERVER_PORT})'
    )
    parser.add_argument(
        '--version', 
        action='version', 
        version='Batalla Naval Server v1.0'
    )
    
def _run_server_with_error_handling(server):
    try:
        asyncio.run(server.start())
    except KeyboardInterrupt:
        pass
    except Exception as e:
        pass
if __name__ == "__main__":
    main()