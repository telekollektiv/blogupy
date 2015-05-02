from cgi import escape
import re


GHETTO_RULES = [
    ('\*\*(.+?)\*\*', '<b>\\1</b>'),
    ('\*(.+?)\*', '<i>\\1</i>'),
]

def ghettodown(txt):
    def swag(txt):
        FRESH = True
        P = False
        print(escape(txt).split('\n'))
        for line in escape(txt).split('\n'):
            line = line.rstrip('\r')
            if line:
                if line[0:2] == '# ':
                    if P:
                        yield '</p>'
                        P = False
                    line = re.sub('^# (.+)', '<h2>\\1</h2>', line)
                    line = re.sub('^## (.+)', '<h3>\\1</h3>', line)
                    FRESH = True
                else:
                    if FRESH:
                        if not P:
                            yield '<p>'
                            FRESH = False
                            P = True
                    else:
                        if P:
                            yield '<br>'

                    for x, y in GHETTO_RULES:
                        line = re.sub(x, y, line)
            else:
                FRESH = True
                if P:
                    yield '</p>'
                    P = False

            yield line

    return '\n'.join(swag(txt))
