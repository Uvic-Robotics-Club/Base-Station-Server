let settings = {};
let state = {};

/* Fetch application state and update.
   Also fetch base station settings */
let update_state = setInterval(function() {
    const fetch_promise = fetch('/ui/get_state');
    fetch_promise.then(response => {
        return response.json();
    }).then(data => {
        state = data;
        
        /* Update joystick component */
        update_joystick();

        /* Update settings config values */
        update_settings_config();
    });
}, 1000);