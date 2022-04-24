let state = {};

/* Update connection status asynchronously. */
let update_conn_status = function() {
    /* Update connection status elements */

    /* Update connection status */
    let conn_established = state['connection_established'];
    let conn_status_element = document.getElementById('conn-status');
    if (conn_established == true) {
        conn_status_element.className = 'badge bg-success';
        conn_status_element.innerHTML = 'Connected';
    } else {
        conn_status_element.className = 'badge bg-danger';
        conn_status_element.innerHTML = 'Not Connected';
    }

    /* Update connection ID */
    let conn_id = state['connection_id'];
    let conn_id_element = document.getElementById('conn-id');
    if (conn_id != null) {
        conn_id_element.innerHTML = conn_id;
    } else {
        conn_id_element.innerHTML = 'N/A';
    }
    
    /* Update remote address */
    let conn_remote_addr = state['connection_remote_addr'];
    let conn_remote_addr_element = document.getElementById('conn-remote-addr');
    if (conn_remote_addr != null) {
        conn_remote_addr_element.innerHTML = conn_remote_addr;
    } else {
        conn_remote_addr_element.innerHTML = 'N/A';
    }
    
    /* Update remote port */
    let conn_remote_port = state['connection_port'];
    let conn_remote_port_element = document.getElementById('conn-remote-port');
    if (conn_remote_port != null) {
        conn_remote_port_element.innerHTML = conn_remote_port;
    } else {
        conn_remote_port_element.innerHTML = 'N/A';
    }
    
    /* Update ping status */
    let conn_ping_status = state['connection_ping_status'];
    let conn_ping_status_element = document.getElementById('conn-ping-status');
    if (conn_ping_status == 'healthy') {
        conn_ping_status_element.className = 'badge bg-success';
        conn_ping_status_element.innerHTML = 'Healthy';
    } else if (conn_ping_status == 'unreachable') {
        conn_ping_status_element.className = 'badge bg-warning text-dark';
        conn_ping_status_element.innerHTML = 'Unreachable';
    } else if (conn_ping_status == 'timeout') {
        conn_ping_status_element.className = 'badge bg-danger';
        conn_ping_status_element.innerHTML = 'Timeout';
    } else {
        conn_ping_status_element.className = 'badge bg-dark';
        conn_ping_status_element.innerHTML = 'N/A';          
    }

    /* Update last successful ping timeline */
    let conn_ping_last_response = state['connection_ping_last_response'];
    let conn_ping_last_response_element = document.getElementById('conn-ping-last-response');
    if (conn_ping_last_response != null) {
        current_timestamp_sec = Date.now() / 1000;
        last_response_timestamp = current_timestamp_sec - conn_ping_last_response;
        conn_ping_last_response_element.innerHTML = last_response_timestamp.toFixed(2) + ' s ago';
    }
};

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

/* Update joystick component */
let update_joystick_status = function() {
    let joystick_status = state['joystick_status'];
    let joystick_speed_left = state['joystick_speed_left'];
    let joystick_speed_right = state['joystick_speed_right'];
    let joystick_direction_left = state['joystick_direction_left'];
    let joystick_direction_right = state['joystick_direction_right'];

    /* Update joystick status element */
    let joystick_status_element = document.getElementById('drivetrain-joystick-status');
    if (joystick_status == null ||  joystick_status == undefined) {
        joystick_status_element.innerHTML = 'N/A';
    } else if (joystick_status == 'uninitialized') {
        joystick_status_element.className = 'badge bg-danger'
        joystick_status_element.innerHTML = 'Uninitialized';
    } else if (joystick_status == 'not found') {
        joystick_status_element.className = 'badge bg-warning text-dark';
        joystick_status_element.innerHTML = 'Not Found';
    } else if (joystick_status == 'initialized') {
        joystick_status_element.className = 'badge bg-success';
        joystick_status_element.innerHTML = 'Initialized';
    } else if (joystick_status == 'tearing down') {
        joystick_status_element.className = 'badge bg-secondary';
        joystick_status_element.innerHTML = 'Tearing Down';        
    } else {
        joystick_status_element.className = '';
        joystick_status_element.innerHTML = 'Unrecognized Status';
    }

    /* Update joystick speeds and direction */
    let joystick_speed_left_element = document.getElementById('drivetrain-joystick-speed-left');
    if (joystick_speed_left == null) {
        joystick_speed_left_element.innerHTML = 'N/A';
    } else {
        joystick_speed_left_element.innerHTML = joystick_speed_left;
    }

    let joystick_speed_right_element = document.getElementById('drivetrain-joystick-speed-right');
    if (joystick_speed_right == null) {
        joystick_speed_right_element.innerHTML = 'N/A';
    } else {
        joystick_speed_right_element.innerHTML = joystick_speed_right;
    }

    let joystick_direction_left_element = document.getElementById('drivetrain-joystick-direction-left');
    if (joystick_direction_left == null) {
        joystick_direction_left_element.innerHTML = 'N/A';
    } else {
        joystick_direction_left_element.innerHTML = joystick_direction_left;
    }

    let joystick_direction_right_element = document.getElementById('drivetrain-joystick-direction-right');
    if (joystick_direction_right == null) {
        joystick_direction_right_element.innerHTML = 'N/A';
    } else {
        joystick_direction_right_element.innerHTML = joystick_direction_right;
    }

    /* Update joystick initialize button */
    let joystick_initialize_button_element = document.getElementById('drivetrain-joystick-initialize-btn'); 
    if (joystick_status == 'uninitialized' || joystick_status == 'not found') {
        joystick_initialize_button_element.className = 'btn btn-primary';
    } else {
        joystick_initialize_button_element.className = 'btn btn-primary disabled';
    }

    /* Update joystick teardown button */
    let joystick_teardown_button_element = document.getElementById('drivetrain-joystick-teardown-btn');
    if (joystick_status == 'initialized') {
        joystick_teardown_button_element.className = 'btn btn-danger';
    } else {
        joystick_teardown_button_element.className = 'btn btn-danger disabled';
    }
};

/* Fetch application state and update */
let update_state = setInterval(function() {
    const fetch_promise = fetch('/ui/get_state');
    fetch_promise.then(response => {
        return response.json();
    }).then(data => {
        state = data;
        
        /* Update connection status */
        update_conn_status();

        /* Update connection manager */
        update_conn_manager();

        /* Update joystick status */
        update_joystick_status();
    });
}, 1000);

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

/* Event listener for user clicking joystick initialize button */
document.getElementById('drivetrain-joystick-initialize-btn').addEventListener('click', function() {
    const fetch_promise = fetch('/api/joystick/initialize');
});

/* Event listener for user clicking joystick teardown button */
document.getElementById('drivetrain-joystick-teardown-btn').addEventListener('click', function() {
    const fetch_promise = fetch('/api/joystick/teardown');
});