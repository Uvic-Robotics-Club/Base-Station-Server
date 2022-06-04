current_settings = {};

/* Maps name of settings returned from server to name that will be shown to the user. This
   is for readability. */
settings_name_mapping = {
    'port_base_station_udp_video': 'UDP Video Port',
    'timeout_ping_sec': 'Rover Ping Timeout (sec)',
    'timeout_send_command_sec': 'Rover Command Timeout (sec)',
    'timeout_request_connection_sec': 'Rover Request Timeout (sec)',
    'healthcheck_timeout_rover_connection_sec': 'Rover Connection Timeout (sec)',
    'healthcheck_interval_rover_ping_sec': 'Rover Health Check Request Interval (sec)'
}

/* Update settings configuration values */
let update_settings_config = function() {
    let settings_form = document.getElementById('settings-config-form');    

    /* Fetch base station settings */
    const fetch_settings_promise = fetch('/ui/get_settings');
    fetch_settings_promise.then(response => {
        return response.json();
    }).then(data => {
        // If new response is different from last response, then a setting 
        // most likely has changed.
        if (JSON.stringify(current_settings) === JSON.stringify(data)) return;
        current_settings = data;

        // Clear all existing settings rows
        settings_form.innerHTML = '';
        for (const [setting_name, setting_value] of Object.entries(current_settings)) {
            settings_form.innerHTML+='<div class="row mb-3"><label for="settings_' + setting_name + '" class="col-sm-2 col-form-label">' + settings_name_mapping[setting_name] + '</label><div class="col-sm-10"><input class="form-control setting-value-input" aria-setting-name="' + setting_name + '" value="' + setting_value + '"></div></div>';
        }
    });
};

/* Event listener for user submitting setting changes */
document.getElementById('settings-config-submit').addEventListener('click', function() {
    // Select all input elements containing setting values
    let setting_inputs = document.getElementsByClassName('setting-value-input');

    // For each setting, build URL to change base station setting values
    let request_url = '/ui/change_settings?';
    for (let i=0; i<setting_inputs.length; i++) {
        let setting_input = setting_inputs[i];
        let setting_name = setting_input.getAttribute('aria-setting-name');
        let setting_value = setting_input.value;

        // Append setting name and value to request as GET parameter
        request_url+=setting_name+'='+setting_value+'&';
    }

    // Send request to change settings.
    const fetch_promise = fetch(request_url);
    fetch_promise.then(response => {
        return response.json();
    }).then(data => {
        message = data['message'];
        status = data['status'];
        alert('Message: ' + message + '\nStatus: ' + status);
    }); 
});