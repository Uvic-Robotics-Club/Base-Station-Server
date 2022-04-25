/* Update drivetrain component */
let update_drivetrain_status = function() {
    let joystick_status = state['drivetrain_joystick_status'];
    let joystick_speed_left = state['drivetrain_joystick_speed_left'];
    let joystick_speed_right = state['drivetrain_joystick_speed_right'];
    let joystick_direction_left = state['drivetrain_joystick_direction_left'];
    let joystick_direction_right = state['drivetrain_joystick_direction_right'];

    /* Update joystick status element */
    let joystick_status_element = document.getElementById('drivetrain-joystick-status');
    if (joystick_status == null ||  joystick_status == undefined) {
        joystick_status_element.innerHTML = 'N/A';
    } else if (joystick_status == 'uninitialized') {
        joystick_status_element.className = 'badge bg-danger'
        joystick_status_element.innerHTML = 'Uninitialized';
    } else if (joystick_status == 'initialized') {
        joystick_status_element.className = 'badge bg-success';
        joystick_status_element.innerHTML = 'Initialized';
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
};