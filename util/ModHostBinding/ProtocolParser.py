'''
Prepare the objects to <a href="https://github.com/moddevices/mod-host">mod-parse</a>
string command
'''
class ProtocolParser:
    
    '''
    add <lv2_uri> <instance_number>
    
    add a LV2 plugin encapsulated as a jack client
    e.g.: add http://lv2plug.in/plugins/eg-amp 0
    instance_number must be any value between 0 ~ 9999, inclusively
    '''
    @staticmethod
    def add(plugin):
        return "add " + plugin.getLv2Uri() + " " + plugin.getInstanceNumber()

    '''
    remove <instance_number>
    
    remove a LV2 plugin instance (and also the jack client)
    e.g.: remove 0
    '''
    @staticmethod
    def remove(plugin):
        return "remove " + plugin.getInstanceNumber()

    '''
    Connect system input in 'plugin'
    '''
    @staticmethod
    def connectInputIn(plugin):
        return "connect system:capture_1 " + getInNameOf(plugin)

    
    '''
    Connect plugin on output
    '''
    @staticmethod
    def connectOnOutput(plugin):
        return "connect " + getOutNameOf(plugin) + " system:playback_1"

    
    '''
    Connect 'plugin' in 'anotherPlugin'
    
    connect <origin_port> <destination_port>
    
    connect two plugin audio ports
    e.g.: connect system:capture_1 plugin_0:in
    '''
    @staticmethod
    def connect(plugin, anotherPlugin):
        return "connect " + getOutNameOf(plugin) + " " + getInNameOf(anotherPlugin)

    #@privatemethod
    @staticmethod
    def getOutNameOf(plugin):
        Lv2Port output = plugin.getPorts(Lv2PortType.AudioPort, Lv2PortType.OutputPort).get(0)
        return plugin.getName() + ":" + output.getSymbol()

    #@privatemethod
    @staticmethod
    def getInNameOf(plugin):
        Lv2Port input  = plugin.getPorts(Lv2PortType.AudioPort, Lv2PortType.InputPort).get(0)
        return plugin.getName() + ":" + input.getSymbol()


    '''
    disconnect <origin_port> <destination_port>
    
    disconnect two plugin audio ports
    e.g.: disconnect system:capture_1 plugin_0:in
   '''
    @staticmethod
    def disconnect(plugin, anotherPlugin):
        return "disconnect " + getOutNameOf(plugin) + " " + getInNameOf(anotherPlugin)


    '''
    preset_load <instance_number> <preset_uri>
    
    load a preset state to given plugin instance
    e.g.: preset_load 0 "http://drobilla.net/plugins/mda/presets#JX10-moogcury-lite"
    '''
    @staticmethod
    def presetLoad():
        return null


    '''
    preset_save <instance_number> <preset_name> <dir> <file_name>
    
    save a preset state from given plugin instance
    e.g.: preset_save 0 "My Preset" /home/user/.lv2/my-presets.lv2 mypreset.ttl
    '''
    @staticmethod
    def presetSave():
        return null


    '''
    preset_show <instance_number> <preset_uri>
    
    show the preset information of requested instance / URI
    e.g.: preset_show 0 http://drobilla.net/plugins/mda/presets#EPiano-bright
    '''
    def presetShow():
        return null


    '''
    param_set <instance_number> <param_symbol> <param_value>
    
    set a value to given control
    e.g.: param_set 0 gain 2.50
    '''
    @staticmethod
    def paramSet():
        return null


    '''
    param_get <instance_number> <param_symbol>
    
    get the value of the request control
    e.g.: param_get 0 gain
    '''
    @staticmethod
    def paramGet():
        return null


    
    '''
    param_monitor <instance_number> <param_symbol> <cond_op> <value>
    
    do monitoring a plugin instance control port according given condition
    e.g: param_monitor 0 gain > 2.50
    '''
    @staticmethod
    def paramMonitor():
        return null


    '''
    monitor <addr> <port> <status>
    
    open a socket port to monitoring parameters
    e.g: monitor localhost 12345 1
    if status = 1 start monitoring
    if status = 0 stop monitoring
    '''
    @staticmethod
    def monitor():
        return null


    '''
    public enum PluginStatus:
        BYPASS(1),
        PROCESS(0)
        
        private int status

        private PluginStatus(int status):
            this.status = status
    
        
        public int getStatus():
            return status
    '''

    '''
    bypass <instance_number> <bypass_value>
    
    toggle plugin processing
    e.g.: bypass 0 1
    if bypass_value = 1 bypass plugin
    if bypass_value = 0 process plugin
    '''
    @staticmethod
    def bypass(plugin, status):
        return "bypass " + status.getStatus()

    '''
    load <file_name>
    
    load a history command file
    dummy way to save/load workspace state
    e.g.: load my_setup
    '''
    @staticmethod
    def load():
        return null

    '''
    save <file_name>
    
    saves the history of typed commands
    dummy way to save/load workspace state
    e.g.: save my_setup 
    '''
    @staticmethod
    def save(filename):
        return "save " + filename

    '''
    help
    
    show a help message
    '''
    @staticmethod
    def help():
        return "help"

    '''
    quit
    
    bye!
    '''
    @staticmethod
    def quit():
        return "quit"