def remote_address(request):
    peername = request.transport.get_extra_info('peername')
    host, port = peername
    return host
