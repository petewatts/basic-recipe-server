import argparse
from flask import Flask, abort, request
from flask_restplus import Api, Resource, fields
from werkzeug.middleware.proxy_fix import ProxyFix
from recipes import RecipeDAO


app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app)
api = Api(app, version="1.0", title="Recipe API", description="Gousto Recipe API")

# API layout:
#   GET /by-cuisine/<type>  - List of recipes by cuisine
#   GET /recipes/<id>       - Retrieve recipe
#   PUT /recipes/<id>       - Update recipe details


recipe_ns = api.namespace("recipes", description="Recipe operations")

recipe = api.model(
    "Recipe",
    {
        "id": fields.Integer(readOnly=True, description="Recipe ID"),
        "created_at": fields.DateTime(description="Date the recipe was created"),
        "updated_at": fields.DateTime(description="Date the recipe was last Updated"),
        "box_type": fields.String(required=True, description="Recipe box type"),
        "title": fields.String(required=True, description="Recipe title"),
        "slug": fields.String(description="Recipe slug"),
        "short_title": fields.String(required=True, description="Recipe short title"),
        "marketing_description": fields.String(required=True, description="Recipe description"),
        "calories_kcal": fields.Integer(required=True, description="Calories (kcal)"),
        "protein_grams": fields.Integer(required=True, description="Protein (grams)"),
        "fat_grams": fields.Integer(required=True, description="Fat (grams)"),
        "carbs_grams": fields.Integer(required=True, description="Carbs (grams)"),
        "bulletpoint1": fields.String(required=True, description="Bulletpoint 1"),
        "bulletpoint2": fields.String(required=True, description="Bulletpoint 2"),
        "bulletpoint3": fields.String(required=True, description="Bulletpoint 3"),
        "recipe_diet_type_id": fields.String(required=True, description="Diet type ID"),
        "season": fields.String(required=True, description="Season"),
        "base": fields.String(required=True, description="Recipe base"),
        "protein_source": fields.String(required=True, description="Protein source"),
        "preparation_time_minutes": fields.Integer(required=True, description="Preparation time (minutes)"),
        "shelf_life_days": fields.Integer(required=True, description="Shelf life (days)"),
        "equipment_needed": fields.String(required=True, description="Equipment needed"),
        "origin_country": fields.String(required=True, description="Country of Origin"),
        "recipe_cuisine": fields.String(required=True, description="Recipe cuisine"),
        "in_your_box": fields.String(required=True, description="What's in your box?"),
        "gousto_reference": fields.Integer(required=True, description="Gousto reference"),
    },
)


DAO = RecipeDAO()
DAO.import_file('recipe-data.csv')


@recipe_ns.route("/<int:id>")
@recipe_ns.response(404, "Recipe not found")
@recipe_ns.param("id", "The recipe identifier")
class Recipe(Resource):
    """Show a single recipe item allow updating fields"""

    @recipe_ns.doc("get_recipe")
    @recipe_ns.marshal_with(recipe)
    def get(self, id):
        """Fetch a given resource"""
        return DAO.get(id)

    @recipe_ns.expect(recipe)
    @recipe_ns.marshal_with(recipe)
    def put(self, id):
        """Update a recipe by ID"""
        print(id, api.payload)
        return DAO.update(id, api.payload)


@api.route('/by-cuisine/<cuisine>')
@api.response(404, "Cuisine not found")
class Cuisine(Resource):
    """Show recipes by cuisine"""

    def get(self, cuisine):

        start = int(request.args.get('start', 1))
        limit = int(request.args.get('limit', 10))

        return get_paginated_list(cuisine, start, limit)


def get_paginated_list(cuisine, start, limit):
    recipes = DAO.by_cuisine(cuisine)
    if not recipes:
        return abort(404)

    def build_recipe(recipe):
        fields = ['id', 'title', 'marketing_description']
        return {field: recipe[field] for field in fields}

    count = len(recipes)
    if count < start:
        abort(404)
    # make response
    obj = {}
    obj['start'] = start
    obj['limit'] = limit
    obj['count'] = count
    obj['recipes'] = [build_recipe(recipe) for recipe in recipes[start - 1:start - 1 + limit]]
    return obj


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Recipe REST App")
    parser.add_argument("-d", "--debug", action="store_true", help="Debug (Do not use in production)")
    args = parser.parse_args()

    app.run(debug=args.debug)
