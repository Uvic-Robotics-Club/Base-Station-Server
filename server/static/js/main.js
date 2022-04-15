
/* Update connection status asynchronously */
let update_conn_status = setInterval(function() {
    const fetch_promise = fetch("/ui/get_connection_status")
    fetch_promise.then(response => {
        return response.json();
    }).then(data => {
        /* Update connection status elements */

        /* Update connection status */
        conn_established = data['connection_established'];
        conn_status_element = document.getElementById('conn-status');
        if (conn_established == true) {
            conn_status_element.className = "badge bg-success";
            conn_status_element.innerHTML = "Connected";
        } else {
            conn_status_element.className = "badge bg-danger";
            conn_status_element.innerHTML = "Not Connected";
        }

        /* Update connection ID */
        conn_id = data['connection_id'];
        conn_id_element = document.getElementById('conn-id');
        conn_id_element.innerHTML = conn_id;

        /* Update remote address */
        conn_remote_addr = data['connection_remote_addr'];
        conn_remote_addr_element = document.getElementById('conn-remote-addr');
        conn_remote_addr_element.innerHTML = conn_remote_addr;

        /* Update remote port */
        conn_remote_port = data['connection_port'];
        conn_remote_port_element = document.getElementById('conn-remote-port');
        conn_remote_port_element.innerHTML = conn_remote_port;
    });
}, 2000);