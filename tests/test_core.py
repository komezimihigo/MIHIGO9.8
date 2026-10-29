from rights.policy import validate_source
from publishing.metadata import generate_metadata
from orchestrator.healthcheck import HealthCheck

def test_rights_fail_closed():
    assert not validate_source('owned',False).allowed
    assert validate_source('owned',True).allowed
    assert not validate_source('licensed',True,'').allowed
    assert validate_source('licensed',True,'Creator credit').allowed

def test_metadata():
    m=generate_metadata('funny_cat_clip.mp4')
    assert m['title']=='funny cat clip'
    assert m['tags']

def test_health():
    h=HealthCheck(); h.register('database',True); h.register('ffmpeg',False,'missing')
    assert not h.snapshot()['ok']
