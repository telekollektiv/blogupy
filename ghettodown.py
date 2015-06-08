from cgi import escape
import re


GHETTO_RULES = [
    ('\*\*(.+?)\*\*', '<b>\\1</b>'),
    ('\*(.+?)\*', '<i>\\1</i>'),
    ('!\\[([^\\]]+)\\]\\((https?://[^\\)]+)\\)', '<img src="\\2" alt="\\1">'),
    ('\\[([^\\]]+)\\]\\((https?://[^\\)]+)\\)', '<a href="\\2">\\1</a>'),
]

def ghettodown(txt):
    def swag(txt):
        fresh = True
        p = False
        for line in escape(txt).split('\n'):
            line = line.rstrip('\r')
            if line:
                if line[0:2] == '# ':
                    if p:
                        yield '</p>'
                        p = False
                    line = re.sub('^# (.+)', '<h2>\\1</h2>', line)
                    line = re.sub('^## (.+)', '<h3>\\1</h3>', line)
                    fresh = True
                else:
                    if fresh:
                        if not p:
                            yield '<p>'
                            fresh = False
                            p = True
                    else:
                        if p:
                            yield '<br>'

                    for x, y in GHETTO_RULES:
                        line = re.sub(x, y, line)
            else:
                fresh = True
                if p:
                    yield '</p>'
                    p = False

            yield line

        if p:
            yield '</p>'

    return '\n'.join(swag(txt))
