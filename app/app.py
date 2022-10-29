import hashlib
import os

import requests
from flask import Flask, json, Response
from flask import request
from flask_mongoengine import MongoEngine
from datetime import datetime


ONSALE_DATE = "onsaleDate"

app = Flask(__name__, template_folder='template')
app.debug = True
app.config['SECRET_KEY'] = 'DoEQqn2hVMkPJ4xj9iwNUGqK3gUlRmKbPGsuJb3mPgV2bxj9EJ'

db = MongoEngine(app)

if __name__ == "__main__":
    app.run()

@app.route('/api/searchComics', methods=["post"])
@app.route('/api/searchComics/', methods=["post"])
def search_comics():
    characters = request.json.get("characters", None)
    comics = request.json.get("comics", None)
    limit = request.json.get("limit", 10)
    offset = request.json.get("offset", 0)
    marvel_url = os.environ.get("MARVEL_URL")
    marvel_path_comics = os.environ.get("MARVEL_PATH_COMICS")
    marvel_path_character = os.environ.get("MARVEL_PATH_CHARACTER")
    public_key = os.environ.get("MARVEL_PUBLIC_KEY")
    private_key = os.environ.get("MARVEL_PRIVATE_KEY")
    dt = datetime.now()
    ts = datetime.timestamp(dt)
    array_ts = str(ts).split(".")
    str2hash = array_ts[0] + private_key + public_key
    result = hashlib.md5(str2hash.encode())
    hash_marvel = str(result.hexdigest())
    if offset == '':
        offset = 0
    if limit == '':
        limit = 10
    if comics is not None:
        base_url = marvel_url + "/" + marvel_path_comics + "?ts=" + str(array_ts[0]) + "&apikey=" + str(
            public_key) + "&hash=" + hash_marvel + "&orderBy=title"
        if comics is not None:
            if len(comics) > 0:
                base_url += "&titleStartsWith=" + str(comics)
        base_url += "&limit=" + str(limit)
        base_url += "&offset=" + str(offset)
        url = base_url
        headers = {
            'Accept': 'application/json',
        }
        print(url)
        response = requests.request("GET", url, headers=headers)
        if response:
            response_json = response.json()
            if response_json["code"] == 200 and response_json["status"] == "Ok":
                data = response_json["data"]
                comics = {
                    "offset": data["offset"],
                    "limit": data["limit"],
                    "total": data["total"],
                    "count": data["count"],
                    "data": [],
                }
                results = data["results"]
                for result in results:
                    imagen = ""
                    if len(result["images"]):
                        imagen = result["images"][0]["path"] + "." + result["images"][0]["extension"]
                    onsale_date = ""
                    if result["dates"]:
                        for dates in result["dates"]:
                            if dates["type"] == ONSALE_DATE:
                                onsale_date = dates["date"]
                    c = {
                        "id": result["id"],
                        "name": result["title"],
                        "imagen": imagen,
                        "onsaleDate": onsale_date,
                    }
                    comics["data"].append(c)
                return Response(response=json.dumps(comics), status=200, mimetype='application/json')
    else:
        base_url = marvel_url + "/" + marvel_path_character + "?ts=" + str(array_ts[0]) + "&apikey=" + str(
            public_key) + "&hash=" + hash_marvel + "&orderBy=name"
        if characters is not None:
            if len(characters) > 0:
                base_url += "&nameStartsWith=" + str(characters)
        base_url += "&limit=" + str(limit)
        base_url += "&offset=" + str(offset)
        url = base_url
        headers = {
            'Accept': 'application/json',
        }
        print(url)
        response = requests.request("GET", url, headers=headers)
        if response:
            response_json = response.json()
            if response_json["code"] == 200 and response_json["status"] == "Ok":
                data = response_json["data"]
                comics = {
                    "offset": data["offset"],
                    "limit": data["limit"],
                    "total": data["total"],
                    "count": data["count"],
                    "data": [],
                }
                results = data["results"]
                for result in results:
                    imagen = ""
                    if len(result["thumbnail"]):
                        imagen = result["thumbnail"]["path"] + "." + result["thumbnail"]["extension"]
                    appearances = 0
                    if result["comics"]:
                        appearances = appearances + result["comics"]["available"]
                    if result["series"]:
                        appearances = appearances + result["series"]["available"]
                    if result["stories"]:
                        appearances = appearances + result["stories"]["available"]
                    if result["events"]:
                        appearances = appearances + result["events"]["available"]
                    c = {
                        "id": result["id"],
                        "name": result["name"],
                        "imagen": imagen,
                        "appearances": appearances,
                    }
                    comics["data"].append(c)
                return Response(response=json.dumps(comics), status=200, mimetype='application/json')

@app.route('/api/comics/<int:id>', methods=["get"])
def get_comic(id):
    marvel_url = os.environ.get("MARVEL_URL")
    marvel_path_comics = os.environ.get("MARVEL_PATH_COMICS")
    public_key = os.environ.get("MARVEL_PUBLIC_KEY")
    private_key = os.environ.get("MARVEL_PRIVATE_KEY")
    dt = datetime.now()
    ts = datetime.timestamp(dt)
    array_ts = str(ts).split(".")
    str2hash = array_ts[0] + private_key + public_key
    result = hashlib.md5(str2hash.encode())
    hash_marvel = str(result.hexdigest())
    base_url = marvel_url + "/" + marvel_path_comics + "/" + str(id) + "?ts=" + str(array_ts[0]) + "&apikey=" + str(
        public_key) + "&hash=" + hash_marvel + "&orderBy=title"
    url = base_url
    headers = {
        'Accept': 'application/json',
    }
    print(url)
    response = requests.request("GET", url, headers=headers)
    if response:
        response_json = response.json()
        if response_json["code"] == 200 and response_json["status"] == "Ok":
            data = response_json["data"]
            comics = {
                "offset": data["offset"],
                "limit": data["limit"],
                "total": data["total"],
                "count": data["count"],
                "data": [],
            }
            results = data["results"]
            for result in results:
                imagen = ""
                if len(result["images"]):
                    imagen = result["images"][0]["path"] + "." + result["images"][0]["extension"]
                onsale_date = ""
                if result["dates"]:
                    for dates in result["dates"]:
                        if dates["type"] == ONSALE_DATE:
                            onsale_date = dates["date"]
                c = {
                    "id": result["id"],
                    "name": result["title"],
                    "imagen": imagen,
                    "onsaleDate": onsale_date,
                }
                comics["data"].append(c)
            return Response(response=json.dumps(comics), status=200, mimetype='application/json')