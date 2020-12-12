# Python 3 server example
from http.server import BaseHTTPRequestHandler, HTTPServer
import time

hostName = "localhost"
serverPort = 8080

class MyServer(BaseHTTPRequestHandler):
    def getTextFromFile(self, filename):
        with open(filename, 'r') as myFile:
            return myFile.read()

    def tooglePlayersLight(self, on, id):
        """ This will toggle a players light (determined by id) On (if true) or off"""
        return

    def do_GET(self):
        if self.path == "/":  # If root path
            # Request OK
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            content = self.getTextFromFile("./main.html")
            self.wfile.write(bytes(content, "utf-8"))
            return
        else:
            self.send_response(403)
            self.wfile.write(bytes("403: You don't have access here. Try accessing '/' instead.", "utf-8"))
            return


if __name__ == "__main__":        
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")

