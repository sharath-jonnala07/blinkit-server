from typing import List, Dict

PRODUCTS_CATALOG: List[Dict] = [
    # Kitchen / Breakfast / Coffee
    { "id": "coffee-espresso", "brand": "Blue Tokai", "name": "Organic Espresso Roast Beans", "meta": "250g · whole bean", "price": 499, "strike": 550, "rating": 4.8, "tags": ["coffee","breakfast","workspace","morning","kitchen"], "description": "Single-estate arabica, medium-dark roast." },
    { "id": "butter-kerrygold", "brand": "Kerrygold", "name": "Irish Grass-Fed Butter", "meta": "200g · salted", "price": 245, "rating": 4.9, "tags": ["breakfast","cooking","kitchen"], "description": "Cultured, grass-fed, gloriously yellow." },
    { "id": "bread-sourdough", "brand": "The Baker's Atelier", "name": "Artisanal Sourdough", "meta": "500g · baked today", "price": 180, "strike": 200, "rating": 4.7, "tags": ["breakfast","kitchen","bread"], "description": "72-hour ferment. Blistered crust." },
    { "id": "eggs-happy", "brand": "Happy Hens", "name": "Organic Free-Range Eggs", "meta": "Pack of 6", "price": 120, "strike": 135, "rating": 4.6, "tags": ["breakfast","gym","protein","kitchen"], "description": "Pasture-raised. Deep orange yolks." },
    { "id": "avocado-hass", "brand": "Nature's Basket", "name": "Ripe Hass Avocados", "meta": "Pack of 2", "price": 320, "strike": 380, "rating": 4.5, "tags": ["breakfast","kitchen","fresh"], "description": "Pre-ripened. Ready to slice." },
    { "id": "coffee-cold", "brand": "Blue Tokai", "name": "Cold Brew Concentrate", "meta": "500ml · smooth", "price": 349, "rating": 4.7, "tags": ["coffee","morning","kitchen"], "description": "18-hour steep. Ice, milk, done." },
    
    # Gym / Fitness
    { "id": "protein-on", "brand": "Optimum Nutrition", "name": "Gold Standard Whey", "meta": "1kg · vanilla", "price": 3299, "strike": 3599, "rating": 4.9, "tags": ["gym","protein","fitness"], "description": "24g protein per scoop." },
    { "id": "protein-bar", "brand": "RiteBite", "name": "Max Protein Bar (Pack of 6)", "meta": "20g protein · choco", "price": 540, "strike": 600, "rating": 4.5, "tags": ["gym","protein","snack"], "description": "Real bar, real protein, real chocolate." },
    { "id": "electrolyte", "brand": "Fast&Up", "name": "Electrolyte Hydration Tabs", "meta": "20 tabs · lime", "price": 449, "rating": 4.6, "tags": ["gym","hydration"], "description": "Drop, fizz, sip. Beat the heat." },

    # Living / Ambience / Host
    { "id": "plant-monstera", "brand": "Leaf & Loam", "name": "Monstera in Terracotta", "meta": "Small · pet-friendly", "price": 649, "rating": 4.8, "tags": ["home","living","calm"], "description": "Live, hand-potted, indirect light." },
    { "id": "candle-sandalwood", "brand": "Ember & Oak", "name": "Sandalwood Soy Candle", "meta": "40h burn", "price": 890, "strike": 990, "rating": 4.7, "tags": ["home","living","bedroom","gift"], "description": "Warm sandalwood + amber." },
    { "id": "popcorn-truffle", "brand": "Popd", "name": "Truffle Butter Popcorn", "meta": "80g", "price": 149, "rating": 4.4, "tags": ["snack","movie","living","late-night"], "description": "Movie night, upgraded." },

    # Bedroom / Wind-down
    { "id": "linen-sheets", "brand": "Sleep Society", "name": "Washed Linen Sheet Set", "meta": "Queen · sand", "price": 3990, "strike": 4500, "rating": 4.9, "tags": ["bedroom","sleep","home"], "description": "Softer with every wash." },
    { "id": "serum-ren", "brand": "Ren Skin", "name": "Overnight Recovery Serum", "meta": "30ml · vitamin C", "price": 1490, "strike": 1650, "rating": 4.8, "tags": ["skincare","bedroom","glow"], "description": "Wake up looking like you slept nine hours." },

    # Pet Corner
    { "id": "dogfood-eco", "brand": "Ecobd", "name": "Premium Dry Dog Food", "meta": "3kg · chicken", "price": 1890, "strike": 2100, "rating": 4.8, "tags": ["pet","dog","living"], "description": "Real chicken, brown rice, no fillers." },

    # Laundry / Clean
    { "id": "detergent-method", "brand": "Method", "name": "Plant-Based Detergent", "meta": "1L · fresh linen", "price": 599, "strike": 699, "rating": 4.6, "tags": ["home","laundry","clean"], "description": "Concentrated, biodegradable." },
]

MISSIONS_TEMPLATE = [
    {
        "id": "morning-breakfast",
        "title": "7-Min Morning Breakfast Mission",
        "subtitle": "Fresh sourdough, eggs, avocado & single-estate espresso.",
        "eyebrow": "Kitchen Routine",
        "target_room": "Kitchen",
        "target_routine": "Breakfast",
        "recommended_product_ids": ["bread-sourdough", "butter-kerrygold", "eggs-happy", "coffee-espresso", "avocado-hass"],
        "cta": "Fulfill Breakfast Mission"
    },
    {
        "id": "level-up-workouts",
        "title": "Post-Lift Recovery Mission",
        "subtitle": "Whey protein, electrolytes & protein bars at your door before your shower.",
        "eyebrow": "Fitness Routine",
        "target_room": "Gym",
        "target_routine": "Fitness",
        "recommended_product_ids": ["protein-on", "protein-bar", "electrolyte", "eggs-happy"],
        "cta": "Fuel the Workout"
    },
    {
        "id": "movie-marathon",
        "title": "Weekend Host & Vibe Mission",
        "subtitle": "Truffle popcorn, sandalwood candle & cold brew.",
        "eyebrow": "Living Room Routine",
        "target_room": "Living Area",
        "target_routine": "Snacks",
        "recommended_product_ids": ["popcorn-truffle", "candle-sandalwood", "coffee-cold", "plant-monstera"],
        "cta": "Set up the Evening"
    },
    {
        "id": "bedtime-wind-down",
        "title": "Bedtime Recovery & Sleep Ritual",
        "subtitle": "Washed linen, overnight serum & relaxing ambience.",
        "eyebrow": "Bedroom Routine",
        "target_room": "Bedrooms",
        "target_routine": "Wind-down",
        "recommended_product_ids": ["linen-sheets", "serum-ren", "candle-sandalwood"],
        "cta": "Prepare the Room"
    },
    {
        "id": "pet-care",
        "title": "Pet Parent Restock Mission",
        "subtitle": "Kibble & pet care essentials delivered in 8 minutes.",
        "eyebrow": "Pet Corner Routine",
        "target_room": "Pet Corner",
        "target_routine": "Pet Care",
        "recommended_product_ids": ["dogfood-eco", "popcorn-truffle"],
        "cta": "Restock Bowl"
    },
    {
        "id": "freshen-home",
        "title": "Plant-Based Home Reset Mission",
        "subtitle": "Concentrated detergent, fresh linen scent & greenery.",
        "eyebrow": "Laundry & Hall Routine",
        "target_room": "Restroom",
        "target_routine": "Laundry",
        "recommended_product_ids": ["detergent-method", "candle-sandalwood", "plant-monstera"],
        "cta": "Reset the House"
    },
    {
        "id": "coffee-break",
        "title": "Home Barista Coffee Break",
        "subtitle": "Single-origin beans, cold brew & a proper knob of butter.",
        "eyebrow": "Kitchen Routine",
        "target_room": "Kitchen",
        "target_routine": "Coffee Break",
        "recommended_product_ids": ["coffee-espresso", "coffee-cold", "butter-kerrygold", "bread-sourdough"],
        "cta": "Brew at Home"
    },
    {
        "id": "weekend-cooking",
        "title": "Slow Weekend Cooking Mission",
        "subtitle": "Sourdough, eggs, avocado & butter for a proper Sunday spread.",
        "eyebrow": "Kitchen Routine",
        "target_room": "Kitchen",
        "target_routine": "Weekend Cooking",
        "recommended_product_ids": ["bread-sourdough", "eggs-happy", "avocado-hass", "butter-kerrygold", "coffee-espresso"],
        "cta": "Plan the Spread"
    },
    {
        "id": "guests-coming-over",
        "title": "Guests in Two Hours Mission",
        "subtitle": "Candles, popcorn, fresh bread & butter — hero moment sorted.",
        "eyebrow": "Living Room Routine",
        "target_room": "Living Area",
        "target_routine": "Hosting",
        "recommended_product_ids": ["candle-sandalwood", "popcorn-truffle", "bread-sourdough", "butter-kerrygold", "plant-monstera"],
        "cta": "Prep the Evening"
    },
    {
        "id": "glowing-skin",
        "title": "Overnight Glow Ritual",
        "subtitle": "Recovery serum, soft linen & a candlelit wind-down.",
        "eyebrow": "Bedroom Routine",
        "target_room": "Bedrooms",
        "target_routine": "Skincare",
        "recommended_product_ids": ["serum-ren", "candle-sandalwood", "linen-sheets", "plant-monstera"],
        "cta": "Start the Ritual"
    },
    {
        "id": "lunchbox",
        "title": "Seven-Minute Lunchbox Mission",
        "subtitle": "Sourdough, eggs, avocado & a treat that won't get traded.",
        "eyebrow": "Kitchen Routine",
        "target_room": "Kitchen",
        "target_routine": "Meal Prep",
        "recommended_product_ids": ["bread-sourdough", "eggs-happy", "avocado-hass", "butter-kerrygold", "popcorn-truffle"],
        "cta": "Pack the Box"
    },
    {
        "id": "late-night",
        "title": "Midnight Rescue Mission",
        "subtitle": "Truffle popcorn, one perfect egg & cold brew for the 12 AM craving.",
        "eyebrow": "Living Room Routine",
        "target_room": "Living Area",
        "target_routine": "Late Night",
        "recommended_product_ids": ["popcorn-truffle", "eggs-happy", "coffee-cold", "butter-kerrygold"],
        "cta": "Feed the Craving"
    }
]
