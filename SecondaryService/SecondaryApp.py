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
        self.config[ConfigKeys.RANDOM_FAIL_MESSAGE_READ] = False
        self.parse_args()

    def parse_args(self):
        args = self.arg_parser.parse_args()
        self.config[ConfigKeys.PORT] = args.port
        self.config[ConfigKeys.MASTER_ADDR] = args.master
        self.config[ConfigKeys.LAG] = args.lag
        if args.fail_every_2_msg is not None:
            self.config[ConfigKeys.RANDOM_FAIL_MESSAGE_READ] = args.fail_every_2_msg

    def add_args_to_parser(self):
        self.arg_parser.add_argument('-p', '--port', type=int) 
        self.arg_parser.add_argument('-m', '--master', type=str) 
        self.arg_parser.add_argument('-l', '--lag', type=int) 
        self.arg_parser.add_argument('--fail_every_2_msg', type=bool) 

    def run(self):
        SecondaryDomain(self.config[ConfigKeys.MASTER_ADDR], self.config[ConfigKeys.PORT], self.config[ConfigKeys.LAG], self.config[ConfigKeys.RANDOM_FAIL_MESSAGE_READ])

        server_address = ('', self.config[ConfigKeys.PORT])
        httpd = HTTPServer(server_address, SecondaryService)
        app_log('Starting httpd at ' + str(server_address))
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            pass
        httpd.server_close()
        app_log('Stopping httpd...')