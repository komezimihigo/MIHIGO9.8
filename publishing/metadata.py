import re

def generate_metadata(filename: str, topic: str='') -> dict:
    base=topic.strip() or re.sub(r'[_-]+',' ',filename.rsplit('/',1)[-1].rsplit('.',1)[0])
    title=' '.join(base.split())[:95] or 'New video'
    tags=[]
    for word in re.findall(r'[A-Za-z0-9]{3,}',title.lower()):
        if word not in tags: tags.append(word)
    return {'title':title,'description':f'{title}\n\nEdited with MIHIGO 9.8. Check source rights and details before publishing.','tags':tags[:15]}
