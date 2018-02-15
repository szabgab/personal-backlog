import os
import PersonalBacklog
import pytest

@pytest.fixture
def pb(tmpdir):
    filename = os.path.join(tmpdir, 'test.json')
    return PersonalBacklog.PB(filename)


class TestPB(object):
    def test_pb(self, pb, capsys):

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

        assert pb.add("Third Thing", '0', '7') == None
        out, err = capsys.readouterr()
        assert err == ''
        assert out == ''

        assert pb.list_todo() == None
        out, err = capsys.readouterr()
        assert err == ''
        assert out == '0) 3 - 1 - Hello World\n1) 2 - 3 - Second Task\n2) 7 - 0 - Third Thing\n'

        assert pb.delete('1') == {}
        out, err = capsys.readouterr()
        assert err == ''
        assert out == ''

        assert pb.list_todo() == None
        out, err = capsys.readouterr()
        assert err == ''
        assert out == '0) 3 - 1 - Hello World\n1) 7 - 0 - Third Thing\n'
