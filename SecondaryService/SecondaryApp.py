from http.server import HTTPServer
import argparse

from SecondaryService.Logging import *
import SecondaryService.Constants as constants
from SecondaryService.Constants import ConfigKeys
from SecondaryService.SecondaryDomain import SecondaryDomain
from SecondaryService.SecondaryService import SecondaryService

class SecondaryApp:
    def __init__(self):
        configure_logging(constants.SERVICE_NAME)

        self.arg_parser = argparse.ArgumentParser(
                    prog = constants.SERVICE_NAME,
                    description = 'Service to log messages')
        self.add_args_to_parser()
        
        self.config = dict()
        self.parse_args()

    def parse_args(self):
        args = self.arg_parser.parse_args()
        self.config[ConfigKeys.PORT] = args.port
        self.config[ConfigKeys.MASTER_ADDR] = args.master

    def add_args_to_parser(self):
        self.arg_parser.add_argument('-p', '--port', type=int) 
        self.arg_parser.add_argument('-m', '--master', type=str) 

    def run(self):
        SecondaryDomain(self.config[ConfigKeys.MASTER_ADDR], self.config[ConfigKeys.PORT])

        server_address = ('', self.config[ConfigKeys.PORT])
        httpd = HTTPServer(server_address, SecondaryService)
        app_log('Starting httpd at ' + str(server_address))
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            pass
        httpd.server_close()
        app_log('Stopping httpd...')