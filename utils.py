import yaml
import re


def write_article(diretory, title, article, body):
    output = yaml.dump(article, default_flow_style=False, allow_unicode=True) + '\n' + body
    output = output.replace('!!python/str ', '')

    path = re.sub('[^a-z0-9]', '_', title.lower())
    with open('content/%s/%s.md' % (diretory, path), 'w') as f:
        f.write(output)
