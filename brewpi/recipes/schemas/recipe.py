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
        """Serialize yeasts."""
        recipe = data.beerpy
        yeasts = list()
        for yeast in recipe.yeasts:
            y = dict()
            y["name"] = yeast.name
            y["version"] = yeast.version
            y["type"] = yeast.type
            y["form"] = yeast.form
            y["amount"] = yeast.amount
            y["_amount_is_weight"] = yeast._amount_is_weight
            y["laboratory"] = yeast.laboratory
            y["product_id"] = yeast.product_id
            y["min_temperature"] = yeast.min_temperature
            y["max_temperature"] = yeast.max_temperature
            y["flocculation"] = yeast.flocculation
            y["attenuation"] = yeast.attenuation
            y["notes"] = yeast.notes
            y["best_for"] = yeast.best_for
            y["times_cultured"] = yeast.times_cultured
            y["max_reuse"] = yeast.max_reuse
            y["_add_to_secondary"] = yeast._add_to_secondary
            # y["inventory"] = yeast.inventory
            # y["culture_date"] = yeast.culture_date
            yeasts.append(y)
        return yeasts

    def dump_hops(self, data):
        """Serialize Hops."""
        recipe = data.beerpy
        hops = list()
        for hop in recipe.hops:
            h = dict()
            h["name"] = hop.name
            h["alpha"] = hop.alpha
            h["amount"] = hop.amount
            h["use"] = hop.use
            h["time"] = hop.time
            h["notes"] = hop.notes
            h["type"] = hop.type
            h["form"] = hop.form
            h["beta"] = hop.beta
            h["hsi"] = hop.hsi
            h["origin"] = hop.origin
            h["substitutes"] = hop.substitutes
            h["humulene"] = hop.humulene
            h["caryophyllene"] = hop.caryophyllene
            h["cohumulone"] = hop.cohumulone
            h["myrcene"] = hop.myrcene
            # h["version"] = hop.version
            hops.append(h)
        return hops

    def dump_fermentables(self, data):
        """Serialize Fermentables."""
        fermentables = list()
        for fermentable in data.beerpy.fermentables:
            f = dict()
            f["name"] = fermentable.name
            f["version"] = fermentable.version
            f["type"] = fermentable.type
            f["amount"] = fermentable.amount
            f["_yield"] = fermentable._yield
            f["color"] = fermentable.color
            f["_add_after_boil"] = fermentable._add_after_boil
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
        """Serialize Miscs."""
        miscs = list()
        for misc in data.beerpy.miscs:
            m = dict()
            m["name"] = misc.name
            m["type"] = misc.type
            m["use"] = misc.use
            m["time"] = misc.time
            m["amount"] = misc.amount
            m["_amount_is_weight"] = misc._amount_is_weight
            m["use_for"] = misc.use_for
            m["notes"] = misc.notes
            miscs.append(m)
        return miscs

    def dump_style(self, data):
        """Serialize Style."""
        recipe = data.beerpy
        s = dict()
        style = recipe.style
        s["name"] = style.name
        s["category"] = style.category
        s["version"] = style.version
        s["category_number"] = style.category_number
        s["style_letter"] = style.style_letter
        s["style_guide"] = style.style_guide
        s["type"] = style.type
        s["og_min"] = style.og_min
        s["og_max"] = style.og_max
        s["fg_min"] = style.fg_min
        s["fg_max"] = style.fg_max
        s["ibu_min"] = style.ibu_min
        s["ibu_max"] = style.ibu_max
        s["color_min"] = style.color_min
        s["color_max"] = style.color_max
        s["carb_min"] = style.carb_min
        s["carb_max"] = style.carb_max
        s["abv_min"] = style.abv_min
        s["abv_max"] = style.abv_max
        s["notes"] = style.notes
        # s["profile"] = style.profile
        # s["ingredients"] = style.ingredients
        # s["examples"] = style.examples
        return s

    def dump_recipe(self, data):
        """Serialize Recipe."""
        recipe = data.beerpy
        r = dict()
        r["name"] = recipe.name
        r["version"] = recipe.version
        r["type"] = recipe.type
        r["brewer"] = recipe.brewer
        r["asst_brewer"] = recipe.asst_brewer
        r["batch_size"] = recipe.batch_size
        r["boil_size"] = recipe.boil_size
        r["boil_time"] = recipe.boil_time
        r["efficiency"] = recipe.efficiency
        r["notes"] = recipe.notes
        r["taste_notes"] = recipe.taste_notes
        r["taste_rating"] = recipe.taste_rating
        r["og"] = recipe.og
        r["fg"] = recipe.fg
        r["fermentation_stages"] = recipe.fermentation_stages
        r["primary_age"] = recipe.primary_age
        r["primary_temp"] = recipe.primary_temp
        r["secondary_age"] = recipe.secondary_age
        r["secondary_temp"] = recipe.secondary_temp
        r["tertiary_age"] = recipe.tertiary_age
        r["tertiary_temp"] = recipe.tertiary_temp
        r["age"] = recipe.age
        r["age_temp"] = recipe.age_temp
        r["date"] = recipe.date
        r["carbonation"] = recipe.carbonation
        r["_forced_carbonation"] = recipe._forced_carbonation
        r["priming_sugar_name"] = recipe.priming_sugar_name
        r["carbonation_temp"] = recipe.carbonation_temp
        r["priming_sugar_equiv"] = recipe.priming_sugar_equiv
        r["keg_priming_factor"] = recipe.keg_priming_factor
        # extensions
        r["est_og"] = recipe.est_og
        r["est_fg"] = recipe.est_fg
        r["est_color"] = recipe.est_color
        r["ibu"] = recipe.ibu
        r["ibu_method"] = recipe.ibu_method
        r["est_abv"] = recipe.est_abv
        r["abv"] = recipe.abv
        r["actual_efficiency"] = recipe.actual_efficiency
        r["calories"] = recipe.calories
        r["carbonation_used"] = recipe.carbonation_used
        r["color"] = recipe.color
        return r

    def dump_waters(self, data):
        """Serialize Water."""
        waters = data.beerpy.waters
        ws = list()
        for water in waters:
            w = dict()
            w["name"] = water.name
            w["version"] = water.version
            w["amount"] = water.amount
            w["calcium"] = water.calcium
            w["bicarbonate"] = water.bicarbonate
            w["sulfate"] = water.sulfate
            w["chloride"] = water.chloride
            w["sodium"] = water.sodium
            w["magnesium"] = water.magnesium
            w["ph"] = water.ph
            w["notes"] = water.notes
            ws.append(w)
        return ws

    def dump_mash(self, data):
        """Serialize Mash."""
        mash = data.beerpy.mash
        m = dict()
        m["name"] = mash.name
        m["version"] = mash.version
        m["grain_temp"] = mash.grain_temp
        m["notes"] = mash.notes
        m["tun_temp"] = mash.tun_temp
        m["sparge_temp"] = mash.sparge_temp
        m["ph"] = mash.ph
        m["tun_weight"] = mash.tun_weight
        m["tun_specific_heat"] = mash.tun_specific_heat
        m["equip_adjust"] = mash.equip_adjust
        msteps = mash.steps
        sps = list()
        for step in msteps:
            # print(step)
            ms = dict()
            ms["name"] = step.name
            ms["version"] = step.version
            ms["type"] = step.type
            ms["infuse_amount"] = step.infuse_amount
            ms["step_temp"] = step.step_temp
            ms["step_time"] = step.step_time
            ms["end_temp"] = step.end_temp
            ms["decoction_amt"] = step.decoction_amt
            # m["ramp_time"] = step.ramp_time
            # print(m)
            sps.append(ms)
        m["mash_steps"] = sps
        return m

    def dump_beerpy(self, data):
        """Serialize full xml."""
        ret_recipe = dict()
        # recipe = data.beerpy
        ret_recipe = self.dump_recipe(data)
        ret_recipe["id"] = data.id
        ret_recipe["hops"] = self.dump_hops(data)
        ret_recipe["fermentables"] = self.dump_fermentables(data)
        ret_recipe["yeasts"] = self.dump_yeasts(data)
        ret_recipe["miscs"] = self.dump_miscs(data)
        ret_recipe["style"] = self.dump_style(data)
        ret_recipe["waters"] = self.dump_waters(data)
        ret_recipe["mash"] = self.dump_mash(data)
        return ret_recipe

    def dump(self, in_data, **kwargs):
        """Serialize List."""
        ret_recipes = list()

        if type(in_data) is list:
            for data in in_data:
                ret_recipes.append(self.dump_beerpy(data))
            return ret_recipes
        else:
            return self.dump_beerpy(in_data)
