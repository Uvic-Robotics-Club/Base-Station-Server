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