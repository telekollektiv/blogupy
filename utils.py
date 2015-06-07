import math
import yaml
import re


def get_pages(total, limit):
    return range(1, int(math.ceil(float(total) / limit)) + 1)


def write_article(diretory, title, article, body):
    output = yaml.dump(article, default_flow_style=False, allow_unicode=True) + '\n' + body
    output = output.replace('!!python/str ', '')

    path = re.sub('[^a-z0-9]', '_', title.lower())
    with open('content/%s/%s.md' % (diretory, path), 'w') as f:
        f.write(output)
