import os
import PersonalBacklog

def test_pb(tmpdir, capsys):
    filename = os.path.join(tmpdir, 'test.json')
    pb = PersonalBacklog.PB(filename)
    assert pb.list_calendar() == None
    out, err = capsys.readouterr()
    assert err == ''
    assert out == ''
