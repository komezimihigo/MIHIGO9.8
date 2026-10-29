"""YouTube upload adapter. Real uploads require OAuth credentials and explicit opt-in."""
import os

def upload_video(path: str, metadata: dict, channel_id: str|None=None, privacy: str='private') -> dict:
    if os.getenv('ENABLE_YOUTUBE_UPLOAD','false').lower()!='true':
        return {'status':'dry_run','message':'Upload disabled. Set ENABLE_YOUTUBE_UPLOAD=true only after OAuth setup and review.','path':path,'metadata':metadata,'channel_id':channel_id,'privacy':privacy}
    try:
        from googleapiclient.discovery import build
        from googleapiclient.http import MediaFileUpload
        from google.oauth2.credentials import Credentials
    except ImportError as e: raise RuntimeError('Install Google API dependencies before YouTube upload') from e
    token=os.getenv('YOUTUBE_TOKEN_JSON')
    if not token: raise RuntimeError('YOUTUBE_TOKEN_JSON OAuth credentials are required; use private upload first')
    import json
    creds=Credentials.from_authorized_user_info(json.loads(token),scopes=['https://www.googleapis.com/auth/youtube.upload'])
    yt=build('youtube','v3',credentials=creds)
    body={'snippet':{'title':metadata['title'],'description':metadata['description'],'tags':metadata.get('tags',[]),'categoryId':'22'},'status':{'privacyStatus':privacy}}
    request=yt.videos().insert(part='snippet,status',body=body,media_body=MediaFileUpload(path,resumable=True))
    response=request.execute()
    return {'status':'uploaded','video_id':response.get('id'),'channel_id':channel_id}
