from datetime import datetime
import logic
import yaml
import re


def write_article(diretory, title, article, body):
    output = yaml.dump(article, default_flow_style=False, allow_unicode=True) + '\n' + body
    output = output.replace('!!python/str ', '')

    path = re.sub('[^a-z0-9]', '_', title.lower())
    with open('content/%s/%s.md' % (diretory, path), 'w') as f:
        f.write(output)


def get_section(path):
    x = path.split('/')
    return x[0] if len(x) == 2 else x[1]


def strptime(date):
    return datetime.strptime(date, '%Y-%m-%d %H:%M')


def strftime(date):
    return date.strftime('%Y-%m-%d %H:%M')


def freeze_meta(content):
    pass


def unfreeze_meta(content):
    for date in logic.DATES:
        if date in content:
            content[date] = strptime(content[date])
    return content
