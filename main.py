# Python 3 server example
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse
from urllib.parse import parse_qs
import time
from pprint import pprint

hostName = "localhost"
serverPort = 8080

class proglogic():
    """This is the game logic, which also controls the LED-lights"""

    count_debug=0
    
    def __init__(self):
        self.count_debug=0

    def tooglePlayersLight(self, on, id):
        """ This will toggle a players light (determined by id) On (if true) or off"""
        return

    def setPlayerName(self, name, id):
        """This will set the players name"""
        print("Name: " + name)  # DEBUG
        print("id: " + id)  # Debug
        print("Debug: " + str(self.count_debug))  # DEBUG
        self.count_debug+=1
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
            self.send_response(200)          
            if ('?' in self.path):
                    qs = {}
                    path, tmp = self.path.split('?', 1)                    
                    qs = parse_qs(tmp)
                    # print("Path: " + path)  # Debug
                    #print("qs: " + str(qs))  # Debug
                    if (qs['job'] is None):
                        print("Job-variable not set!")  # DEBUG
                        return  # Job is not set
                    if (qs['job'][0] == "setplayer"):
                        # Set Playersname
                        # self.setPlayerName(qs['name'][0], qs['id'][0])  # Need a way to access the other class's object
                        pass
            return
        else:
            self.send_response(403)
            self.wfile.write(bytes("403: You don't have access here. Try accessing '/' instead.", "utf-8"))
            return

     

if __name__ == "__main__":        
    gamelogic = proglogic()

    webServer = HTTPServer((hostName, serverPort), MyRequestHandler)    
    print("Server started http://%s:%s" % (hostName, serverPort))    

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")

