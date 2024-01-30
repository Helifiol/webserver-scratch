import socket, re, os

PORT = 8080

s = socket.socket()
print("Socket created")

s.bind(('127.0.0.1', PORT))
print(f"Socket bound to IP: 127.0.0.1 on port {PORT}")

s.listen(4)
print("Listening")

#creating a response
def create_response(file, code):
    if code == 200:
        response = f"HTTP/1.1 {code} OK\r\n"
        response += "Content-Type: text/html\r\n"
        response += f"Content-Length: {os.path.getsize(file)}\r\n\r\n"
        with open(file, 'r') as content:
            response += content.read()
        return response
    elif code == 404:
        content = "<h1>page not found</h1>"
        response = f"HTTP/1.1 {code} OK\r\n"
        response += "Content-Type: text/html\r\n"
        response += f"Content-Length: {len(content)}\r\n\r\n"
        response += content
        return response

def send_file(file_name):
    if os.path.exists(file_name):
        return True
    else:
        return False

#analyze requests
class analyze_reqests:
    def __init__(self, data):
        self.data = data

    def analyze_req(self):
        decoded_data = self.data.decode("utf-8").replace('\r', '').split("\n")

        self.request_url = decoded_data[0]
        print("request url: " + self.request_url)

        pattern = self.request_url.split(" ")
        self.request_file = pattern[1]
        # self.request_file = pattern[1].replace("/", "")
        print("File name: " + self.request_file)

        parts = self.request_file.split(".")
        request_file_type = parts[-1]
        print("Request file type: " + request_file_type)

        http_protocol = pattern[2]
        print("HTTP protocol: " + http_protocol)

        request_method = pattern[0]
        print("request method: " + request_method)




while True:
    conn, addr = s.accept()
    with conn:
        print(f"Connected by {addr}")

        incomming_data = b''
        while True:
            data = conn.recv(1024)
            if not data:
                break
            incomming_data += data
            # print(data)

            print("-------------")
            req = analyze_reqests(incomming_data)
            req.analyze_req()

            if req.request_file == '/':
                filename = 'index.html'
            else:
                filename = req.request_file.lstrip('/')
            
            print(filename)

            if send_file(filename):
                data = create_response(filename, 200)
            else:
                data = create_response("not-found.html", 404)

            conn.sendall(data.encode('utf-8')) 
            incomming_data = b''
 

