# Python 3 web server and light control
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse
from urllib.parse import parse_qs
import time
from events import Events
import lib8relay  # Needed to control the relay-board (via pip3 install lib8relay or https://github.com/SequentMicrosystems/8relay-rpi/tree/master/python)

# hostName = "localhost"  # localhost only
hostName = ""  # Any IP
serverPort = 8080

# Begin: Classes

class proglogic():
    """This is the game logic, which also controls the LED-lights"""

    count_debug=0
    player_names = {}  # Dictionary of the player names
    player_states = {}  # Dictionary of the player (light) states
    
    def __init__(self):
        self.count_debug=0

    def Handle_external_EngineCall(self, request):
        """Will handle EngineCall-Events from MyRequestHandler"""
        # print("Enginecall handled... => " + str(request))  # DEBUG
        if ('?' in request):  # Only do something if variables had been submitted
            qs = {}
            path, tmp = request.split('?', 1)                    
            qs = parse_qs(tmp)
            # print("Path: " + path)  # Debug
            # print("qs: " + str(qs))  # Debug
            if (qs['job'] is None):
                # print("Job-variable not set!")  # DEBUG
                return  # Job is not set
            if (qs['job'][0] == "setplayer" and qs['name'][0] is not None and qs['id'][0] is not None):
                # Set Playersname
                self.setPlayerName(qs['name'][0], qs['id'][0])  # Set player's name in our dictionary
            elif (qs['job'][0] == "enlightplayer" and qs['id'][0] is not None and qs['onoff'][0] is not None and qs['pnum'][0] is not None):
                # we should enable or disable a player's light
                enlighten = False  # should we enlighten the player. If false, the light should turn off
                if qs['onoff'][0] == "light":
                    enlighten = True
                self.tooglePlayersLight(enlighten, qs['id'][0], int(qs['pnum'][0]))
        return

    def tooglePlayersLight(self, on, id, pnum):
        """ This will toggle a players light (determined by id) On (if true) or off"""        
        currentstate = None
        if id in self.player_states.keys():
            # print("The old books told me stories about a hero called " + str(id))  # DEBUG
            currentstate = self.player_states[id]
        else:
            # print("I didn't know about a hero called " + str(id) + " yet. I'll never forget...")
            pass
        
        if currentstate is not None:
            # A previous player state exists
            # print("Light-State-Transition for player \"" + str(id) + "\": " + str(currentstate) + " => " + str(on))  # DEBUG
            if currentstate != on:
                # New state is different than the previous state. We should do something                      
                # as pnum's index is 1-based but the lib8relay-lib is zero-based we need to substract 1 from pnum
                pnum-=1
                # Turn relay's on/off here below. We need to import the libraries for the relay-board
                if on:
                    print("Will bath player " + str(id) + " in the divine light of the builder of the worlds")  # DEBUG
                    try:
                        lib8relay.set(0, pnum, 1)  # Turn relay for the player with the given index ON                    
                    except:
                        print("Error while setting light-state. Is the relay-board connected?")
                else:
                    print("Will drop player " + str(id) + " in eternal darkness.")  # DEBUG
                    try:
                        lib8relay.set(0, pnum, 0)  # Turn relay for the player with the given index OFF
                    except:
                        print("Error while setting light-state. Is the relay-board connected?")
                time.sleep(0.1)  # Give the relay time to change it's state
            else:
                # print("Previous state matches new state. Will not change anything.")  # DEBUG                
                pass
        else:
            # print("Error: Player's state is not set!")  # DEBUG
            pass
        self.player_states.update({id: on})  # Update the states-dictionary. Will add item if new, will update if it exists...
        return

    def setPlayerName(self, name, id):
        """This will add or update the players name"""
        # print("Name: " + name)  # DEBUG
        # print("id: " + id)  # Debug
        # Update the dictionary. Will add item if new, will update if it exists...
        self.player_names.update({id: name})        
        # print(str(self.player_names))  # DEBUG
        return

class MyRequestHandler(BaseHTTPRequestHandler):
    """This is a child of BaseHTTPRequestHandler which will only be alive during an request."""

    def getTextFromFile(self, filename):
        """ Will read a text from a specified file """
        with open(filename, 'r') as myFile:
            return myFile.read()

    def do_GET(self):
        """Will process incoming GET-requests"""
        # print("Got a request...")  # DEBUG
        if self.path == "/":  # If root path - normal webpage
            # Request OK
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            content = self.getTextFromFile("./main.html")  # Serve the main-web-page which includes javascript-logic
            self.wfile.write(bytes(content, "utf-8"))
            return
        elif self.path.startswith("/engine"): # engine-call (used internally)  
            # Request OK
            self.send_response(200)
            self.events.on_enginerequest(self.path)            
            return
        else:
            # Request not OK
            self.send_response(403)
            self.wfile.write(bytes("403: You don't have the right spell to access to this dungeon! Try accessing the main entrance ('/') instead.", "utf-8"))
            return

    def __init__(self, request, client_address, server):
        """Ovewritten/Extended Constructor. Will be called everytime this object is newly instantiated. => on every incoming request."""
        # print("I'm a new request-handler-object...")  # DEBUG
        # Init events
        self.child_request=request
        self.child_client_address=client_address
        self.child_server=server

        # Declare our events, that might be subscribed
        self.events = Events(
            (
                'on_enginerequest'
            )
        )        
     
    def SuperRequestHandler(self):
        """Will instantiate the parents-object, which should allow us to subscribe event after instantiating child-object"""
        super(MyRequestHandler, self).__init__(self.child_request, self.child_client_address, self.child_server)  # Pass all information to the parent's constructor


class MyHTTPServer(HTTPServer):
    """This is a child of HTTPServer which will use MyRequestHandler as the RequestHandler-Class and also implements the programlogic"""
    proglogic=None
    newest_requesthandler=None
    def __init__(self, server_address, proglogic):        
        if (proglogic is None):
            raise("MyHTTPServer: Proglogic is None!")  # Abort here
        else:
            # Use the given logic-instance
            self.proglogic=proglogic                  
            # Create a new server instance            
            super(MyHTTPServer, self).__init__(server_address, MyRequestHandler)  # Pass all information to the partent's constructor
        
     
    def finish_request(self, request, client_address):
        """Overwritten/extended finish_request method (from SocketServer.py) which will normaly invoke a new request-handler-instance"""
        # We need to overwrite this base method in order to inject event-handling here. Original-code is within SocketServer.py from which HTTPServer is derived...             
        self.newest_requesthandler = self.RequestHandlerClass(request, client_address, self) # Imitate parents method which will call the constructor of our Request-Handler-Class 
        # Subscribe Events of the extended Request-Handler here...
        self.newest_requesthandler.events.on_enginerequest += self.proglogic.Handle_external_EngineCall                 
        self.newest_requesthandler.SuperRequestHandler()  # Call our Request-Handler's parent-constructor

# End: Classes


# Main Program:
if __name__ == "__main__":
    gamelogic = proglogic()  # Create a new instance of the gamelogic        
    
    webServer = MyHTTPServer((hostName, serverPort), gamelogic)  # Create a new customized webserver-instance which can access the gamelogic-instance       
    print("Server started http://%s:%s" % (hostName, serverPort))    

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")
    exit(0)

