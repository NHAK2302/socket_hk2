import socket
import time
#get ip
def sendFile_CTE(file_name,stream):
    file=open(file_name,"rb")
    while True:
        chunk = file.read(65536)
        stream.sendall(bytes("%s\r\n" % hex(len(chunk))[2:],"utf8"))
        #print(bytes("%s\r\n" % hex(len(chunk))[2:],"utf8"))#debug
        chunk+=bytes("\r\n","utf8")
        stream.sendall(chunk)
        #print(chunk)#debug
        if len(chunk) == 2: #string only has 2 char "\r\n", that is empty string : break out
            break
        #time.sleep(1)#debug

    #CTE flow ends with 2 character "\r\n"
    stream.send(bytes("\r\n","utf8"))

hostname = socket.gethostname()
host = socket.gethostbyname(hostname)
#Set up socket and listen
server = socket.socket()
server.bind((host,80))
print("ip : ",host)
server.listen(1)
#receive message from client
while True:
    #set up new socket (vanish after this loop)
    stream,addr=server.accept()

    #receive request from client by new socket
    request=stream.recv(10000)
    #print(request)#debug
    #Process the request
    request=request.decode()
    request_lines=request.splitlines()
    print(request) #debug
    #Ignore ACK-NAK whose length is 1
    if(len(request_lines)<=1): 
        continue
    #Method is word [0] at line [0] in the request
    method = request_lines[0].split(' ')[0]
    if(method == "GET"):
        file_name=request_lines[0].split(' ')[1]
        file_name=file_name.split('/')[1]
        if(file_name==""):
            file_name="index.html"
        # file=open(file_name,"rb")
        # response_data=file.read()
        response_head="HTTP/1.1 200 OK\n"
    elif(method == "POST"):
        message = request[-1]
        print(message)
        header = '''HTTP/1.1 301 Moved Permanently\nLocation:/post.html'''
        stream.send(header.encode())
        stream.close()
        continue
    if(file_name.endswith(".html")):
        response_head+="Content-Type: text/html\n"
    elif(file_name.endswith(".png")):
        response_head+="Content-Type: image/png\n"
    response_head +="Transfer-Encoding: chunked\n\n"
    #print(response_head.encode())
    stream.send(response_head.encode())
    sendFile_CTE(file_name,stream)
    stream.close()

