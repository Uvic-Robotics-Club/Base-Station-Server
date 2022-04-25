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
    });
}, 1000);

/* Event listener for user clicking joystick initialize button */
//document.getElementById('drivetrain-joystick-initialize-btn').addEventListener('click', function() {
//    const fetch_promise = fetch('/api/joystick/initialize');
//});

/* Event listener for user clicking joystick teardown button */
//document.getElementById('drivetrain-joystick-teardown-btn').addEventListener('click', function() {
//    const fetch_promise = fetch('/api/joystick/teardown');
//});

/* Initialize joystick thread */
// const initialize_joystick_fetch_promise = fetch('/api/joystick/initialize');