from common import exec_command


def test_help():
    returncode, stdout, stderr = exec_command(['dcos', 'config', '--help'])

    assert returncode == 0
    assert stdout == b"""Usage:
    dcos config info
    dcos config <name> [<value>]
    dcos config --unset <name>
    dcos config --list

Options:
    -h, --help            Show this screen
    --version             Show version
    --unset               Remove property from the config file
"""
    assert stderr == b''


def test_info():
    returncode, stdout, stderr = exec_command(['dcos', 'config', 'info'])

    assert returncode == 0
    assert stdout == b'Get and set DCOS command line options\n'
    assert stderr == b''


def test_version():
    returncode, stdout, stderr = exec_command(['dcos', 'config', '--version'])

    assert returncode == 0
    assert stdout == b'dcos-config version 0.1.0\n'
    assert stderr == b''


def test_list_property():
    returncode, stdout, stderr = exec_command(['dcos', 'config', '--list'])

    assert returncode == 0
    assert stdout == b"""marathon.host=localhost
marathon.port=8080
package.cache=tmp/cache
package.sources=['git://github.com/mesosphere/universe.git', \
'https://github.com/mesosphere/universe/archive/master.zip']
"""
    assert stderr == b''


def test_get_existing_property():
    _get_value('marathon.host', 'localhost')


def test_get_missing_proerty():
    _get_missing_value('missing.property')


def test_set_existing_property():
    _set_value('marathon.host', 'newhost')
    _get_value('marathon.host', 'newhost')
    _set_value('marathon.host', 'localhost')


def test_unset_property():
    _unset_value('marathon.host')
    _get_missing_value('marathon.host')
    _set_value('marathon.host', 'localhost')


def test_set_missing_property():
    _set_value('path.to.value', 'cool new value')
    _get_value('path.to.value', 'cool new value')
    _unset_value('path.to.value')


def _set_value(key, value):
    returncode, stdout, stderr = exec_command(['dcos', 'config', key, value])

    assert returncode == 0
    assert stdout == b''
    assert stderr == b''


def _get_value(key, value):
    returncode, stdout, stderr = exec_command(['dcos', 'config', key])

    assert returncode == 0
    assert stdout == '{}\n'.format(value).encode('utf-8')
    assert stderr == b''


def _unset_value(key):
    returncode, stdout, stderr = exec_command(
        ['dcos', 'config', '--unset', key])

    assert returncode == 0
    assert stdout == b''
    assert stderr == b''


def _get_missing_value(key):
    returncode, stdout, stderr = exec_command(['dcos', 'config', key])

    assert returncode == 1
    assert stdout == b''
    assert stderr == b''
