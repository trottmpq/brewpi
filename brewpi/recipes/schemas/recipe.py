"""Recipe schemas."""

from brewpi.extensions import ma
from ..models import Recipe


class RecipeSchema(ma.SQLAlchemyAutoSchema):
    """A Recipe Schema."""

    class Meta:
        """A Recipe Schema Metaclass."""

        model = Recipe
        include_fk = True
    
    def dump_beerpy(self,data):
        ret_recipe=dict()
        recipe = data.beerpy
        ret_recipe["id"] = data.id
        ret_recipe["name"] = recipe.name
        ret_recipe["brewer"] = recipe.brewer
        ret_recipe["og"] = recipe.og
        ret_recipe["fg"] = recipe.fg
        ret_recipe["ibu"] = recipe.ibu
        ret_recipe["abv"] = recipe.abv
        hops = list()
        for hop in recipe.hops:
            h = dict()
            h["name"] = hop.name
            h["alpha"] = hop.alpha
            h["amount"] = hop.amount
            h["use"] = hop.use
            h["form"] = hop.form
            h["notes"] = hop.notes
            h["time"] = hop.time
            h["version"] = hop.version
            h["type"] = hop.type
            h["beta"] = hop.beta
            h["hsi"] = hop.hsi
            h["origin"] = hop.origin
            h["substitutes"] = hop.substitutes
            h["humulene"] = hop.humulene
            h["caryophyllene"] = hop.caryophyllene
            h["cohumulone"] = hop.cohumulone
            h["myrcene"] = hop.myrcene
            hops.append(h)
        ret_recipe["hops"] = hops

        fermentables=list()
        for fermentable in recipe.fermentables:
            f=dict()
            f["name"] = fermentable.name
            f["amount"] = fermentable.amount
            f["_yield"] = fermentable._yield
            f["color"] = fermentable.color
            f["_add_after_boil"] = fermentable._add_after_boil
            f["version"] = fermentable.version
            f["type"] = fermentable.type
            f["origin"] = fermentable.origin
            f["supplier"] = fermentable.supplier
            f["notes"] = fermentable.notes
            f["coarse_fine_diff"] = fermentable.coarse_fine_diff
            f["moisture"] = fermentable.moisture
            f["diastatic_power"] = fermentable.diastatic_power
            f["protein"] = fermentable.protein
            f["max_in_batch"] = fermentable.max_in_batch
            f["_recommend_mash"] = fermentable._recommend_mash
            f["ibu_gal_per_lb"] = fermentable.ibu_gal_per_lb
            fermentables.append(f)
        ret_recipe["fermentables"] = fermentables

        yeasts = list()
        for yeast in recipe.yeasts:
            y = dict()
            y["name"] = yeast.name
            y["version"] = yeast.version
            y["type"] = yeast.type
            y["form"] = yeast.form
            y["attenuation"] = yeast.attenuation
            y["notes"] = yeast.notes
            y["laboratory"] = yeast.laboratory
            y["product_id"] = yeast.product_id
            y["flocculation"] = yeast.flocculation
            y["amount"] = yeast.amount
            y["_amount_is_weight"] = yeast._amount_is_weight
            y["min_temperature"] = yeast.min_temperature
            y["max_temperature"] = yeast.max_temperature
            y["best_for"] = yeast.best_for
            y["times_cultured"] = yeast.times_cultured
            y["max_reuse"] = yeast.max_reuse
            y["_add_to_secondary"] = yeast._add_to_secondary
            y["inventory"] = yeast.inventory
            y["culture_date"] = yeast.culture_date
            yeasts.append(y)
        ret_recipe["yeasts"] = yeasts

        miscs=list()
        for misc in recipe.miscs:
            m=dict()
            m["name"] = misc.name
            m["type"] = misc.type
            m["amount"] = misc.amount
            m["_amount_is_weight"] = misc._amount_is_weight
            m["use"] = misc.use
            m["use_for"] = misc.use_for
            m["time"] = misc.time
            m["notes"] = misc.notes
            miscs.append(m)
        ret_recipe["miscs"] = miscs


        return ret_recipe

    def dump(self, in_data, **kwargs):
        ret_recipes = list()
        
        if(type(in_data) is list):
            for data in in_data:
                ret_recipes.append(self.dump_beerpy(data))
            return ret_recipes
        else:
            return self.dump_beerpy(in_data)


