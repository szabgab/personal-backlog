import os
import PersonalBacklog

def test_pb(tmpdir, capsys):
    filename = os.path.join(tmpdir, 'test.json')
    pb = PersonalBacklog.PB(filename)

    assert pb.list_calendar() == None
    out, err = capsys.readouterr()
    assert err == ''
    assert out == ''

    assert pb.list_todo() == None
    out, err = capsys.readouterr()
    assert err == ''
    assert out == ''

    assert pb.add("Hello World", '1', '3') == None
    out, err = capsys.readouterr()
    assert err == ''
    assert out == ''

    assert pb.list_todo() == None
    out, err = capsys.readouterr()
    assert err == ''
    assert out == '0) 3 - 1 - Hello World\n'

    assert pb.add("Second Task", '3', '2') == None
    out, err = capsys.readouterr()
    assert err == ''
    assert out == ''

    assert pb.list_todo() == None
    out, err = capsys.readouterr()
    assert err == ''
    assert out == '0) 3 - 1 - Hello World\n1) 2 - 3 - Second Task\n'
