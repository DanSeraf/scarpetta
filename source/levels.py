#TODO Regex

def test():
    url = 'http://fragal.eu'
    main_domain = url

    assert checkLevel('http://fragal.eu/', 'http://fragal.eu', 1)
    assert checkLevel('http://fragal.eu/', 'http://fragal.eu/a/b/c', 3)
    assert not checkLevel('http://fragal.eu/', 'http://fragal.eu/a/b/c', 1)
    assert checkLevel('http://fragal.eu', 'http://fragal.eu/', 1)
    assert checkLevel('fragal.eu', 'http://fragal.eu/', 1)
    assert checkLevel('fragal.eu', 'https://fragal.eu/', 1)
    assert checkLevel('http://fragal.eu', 'http://fragal.eu', 1)
    assert checkLevel('fragal.eu', 'http://fragal.eu/', 1)
    assert checkLevel('http://.*.eu', 'fragal.eu', 1)
    assert checkLevel('http://.*', 'fragal.eu', 1)
    assert not checkLevel('http://.*/', 'fragal.eu/git', 0)
    assert not checkLevel('http://.*.fragal.eu/', 'http://fragal.eu/git', 0)
    assert not checkLevel('http://.*.eu', 'fragal.eu/git', 0)
    assert checkLevel('http://.*.eu', 'fragal.eu/git', 1)
    assert checkLevel('http://.*.fragal.eu', 'http://git.fragal.eu', 1)
    assert checkLevel('.*.fragal.eu', 'http://git.fragal.eu', 1)
    assert checkLevel('.*.*.fragal.eu', 'http://a.b.fragal.eu', 1)

    assert checkLevel('http://fragal.eu:80/', 'http://fragal.eu:80', 1)
    assert not checkLevel('http://fragal.eu:80/', 'http://fragal.eu:80/a/b/c', 1)
    assert checkLevel('http://fragal.eu:80', 'http://fragal.eu:80/', 1)
    assert checkLevel('fragal.eu:80', 'http://fragal.eu:80/', 1)
    assert checkLevel('http://.*.eu:80', 'fragal.eu:80', 1)
    assert checkLevel('http://.*', 'fragal.eu:80', 1)
    assert not checkLevel('http://.*/', 'fragal.eu:80/git', 0)
    assert not checkLevel('http://.*.fragal.eu:80/', 'http://fragal.eu:80/git', 0)
    assert not checkLevel('http://.*.eu:80', 'fragal.eu:80/git', 0)
    assert checkLevel('http://.*.eu:80', 'fragal.eu:80/git', 1)
    assert checkLevel('.*.fragal.eu:80', 'http://git.fragal.eu:80', 1)

def checkLevel(rule = None, url = None, level = None):

    

    

