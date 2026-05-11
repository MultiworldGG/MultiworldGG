data.raw.planet.nauvis.map_gen_settings.autoplace_settings["entity"].settings["fulgoran-ruin-attractor"] = {}
data.raw.planet.nauvis.lightning_properties = {
      lightnings_per_chunk_per_tick = 1 / (60 * 10), --cca once per chunk every 10 seconds (600 ticks)
      search_radius = 10.0,
      lightning_types = {"lightning"},
      priority_rules =
      {
        {
          type = "id",
          string = "lightning-collector",
          priority_bonus = 10000
        },
        {
          type = "prototype",
          string = "lightning-attractor",
          priority_bonus = 1000
        },
        {
          type = "id",
          string = "fulgoran-ruin-vault",
          priority_bonus = 95
        },
        {
          type = "id",
          string = "fulgoran-ruin-colossal",
          priority_bonus = 94
        },
        {
          type = "id",
          string = "fulgoran-ruin-huge",
          priority_bonus = 93
        },
        {
          type = "id",
          string = "fulgoran-ruin-big",
          priority_bonus = 92
        },
        {
          type = "id",
          string = "fulgoran-ruin-medium",
          priority_bonus = 91
        },
        {
          type = "prototype",
          string = "pipe",
          priority_bonus = 1
        },
        {
          type = "prototype",
          string = "pump",
          priority_bonus = 1
        },
        {
          type = "prototype",
          string = "offshore-pump",
          priority_bonus = 1
        },
        {
          type = "prototype",
          string = "electric-pole",
          priority_bonus = 10
        },
        {
          type = "prototype",
          string = "power-switch",
          priority_bonus = 10
        },
        {
          type = "prototype",
          string = "logistic-robot",
          priority_bonus = 100
        },
        {
          type = "prototype",
          string = "construction-robot",
          priority_bonus = 100
        },
        {
          type = "impact-soundset",
          string = "metal",
          priority_bonus = 1
        }
      },
      exemption_rules =
      {
        {
          type = "prototype",
          string = "rail-support",
        },
        {
          type = "prototype",
          string = "legacy-straight-rail",
        },
        {
          type = "prototype",
          string = "legacy-curved-rail",
        },
        {
          type = "prototype",
          string = "straight-rail",
        },
        {
          type = "prototype",
          string = "curved-rail-a",
        },
        {
          type = "prototype",
          string = "curved-rail-b",
        },
        {
          type = "prototype",
          string = "half-diagonal-rail",
        },
        {
          type = "prototype",
          string = "rail-ramp",
        },
        {
          type = "prototype",
          string = "elevated-straight-rail",
        },
        {
          type = "prototype",
          string = "elevated-curved-rail-a",
        },
        {
          type = "prototype",
          string = "elevated-curved-rail-b",
        },
        {
          type = "prototype",
          string = "elevated-half-diagonal-rail",
        },
        {
          type = "prototype",
          string = "rail-signal",
        },
        {
          type = "prototype",
          string = "rail-chain-signal",
        },
        {
          type = "prototype",
          string = "locomotive",
        },
        {
          type = "prototype",
          string = "artillery-wagon",
        },
        {
          type = "prototype",
          string = "cargo-wagon",
        },
        {
          type = "prototype",
          string = "fluid-wagon",
        },
        {
          type = "prototype",
          string = "land-mine",
        },
        {
          type = "prototype",
          string = "wall",
        },
        {
          type = "prototype",
          string = "tree",
        },
        {
          type = "countAsRockForFilteredDeconstruction",
          string = "true",
        },
        {
          type = "prototype",
          string = "cargo-pod"
        }
      }
    }

