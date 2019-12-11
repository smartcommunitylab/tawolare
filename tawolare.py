# -*- coding: utf-8 -*-
"""
Created on Tue Apr 07 15:11:49 2014
@author: Maurizio Napolitano <napo@fbk.eu>
The MIT License (MIT)
Copyright (c) 2016 Fondazione Bruno Kessler http://fbk.eu
Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
"""

from catastodb import Catasto
from gpsphoto import Photo
from bottle import Bottle, view, request, response, template,  static_file
import os
import json
app =Bottle()
app.config['autojson'] = True

@app.route('/serverinfo')
def serverInfo():
    servername = request.environ.get('SERVER_NAME')
    port =  request.environ.get('SERVER_PORT')
    scriptname = request.script_name
    scriptname.strip("/")
    if port != "80":
        port = ":" + port 
    else:
	port = ""
    servername = "http://" + servername +port + scriptname 
    return servername

@app.route('/www/<filepath:path>')
def server_static(filepath):
    return static_file(filepath, root= './www/')
    
@app.route('/api')
@view('api.tpl')
def apidesc():
    try:
        return {"servername": serverInfo() }
    except Exception as e:
        return e
    
@app.route('/showip')
def show_ip():
    ip = request.environ.get('REMOTE_ADDR')
    return template("Your IP is: {{ip}}", ip=ip)

@app.route('/api/particella/<y>/<x>')
def particella(x,y):
    response.content_type = 'application/json'
    try:
        catasto = Catasto()
        landParcel = catasto.findLandParcel(x,y)  
        return catasto.joinGeoJSON(landParcel)
    except Exception as e:
        return e

@app.route('/api/trovaparticella')
def trovaparticella():
    if request.get_header('Accept'):
        print('Get header: {0}'.format(request.get_header('Accept')))
    #if request.get_header('Accept') and request.get_header('Accept') == 'application/json':
    response.content_type = 'application/json'
    try:
        ccat = request.query['idcomune']
        nums = request.query['numparticella'].split(',')
        catasto = Catasto()
        parcels = []
        for num in nums:
            parcels += catasto.findLandParcelbyId(num.strip(),ccat)
        idgeom = 0
        for parcel in parcels:
            parcel['geometry']['id'] = idgeom
            idgeom += 1
        return catasto.joinGeoJSON(parcels)
    except Exception as e:
        return e

@app.route('/api/comune/amministrativo/<ids>')
def nametownship(ids):
    response.content_type = 'application/json'
    catasto = Catasto()
    townships = []
    idgeom = 0
    for id in ids.split(','):
        townships += catasto.nameGeoTowhship(id.strip(),idgeom)
        idgeom += 1
    return catasto.joinGeoJSON(townships)

@app.route('/api/comune/amministrativo/<y>/<x>')
def township(x,y):
    response.content_type = 'application/json'
    catasto = Catasto()
    township = catasto.findGeoTownship(x,y)
    return township

@app.route('/api/comune/catastale/<ids>')
def namecadastry(ids):
    response.content_type = 'application/json'
    catasto = Catasto()
    cadastries = []
    idgeom = 0
    for id in ids.split(','):
        cadastries += catasto.findGeoCadastryById(id.strip(),idgeom)
        idgeom += 1
    return catasto.joinGeoJSON(cadastries)

@app.route('/api/comune/catastale/<y>/<x>')
def findcadastry(x,y):
    response.content_type = 'application/json'
    catasto = Catasto()
    cadastries = catasto.findGeoCadastry(x,y)
    return cadastries

@app.error(404)
@view('404.tpl')
def error404(error):
    try:
        return
    except Exception as e:
        return e


@app.route('/api/comune/catastale/lista',method='GET')
def getCadastryTownships():
    response.content_type = 'application/json'
    catasto = Catasto()
    cadastries = catasto.listCadastryTownships()
    return json.dumps(cadastries, ensure_ascii=False).encode('utf-8')

@app.route('/api/upload', method='POST')
def do_upload():
    upload = request.files.get('upload')
    data = request.files.upload
    name, ext = os.path.splitext(upload.filename)
    if ext not in ('.png','.jpg','.jpeg'):
        return 'File extension not allowed.'
    save_path = os.path.curdir + os.sep + "www" + os.sep + "photos" +  os.sep + upload.filename
    if os.path.isfile(save_path):
        os.remove(save_path)
    with open(save_path, 'w') as open_file:
        open_file.write(data.file.read())
    open_file.close()
    p = Photo(save_path)
    geoposition = []
    if p.latitudine != None:
        geoposition.append(str(p.getGeoJSON()))
        catasto = Catasto()
        particelle = catasto.findLandParcel(p.longitudine,p.latitudine)  
        for p in particelle:
            geoposition.append(p)
        geoposition = catasto.joinGeoJSON(geoposition)
    return str(geoposition)

@app.route('/api/comprensorio/<ids>')
def getComprensorio(ids):
    response.content_type = 'application/json'
    catasto = Catasto()
    comprensori = []
    idgeom = 0
    for id in ids.split(','):
        comprensori += catasto.findComprensorioById(id.strip(),idgeom)
        idgeom += 1
    return catasto.joinGeoJSON(comprensori)

@app.route('/api/comunitadivalle/<ids>')
def getCValle(ids):
    response.content_type = 'application/json'
    catasto = Catasto()
    cvalle = []
    idgeom = 0
    for id in ids.split(','):
        cvalle += catasto.findCValleById(id.strip(),idgeom)
        idgeom += 1
    return catasto.joinGeoJSON(cvalle)

        
@app.route("/")
@view('index.tpl')
def home():
    try:
        return {"servername": serverInfo()}
    except Exception as e:
        return e
        
@app.route('/test')
def test():
    try:
        y = '46.06683'
        x = '11.12164'
        y = '46.05867'
        x = '11.11297' #?z=19
        catasto = Catasto()
        landParcel = catasto.findLandParcel(x,y)
        print len(landParcel)
        print landParcel
        cadastry = catasto.findCadastry(x,y)
        comune = catasto.findTownship(x,y)
        print cadastry
        print comune
        dimmi = catasto.touch(catasto.ammcat,catasto.ammcat_id,catasto.ammcat_label,x,y)
        print dimmi
        return "<a href='./api/particella/46.06683/11.12164'>particella/</a>"
    except Exception as e:
        print(e)
        
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8515, debug=True,reloader=True)

