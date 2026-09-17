"""Generate the six-page static site. Requires Python 3.10+; no packages."""
from pathlib import Path
from string import Template
from collections import defaultdict
import json, shutil, html

ROOT=Path(__file__).resolve().parent
DIST=ROOT/'dist'
def read(name): return json.loads((ROOT/'content'/name).read_text(encoding='utf-8'))
def esc(value): return html.escape(str(value),quote=True)
def fragment(name): return (ROOT/'content'/name).read_text(encoding='utf-8')
profile=read('profile.json'); research=read('research.json'); publications=read('publications.json')
news=read('news.json'); members=read('members.json'); awards=read('awards.json')
sources={s['key']:s for s in read('sources.json')}
nav=[('index','Home'),('research','Research'),('publications','Publications'),('group','Group'),('awards','Awards'),('news','News')]
def source_label(keys):
    labels=[]
    for key in keys:
        item=sources.get(key, {})
        if not item.get('name'):continue
        labels.append(f'<a href="{esc(item["url"])}">{esc(item["name"])}</a>' if item.get('url') else esc(item['name']))
    return '<span class="source-label">'+' / '.join(labels)+'</span>' if labels else ''
def resource_links(p):
    if not p['links']:return ''
    return '<div class="resource-links">'+''.join(f'<a href="{esc(a["url"])}" rel="noopener noreferrer">{esc(a["label"])} ↗</a>' if a.get('url') else f'<span class="unavailable">{esc(a["label"])} · Link unavailable</span>' for a in p['links'])+'</div>'
def picture(path, label, css):
    if path:return f'<img class="{css}" src="{esc(path)}" alt="{esc(label)}" loading="lazy">'
    return ''
def email_link(label=None):
    address=profile.get('email')
    return f'<a href="mailto:{esc(address)}">{esc(label or address)}</a>' if address else '<span class="unavailable">Email unavailable</span>'
def year_label(year):return str(year) if year is not None else 'Year pending'
def year_key(year):return str(year) if year is not None else 'pending'
def ordered_years(values):return sorted(values, key=lambda y: y if y is not None else -1, reverse=True)
def section(title,body,link=None):
    more=f'<a href="{link[0]}">{link[1]} →</a>' if link else ''
    return f'<section class="section"><div class="section-heading"><h2>{title}</h2>{more}</div>{body}</section>'
def head(eyebrow,title,description): return f'<p class="eyebrow">{eyebrow}</p><h1>{title}</h1><p class="page-intro">{description}</p>'
def jump(entries):return '<nav class="jump-nav" aria-label="On this page">'+''.join(f'<a href="#{esc(id)}">{esc(label)}</a>' for id,label in entries)+'</nav>'
def news_rows(items):
    result='<ul class="news-list">'
    for n in items:
        if n.get('year') is not None and n.get('month') is not None:
            date=f'<time datetime="{n["year"]}-{n["month"]:02d}">{n["year"]}.{n["month"]:02d}</time>'
        else:date='<span class="pending-date">Date pending</span>'
        result+=f'<li class="news-row">{date}<div class="news-text">{n["html"]}{source_label([n["source"]])}</div></li>'
    return result+'</ul>'

def home():
    links=''.join(f'<a href="{esc(x["url"])}">{esc(x["label"])} ↗</a>' if x.get('url') else f'<span class="unavailable">{esc(x["label"])} · Link unavailable</span>' for x in profile['links'])
    profile_class='profile' if profile.get('photo') else 'profile profile-no-photo'
    body=f'''<section class="{profile_class}">{picture(profile.get('photo'), profile['name'], 'portrait')}<div><h1>{esc(profile['name'])}</h1><p class="position">{esc(profile['role'])}</p><p class="affiliation">{esc(profile['affiliation'])}</p><p class="secondary-role">{esc(profile['secondary_role'])}</p><div class="contact">{email_link()}<br>{esc(profile['office'])}</div><div class="academic-links">{links}</div></div></section>'''
    body+='<div class="bio">'+fragment('bio.html')+'</div>'
    body+=section('Research interests',f'<p>{esc(profile["research_statement"])}</p><div class="topic-overview">'+''.join(f'<a href="research.html#{t["id"]}"><span>0{i+1}</span><strong>{esc(t["title"])}</strong></a>' for i,t in enumerate(research[:4]))+'</div>',('research.html','Explore research'))
    body+=section('Recent news',news_rows(news[:profile['news_limit']]),('news.html','All updates'))
    features=''; by_id={p['id']:p for p in publications}
    for f in read('featured.json'):
        p=by_id[f['publication_id']]
        description=f'<dl class="featured-summary"><div><dt>Research question</dt><dd>{esc(f["problem"])}</dd></div><div><dt>Main findings</dt><dd>{esc(f["result"])}</dd></div></dl>'
        features+=f'<article class="featured-item"><div><h3><a href="publications.html#{esc(p["id"])}">{esc(p["title"])}</a></h3>{description}<div class="venue">{esc(p["venue"])}</div>{resource_links(p)}{source_label(p["sources"])}</div></article>'
    body+=section('Selected work',features,('publications.html','All publications'))
    recruit=f'<div class="recruitment"><p>Prospective students &amp; collaborators</p><p class="source-label">{esc(profile.get("recruitment_status", ""))}</p><details><summary>Research fit, application materials &amp; availability</summary>{fragment("recruitment.html")}</details></div>'
    body+=section('Join & collaborate',recruit)
    return body

def research_page():
    body=head('Research','Research directions','Our research addresses visual perception and reliable learning in open, real-world environments. Each direction below introduces its core problems, general approach, research topics, and representative publications.')
    body+=jump([(t['id'],t['title']) for t in research])
    for t in research:
        illustration=''
        if t.get('image'):
            caption=esc(t.get('image_caption',''))
            source=esc(t.get('image_source',''))
            caption_html=f'<a href="{source}" target="_blank" rel="noopener">{caption}</a>' if source else caption
            illustration=(f'<figure class="research-figure">'
                          f'<img class="research-image" src="{esc(t["image"])}" alt="{esc(t.get("image_alt",t["title"]))}">'
                          f'<figcaption>Source: {caption_html}</figcaption></figure>')
        body+=f'<section class="research-topic" id="{t["id"]}"><h2>{esc(t["title"])}</h2>{source_label([t["source"]])}{illustration}<div class="research-copy">{t["html"]}</div></section>'
    return body

def publications_page():
    grouped=defaultdict(list)
    for p in publications: grouped[p['year']].append(p)
    body=head('Publications','Publications','Publications are organized by year and type. Each entry includes authors, venue information, and available resources.')
    body+=jump([(f'year-{year_key(y)}',year_label(y)) for y in ordered_years(grouped)])
    for year in ordered_years(grouped):
        actual=sum(not p.get('placeholder', False) for p in grouped[year])
        pending=len(grouped[year])-actual
        count_label=f'{actual} publications' if actual else ''
        if pending:count_label+=(' · ' if count_label else '')+f'{pending} entries pending'
        body+=f'<section class="year-section" id="year-{year_key(year)}"><h2 class="year-title">{year_label(year)}<span>{count_label}</span></h2>'
        for kind,label in [('conference','Conference papers'),('journal','Journal articles')]:
            entries=[p for p in grouped[year] if p['kind']==kind]
            if not entries:continue
            body+=f'<h3 class="publication-type">{label}</h3>'
            for p in entries:
                authors=esc(p['authors'])
                for name in sorted(filter(None, profile['highlight_names']), key=len, reverse=True):authors=authors.replace(esc(name),f'<strong>{esc(name)}</strong>')
                body+=f'<article class="publication" id="{esc(p["id"])}"><h3>{esc(p["title"])}</h3><p class="authors">{authors}</p><div class="venue">{esc(p["venue"])}</div>{resource_links(p)}{source_label(p["sources"])}</article>'
        body+='</section>'
    return body

def group_page():
    body=head('Group','People & supervision','This page lists current students, including their degree program, research interests, start date, and supervision relationship.')
    groups=defaultdict(list)
    for m in members:groups[m['group']].append(m)
    if len(groups) > 1:
        body+=jump([(f'members-{i}',title) for i,title in enumerate(groups,1)])
    group_name=profile.get('group_name','').strip()
    group_heading=f'<h2>{esc(group_name)}</h2>' if group_name else ''
    body+=f'<section class="section">{group_heading}'
    for i,(title,people) in enumerate(groups.items(),1):
        body+=f'<h3 class="group-heading" id="members-{i}">{esc(title)}</h3><div class="member-grid">'
        for m in people:
            img=picture(m['image'], m['name'], 'member-photo')
            body+=f'<article class="member">{img}<div class="member-copy">{m["html"]}{source_label([m["source"]])}</div></article>'
        body+='</div>'
    return body+'</section>'

def awards_page():
    body=head('Awards','Awards & honors','Selected awards and honors.')
    sections=[('personal','Academic & community honors')]
    body+=jump(sections)
    for kind,label in sections:
        body+=f'<section class="section" id="{kind}"><h2>{label}</h2><ul class="award-list">'
        for a in awards:
            if a['kind']==kind:body+=f'<li>{a["html"]}{source_label([a["source"]])}</li>'
        body+='</ul></section>'
    return body

def news_page():
    years=ordered_years({n['year'] for n in news})
    body=head('News','News archive','Research updates, publications, and group achievements, listed in reverse chronological order.')
    body+=jump([(f'news-{year_key(y)}',year_label(y)) for y in years])
    for y in years:body+=f'<section class="year-section" id="news-{year_key(y)}"><h2 class="year-title">{year_label(y)}</h2>{news_rows([n for n in news if n["year"]==y])}</section>'
    return body

def build():
    if DIST.exists():
        shutil.rmtree(DIST)
    DIST.mkdir()
    shutil.copytree(ROOT/'assets',DIST/'assets',dirs_exist_ok=True)
    (DIST/'.nojekyll').write_text('',encoding='utf-8')
    template=Template((ROOT/'templates'/'page.html').read_text(encoding='utf-8'))
    pages={'index':home(),'research':research_page(),'publications':publications_page(),'group':group_page(),'awards':awards_page(),'news':news_page()}
    for key,title in nav:
        navigation=''.join(f'<a href="{slug}.html"'+(' aria-current="page"' if slug==key else '')+f'><span>{label}</span></a>' for slug,label in nav)
        result=template.substitute(title=title,name=esc(profile['name']),role=esc(profile['role']),email=esc(profile['email']),description=esc(f'{profile["name"]} · {title} · Academic homepage'),sidebar_topics=esc(profile.get('sidebar_topics', '')),sidebar_email=email_link('Email ↗'),navigation=navigation,sample_notice='',content=pages[key])
        (DIST/f'{key}.html').write_text(result,encoding='utf-8')
    print(f'Built {len(pages)} pages in {DIST}')

if __name__=='__main__':build()
