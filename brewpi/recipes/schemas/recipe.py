"""Recipe schemas."""

from brewpi.extensions import ma
from ..models import Recipe


class RecipeSchema(ma.SQLAlchemyAutoSchema):
    """A Recipe Schema."""

    class Meta:
        """A Recipe Schema Metaclass."""

        model = Recipe
        include_fk = True
    
    def dump_yeasts(self, data):
        recipe = data.beerpy
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
        return yeasts
    
    def dump_hops(self, data):
        recipe = data.beerpy
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
        return hops


    def dump_fermentables(self, data):
        recipe = data.beerpy
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
        return fermentables

    def dump_miscs(self, data):
        recipe = data.beerpy
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
        return miscs

    def dump_recipe(self, data):
        recipe = data.beerpy
        r=dict()
        r["name"] = recipe.name
        r["version"] = recipe.version
        r["type"] = recipe.type
        r["brewer"] = recipe.brewer
        r["asst_brewer"] = recipe.asst_brewer
        r["batch_size"] = recipe.batch_size
        r["boil_time"] = recipe.boil_time
        r["boil_size"] = recipe.boil_size
        r["efficiency"] = recipe.efficiency
        r["notes"] = recipe.notes
        r["taste_notes"] = recipe.taste_notes
        r["taste_rating"] = recipe.taste_rating
        r["fermentation_stages"] = recipe.fermentation_stages
        r["primary_age"] = recipe.primary_age
        r["primary_temp"] = recipe.primary_temp
        r["secondary_age"] = recipe.secondary_age
        r["secondary_temp"] = recipe.secondary_temp
        r["tertiary_age"] = recipe.tertiary_age
        r["tertiary_temp"] = recipe.tertiary_temp
        r["carbonation"] = recipe.carbonation
        r["carbonation_temp"] = recipe.carbonation_temp
        r["age"] = recipe.age
        r["age_temp"] = recipe.age_temp
        r["date"] = recipe.date
        r["carbonation"] = recipe.carbonation
        r["_forced_carbonation"] = recipe._forced_carbonation
        r["priming_sugar_name"] = recipe.priming_sugar_name
        r["carbonation_temp"] = recipe.carbonation_temp
        r["priming_sugar_equiv"] = recipe.priming_sugar_equiv
        r["keg_priming_factor"] = recipe.keg_priming_factor
        r["est_og"] = recipe.est_og
        r["est_fg"] = recipe.est_fg
        r["est_color"] = recipe.est_color
        r["ibu_method"] = recipe.ibu_method
        r["est_abv"] = recipe.est_abv
        r["actual_efficiency"] = recipe.actual_efficiency
        r["calories"] = recipe.calories
        r["carbonation_used"] = recipe.carbonation_used
        r["abv"] = recipe.abv
        r["og"] = recipe.og
        r["fg"] = recipe.fg
        r["ibu"] = recipe.ibu
        r["color"] = recipe.color
        return r


    def dump_beerpy(self,data):
        ret_recipe=dict()
        recipe = data.beerpy
        ret_recipe = self.dump_recipe(data)
        ret_recipe["id"] = data.id
        
        
        ret_recipe["hops"] = self.dump_hops(data)
        ret_recipe["fermentables"] = self.dump_fermentables(data)
        ret_recipe["yeasts"] = self.dump_yeasts(data)
        ret_recipe["miscs"] = self.dump_miscs(data)
        return ret_recipe

    def dump(self, in_data, **kwargs):
        ret_recipes = list()
        
        if(type(in_data) is list):
            for data in in_data:
                ret_recipes.append(self.dump_beerpy(data))
            return ret_recipes
        else:
            return self.dump_beerpy(in_data)


