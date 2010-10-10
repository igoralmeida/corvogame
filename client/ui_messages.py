def logon(user):
    return {u'action': 'logon', u'user': user}

def logout(user):
    return {u'action': 'logout', u'user': user}

def enable_chat():
    return {u'action': 'enable_chat'}

def chat_received(user, msg):
    return {u'action': 'chat', u'sender': user, u'message': msg}

def connection(status):
    ''' Possible 'status' values:
        init
        established
        off
    '''
    # TODO this will probably change A LOT
    if status not in ['init', 'established', 'off']:
        raise ValueError

    return {u'action': 'connection', u'status': status}
