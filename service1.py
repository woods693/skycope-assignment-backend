"""
This module accompanies the interview question: Implement a Web server + UI.
This is a tool to simulate a service and generate three log files, info, debug
and error.
By default the logs will be generated in the current directory under a folder
named "logs".
"""
import argparse
import logging
import logging.config
from time import sleep
import os
import random


class Log:
    def __init__(self, path):
        self.log_path = path
        self.config = {
            'version': 1,
            'disable_existing_loggers': False,
            'formatters': {
                'simple': {
                    'format': '%(asctime)s - %(levelname)s - %(message)s'
                }
            },
            'handlers': {
                'console': {
                    'class': 'logging.StreamHandler',
                    'level': 'DEBUG',
                    'formatter': 'simple',
                    'stream': 'ext://sys.stdout'
                },
                'debug_file_handler': {
                    'class': 'logging.handlers.RotatingFileHandler',
                    'level': 'DEBUG',
                    'formatter': 'simple',
                    'filename': '{}/service1-debug.log'.format(self.log_path),
                    'maxBytes': 10485760,
                    'backupCount': 20,
                    'encoding': 'utf8'
                },
                'info_file_handler': {
                    'class': 'logging.handlers.RotatingFileHandler',
                    'level': 'INFO',
                    'formatter': 'simple',
                    'filename': '{}/service1-info.log'.format(self.log_path),
                    'maxBytes': 10485760,
                    'backupCount': 20,
                    'encoding': 'utf8'
                },
                'error_file_handler': {
                    'class': 'logging.handlers.RotatingFileHandler',
                    'level': 'ERROR',
                    'formatter': 'simple',
                    'filename': '{}/service1-error.log'.format(self.log_path),
                    'maxBytes': 10485760,
                    'backupCount': 20,
                    'encoding': 'utf8'
                }
            },
            'loggers': {
                'my_module': {
                    'level': 'DEBUG',
                    'handlers': [
                        'console',
                        'debug_file_handler',
                        'info_file_handler',
                        'error_file_handler'
                    ],
                    'propagate': False
                }
            },
            'root': {
                'level': 'DEBUG',
                'handlers': [
                    'console',
                    'debug_file_handler',
                    'info_file_handler',
                    'error_file_handler'
                ]
            }
        }

    def setup_logging(self, log_level):
        if not os.path.exists(self.log_path):
            os.makedirs(self.log_path)
        logging.config.dictConfig(self.config)
        logging.getLogger().setLevel(log_level)


def parse_argument():
    parser = argparse.ArgumentParser(prog='{}'.format(__file__),
                                     usage='python %(prog)s [options]',
                                     description='A tool to generate sample logs for {}.'.format(__file__))
    parser.add_argument('--path', '-p', type=str, action='store', default='./logs',
                        help='the path where to store the log files. (default: ./logs')

    args = parser.parse_args()
    return args.path


def main():
    try:
        path = parse_argument()
        Log(path).setup_logging(logging.DEBUG)
        logger = logging.getLogger(__name__)
        while True:
            logger.info("This is a sample info log and generated by {} for the purpose of simulating a service.".format(__file__))
            logger.info("You may use a KEYWORD to filter a line!")
            logger.info("You may use a KEYWORD to be highlighted in a line!")
            logger.debug("This is a sample debug log and generated by {} for the purpose of simulating a service.".format(__file__))
            sleep(random.random())
    except KeyboardInterrupt:
        logger.info('Bye.')
        logger.debug('Bye.')
    except Exception as e:
        logger.error(e)


if __name__ == '__main__':
    main()
