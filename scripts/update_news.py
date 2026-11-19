"""Refresh BleepingComputer RSS news cards in profile README.

No API keys required. Use --seed to render the bundled, verified starter stories
without network. Use --fetch in a GitHub Action to fetch and render new headlines.
Only uses Pillow and the standard library. No executable content in feeds.
"""
from __future__ import annotations
import argparse
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
import html
import json
import math
from pathlib import Path
import re
import textwrap
import urllib.request
import xml.etree.ElementTree as ET
from PIL import Image,ImageDraw,ImageFont,ImageFilter

ROOT=Path(__file__).resolve().parents[1]
AS=ROOT/'assets'
AS.mkdir(exist_ok=True)
FEED='https://www.bleepingcomputer.com/feed/'
COLORS=[(55,228,252),(174,104,255),(255,104,198)]
BG=(12,13,33); WHITE=(245,245,255); MUTED=(176,179,211)
FONTROOT='/usr/share/fonts/opentype/inter'
if not Path(FONTROOT+'/Inter-Bold.otf').exists(): FONTROOT='/usr/share/fonts/truetype/dejavu'

def ft(size,bold=False):
    p=f'{FONTROOT}/Inter-{"Bold" if bold else "Regular"}.otf' if 'inter' in FONTROOT else f'{FONTROOT}/DejaVuSans.ttf'
    return ImageFont.truetype(p,size)

def width(draw,txt,font):return draw.textbbox((0,0),txt,font=font)[2]

def truncate(txt,n=110):
    txt=' '.join(txt.split())
    return txt if len(txt)<=n else txt[:n-1].rstrip()+'…'

def wrap_text(draw,text,font,maxwidth,maxlines=3):
    out=[];line=''
    for word in text.split():
        cand=(line+' '+word).strip()
        if width(draw,cand,font)<=maxwidth: line=cand
        else:
            if line:out.append(line)
            line=word
            if len(out)>=maxlines:break
    if len(out)<maxlines and line:out.append(line)
    if len(out)>maxlines:out=out[:maxlines]
    if len(out)==maxlines and ' '.join(out)!=text:
        while out[-1] and width(draw,out[-1]+'…',font)>maxwidth:out[-1]=out[-1][:-1]
        out[-1]+='…'
    return out

def get_feed():
    req=urllib.request.Request(FEED,headers={'User-Agent':'BrunoBibianoCyberProfile/1.0 (public RSS metadata only)','Accept':'application/rss+xml, application/xml, text/xml'})
    with urllib.request.urlopen(req,timeout=18) as r:
        raw=r.read(2_000_000)
    root=ET.fromstring(raw)
    items=[];seen=set()
    terms=('ransom','breach','hacker','cyber','malware','vulnerab','zero-day','exploit','attack','compromised','security','phish','patch','cve','credential','backdoor')
    for item in root.findall('./channel/item'):
        title=html.unescape((item.findtext('title') or '').strip())
        link=(item.findtext('link') or '').strip()
        if not link.startswith('https://www.bleepingcomputer.com/news/') or not any(w in title.lower() for w in terms):continue
        if link in seen:continue
        seen.add(link)
        stamp=item.findtext('pubDate') or ''
        try: published=parsedate_to_datetime(stamp).astimezone(timezone.utc).strftime('%Y-%m-%d')
        except Exception: published='Sem data'
        low=title.lower()
        category=('RANSOMWARE' if 'ransom' in low else 'VULNERABILIDADES' if any(w in low for w in ['zero-day','flaw','exploit','vulnerability','cve']) else 'CYBER NEWS')
        items.append({'title':truncate(title,115),'summary':'Acompanhe a reportagem na fonte original.', 'url':link,'source':'BleepingComputer','published':published,'tag':category})
        if len(items)==3:break
    if len(items)!=3: raise RuntimeError('RSS retornou menos de 3 noticias relevantes: evitando sobrescrever cards existentes')
    return items

def card_base(index,story):
    W,H=436,391
    co=COLORS[index]
    im=Image.new('RGBA',(W,H),(9,10,27,255));d=ImageDraw.Draw(im,'RGBA')
    d.rounded_rectangle((2,2,W-3,H-3),radius=25,fill=(18,19,45,255),outline=(61,66,120,220),width=2)
    # cover art
    d.rounded_rectangle((12,13,W-13,207),radius=18,fill=(11,12,37,255),outline=(*co,94),width=2)
    # backdrop oscillatory circuit map, radial radar and perspective grid
    cx=216;cy=108
    for rad in (40,65,87):
        d.arc((cx-rad,cy-rad,cx+rad,cy+rad),195,342,fill=(*co,70),width=2)
        d.arc((cx-rad,cy-rad,cx+rad,cy+rad),20,95,fill=(*co,35),width=2)
    for i in range(7):
        x=35+i*64
        d.line((x,32,x,185),fill=(*co,15),width=1)
        d.line((25,35+i*24,412,35+i*24),fill=(*co,12),width=1)
    if index==0:
        for x,y in [(121,70),(312,74),(138,150),(290,145)]:
            d.line((cx,cy,x,y),fill=(*co,95),width=2)
            d.ellipse((x-7,y-7,x+7,y+7),fill=(20,29,57,255),outline=(*co,180),width=2)
        d.rounded_rectangle((183,73,251,143),radius=15,fill=(27,51,73,255),outline=(*co,230),width=3)
        d.text((217,108),'PY',font=ft(26,True),anchor='mm',fill=WHITE)
    elif index==1:
        pts=[(216,44),(283,169),(149,169)]
        d.line(pts+[pts[0]],fill=(*co,225),width=5)
        d.text((216,129),'!',font=ft(70,True),anchor='mm',fill=WHITE)
    else:
        for r in range(3):
            d.arc((cx-60-r*23,cy-60-r*23,cx+60+r*23,cy+60+r*23),220,330,fill=(*co,140-r*25),width=3)
        d.rounded_rectangle((181,88,251,146),radius=10,fill=(30,28,63,255),outline=(*co,210),width=3)
        d.arc((192,52,241,111),180,360,fill=(*co,240),width=5)
        d.text((217,118),'●',font=ft(26,True),anchor='mm',fill=(*co,255))
    # topical pill and text
    tag=story.get('tag','CYBER NEWS')[:23]
    d.rounded_rectangle((25,221,26+max(125,len(tag)*11),254),radius=11,fill=(33,25,65,255),outline=(*co,125),width=1)
    d.text((38,229),tag,font=ft(13,True),fill=(*co,255))
    title=story.get('title','Noticia').replace('\n',' ')
    for j,line in enumerate(wrap_text(d,title,ft(22,True),W-48,3)):
        d.text((25,265+j*29),line,font=ft(22,True),fill=WHITE)
    d.line((25,361,W-25,361),fill=(77,80,132,140),width=2)
    date=story.get('published','')
    try:date=datetime.strptime(date,'%Y-%m-%d').strftime('%d/%m/%Y')
    except ValueError:pass
    d.text((25,368),f"{story.get('source','Fonte')}   ·   {date}",font=ft(14),fill=MUTED)
    return im

def render_card(index,story):
    base=card_base(index,story)
    color=COLORS[index]
    frames=[]
    for i in range(20):
        fr=base.copy();d=ImageDraw.Draw(fr,'RGBA')
        # scanning glint restricted to cover area
        x=28+(i*19+index*22)%372
        d.line((x,29,x,189),fill=(*color,55),width=2)
        d.ellipse((x-3,96,x+3,102),fill=(*color,180))
        # small status LED in lower source line
        alpha=int(105+100*abs(math.sin(i*.28+index)))
        d.ellipse((407,370,418,381),fill=(*color,alpha))
        frames.append(fr.convert('RGB'))
    pal=frames[0].quantize(colors=96,method=Image.Quantize.FASTOCTREE)
    ps=[x.quantize(palette=pal,dither=Image.Dither.NONE) for x in frames]
    p=AS/f'news-{index+1}.gif'
    ps[0].save(p,save_all=True,append_images=ps[1:],duration=135,loop=0,optimize=True,disposal=2)
    return p

def news_markdown(stories):
    lines=['<!-- NEWS:START -->','<table><tr>']
    for i,x in enumerate(stories):
        label=html.escape(x['title'],quote=True)
        url=html.escape(x['url'],quote=True)
        lines.append(f'<td width="33%"><a href="{url}"><img src="./assets/news-{i+1}.gif" alt="{label}" width="100%"/></a></td>')
    lines+=['</tr></table>','',f'<p align="center"><sub>Fonte: BleepingComputer · Títulos originais podem estar em inglês · Data da última seleção: {max(x["published"] for x in stories)} · Clique nos cards para ler a matéria.</sub></p>','<!-- NEWS:END -->']
    return '\n'.join(lines)

def update_readme(stories):
    p=ROOT/'README.md'
    s=p.read_text(encoding='utf-8')
    m=re.search(r'<!-- NEWS:START -->.*?<!-- NEWS:END -->',s,flags=re.S)
    if not m:raise RuntimeError('Marcadores NEWS:START / NEWS:END ausentes no README')
    s=s[:m.start()]+news_markdown(stories)+s[m.end():]
    p.write_text(s,encoding='utf-8')

def main():
    ap=argparse.ArgumentParser();g=ap.add_mutually_exclusive_group(required=True)
    g.add_argument('--seed',action='store_true',help='use curated initial JSON (no network)')
    g.add_argument('--fetch',action='store_true',help='fetch newest RSS headlines')
    a=ap.parse_args()
    if a.fetch:
        stories=get_feed()
        (ROOT/'news.json').write_text(json.dumps(stories,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    else:stories=json.loads((ROOT/'news.json').read_text(encoding='utf-8'))
    for i,s in enumerate(stories):render_card(i,s)
    update_readme(stories)
    print('3 cards de noticias renderizados; README atualizado.')

if __name__=='__main__':main()
