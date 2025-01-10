import urllib.request


def get(url, headers={}):
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req) as res:
        return res.read().decode("utf-8")
