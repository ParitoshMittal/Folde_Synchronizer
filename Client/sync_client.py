import socket
import time
import os


def receive_file():
    try:
        os.mkdir("remote_folder")
    except FileExistsError:
        pass

    # get the IP address of the server
    host = input("Enter IP address of server: ")

    # set the port number
    port = 1234

    while True:
        time.sleep(0.1)
        # create a socket object
        s = socket.socket()

        # connect to the server
        s.connect((host, port))

        # print("Connected to server")
        path = './remote_folder'

        # receive the "hey" received_filename from the server
        received_filename = s.recv(1024)

        # print("received_filename: {}".format(received_filename.decode()))

        # receive the file data
        file_data = s.recv(1024)

        # write the file data to a file
        with open(os.path.join(path, received_filename.decode()), "wb") as f:
            f.write(file_data)

        print(f"\n{received_filename.decode()} file synced\n")

        # close the connection
        s.close()


if __name__ == '__main__':
    # call the function to receive the file
    receive_file()