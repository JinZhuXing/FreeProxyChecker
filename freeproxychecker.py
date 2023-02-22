import argparse
import sys

from config import getConfig
from logproc import init_logger
from checkproc import check_proc


# main process
def main(args):
    # parse arguments
    conf_file = args.conf

    # initialize log
    log_file = getConfig(conf_file, 'log', 'log_file')
    init_logger(log_file)

    # proxy information
    proxy_list_file = getConfig(conf_file, 'proxy_info', 'proxy_list_file')
    proxy_success_list = getConfig(conf_file, 'proxy_info', 'proxy_success_list')

    # check rule
    check_url = getConfig(conf_file, 'check_rule', 'check_url')
    header_referer = getConfig(conf_file, 'check_rule', 'header_referer')
    header_host = getConfig(conf_file, 'check_rule', 'header_host')

    # check process
    check_proc(proxy_list_file, proxy_success_list, check_url, header_referer, header_host)


# argument parser
def parse_arguments(argv):
    parser = argparse.ArgumentParser()

    parser.add_argument('--conf', type = str,
            help = 'Configure file path', default = './freeproxychecker.conf')
    
    return (parser.parse_args(argv))


# start point
if __name__ == '__main__':
    main(parse_arguments(sys.argv[1:]))