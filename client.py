import socket
import time
import os
import sys

def receive_file():
    try:
        os.mkdir("remote_folder")
    except FileExistsError:
        pass

    // get the IP address of the server
    var ip_address = document.getElementById("ip_address").value;

    // set the port number
    var port = 1234;

    while (true) {
        time.sleep(0.1);
        // create a socket object
        var s = new WebSocket("ws://" + ip_address + ":" + port);

        s.onopen = function(event) {
            console.log("Connected to server.");
            // send a "hey" message to the server
            var message = "hey";
            s.send(message);
        };

        s.onmessage = function(event) {
            var received_filename = event.data;
            // receive the file data
            s.onmessage = function(event) {
                var file_data = event.data;
                // write the file data to a file
                var file_path = "remote_folder/" + received_filename;
                var file = new Blob([file_data], {type: 'text/plain'});
                var url = URL.createObjectURL(file);
                var a = document.createElement("a");
                a.href = url;
                a.download = received_filename;
                document.body.appendChild(a);
                a.click();
                document.body.removeChild(a);
                console.log(received_filename + " file synced");
            };
        };
    }
}

if (typeof module !== 'undefined') {
    module.exports = { receive_file };
}
