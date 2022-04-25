let connected_joysticks = {};

/* Update joystick component in settings page */
let update_joystick = function() {
    let joystick_table_element = document.getElementById('settings-joystick-table');
    
    // Fetch all connected joysticks
    const fetch_promise = fetch('/api/joystick/get_connected_joysticks');
    fetch_promise.then(response => {
        return response.json();
    }).then(data => {
        // If new response is different from last response, then a joystick may have been 
        // connected or disconnected.
        if (JSON.stringify(connected_joysticks) === JSON.stringify(data)) return;
        connected_joysticks = data;

        // Clear table before populating with connected joysticks
        joystick_table_element.innerHTML = '';
        
        // For each joystick, add a new row with device index, name, and options.
        for (const [device_index, device_values] of Object.entries(data)) {
            var device_name = device_values['name'];
            var device_controls_drivetrain = device_values['controls_drivetrain'];
            var device_controls_arm = device_values['controls_arm'];

            var new_row = joystick_table_element.insertRow();

            // Device index
            var device_index_cell = new_row.insertCell();
            var device_index_text = document.createTextNode(device_index);
            device_index_cell.appendChild(device_index_text);

            // Device name
            var device_name_cell = new_row.insertCell();
            var device_name_text = document.createTextNode(device_name);
            device_name_cell.appendChild(device_name_text);

            // Drivetrain check box
            var drivetrain_checkbox_cell = new_row.insertCell();
            // If joystick controls drivetrain, then make check box checked
            var drivetrain_checkbox_status = device_controls_drivetrain ? 'checked': '';
            drivetrain_checkbox_cell.innerHTML = '<div class="form-check form-switch"><input class="form-check-input drivetrain-check-switch" type="checkbox"' + drivetrain_checkbox_status + ' aria-device-index=' + device_index + ' aria-device-name="' + device_name + '"></div>';

            // Arm check box
            var drivetrain_checkbox_cell = new_row.insertCell();
            // If joystick controls arm, then make check box checked
            var arm_checkbox_status = device_controls_arm ? 'checked': '';
            drivetrain_checkbox_cell.innerHTML = '<div class="form-check form-switch"><input class="form-check-input arm-check-switch" type="checkbox"' + arm_checkbox_status + ' aria-device-index=' + device_index + ' aria-device-name="' + device_name + '"></div>';
        }

        /* Add event listener to drivetrain check switches, which are 
           switched when a user wants to start using a joystick either 
           as a drivetrain or arm controller */
        var drivetrain_check_switches = document.getElementsByClassName('drivetrain-check-switch');
        for (var i=0; i<drivetrain_check_switches.length; i++) {
            drivetrain_check_switches[i].addEventListener('click', function() {
                let device_index = this.getAttribute('aria-device-index');
                let device_name = this.getAttribute('aria-device-name');
                let is_checked = this.checked;

                // Send request for joystick to start controlling drive train
                if (is_checked) {
                    const fetch_promise = fetch('/api/joystick/start_drivetrain_joystick?device_index=' + device_index + '&name=' + device_name);
                    fetch_promise.then(response => {
                        return response.json();
                    }).then(data => {
                        message = data['message'];
                        status = data['status'];
                        if (status != 'success') alert('Message: ' + message + '\nStatus: ' + status);
                    }); 
                } else {
                    const fetch_promise = fetch('/api/joystick/stop_drivetrain_joystick');
                    fetch_promise.then(response => {
                        return response.json();
                    }).then(data => {
                        message = data['message'];
                        status = data['status'];
                        if (status != 'success') alert('Message: ' + message + '\nStatus: ' + status);
                    });                     
                }
            });
        }

        /* Add event listener to arm check switches, which are switched
           when a user wants to start using a joystick either as a drivetrain
           or arm controller */
        var arm_check_switches = document.getElementsByClassName('arm-check-switch');
        for (var i=0; i<arm_check_switches.length; i++) {
            arm_check_switches[i].addEventListener('click', function() {
                let device_index = this.getAttribute('aria-device-index');
                let device_name = this.getAttribute('aria-device-name');
                let is_checked = this.checked;

                // Send request for joystick to start controlling arm
                if (is_checked) {
                    const fetch_promise = fetch('/api/joystick/start_arm_joystick?device_index=' + device_index + '&name=' + device_name);
                    fetch_promise.then(response => {
                        return response.json();
                    }).then(data => {
                        message = data['message'];
                        status = data['status'];
                        if (status != 'success') alert('Message: ' + message + '\nStatus: ' + status);
                    }); 
                } else {
                    const fetch_promise = fetch('/api/joystick/stop_arm_joystick');
                    fetch_promise.then(response => {
                        return response.json();
                    }).then(data => {
                        message = data['message'];
                        status = data['status'];
                        if (status != 'success') alert('Message: ' + message + '\nStatus: ' + status);
                    });                     
                }
            });
        }
    });
}