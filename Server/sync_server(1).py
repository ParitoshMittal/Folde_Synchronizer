import socket
import os

try:
    os.mkdir("server_folder")
except FileExistsError:
    pass


def send_file():
    # get the IP address of the local host
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    host = s.getsockname()[0]
    s.close()
    # set the port number
    port = 1234

    # create a socket object
    s = socket.socket()

    # bind the socket to a public host and port
    s.bind((host, port))

    # listen for incoming connections
    s.listen(5)

    print(f"\nServer listening on {host}:{port}\n")
    print(f"\n\nAddress of server: {host}\n")
    path = './server_folder'
    file_dict = {}

    while True:
        update = []
        new_dict = {}
        for dirpath, dirnames, filenames in os.walk(path):
            for filename in filenames:
                file_path = os.path.join(dirpath, filename)
                modified_time = os.path.getmtime(file_path)
                new_dict[file_path] = [modified_time, filename]
        # print(new_dict)
        for file_path, modified_time in new_dict.items():
            if file_path not in file_dict:
                print(f"{file_path} has been created")
                update.append(os.path.basename(file_path))
            elif modified_time > file_dict[file_path]:
                print(f"{file_path} has been modified")
                update.append(os.path.basename(file_path))

        # for file_path in file_dict:
        #     if file_path not in new_dict:
        #         print(f"{file_path} has been deleted")

        file_dict = new_dict

        for filename in update:
            # establish a connection
            conn, addr = s.accept()

            # print("Connected to client: ", addr)

            # send a "hey" message to the client
            message = filename
            conn.sendall(message.encode())

            # open the file in binary mode
            with open(os.path.join(path, filename), "rb") as f:
                # read the contents of the file
                file_data = f.read()

            # send the file data to the client
            conn.sendall(file_data)

            print(f"\n{filename} file synced\n")

            # close the connection
            conn.close()
        #update=[]


if __name__ == '__main__':
    # call the function to send the file
    send_file()