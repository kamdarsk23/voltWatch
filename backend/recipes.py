#is a page
from flask import Flask, request,jsonify
from flask_restx import Resource,Namespace,fields
from models import Recipe
from flask_jwt_extended import jwt_required

recipes_ns=Namespace('recipes',description="A namespace for recipes")

#model (serializer)
Recipe_model = recipes_ns.model (
    "Recipe",
    {
        "id":fields.Integer(),
        "title":fields.String(),
        "description":fields.String(),
    }
)



@recipes_ns.route('/hello')
class HelloResource(Resource):
    def get(self):
        return jsonify({"message":"Hello World"})

@recipes_ns.route('/Recipes')
class RecipesResouce(Resource):

    @recipes_ns.marshal_list_with(Recipe_model)
    def get(self):
        """return a list of all the Recipes"""
        recipes = Recipe.query.all()
        return recipes
    
    @recipes_ns.marshal_with(Recipe_model)
    @recipes_ns.expect(Recipe_model)
    @jwt_required()
    def post(self):
        """add a new Recipe """
        data=request.get_json()
        new_recipe=Recipe(
            title=data.get("title"),
            description=data.get("description"),
        )
        new_recipe.save()
        return new_recipe,201

@recipes_ns.route('/Recipe/<int:id>')
class RecipeResource(Resource):

    @recipes_ns.marshal_with(Recipe_model)
    def get(self,id):
        """get a Recipe from id"""
        recipe = Recipe.query.get_or_404(id)
        return recipe
    
    @recipes_ns.marshal_with(Recipe_model)
    @jwt_required()
    def put(self,id):
        """update a recipe by id"""
        recipe_to_update=Recipe.query.get_or_404(id)
        data=request.get_json()

        recipe_to_update.update(data.get("title"), data.get("description"))
        return recipe_to_update
    
    @recipes_ns.marshal_with(Recipe_model)
    @jwt_required()
    def delete(self,id):
        """delete a recipe by id"""
        recipe_to_delete=Recipe.query.get_or_404(id)
        recipe_to_delete.delete()
        return recipe_to_delete