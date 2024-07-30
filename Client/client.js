function start_server() {
    // prevent the form from submitting
    event.preventDefault();
    var ip_address = document.getElementById("ip_address").value;
    var log = document.getElementById("log");

    // create a WebSocket connection to the server
    var ws = new WebSocket("ws://" + ip_address + ":5000/log");

    // log any messages received from the server
    ws.onmessage = function(event) {
        var p = document.createElement("p");
        p.innerText = event.data;
        log.appendChild(p);
    };

    // send a "start_server" message to the server
    ws.onopen = function(event) {
        ws.send("start_server");
        var p = document.createElement("p");
        p.innerText = "Server started";
        log.appendChild(p);
        receive_file();
    };

    // return false to prevent the form from submitting
    return false;
}
