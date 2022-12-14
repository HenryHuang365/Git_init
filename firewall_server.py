# www.theforage.com - Telstra Cyber Task 3
# Firewall Server Handler

from http.server import BaseHTTPRequestHandler, HTTPServer
import time

host = "localhost"
port = 8000

#########
# Handle the response here 
def block_request(self):
    # This is the attacking HTTP request headers
    # This is also a filter condition
    Attack_headers_payload = {
        "suffix": "%>//",
        "c1": "Runtime",
        "c2": "<%",
        "DNT": "1",
        "Content-Type": "application/x-www-form-urlencoded",
    }

    # Loop through every keys in the attacking header payload
    for key in Attack_headers_payload.keys():
        # If a key is in the requesting header payload
        # Check if the key is matching with the attacking header payload key
        if key in self.headers:
            if self.headers[key] == Attack_headers_payload[key]:
                # Block request and throw 403 error
                self.send_error(403, "This request has been blocked.\n")
                print("Blocking request")
        else: 
            continue



def handle_request(self):
    # Find out requests that have same path in the firewall logs
    # These requeses need to be blocked
    if self.path == "/tomcatwar.jsp":
        return block_request(self)

    # Return successful response
    self.send_response(200)
    self.send_header("content-type", "application/json")
    self.end_headers()
    self.wfile.write(bytes("<p>This HTTP request passes through the firewall.</p>", "utf-8"))

    


    
#########


class ServerHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        handle_request(self)

    def do_POST(self):
        handle_request(self)

if __name__ == "__main__":        
    server = HTTPServer((host, port), ServerHandler)
    print("[+] Firewall Server")
    print("[+] HTTP Web Server running on: %s:%s" % (host, port))

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass

    server.server_close()
    print("[+] Server terminated. Exiting...")
    exit(0)