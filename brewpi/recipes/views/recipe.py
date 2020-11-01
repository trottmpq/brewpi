"""Recipe views."""
from flask import current_app, request
from flask_restx import Namespace, Resource, fields

from ..models import Recipe
from ..schemas import RecipeSchema

api = Namespace("Recipe", description="Recipe related operations")

nsmodel = api.model(
    "Recipe",
    {
        "id": fields.Integer(readonly=True, description="Recipe Identifier"),
        "xml": fields.String(required=True, description="Recipe XML file", example="brewpi/recipes/xml/sierranevada.xml"),
    },
)



@api.route("/")
class RecipeList(Resource):
    """Shows a list of all Recipes, and lets you POST to add new recipes."""

    @api.doc("list_recipes")
    # @api.marshal_list_with(nsmodel)
    def get(self):
        """List all Recipes."""
        schema = RecipeSchema(many=True)
        query = Recipe.query.all()
        return schema.dump(query)

    @api.doc("create_recipe")
    @api.expect(nsmodel)
    def post(self):
        """Create a new Recipe."""
        schema = RecipeSchema()
        data = schema.load(request.get_json())
        if not schema.validate(data):
            current_app.logger.info(f"New Item Data: {data}")
            new_item = Recipe.create(**data)
            return schema.dump(new_item)
        return api.abort(404, message="Invalid Fields. Cannot Create Item")


@api.route("/<id>")
@api.param("id", "The Recipe identifier")
@api.response(404, "Recipe not found")
class RecipeItem(Resource):
    """Retrieve a recipe instance."""

    @api.doc("get_recipe")
    # @api.marshal_with(nsmodel)
    def get(self, id):
        """Fetch a Recipe given its identifier."""
        schema = RecipeSchema()
        query = Recipe.get_by_id(id)
        if not query:
            api.abort(404, message="Recipe {} doesn't exist".format(id))
        return schema.dump(query)

    
    @api.doc("delete_recipe")
    @api.response(204, "Recipe deleted")
    @api.response(404, "Recipe does not exist")
    def delete(self, id):
        """Delete a recipe given its identifier."""
        recipe = Recipe.get_by_id(id)
        if not recipe:
            api.abort(404, message=f"Recipe {id} doesn't exist")
        recipe.delete()
        return "", 204

    @api.expect(nsmodel)
    @api.marshal_with(nsmodel)
    def put(self, id):
        """Update a recipe given its identifier."""
        schema = RecipeSchema()
        recipe = Recipe.get_by_id(id)
        if not recipe:
            api.abort(404, message=f"Recipe {id} doesn't exist")

        data = schema.load(request.get_json(), partial=True)
        if data:
            for key, value in data.items():
                if value is not None:
                    if hasattr(recipe, key):
                        setattr(recipe, key, value)
            recipe.update()
            return schema.dump(recipe)
        return api.abort(404, message="Invalid Fields. Cannot Update recipe")


@api.route("/<id>/yeasts")
@api.param("id", "The Recipe identifier")
@api.response(404, "Recipe not found")
class RecipeItemYeast(Resource):
    """Retrieve recipe yeasts."""
    @api.doc("get_recipe_yeasts")
    def get(self, id):
        """Fetch the yeasts used in a recipe."""
        schema = RecipeSchema()
        recipe = Recipe.get_by_id(id)
        if not recipe:
            api.abort(404, message="Recipe {} doesn't exist".format(id))
        return schema.dump_yeasts(recipe)

@api.route("/<id>/miscs")
@api.param("id", "The Recipe identifier")
@api.response(404, "Recipe not found")
class RecipeItemMiscs(Resource):
    """Retrieve the miscs of a recipe."""
    @api.doc("get_recipe_miscs")
    def get(self, id):
        """Fetch the miscs of a recipe."""
        schema = RecipeSchema()
        recipe = Recipe.get_by_id(id)
        if not recipe:
            api.abort(404, message="Recipe {} doesn't exist".format(id))
        return schema.dump_miscs(recipe)


@api.route("/<id>/fermentables")
@api.param("id", "The Recipe identifier")
@api.response(404, "Recipe not found")
class RecipeItemFermentables(Resource):
    """Retrieve the recipe fermentables"""
    @api.doc("get_recipe_fermentables")
    def get(self, id):
        """Retrieve the recipe fermentables"""
        schema = RecipeSchema()
        recipe = Recipe.get_by_id(id)
        if not recipe:
            api.abort(404, message="Recipe {} doesn't exist".format(id))
        return schema.dump_fermentables(recipe)


@api.route("/<id>/hops")
@api.param("id", "The Recipe identifier")
@api.response(404, "Recipe not found")
class RecipeItemHops(Resource):
    """Retrieve the hops of a recipe."""
    @api.doc("get_recipe_yeast")
    def get(self, id):
        """Fetch the hops of a recipe."""
        schema = RecipeSchema()
        recipe = Recipe.get_by_id(id)
        if not recipe:
            api.abort(404, message="Recipe {} doesn't exist".format(id))
        return schema.dump_hops(recipe)