from logproc import info_logger


def check_proc(proxy_list_file, proxy_success_list):
    info_logger('Check process start with following parameters')
    info_logger('Proxy List File: ' + proxy_list_file)
    info_logger('Proxy List Save Path: ' + proxy_success_list)
    