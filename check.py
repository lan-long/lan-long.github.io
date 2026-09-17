"""Check generated local links, assets, navigation and editable content."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote
import json

ROOT=Path(__file__).resolve().parent
DIST=ROOT/'dist'
class Document(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.ids=[];self.refs=[];self.current=[];self.scripts=[];self.images=[];self.viewport=False;self.robots=[]
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if a.get('id'):self.ids.append(a['id'])
        if a.get('aria-current')=='page':self.current.append(a.get('href'))
        if tag=='meta' and a.get('name')=='viewport':self.viewport=True
        if tag=='meta' and a.get('name')=='robots':self.robots.append(a.get('content',''))
        if tag=='script':self.scripts.append(a.get('src'))
        if tag=='img':self.images.append(a)
        for name in ['href','src']:
            if a.get(name):self.refs.append((name,a[name]))

def run():
    docs={}; errors=[]
    for path in DIST.glob('*.html'):
        doc=Document();doc.feed(path.read_text(encoding='utf-8'));docs[path.name]=doc
        if len(doc.ids)!=len(set(doc.ids)):errors.append(f'{path.name}: duplicate IDs')
        if doc.current!=[path.name]:errors.append(f'{path.name}: active navigation is incorrect')
        if not doc.viewport:errors.append(f'{path.name}: missing viewport')
        if any('noindex' in value.lower() for value in doc.robots):errors.append(f'{path.name}: search indexing is disabled')
        if doc.scripts!=['assets/site.js']:errors.append(f'{path.name}: unexpected executable scripts')
        for img in doc.images:
            if not img.get('alt'):errors.append(f'{path.name}: missing image alternative text')
    if set(docs)!={'index.html','research.html','publications.html','group.html','awards.html','news.html'}:errors.append('Expected exactly six pages')
    if not (DIST/'.nojekyll').is_file():errors.append('Missing dist/.nojekyll deployment marker')
    for name,doc in docs.items():
        for attr,ref in doc.refs:
            u=urlsplit(ref)
            if u.scheme or u.netloc:continue
            target=unquote(u.path) or name
            path=DIST/target
            if not path.is_file():errors.append(f'{name}: missing local target {target}')
            if u.fragment and target in docs and unquote(u.fragment) not in docs[target].ids:errors.append(f'{name}: missing anchor {ref}')
    pubs=json.loads((ROOT/'content/publications.json').read_text(encoding='utf-8'))
    if len({p['id'] for p in pubs})!=len(pubs):errors.append('Duplicate publication IDs')
    for p in pubs:
        if not (p.get('placeholder') is True and p['year'] is None) and not (type(p['year']) is int and 1900<=p['year']<=2100):errors.append(f'Invalid year: {p["title"]}')
        if len(p['venue'])>1200 or len(p['authors'])>1600:errors.append(f'Possible nested-list import: {p["title"]}')
    for n in json.loads((ROOT/'content/news.json').read_text(encoding='utf-8')):
        if n.get('placeholder') is True and n['year'] is None and n['month'] is None:continue
        if not (type(n['year']) is int and 1900<=n['year']<=2100 and type(n['month']) is int and 1<=n['month']<=12):errors.append('Invalid news date')
    if errors:raise SystemExit('\n'.join(errors))
    print(f'PASS: {len(docs)} pages, {sum(not p.get("placeholder", False) for p in pubs)} publications, {sum(bool(p.get("placeholder")) for p in pubs)} placeholders; local paths, anchors, active navigation and image labels.')
    print('External resource availability and actual browser rendering are not checked.')

if __name__=='__main__':run()
