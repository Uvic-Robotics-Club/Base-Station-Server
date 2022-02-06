from flask import Blueprint, request
import subprocess

bp = Blueprint('hotspot', __name__, url_prefix='/hotspot')

@bp.route('/status')
def status():
    '''
    Returns the status of the WiFi hotspot.
    '''

    try:
        print(subprocess.check_output('<COMPLETE>', shell=True))
    except subprocess.CalledProcessError as err:
        raise err

@bp.route('/start', methods=['GET'])
def start():
    '''
    Starts WiFi hotspot

    Request parameters:
        ifname: WiFi device to be used
        # conname: Name of created hotspot connection profile
        ssid: Hotspot SSID
        # band: WiFi band to use
        # channel: WiFi channel to use
        password: Password to use for created hotspot

    '''
    response = {'status': None}
    args = dict(request.args)

    # Validate all required request parameters are present
    try:
        assert 'ifname' in args, 'ifname parameter not provided.'
        #assert 'conname' in args, 'conname parameter not provided.'
        assert 'ssid' in args, 'ssid parameter not provided.'
        #assert 'band' in args, 'band parameter not provided.'
        #assert 'channel' in args, 'channel parameter not provided.'
        assert 'password' in args, 'password parameter not provided.'

    except AssertionError as err:
        response['status'] = 'Malformed request'
        response['message'] = str(err)
        return response

    try:
        command_to_execute = 'nmcli dev wifi hotspot ifname {} ssid {} password "{}"'
        subprocess.check_output(command_to_execute.format(args['ifname'], args['ssid'], args['password']), stderr=subprocess.STDOUT, shell=True)
    except subprocess.CalledProcessError as err:
        response['status'] = 'OS command to start hotspot exited with non-zero code'
        response['message'] = 'Return code: {}, Output: {}'.format(err.returncode, err.output)
        return response

    print('heelo!')
    print(request.args.get('password'))