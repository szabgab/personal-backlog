import os
import PersonalBacklog
import pytest

@pytest.fixture
def pb(tmpdir):
    filename = os.path.join(str(tmpdir), 'test.json')
    return PersonalBacklog.PB(filename)

@pytest.fixture
def pbx(pb):
    pb.add("Hello World", '1', '3')
    pb.add("Second Task", '3', '2')
    pb.add("Third Thing", '0', '7')
    pb.add("Fourth todo", '2', '2')
    return pb


class TestPB(object):


    def test_empty(self, pb, capsys):

        assert pb.list_calendar('0') == {}
        assert pb.list_calendar('') == { 'error' : "Invalid input ''" }
        assert pb.list_todo() == None
        out, err = capsys.readouterr()
        assert err == ''
        assert out == ''

    def test_add(self, pb, capsys):
        assert pb.add("First Class", 'x', '3') == { 'error' : "Invalid estimate 'x'" }
        assert pb.add("Second Class", '1', 'z') == { 'error' : "Invalid priority 'z'" }

        assert pb.add("Hello World", '1', '3') == {}
        out, err = capsys.readouterr()
        assert err == ''
        assert out == ''

        assert pb.list_todo() == None
        out, err = capsys.readouterr()
        assert err == ''
        assert out == '0) 3 - 1 - Hello World\n'

        assert pb.add("Second Task", '3', '2') == {}
        out, err = capsys.readouterr()
        assert err == ''
        assert out == ''

        assert pb.add("Third Thing", '0', '7') == {}
        out, err = capsys.readouterr()
        assert err == ''
        assert out == ''

        assert pb.list_todo() == None
        out, err = capsys.readouterr()
        assert err == ''
        assert out == '0) 3 - 1 - Hello World\n1) 2 - 3 - Second Task\n2) 7 - 0 - Third Thing\n'

    def test_delete(self, pbx, capsys):
        pb = pbx

        assert pb.delete('x') == {'error': "Invalid input 'x'"}
        out, err = capsys.readouterr()
        assert err == ''
        assert out == ''

        # delete before listing does not know what to delete
        assert pb.delete('1') == {'error': "Invalid id - not in range '1'"}
        out, err = capsys.readouterr()
        assert err == ''
        assert out == ''

        assert pb.list_todo() == None
        out, err = capsys.readouterr()
        assert err == ''
        assert out == '0) 3 - 1 - Hello World\n1) 2 - 3 - Second Task\n2) 7 - 0 - Third Thing\n3) 2 - 2 - Fourth todo\n'

        assert pb.delete('4') == {'error': "Invalid id - not in range '4'"}
        out, err = capsys.readouterr()
        assert err == ''
        assert out == ''

        assert pb.delete('1') == {}
        out, err = capsys.readouterr()
        assert err == ''
        assert out == ''

        assert pb.list_todo() == None
        out, err = capsys.readouterr()
        assert err == ''
        assert out == '0) 3 - 1 - Hello World\n1) 7 - 0 - Third Thing\n2) 2 - 2 - Fourth todo\n'

        assert pb.delete('1') == {}
        out, err = capsys.readouterr()
        assert err == ''
        assert out == ''

        # TODO: maybe we need a better error message when the user tries to double-delete, or we need feedback for deletition?
        assert pb.delete('1') == {'error': 'Internal error. Could not find it.'}
        out, err = capsys.readouterr()
        assert err == ''
        assert out == ''

        assert pb.list_todo() == None
        out, err = capsys.readouterr()
        assert err == ''
        assert out == '0) 3 - 1 - Hello World\n1) 2 - 2 - Fourth todo\n'


    def test_save_and_load_again(self, tmpdir, capsys):
        filename = os.path.join(str(tmpdir), 'test_save.json')
        pb1 = PersonalBacklog.PB(filename)

        assert pb1.list_todo() == None
        out, err = capsys.readouterr()
        assert err == ''
        assert out == ''

        pb1.add("Hello World", '1', '3')
        assert pb1.list_todo() == None
        out, err = capsys.readouterr()
        assert err == ''
        assert out == '0) 3 - 1 - Hello World\n'

        filename = os.path.join(str(tmpdir), 'test_save.json')
        pb2 = PersonalBacklog.PB(filename)

        assert pb2.list_todo() == None
        out, err = capsys.readouterr()
        assert err == ''
        assert out == '0) 3 - 1 - Hello World\n'
