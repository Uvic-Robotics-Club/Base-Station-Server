/* Update connection manager asynchronously. */
let update_conn_manager = function() {
    let connection_established = state['connection_established'];

    /* Update IP address if connected */
    let ip_address_element = document.getElementById('conn-manager-address');
    if (connection_established == true) {
        ip_address_element.disabled = true;
        ip_address_element.value = state['connection_remote_addr'];
    } else {
        ip_address_element.disabled = false;
    }

    /* Update port if connected */
    let port_element = document.getElementById('conn-manager-port');
    if (connection_established == true) {
        port_element.disabled = true;
        port_element.value = state['connection_port'];
    } else {
        port_element.disabled = false;
    }

    /* Update connect button */
    let connect_button_element = document.getElementById('conn-manager-connect-btn');
    if (connection_established == true) {
        connect_button_element.className = 'btn btn-primary disabled';
    } else {
        connect_button_element.className = 'btn btn-primary';
    }

    /* Update disconnect button */
    let disconnect_button_element = document.getElementById('conn-manager-disconnect-btn');
    if (connection_established == true) {
        disconnect_button_element.className = 'btn btn-danger';
    } else {
        disconnect_button_element.className = 'btn btn-danger disabled';
    }
};

/* Event listener for user clicking connect button */
document.getElementById('conn-manager-connect-btn').addEventListener('click', function() {
    const address_value = document.getElementById('conn-manager-address').value;
    const port_value = document.getElementById('conn-manager-port').value;

    /* Validate that address and port are not empty and of correct format */
    if (address_value.length == 0) {
        alert('Address must not be empty.');
        return;
    }

    if (port_value.length == 0) {
        alert('Port must not be empty.');
        return;
    }

    const fetch_promise = fetch('/api/rover/connect?remote_addr=' + address_value + '&port=' + port_value);
    fetch_promise.then(response => {
        return response.json();
    }).then(data => {
        message = data['message'];
        status = data['status'];
        if (status != 'success') alert('Message: ' + message + '\nStatus: ' + status);
    });
});

/* Event listener for user clicking disconnect button */
document.getElementById('conn-manager-disconnect-btn').addEventListener('click', function() {
    const fetch_promise = fetch('/api/rover/disconnect');
});