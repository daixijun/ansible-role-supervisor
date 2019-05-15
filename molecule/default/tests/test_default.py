import os

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ["MOLECULE_INVENTORY_FILE"]
).get_hosts("all")


def test_configutaion_file(host):
    f = host.file("/etc/supervisord.conf")

    assert f.exists
    assert f.user == "root"
    assert f.group == "root"


def test_supervisord_running_and_enabled(host):
    srv = host.service("supervisord")

    assert srv.is_running
    assert srv.is_enabled


def test_unix_socket(host):
    f = host.file("/var/run/supervisord.sock")

    assert f.exists
    assert f.is_socket


# def test_unix_listening(host):
#     s = host.socket("unix:///var/run/supervisord.sock")

#     assert s.is_listening


def test_http_listening(host):
    s = host.socket("tcp://0.0.0.0:9001")

    assert s.is_listening
