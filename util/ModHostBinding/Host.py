from Connection import Connection

class Host:
    connection = None
    connectionFd = None
    
    plugins = None

    def __init__(self):
        # mod-host works only exists 2 connections:
        #  - For comunication
        self.connection = Connection(5555)
        ##  - For callback?
        self.connectionFd = Connection(5556)
        
        self.plugins = []

    def add(self, plugin):
        plugin.instanceNumber = plugins.size()
        self.plugins.add(plugin)

        self.connection.send(ProtocolParser.add(plugin))
    
    def connectInputIn(self, plugin):
        if plugin not in self.plugins:
            raise Exception("Plugin " + plugin.getLv2Uri() + " has'nt added!")
        
        self.connection.send(ProtocolParser.connectInputIn(plugin))
    
    def connectOnOutput(self, plugin):
        if plugin not in self.plugins:
            raise Exception("Plugin " + plugin.getLv2Uri() + " has'nt added!")
        
        self.connection.send(ProtocolParser.connectOnOutput(plugin))

    
    def connect(self, plugin, anotherPlugin):
        if (plugin not in self.plugins) or (anotherPlugin not in self.plugins):
            raise Exception("An plugin has'nt added!")
        
        self.connection.send(ProtocolParser.connect(plugin, anotherPlugin))


    def disconnect(self, plugin, anotherPlugin):
        if (plugin not in self.plugins) or (anotherPlugin not in self.plugins):
            raise RuntimeException("Has a plugin not added!")

        self.connection.send(ProtocolParser.disconnect(effect, anotherEffect))

Host()