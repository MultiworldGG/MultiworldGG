{% from "macros.lua" import dict_to_recipe, variable_to_lua %}
-- this file gets written automatically by the Archipelago Randomizer and is in its raw form a Jinja2 Template
require('lib')
data.raw["rocket-silo"]["rocket-silo"].fluid_boxes = {
    {
        production_type = "input",
        pipe_picture = assembler2pipepictures(),
        pipe_covers = pipecoverspictures(),
        volume = 1000,
        base_area = 10,
        base_level = -1,
        pipe_connections = {
            { flow_direction = "input", direction = defines.direction.south, position = { 0, 4.2 } },
            { flow_direction = "input", direction = defines.direction.north, position = { 0, -4.2 } },
            { flow_direction = "input", direction = defines.direction.east, position = { 4.2, 0 } },
            { flow_direction = "input", direction = defines.direction.west, position = { -4.2, 0 } }
        }
    },
    {
        production_type = "input",
        pipe_picture = assembler2pipepictures(),
        pipe_covers = pipecoverspictures(),
        volume = 1000,
        base_area = 10,
        base_level = -1,
        pipe_connections = {
            { flow_direction = "input", direction = defines.direction.south, position = { -3, 4.2 } },
            { flow_direction = "input", direction = defines.direction.north, position = { -3, -4.2 } },
            { flow_direction = "input", direction = defines.direction.east, position = { 4.2, -3 } },
            { flow_direction = "input", direction = defines.direction.west, position = { -4.2, -3 } }
        }
    },
    {
        production_type = "input",
        pipe_picture = assembler2pipepictures(),
        pipe_covers = pipecoverspictures(),
        volume = 1000,
        base_area = 10,
        base_level = -1,
        pipe_connections = {
            { flow_direction = "input", direction = defines.direction.south, position = { 3, 4.2 } },
            { flow_direction = "input", direction = defines.direction.north, position = { 3, -4.2 } },
            { flow_direction = "input", direction = defines.direction.east, position = { 4.2, 3 } },
            { flow_direction = "input", direction = defines.direction.west, position = { -4.2, 3 } }
        }
    }
}
data.raw["rocket-silo"]["rocket-silo"].fluid_boxes_off_when_no_fluid_recipe = true
data.raw["rocket-silo"]["rocket-silo"].rocket_parts_required = {{ rocket_parts }}

data.raw.technology["lightning-rod"] = {
    type = "technology",
    name = "lightning-rod",
    icon = "__space-age__/graphics/icons/lightning-rod.png",
    icon_size = 64,
    hidden = true,
    effects =
    {
      {
        type = "unlock-recipe",
        recipe = "lightning-rod",
      },
    },
    prerequisites = {"steel-processing"},
    unit =
    {
      count = 100,
      ingredients =
      {
        {"automation-science-pack", 1}
      },
      time = 5
    }
  }
data.raw.technology["lightning-collector"] = {
    type = "technology",
    name = "lightning-collector",
    icon = "__space-age__/graphics/technology/lightning-collector.png",
    icon_size = 256,
    effects =
    {
      {
        type = "unlock-recipe",
        recipe = "lightning-collector",
      },
    },
    prerequisites = {"electromagnetic-science-pack"}
  }


{%- for recipe_name, recipe in custom_recipes.items() %}
    data.raw["recipe"]["{{recipe_name}}"].category = "{{recipe.category}}"
    data.raw["recipe"]["{{recipe_name}}"].ingredients = {{ dict_to_recipe(recipe.ingredients, liquids) }}
    data.raw["recipe"]["{{recipe_name}}"].results = {{ dict_to_recipe(recipe.products, liquids) }}

{%- endfor %}

local technologies = data.raw["technology"]
local new_tree_copy

local template_tech = table.deepcopy(technologies["automation"])
{#-  ensure the copy unlocks nothing #}
template_tech.unlocks = {}
template_tech.upgrade = false
template_tech.effects = {}
template_tech.prerequisites = {}

{%- if max_science_pack < 10 %}
    technologies["space-science-pack"].effects = {}
    {%- if max_science_pack == 0 %}
        table.insert (technologies["automation"].effects, {type = "unlock-recipe", recipe = "satellite"})
    {%- elif max_science_pack == 1 %}
        table.insert (technologies["logistic-science-pack"].effects, {type = "unlock-recipe", recipe = "satellite"})
    {%- elif max_science_pack == 2 %}
        table.insert (technologies["military-science-pack"].effects, {type = "unlock-recipe", recipe = "satellite"})
    {%- elif max_science_pack == 3 %}
        table.insert (technologies["chemical-science-pack"].effects, {type = "unlock-recipe", recipe = "satellite"})
    {%- elif max_science_pack == 4 %}
        table.insert (technologies["production-science-pack"].effects, {type = "unlock-recipe", recipe = "satellite"})
    {%- elif max_science_pack == 5 %}
        table.insert (technologies["utility-science-pack"].effects, {type = "unlock-recipe", recipe = "satellite"})
    {%- elif max_science_pack == 6 %}
        table.insert (technologies["metallurgic-science-pack"].effects, {type = "unlock-recipe", recipe = "satellite"})
    {%- elif max_science_pack == 7 %}
        table.insert (technologies["agricultural-science-pack"].effects, {type = "unlock-recipe", recipe = "satellite"})
    {%- elif max_science_pack == 8 %}
        table.insert (technologies["electromagnetic-science-pack"].effects, {type = "unlock-recipe", recipe = "satellite"})
    {%- elif max_science_pack == 9 %}
        table.insert (technologies["cryogenic-science-pack"].effects, {type = "unlock-recipe", recipe = "satellite"})
    {% endif %}
{% endif %}
{%- if silo == 2 %}
    data.raw["recipe"]["rocket-silo"].enabled = true
{% endif %}

function set_ap_icon(tech)
    tech.icon = "__{{ mod_name }}__/graphics/icons/ap.png"
    tech.icons = nil
    tech.icon_size = 128
end

function set_ap_unimportant_icon(tech)
    tech.icon = "__{{ mod_name }}__/graphics/icons/ap_unimportant.png"
    tech.icons = nil
    tech.icon_size = 128
end

function copy_factorio_icon(tech, tech_source)
    tech.icon = table.deepcopy(technologies[tech_source].icon)
    tech.icons = table.deepcopy(technologies[tech_source].icons)
    tech.icon_size = table.deepcopy(technologies[tech_source].icon_size)
end

{# This got complex, but seems to be required to hit all corner cases #}
function adjust_energy(recipe_name, factor)
    local recipe = data.raw.recipe[recipe_name]
    if (recipe == nil) then
        return
    end
    local energy = recipe.energy_required

    if (recipe.normal ~= nil) then
        if (recipe.normal.energy_required == nil) then
            energy = 0.5
        else
            energy = recipe.normal.energy_required
        end
        recipe.normal.energy_required = energy * factor
    end
    if (recipe.expensive ~= nil) then
        if (recipe.expensive.energy_required == nil) then
            energy = 0.5
        else
            energy = recipe.expensive.energy_required
        end
        recipe.expensive.energy_required = energy * factor
    end
    if (energy ~= nil) then
        data.raw.recipe[recipe_name].energy_required = energy * factor
    elseif (recipe.expensive == nil and recipe.normal == nil) then
        data.raw.recipe[recipe_name].energy_required = 0.5 * factor
    end
end

function set_energy(recipe_name, energy)
    local recipe = data.raw.recipe[recipe_name]

    if (recipe == nil) then
        return
    end
    if (recipe.normal ~= nil) then
        recipe.normal.energy_required = energy
    end
    if (recipe.expensive ~= nil) then
        recipe.expensive.energy_required = energy
    end
    if (recipe.expensive == nil and recipe.normal == nil) then
        recipe.energy_required = energy
    end
end

data.raw["assembling-machine"]["assembling-machine-1"].crafting_categories = table.deepcopy(data.raw["assembling-machine"]["assembling-machine-3"].crafting_categories)
data.raw["assembling-machine"]["assembling-machine-2"].crafting_categories = table.deepcopy(data.raw["assembling-machine"]["assembling-machine-3"].crafting_categories)
data.raw["assembling-machine"]["assembling-machine-1"].fluid_boxes = table.deepcopy(data.raw["assembling-machine"]["assembling-machine-2"].fluid_boxes)
data.raw["assembling-machine"]["assembling-machine-1"].fluid_boxes_off_when_no_fluid_recipe = data.raw["assembling-machine"]["assembling-machine-2"].fluid_boxes_off_when_no_fluid_recipe
if mods["factory-levels"] then
    -- Factory-Levels allows the assembling machines to get faster (and depending on settings), more productive at crafting products, the more the
    -- assembling machine crafts the product.  If the machine crafts enough, it may auto-upgrade to the next tier.
    for i = 1, 25, 1 do
        data.raw["assembling-machine"]["assembling-machine-1-level-" .. i].crafting_categories = table.deepcopy(data.raw["assembling-machine"]["assembling-machine-3"].crafting_categories)
        data.raw["assembling-machine"]["assembling-machine-1-level-" .. i].fluid_boxes = table.deepcopy(data.raw["assembling-machine"]["assembling-machine-2"].fluid_boxes)
    end
    for i = 1, 50, 1 do
        data.raw["assembling-machine"]["assembling-machine-2-level-" .. i].crafting_categories = table.deepcopy(data.raw["assembling-machine"]["assembling-machine-3"].crafting_categories)
    end
end

data.raw["ammo"]["artillery-shell"].stack_size = 10

{# each randomized tech gets set to be invisible, with new nodes added that trigger those #}
{%- for original_tech_name in base_tech_table -%}
technologies["{{ original_tech_name }}"].hidden = true
technologies["{{ original_tech_name }}"].unit = nil
technologies["{{ original_tech_name }}"].research_trigger = {type = "craft-item", item = "item-unknown"}
{% endfor %}
{%- for location, item in locations %}
{#- the tech researched by the local player #}
new_tree_copy = table.deepcopy(template_tech)
new_tree_copy.name = "ap-{{ location.address }}-"{# use AP ID #}
{%- if location.crafted_item is not none %}
new_tree_copy.research_trigger = {
    type = "{{ 'craft-fluid' if location.crafted_item in liquids else 'craft-item' }}",
    {{ 'fluid' if location.crafted_item in liquids else 'item' }} = {{ variable_to_lua(location.crafted_item) }}
}

new_tree_copy.unit = nil
--
{%- else %}
new_tree_copy.unit.count = {{ location.count }}
new_tree_copy.unit.ingredients = {{ variable_to_lua(location.factorio_ingredients) }}
--
{%- endif %}

{%- if location.revealed and item.name in base_tech_table %}

{#- copy Factorio Technology Icon #}
--

copy_factorio_icon(new_tree_copy, "{{ item.name }}")
{%- if item.name == "rocket-silo" and item.player == location.player %}
{%- for ingredient in custom_recipes["rocket-part"].ingredients %}
table.insert(new_tree_copy.effects, {type = "nothing", effect_description = "Ingredient {{ loop.index }}: {{ ingredient }}"})
{% endfor -%}
{% endif -%}
{%- elif location.revealed and item.name in progressive_technology_table -%}
--

copy_factorio_icon(new_tree_copy, "{{ progressive_technology_table[item.name][0] }}")
{%- else -%}
{#- use default AP icon if no Factorio graphics exist -#}
{% if item.advancement or not tech_tree_information %}--

set_ap_icon(new_tree_copy){% else %}--

set_ap_unimportant_icon(new_tree_copy){% endif %}
{%- endif -%}
{%- if tech_tree_information %}
new_tree_copy.essential = {{ variable_to_lua(item.advancement) }}
{%- endif -%}
{#- connect Technology  #}
{%- if location in tech_tree_layout_prerequisites %}
{%- for prerequisite in tech_tree_layout_prerequisites[location] %}
--

table.insert(new_tree_copy.prerequisites, "ap-{{ prerequisite.address }}-")
{% endfor %}
{% endif -%}
{#- add new Technology to game #}
data:extend{new_tree_copy}
{% endfor %}
{#- Recipe Rando #}
{% if recipe_time_scale %}
{%- for recipe_name, recipe in recipes.items() %}
{%- if recipe.category not in ("basic-solid", "basic-fluid", "agriculture") %}
adjust_energy("{{ recipe_name }}", {{ flop_random(*recipe_time_scale) }})
{%- endif %}
{%- endfor -%}
{% elif recipe_time_range %}
{%- for recipe_name, recipe in recipes.items() %}
{%- if recipe.category not in ("basic-solid", "basic-fluid", "agriculture") %}
set_energy("{{ recipe_name }}", {{ flop_random(*recipe_time_range) }})
{%- endif %}
{%- endfor -%}
{% endif %}

{%- if silo==2 %}
-- disable silo research for pre-placed silo
technologies["rocket-silo"].enabled = false
technologies["rocket-silo"].visible_when_disabled = false
{%- endif %}

data.raw.resource["tungsten-ore"].category = "basic-solid"

data.raw.planet.nauvis.map_gen_settings.autoplace_settings["entity"].settings["iron-stromatolite"] = {}
data.raw.planet.nauvis.map_gen_settings.autoplace_settings["entity"].settings["copper-stromatolite"] = {}

table.insert(data.raw.technology["quality-module-2"].effects, {type = "unlock-quality", quality = "uncommon"})
table.insert(data.raw.technology["quality-module-3"].effects, {type = "unlock-quality", quality = "uncommon"})
table.insert(data.raw.technology["quality-module-2"].effects, {type = "unlock-quality", quality = "rare"})
table.insert(data.raw.technology["quality-module-3"].effects, {type = "unlock-quality", quality = "rare"})

{%- if all_modules_allowed_everywhere %}
--
for name, recipe in pairs(data.raw.recipe) do
    recipe.allow_productivity = true
end
for name, data1 in pairs(data.raw) do
    for name2, data2 in pairs(data1) do
        if data2.allowed_effects ~= nil then
            data2.allowed_effects = {"consumption", "speed", "productivity", "pollution", "quality"}
        end
    end
end
{%- endif %}

data.raw.module["quality-module"].effect.quality = {{ (0.1 * quality_scaling) / 100 }}
data.raw.module["quality-module-2"].effect.quality = {{ (0.2 * quality_scaling) / 100 }}
data.raw.module["quality-module-3"].effect.quality = {{ (0.25 * quality_scaling) / 100 }}

data.raw.module["productivity-module"].effect.productivity = {{ (0.04 * productivity_scaling) / 100 }}
data.raw.module["productivity-module-2"].effect.productivity = {{ (0.06 * productivity_scaling) / 100 }}
data.raw.module["productivity-module-3"].effect.productivity = {{ (0.1 * productivity_scaling) / 100 }}

data.raw.recipe["automation-science-pack"].main_product = "automation-science-pack"
data.raw.recipe["logistic-science-pack"].main_product = "logistic-science-pack"
data.raw.recipe["chemical-science-pack"].main_product = "chemical-science-pack"
data.raw.recipe["military-science-pack"].main_product = "military-science-pack"
data.raw.recipe["production-science-pack"].main_product = "production-science-pack"
data.raw.recipe["utility-science-pack"].main_product = "utility-science-pack"
data.raw.recipe["electromagnetic-science-pack"].main_product = "electromagnetic-science-pack"
data.raw.recipe["agricultural-science-pack"].main_product = "agricultural-science-pack"
data.raw.recipe["metallurgic-science-pack"].main_product = "metallurgic-science-pack"
data.raw.recipe["satellite"].main_product = "satellite"
data.raw.recipe["rocket-silo"].main_product = "rocket-silo"

{%- if free_power %}
require("reenable_lightning")
{%- endif %}
