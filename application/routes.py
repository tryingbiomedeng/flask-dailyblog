from flask import jsonify, request
from werkzeug import exceptions
from application import app, db
from application.models import Entry

print(Entry)

@app.route("/")
def hello_world():
  return jsonify({
    "message": "Hello World!", 
    "description": "Journal API",
    "endpoints": [
      "GET /",
      "GET /entries",
      "POST /entries",
      "GET /entries/<id>",
      "PATCH /entries/<id>",
      "DELETE /entries/<id>"
    ]
  }), 200

@app.route("/entries", methods=["GET"])
def get_entries():
  try:
    entries = Entry.query.all()
    return jsonify([e.json for e in entries]), 200
  except:
    raise exceptions.InternalServerError("An error occurred while fetching entries.")

@app.route("/entries/<int:id>", methods=["GET"])
def get_entry(id):
  try:
    entry = Entry.query.get(id)
    return jsonify(entry.json), 200
  except:
     raise exceptions.NotFound("Entry not available")
  
@app.route("/entries", methods=["POST"]) 
def create_entry():
  try:
    date, title, content, tag, author = request.json.values()
    new_entry = Entry( date=date, title=title, content=content, tag=tag, author=author )
    db.session.add(new_entry)
    db.session.commit()
    return jsonify(new_entry.json), 201
  except:
    raise exceptions.BadRequest(f"We cannot process your request some required fields are missing")

@app.route("/entries/<int:id>", methods=["PATCH"])
def update_entry(id):
  data = request.get_json()
  entry = Entry.query.get(id)

  if data.get('title'):
    entry.title = data['title']
  if data.get('content'):  
    entry.content = data['content']
  db.session.commit()
  return jsonify(entry.json)

@app.errorhandler(exceptions.InternalServerError)
def handle_500(err):
  return jsonify({"error": f"Oops {err}"}), 500

@app.errorhandler(exceptions.NotFound)
def handle_404(err):
  return jsonify({"error": f"Oops {err}"}), 404

@app.errorhandler(exceptions.BadRequest)
def handler_400(err):
  return jsonify({"error": f"Oops {err}"}), 400