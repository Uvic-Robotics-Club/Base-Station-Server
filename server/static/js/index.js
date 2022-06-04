let state = {};

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
        update_drivetrain_status();

        /* Update GPS coordinates */
        update_gps();
    });
}, 1000);