from __future__ import annotations
import uuid
from pathlib import Path
from media.processor import process_video
from publishing.metadata import generate_metadata
from rights.policy import validate_source

def process_upload(db, source_path: str, title: str='', start: float=0, duration: float=36, mode: str='vertical', rights_confirmed: bool=False, source_type: str='owned', attribution: str='') -> dict:
    decision=validate_source(source_type,rights_confirmed,attribution)
    if not decision.allowed: raise ValueError(decision.reason)
    job_id=uuid.uuid4().hex
    out=Path('media')/'outputs'/f'{job_id}.mp4'; out.parent.mkdir(parents=True,exist_ok=True)
    metadata=generate_metadata(title or Path(source_path).name, title)
    db.add_job({'id':job_id,'title':metadata['title'],'source_url':None,'state':'PROCESSING','attempts':1,'max_attempts':5,'channel_id':None,'artifact_path':str(source_path),'output_path':None,'error':None,'metadata':{'source_type':source_type,'rights_confirmed':rights_confirmed,'attribution':attribution,'metadata':metadata}})
    try:
        info=process_video(source_path,str(out),start,duration,mode)
        db.update_job(job_id,state='COMPLETED',output_path=str(out),metadata={'source_type':source_type,'rights_confirmed':rights_confirmed,'attribution':attribution,'metadata':metadata,'media':info})
        return {'job_id':job_id,'state':'COMPLETED','output_path':str(out),'metadata':metadata,'media':info}
    except Exception as exc:
        db.update_job(job_id,state='FAILED',error=str(exc))
        raise
