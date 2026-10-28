"""Geopram Technologies unified Flask application. Configure secrets through environment variables."""
from flask import Flask, render_template, request, redirect, url_for, session, jsonify, send_file, abort, flash, make_response
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.middleware.proxy_fix import ProxyFix
from functools import wraps
from datetime import datetime, timezone, timedelta
from bson import ObjectId
from pymongo import MongoClient, DESCENDING
from pymongo.errors import PyMongoError
from dotenv import load_dotenv
import os, secrets, json, csv, io, gzip, xml.etree.ElementTree as ET, html, smtplib, ssl, socket
from email.message import EmailMessage

load_dotenv()
app=Flask(__name__, template_folder='templates', static_folder='static')
app.secret_key=os.getenv('SESSION_SECRET') or secrets.token_urlsafe(48)
app.wsgi_app=ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1)
app.config.update(SESSION_COOKIE_HTTPONLY=True, SESSION_COOKIE_SECURE=os.getenv('COOKIE_SECURE','true').lower()=='true', SESSION_COOKIE_SAMESITE='Lax', PERMANENT_SESSION_LIFETIME=timedelta(hours=8), MAX_CONTENT_LENGTH=12*1024*1024)
MONGO_URI=os.getenv('MONGODB_URI',''); DB_NAME=os.getenv('DATABASE_NAME','GEOPRAMTECHNOLOGIES')
_client=None; _db=None

def db():
    global _client,_db
    if _db is not None: return _db
    if not MONGO_URI: raise RuntimeError('MONGODB_URI is not configured. Add it in your environment settings.')
    _client=MongoClient(MONGO_URI, serverSelectionTimeoutMS=4000, connectTimeoutMS=4000, tls=True)
    _db=_client[DB_NAME]
    return _db

def now(): return datetime.now(timezone.utc).isoformat()
def oid(v):
    try: return ObjectId(v)
    except Exception: return None
def safe_doc(d):
    if not d: return d
    d=dict(d); d['_id']=str(d.get('_id','')); return d

def admin_required(fn):
    @wraps(fn)
    def wrapper(*a,**kw):
        if not session.get('admin'): return redirect(url_for('login', next=request.path))
        return fn(*a,**kw)
    return wrapper

def setting(key, default=None):
    try:
        x=db().settings.find_one({'key':key})
        return x.get('value',default) if x else default
    except Exception: return default

@app.before_request
def guardrails():
    # Optional country gate. Uses the platform's country header; disabled by default.
    if os.getenv('KENYA_ONLY_MODE','false').lower()=='true':
        country=request.headers.get('x-vercel-ip-country','').upper()
        if country and country!='KE' and not request.path.startswith(('/static/','/health','/login')):
            return render_template('country_block.html'),403
    if request.path.startswith('/api/') and request.method in ('POST','PUT','PATCH','DELETE') and session.get('admin'):
        token=request.headers.get('X-CSRF-Token','')
        if not session.get('csrf') or not secrets.compare_digest(token,session.get('csrf','')):
            return jsonify(error='CSRF validation failed'), 403

@app.after_request
def security_headers(resp):
    resp.headers['X-Content-Type-Options']='nosniff'; resp.headers['X-Frame-Options']='DENY'; resp.headers['Referrer-Policy']='strict-origin-when-cross-origin'; resp.headers['Permissions-Policy']='camera=(), microphone=(), geolocation=()'
    resp.headers['Content-Security-Policy']="default-src 'self' https: data:; script-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net; style-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net https://fonts.googleapis.com; font-src 'self' https://fonts.gstatic.com data:; img-src 'self' data: https:; connect-src 'self' https:; frame-ancestors 'none'; base-uri 'self'; form-action 'self'"
    return resp

@app.route('/health')
def health():
    status={'app':'ok','database':'not_configured','time':now()}
    if MONGO_URI:
        try: db().command('ping'); status['database']='ok'
        except Exception: status['database']='unavailable'
    return jsonify(status), 200 if status['database'] in ('ok','not_configured') else 503

@app.route('/')
def home():
    if setting('maintenance_enabled',False): return render_template('maintenance.html', message=setting('maintenance_message','We are improving our services.'), image=setting('maintenance_image',''))
    try: tagline=setting('landing_tagline','Technology, geospatial intelligence and practical digital solutions.')
    except Exception: tagline='Technology, geospatial intelligence and practical digital solutions.'
    return render_template('home.html', tagline=tagline, company=os.getenv('COMPANY_NAME','Geopram Technologies'))

@app.route('/<path:legacy_page>')
def legacy_pages(legacy_page):
    # Serve retained static pages from the original site without exposing arbitrary filesystem paths.
    allowed={'index.html','academy.html','marketplace.html','pos.html','sms.html','admin.html'}
    if legacy_page in allowed:
        from flask import send_from_directory
        return send_from_directory('.', legacy_page)
    if legacy_page.startswith('forms/') and '..' not in legacy_page:
        from flask import send_from_directory
        return send_from_directory('.', legacy_page)
    abort(404)

@app.route('/login',methods=['GET','POST'])
def login():
    if request.method=='POST':
        email=request.form.get('email','').strip().lower(); password=request.form.get('password','')
        configured=os.getenv('ADMIN_EMAIL','').strip().lower(); stored=os.getenv('ADMIN_PASSWORD','')
        # Password may be a Werkzeug hash; plain text is accepted only for initial local setup.
        ok=email==configured and bool(stored) and (check_password_hash(stored,password) if stored.startswith(('scrypt:','pbkdf2:')) else secrets.compare_digest(stored,password))
        if ok:
            session.clear(); session['admin']=email; session['csrf']=secrets.token_urlsafe(32); session.permanent=True
            try: db().audit.insert_one({'event':'admin_login','actor':email,'ip':request.headers.get('x-forwarded-for','')[:80],'at':now()})
            except Exception: pass
            return redirect(request.args.get('next') or url_for('admin'))
        flash('Login failed. Check your credentials and server configuration.','error')
    return render_template('login.html')

@app.route('/logout',methods=['POST'])
@admin_required
def logout(): session.clear(); return redirect(url_for('login'))

@app.route('/geopram-consoleQWERTYUIOP')
@admin_required
def admin():
    counts={}
    try:
        for c in ['students','staff','courses','products','orders','invoices','certificates','messages','campaigns','subdomains','audit']:
            counts[c]=db()[c].count_documents({})
    except Exception: counts={}
    return render_template('admin.html', counts=counts, csrf=session.get('csrf',''), tagline=setting('landing_tagline',''), maintenance=setting('maintenance_enabled',False))

COLLECTIONS={'students','staff','courses','classes','attendance','fees','products','orders','invoices','certificates','messages','campaigns','subdomains','announcements','documents','tickets','suppliers','inventory','payments','enrollments','timetables','exams','grades','parents','settings','audit','api_checks','sms_logs','email_logs','whatsapp_logs','maintenance_notices'}
@app.route('/api/admin/collections')
@admin_required
def collections():
    out=[]
    for c in sorted(COLLECTIONS):
        try: out.append({'name':c,'count':db()[c].count_documents({})})
        except Exception: out.append({'name':c,'count':None})
    return jsonify(out)

@app.route('/api/admin/<collection>',methods=['GET','POST'])
@admin_required
def collection_api(collection):
    if collection not in COLLECTIONS: abort(404)
    col=db()[collection]
    if request.method=='GET':
        page=max(1,min(10000,int(request.args.get('page',1)))); limit=max(1,min(100,int(request.args.get('limit',25))))
        docs=[safe_doc(x) for x in col.find({}).sort('_id',DESCENDING).skip((page-1)*limit).limit(limit)]
        return jsonify(items=docs,page=page,limit=limit,total=col.count_documents({}))
    data=request.get_json(silent=True) or {}
    if not isinstance(data,dict): return jsonify(error='Expected a JSON object'),400
    data.pop('_id',None); data['updated_at']=now(); data.setdefault('created_at',now())
    # Bound field size and disallow Mongo operator injection through keys.
    if any(str(k).startswith('$') or '.' in str(k) for k in data): return jsonify(error='Invalid field name'),400
    result=col.insert_one(data)
    try: db().audit.insert_one({'event':'create_record','collection':collection,'record_id':str(result.inserted_id),'actor':session['admin'],'at':now()})
    except Exception: pass
    return jsonify(ok=True,id=str(result.inserted_id)),201

@app.route('/api/admin/<collection>/<record_id>',methods=['GET','PATCH','DELETE'])
@admin_required
def record_api(collection,record_id):
    if collection not in COLLECTIONS: abort(404)
    ident=oid(record_id)
    if ident is None: return jsonify(error='Invalid record id'),400
    col=db()[collection]
    if request.method=='GET':
        d=col.find_one({'_id':ident}); return (jsonify(safe_doc(d)) if d else (jsonify(error='Not found'),404))
    if request.method=='DELETE':
        col.delete_one({'_id':ident})
        return jsonify(ok=True)
    data=request.get_json(silent=True) or {}; data.pop('_id',None)
    if any(str(k).startswith('$') or '.' in str(k) for k in data): return jsonify(error='Invalid field name'),400
    data['updated_at']=now(); col.update_one({'_id':ident},{'$set':data})
    return jsonify(ok=True)

@app.route('/api/admin/settings',methods=['GET','POST'])
@admin_required
def admin_settings():
    if request.method=='GET':
        keys=['landing_tagline','maintenance_enabled','maintenance_message','maintenance_image','maintenance_until','maintenance_scope','maintenance_email_customers','subdomain_links','system_notice']
        return jsonify({k:setting(k,False if k=='maintenance_enabled' else '') for k in keys})
    data=request.get_json(silent=True) or {}
    allowed={'landing_tagline','maintenance_enabled','maintenance_message','maintenance_image','maintenance_until','maintenance_scope','maintenance_email_customers','subdomain_links','system_notice'}
    for k,v in data.items():
        if k in allowed: db().settings.update_one({'key':k},{'$set':{'value':v,'updated_at':now()}},upsert=True)
    return jsonify(ok=True)

@app.route('/api/admin/export/<fmt>')
@admin_required
def export_data(fmt):
    chosen=request.args.get('collection','all'); names=[chosen] if chosen in COLLECTIONS else sorted(COLLECTIONS) if chosen=='all' else None
    if names is None: return jsonify(error='Unknown collection'),400
    data={}
    for name in names: data[name]=[safe_doc(d) for d in db()[name].find({}).limit(100000)]
    stamp=datetime.now().strftime('%Y%m%d-%H%M%S')
    if fmt in ('json','database'):
        payload=json.dumps(data,default=str,ensure_ascii=False,indent=2).encode(); mimetype='application/json'; ext='json'
        if fmt=='database': payload=gzip.compress(payload); mimetype='application/gzip'; ext='database.json.gz'
    elif fmt=='xml':
        root=ET.Element('geopram_export',generated_at=now())
        for cname,items in data.items():
            ce=ET.SubElement(root,'collection',name=cname)
            for item in items:
                re=ET.SubElement(ce,'record')
                for k,v in item.items(): ET.SubElement(re,str(k).replace('$','_').replace('.','_')).text=json.dumps(v,default=str,ensure_ascii=False) if isinstance(v,(dict,list)) else str(v)
        payload=ET.tostring(root,encoding='utf-8',xml_declaration=True); mimetype='application/xml'; ext='xml'
    elif fmt=='html':
        body=['<!doctype html><meta charset="utf-8"><title>Geopram data export</title><h1>Geopram data export</h1>']
        for cname,items in data.items(): body.append('<h2>'+html.escape(cname)+'</h2><pre>'+html.escape(json.dumps(items,default=str,indent=2,ensure_ascii=False))+'</pre>')
        payload='\n'.join(body).encode(); mimetype='text/html'; ext='html'
    elif fmt=='csv':
        output=io.StringIO(); w=csv.writer(output); w.writerow(['collection','record_json'])
        for cname,items in data.items():
            for item in items: w.writerow([cname,json.dumps(item,default=str,ensure_ascii=False)])
        payload=output.getvalue().encode('utf-8-sig'); mimetype='text/csv'; ext='csv'
    elif fmt=='xlsx':
        try:
            from openpyxl import Workbook
            output=io.BytesIO(); wb=Workbook(); wb.remove(wb.active)
            for cname,items in data.items():
                ws=wb.create_sheet(cname[:31]); ws.append(['id','record_json'])
                for item in items: ws.append([item.get('_id',''),json.dumps(item,default=str,ensure_ascii=False)])
            wb.save(output); payload=output.getvalue(); mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'; ext='xlsx'
        except ImportError: return jsonify(error='Install openpyxl to export Excel files'),501
    else: return jsonify(error='Supported formats: json, database, xml, html, csv, xlsx'),400
    try: db().audit.insert_one({'event':'database_export','format':fmt,'collections':names,'actor':session['admin'],'at':now()})
    except Exception: pass
    resp=make_response(payload); resp.headers['Content-Type']=mimetype; resp.headers['Content-Disposition']=f'attachment; filename="geopram-export-{stamp}.{ext}"'; return resp

@app.route('/api/admin/import',methods=['POST'])
@admin_required
def import_data():
    # JSON import is enabled by default; XML/CSV/HTML/XLSX are export formats. Importing arbitrary HTML is intentionally disabled.
    data=request.get_json(silent=True)
    if not isinstance(data,dict): return jsonify(error='Upload a JSON object shaped as {collection: [records]}. HTML import is disabled; XML/XLSX import should be reviewed and converted to JSON first.'),400
    total=0
    for cname,items in data.items():
        if cname not in COLLECTIONS or not isinstance(items,list): continue
        docs=[]
        for item in items[:10000]:
            if isinstance(item,dict):
                item={k:v for k,v in item.items() if k!='_id' and not str(k).startswith('$') and '.' not in str(k)}; item['imported_at']=now(); docs.append(item)
        if docs: db()[cname].insert_many(docs,ordered=False); total+=len(docs)
    try: db().audit.insert_one({'event':'database_import','records':total,'actor':session['admin'],'at':now()})
    except Exception: pass
    return jsonify(ok=True,inserted=total)

@app.route('/api/admin/test/<service>',methods=['POST'])
@admin_required
def test_service(service):
    result={'service':service,'ok':False,'checked_at':now(),'details':''}
    try:
        if service=='database': db().command('ping'); result.update(ok=True,details='MongoDB ping succeeded.')
        elif service=='smtp':
            host=os.getenv('SMTP_HOST',''); port=int(os.getenv('SMTP_PORT','587'))
            if not host: raise RuntimeError('SMTP_HOST is missing')
            with socket.create_connection((host,port),timeout=5): pass
            result.update(ok=True,details=f'TCP connection to {host}:{port} succeeded. This does not send an email or verify credentials.')
        elif service=='daraja':
            result.update(ok=bool(os.getenv('CONSUMER_KEY') and os.getenv('CONSUMER_SECRET')),details='Credentials are present.' if os.getenv('CONSUMER_KEY') and os.getenv('CONSUMER_SECRET') else 'Daraja credentials are not configured; no live payment request was sent.')
        elif service in ('whatsapp','sms'):
            result.update(ok=bool(os.getenv('WHATSAPP_TOKEN') if service=='whatsapp' else os.getenv('SMS_API_KEY')),details='Provider credentials present.' if (os.getenv('WHATSAPP_TOKEN') if service=='whatsapp' else os.getenv('SMS_API_KEY')) else f'{service.upper()} provider credentials are not configured; no message was sent.')
        else: return jsonify(error='Unknown service. Try database, smtp, daraja, sms, whatsapp.'),400
    except Exception as e: result['details']=str(e)[:300]
    try: db().api_checks.insert_one(result.copy())
    except Exception: pass
    return jsonify(result)

@app.route('/api/admin/send-email',methods=['POST'])
@admin_required
def send_email():
    data=request.get_json(silent=True) or {}; to=data.get('to','').strip(); subject=data.get('subject','').strip(); body=data.get('body','')
    if not to or '@' not in to or not subject or not body: return jsonify(error='Valid recipient, subject and message are required'),400
    try:
        msg=EmailMessage(); msg['Subject']=subject; msg['From']=os.getenv('SMTP_FROM',os.getenv('SMTP_USERNAME','')); msg['To']=to; msg.set_content(body)
        host=os.getenv('SMTP_HOST','smtp.gmail.com'); port=int(os.getenv('SMTP_PORT','587'))
        with smtplib.SMTP(host,port,timeout=10) as server:
            server.ehlo(); server.starttls(context=ssl.create_default_context()); server.ehlo()
            server.login(os.getenv('SMTP_USERNAME',''),os.getenv('SMTP_PASSWORD','')); server.send_message(msg)
        try: db().email_logs.insert_one({'to':to,'subject':subject,'status':'sent','at':now(),'actor':session['admin']})
        except Exception: pass
        return jsonify(ok=True,message='Email sent')
    except Exception as e:
        try: db().email_logs.insert_one({'to':to,'subject':subject,'status':'failed','error':str(e)[:250],'at':now()})
        except Exception: pass
        return jsonify(ok=False,error='Email delivery failed. Verify SMTP credentials and provider security settings.'),502

@app.route('/receipt/<record_id>')
@admin_required
def receipt(record_id):
    ident=oid(record_id); doc=db().invoices.find_one({'_id':ident}) if ident else None
    if not doc: abort(404)
    return render_template('receipt.html', record=safe_doc(doc), company=os.getenv('COMPANY_NAME','Geopram Technologies'))

@app.route('/certificate/<record_id>')
@admin_required
def certificate(record_id):
    ident=oid(record_id); doc=db().certificates.find_one({'_id':ident}) if ident else None
    if not doc: abort(404)
    return render_template('certificate.html', record=safe_doc(doc), company=os.getenv('COMPANY_NAME','Geopram Technologies'))

@app.errorhandler(404)
def not_found(e):
    if request.path.startswith('/api/'): return jsonify(error='Not found'),404
    return render_template('error.html',code=404,message='The page you requested could not be found.'),404
@app.errorhandler(500)
def server_error(e):
    if request.path.startswith('/api/'): return jsonify(error='Internal server error. Check deployment logs.'),500
    return render_template('error.html',code=500,message='Something went wrong. Please try again.'),500

if __name__=='__main__': app.run(host='0.0.0.0',port=int(os.getenv('PORT','5000')),debug=os.getenv('FLASK_DEBUG','false').lower()=='true')
