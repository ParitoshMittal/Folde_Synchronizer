import socket
import os
import logging

logging.basicConfig(filename='server.log', level=logging.INFO)

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

    logging.info(f"Server listening on {host}:{port}")
    logging.info(f"Address of server: {host}")
    path = './server_folder'
    file_dict = {}

    while True:
        update = []
        new_dict = {}
        for dirpath, dirnames, filenames in os.walk(path):
            for filename in filenames:
                file_path = os.path.join(dirpath, filename)
                modified_time = os.path.getmtime(file_path)
                new_dict[file_path] = modified_time
        for file_path, modified_time in new_dict.items():
            if file_path not in file_dict:
                logging.info(f"{file_path} has been created")
                update.append(os.path.basename(file_path))
            elif modified_time > file_dict[file_path]:
                logging.info(f"{file_path} has been modified")
                update.append(os.path.basename(file_path))

        file_dict = new_dict

        for filename in update:
            # establish a connection
            conn, addr = s.accept()

            # send a "hey" message to the client
            message = filename
            conn.sendall(message.encode())

            # open the file in binary mode
            with open(os.path.join(path, filename), "rb") as f:
                # read the contents of the file
                file_data = f.read()

            # send the file data to the client
            conn.sendall(file_data)

            logging.info(f"{filename} file synced")

            # close the connection
            conn.close()

if __name__ == '__main__':
    # call the function to send the file
    send_file()