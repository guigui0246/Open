import pytest
import os
import debug

#
# Debug
#


@pytest.mark.usefixtures("tmpdir", "monkeypatch", "capfd")
@pytest.hookimpl(tryfirst=True)
@pytest.mark.debug
def test_log(tmpdir, monkeypatch, capfd):
    monkeypatch.chdir(tmpdir)
    debug.debug("This is a test log")
    with open(os.path.join(".", "open.log")) as f:
        txt = f.read()
    assert txt == "This is a test log \n"
    capture = capfd.readouterr()
    assert capture.err == "This is a test log \n"
    assert capture.out == ""
