import time

class MockSession (object):
  def __init__(self, username):
    self.received_messages = {}
    self.username = username
    self.data_holder = {}
    
  def __setitem__(self, key, value):
    #print 'setitem {0} {1}'.format(key, value)
    self.data_holder[key] = value
  
  def __getitem__(self, key):
    #print 'getitem {0}'.format(key)
    
    if key in self.data_holder:
      return self.data_holder[key]
      
    raise StopIteration
  
  def __contains__(self, item):
    return item in self.data_holder
  
  def expect(self, action):
    for i in xrange(10):
      if action not in self.received_messages.keys():
        time.sleep(0.1)
      else:
        return self.received_messages[action]
    
    raise Exception(action)
    
  def purge(self):
    self.received_messages = {}
  
  def write(self, message):
    self.received_messages[message['action']] =  message
    
  def __str__(self):
    return 'MockSession [{0}]'.format(self.username)