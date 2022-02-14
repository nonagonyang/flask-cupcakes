from flask import Flask, request, redirect, render_template,jsonify
from models import db, connect_db,Cupcake
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///flask_cupcakes_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False


from flask_debugtoolbar import DebugToolbarExtension
app.config['SECRET_KEY'] = "SECRETMAOMI"
debug = DebugToolbarExtension(app)
connect_db(app)


"""
Making a RESTful JSON API
"""
@app.route("/api/cupcakes")
def list_cupcakes():
    """
    GET /api/cupcakes
    Get data about all cupcakes.
    Respond with JSON like: {cupcakes: [{id, flavor, size, rating, image}, ...]}.
    The values should come from each cupcake instance.
    """
    cupcakes=[cupcake.serialize() for cupcake in Cupcake.query.all()]
    return jsonify(cupcakes=cupcakes)


@app.route("/api/cupcakes/<int:id>")
def get_todo(id):
    """
    GET /api/cupcakes/[cupcake-id]
    Get data about a single cupcake.
    Respond with JSON like: {cupcake: {id, flavor, size, rating, image}}.
    This should raise a 404 if the cupcake cannot be found.
    """
    cupcake=Cupcake.query.get_or_404(id)
    return jsonify(cupcake=cupcake.serialize())

@app.route("/api/cupcakes", methods=["POST"])
def create_cupcake():
    cupcake=Cupcake(flavor=request.json["flavor"], size=request.json["size"], rating=request.json["rating"],image=request.json["image"])
    db.session.add(cupcake)
    db.session.commit()
    response_json=jsonify(cupcake=cupcake.serialize())
    return(response_json,201)



@app.route("/api/cupcakes/<int:id>",methods=["PATCH"])
def update_cupcake(id):
    """
    PATCH /api/cupcakes/[cupcake-id]
    Update a cupcake with the id passed in the URL 
    and flavor, size, rating and image data 
    from the body of the request. 
    You can always assume that the entire cupcake object will be passed to the backend.
    This should raise a 404 if the cupcake cannot be found.
    Respond with JSON of the newly-updated cupcake, 
    like this: `{cupcake:{id, flavor, size, rating,image}}`.
    """
    cupcake=Cupcake.query.get_or_404(id)
    db.session.query(Cupcake).filter_by(id=id).update(request.json)
    cupcake.flavor=request.json.get("flavor",cupcake.favor)
    cupcake.size=request.json.get("size",cupcake.size)
    cupcake.rating=request.json.get("rating",cupcake.rating)
    cupcake.image=request.json.get("image",cupcake.iamge)
    db.session.commit()
    return jsonify(cupcake=cupcake.serialize())


@app.route("/api/cupcakes/<int:id>",methods=["DELETE"])
def delete_cupcake(id):
    """
    This should raise a 404 if the cupcake cannot be found.
    Delete cupcake with the id passed in the URL. 
    Respond with JSON like`{message:"Deleted"}`.
    """
    cupcake=Cupcake.query.get_or_404(id)
    db.session.delete(cupcake)
    db.session.commit()
    return jsonify(message="deleted")



@app.route("/")
def index_page():
    return render_template("index.html")