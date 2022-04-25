let state = {};

/* Fetch application state and update */
let update_state = setInterval(function() {
    const fetch_promise = fetch('/ui/get_state');
    fetch_promise.then(response => {
        return response.json();
    }).then(data => {
        state = data;
        
        /* Update joystick component */
        update_joystick();
    });
}, 2000);