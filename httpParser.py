

def parseHttpResponse(text):
    lines = text.split('\n')
    statusRaw, lines = lines[0], lines[1:]
    protocol, statusCode, message = statusRaw.split(' ')
    emptyIndex = 1
    headers = {}
    for index, line in enumerate(lines):
        line = line.strip()
        line = line.strip('\r')
        if line == '':
            emptyIndex = index
            break
        k, _, v = line.partition(':')
        headers.setdefault(k.strip(), v.strip())
    content = ''.join(lines[emptyIndex + 1:])
    return int(statusCode), headers, content


def parseHttpRequests(text):
    lines = text.split('\n')
    prefaceRaw, lines = lines[0], lines[1:]
    method, requestURL = prefaceRaw.split(' / ')
    emptyIndex = 1
    headers = {}
    for index, line in enumerate(lines):
        line = line.strip()
        line = line.strip('\r')
        if line == '':
            emptyIndex = index
            break
        k, _, v = line.partition(':')
        headers.setdefault(k.strip(), v.strip())
    content = ''.join(lines[emptyIndex + 1:])
    return method, requestURL, headers, content




