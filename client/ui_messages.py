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

def user_list(user_dicts):
    return {u'action': 'user_list', u'dicts': user_dicts}

def room_list(room_dicts):
    return {u'action': 'room_list', u'dicts': room_dicts}

def request_rooms():
    return {u'action': 'request', u'value': 'rooms'}

def request_users():
    return {u'action': 'request', u'value': 'users'}

