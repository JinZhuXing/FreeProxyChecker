import requests
import csv

from logproc import info_logger, error_logger


def get_current_ip(proxy_info):
    try:
        ip_request = requests.get(
            url = 'http://icanhazip.com/',
            proxies = proxy_info,
            verify = False,
            timeout=10
        )
    except Exception as e:
        error_logger('Failed to get current IP address')
        print(e)
        return ''

    return ip_request.text.rstrip('\n')


def check_proxy_ip(proxy_address, check_url, header_info):
    # prepare proxy information
    proxy_info = {
        'http': proxy_address,
        'https': proxy_address
    }

    # show proxy address
    info_logger('Proxy Address: ' + proxy_address)

    # check proxy ip address
    current_ip = get_current_ip(proxy_info)
    if (current_ip != ''):
        info_logger(current_ip, '\033[41m')

    # check current proxy with check url
    try:
        response = requests.get(
            check_url,
            headers = header_info,
            proxies = proxy_info,
            allow_redirects = False,
            timeout=30
        )
    except Exception as e:
        error_logger('Failed to connect to check URL')
        print(e)
        return False
    
    # show response
    if (response.status_code == 200):
        info_logger(str(response.status_code), '\033[32m')
    else:
        info_logger(str(response.status_code))
        return False

    return True


def check_proc(proxy_list_file, proxy_success_list, check_url, header_referer = '', header_host = ''):
    # show information
    info_logger('=====================================================')
    info_logger('Check process start with following parameters')
    info_logger('Proxy List File: ' + proxy_list_file)
    info_logger('Proxy List Save Path: ' + proxy_success_list)
    info_logger('')
    info_logger('Check URL: ' + check_url)
    info_logger('Header Referer: ' + header_referer)
    info_logger('Header Host' + header_host)
    info_logger('=====================================================')

    # prepare export list file
    export_file = open(proxy_success_list, mode = 'a+', encoding = 'utf-8')
    export_file.seek(0, 2)

    # prepare request header
    header_info = requests.utils.default_headers()
    header_info['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36 Edg/110.0.1587.46'
    if ((header_referer != '') and (len(header_referer) > 0)):
        header_info['Referer'] = header_referer
    if ((header_host != '') and (len(header_host) > 0)):
        header_info['Host'] = header_host

    # load proxy list file
    proxy_list_file = open(proxy_list_file, mode = 'r', encoding = 'utf-8')
    proxy_list_reader = csv.DictReader(proxy_list_file)

    # initialize count variables
    total_count = 0
    success_count = 0

    # scan all proxies
    for proxy_info_dict in proxy_list_reader:
        # prepare proxy address
        proxy_info = dict(proxy_info_dict)
        proxy_url = proxy_info['Protocol'] + '://' + proxy_info['IP'] + ':' + proxy_info['Port']

        # check proxy
        check_result = check_proxy_ip(proxy_url, check_url, header_info)
        if (check_result == True):
            # save current proxy information
            export_file.write(proxy_url + '\n')

            # increase success count
            success_count += 1

        # increase total count
        total_count += 1

        # add line space
        info_logger('*****************************************************')

    # show information
    info_logger('Total Count: ' + str(total_count))
    info_logger('Success Count: ' + str(success_count))
