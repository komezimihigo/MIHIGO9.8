from __future__ import annotations
import os
from pathlib import Path
from flask import Flask, request, redirect, url_for, render_template_string, send_file, abort, flash
from werkzeug.utils import secure_filename
from orchestrator.database import Database
from workers.pipeline import process_upload

BASE=Path(__file__).resolve().parent.parent
HTML='''<!doctype html><html><head><meta name="viewport" content="width=device-width,initial-scale=1"><title>MIHIGO 9.8</title><style>body{font:16px system-ui;max-width:960px;margin:24px auto;padding:0 14px;background:#10141c;color:#edf2f7}section,.job{background:#1b2330;border:1px solid #354154;border-radius:12px;padding:16px;margin:14px 0}input,select,button{font:inherit;padding:10px;margin:5px 0;max-width:100%}button{background:#8bd3ff;border:0;border-radius:8px;font-weight:bold}a{color:#8bd3ff}small{color:#b5c0d0}.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:10px}</style></head><body><h1>MIHIGO 9.8</h1><p>Personal video production dashboard</p>{% with messages=get_flashed_messages() %}{% for m in messages %}<section>{{m}}</section>{% endfor %}{% endwith %}<section><h2>Process a video you own or have permission to use</h2><form method="post" action="/process" enctype="multipart/form-data"><label>Video file<br><input type="file" name="video" accept="video/*" required></label><br><label>Title / topic<br><input name="title" placeholder="Describe the clip"></label><div class="grid"><label>Start seconds<br><input type="number" min="0" step="0.1" name="start" value="0"></label><label>Clip duration<br><input type="number" min="1" max="180" name="duration" value="36"></label><label>Output format<br><select name="mode"><option value="vertical">Vertical 9:16</option><option value="landscape">Landscape 16:9</option><option value="original">Keep dimensions</option></select></label></div><label><input type="checkbox" name="rights_confirmed" value="yes" required> I own this video or have permission to edit and publish it.</label><br><label>Source type<br><select name="source_type"><option value="owned">My own video</option><option value="licensed">Licensed (provide attribution)</option><option value="public_domain">Public domain (verified)</option></select></label><br><label>Attribution (required for licensed sources)<br><input name="attribution"></label><br><button type="submit">Process video</button></form></section><section><h2>Jobs</h2>{% if jobs %}{% for j in jobs %}<div class="job"><b>{{j.title}}</b> — {{j.state}}<br><small>ID: {{j.id}}</small>{% if j.error %}<p>{{j.error}}</p>{% endif %}{% if j.output_path and j.state == 'COMPLETED' %}<p><a href="/download/{{j.id}}">Download edited MP4</a></p>{% endif %}</div>{% endfor %}{% else %}<p>No jobs yet.</p>{% endif %}</section><small>Publishing is not automatic. Review rights and metadata before publishing.</small></body></html>'''

def create_app():
    app=Flask(__name__); app.secret_key=os.getenv('FLASK_SECRET_KEY','local-development-only-change-me')
    db_path=os.getenv('DATABASE_PATH',str(BASE/'data'/'mihigo.sqlite3')); db=Database(db_path); app.config['mihigo_db']=db
    uploads=BASE/'media'/'uploads'; uploads.mkdir(parents=True,exist_ok=True)
    @app.get('/')
    def index(): return render_template_string(HTML,jobs=db.list_jobs())
    @app.post('/process')
    def process():
        f=request.files.get('video')
        if not f or not f.filename: flash('Choose a video file.'); return redirect(url_for('index'))
        safe=secure_filename(f.filename)
        if Path(safe).suffix.lower() not in {'.mp4','.mov','.m4v','.webm','.mkv'}: flash('Unsupported video file extension.'); return redirect(url_for('index'))
        source=uploads/f'{os.urandom(5).hex()}_{safe}'; f.save(source)
        try:
            result=process_upload(db,str(source),request.form.get('title',''),float(request.form.get('start') or 0),float(request.form.get('duration') or 36),request.form.get('mode','vertical'),request.form.get('rights_confirmed')=='yes',request.form.get('source_type','owned'),request.form.get('attribution',''))
            flash(f"Completed job {result['job_id']}. Output: {result['output_path']}")
        except Exception as e: flash(f'Processing failed: {e}')
        return redirect(url_for('index'))
    @app.get('/download/<job_id>')
    def download(job_id):
        job=db.get_job(job_id)
        if not job or not job.get('output_path'): abort(404)
        path=Path(job['output_path']).resolve()
        if not path.is_file() or (BASE/'media'/'outputs').resolve() not in path.parents: abort(404)
        return send_file(path,as_attachment=True,download_name=path.name)
    @app.get('/health')
    def health(): return {'ok':True,'service':'mihigo-9.8','ffmpeg_available':__import__('shutil').which('ffmpeg') is not None}
    return app

if __name__=='__main__':
    app=create_app(); app.run(host=os.getenv('HOST','127.0.0.1'),port=int(os.getenv('PORT','5000')),debug=False)
