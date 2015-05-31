import forms

META = ['drafts', 'depublicate']
DATES = ['date', 'stop']

sections = {
    'articles': {
        'form': forms.ArticleContributeForm
    },
    'events': {
        'form': forms.EventContributeForm
    }
}
