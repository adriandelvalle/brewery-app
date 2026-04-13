from datetime import date
from src.models.recipe import RecipeResponse, BeerStyle
from src.models.batch import BatchResponse, BatchStatus, BatchMeasurements

# Mock data de recetas
RECIPES: dict[int, RecipeResponse] = {
    1: RecipeResponse(
        id=1,
        name="Asturian Pale Ale",
        style=BeerStyle.APA,
        batch_size_liters=50,
        target_og=1.052,
        target_fg=1.010,
        target_ibu=35,
        target_abv=5.5,
        notes="Receta base de la casa. Lupulos Cascade y Centennial.",
        created_at="2026-04-01T10:00:00"
    ),
    2: RecipeResponse(
        id=2,
        name="Sidra de Niebla NEIPA",
        style=BeerStyle.NEIPA,
        batch_size_liters=50,
        target_og=1.065,
        target_fg=1.012,
        target_ibu=45,
        target_abv=7.0,
        notes="NEIPA con dry hop intenso. Citra, Mosaic y Galaxy.",
        created_at="2026-04-05T11:00:00"
    ),
}

# Mock data de lotes
BATCHES: dict[int, BatchResponse] = {
    1: BatchResponse(
        id=1,
        recipe_id=1,
        brew_date=date(2026, 4, 8),
        brewer="jota",
        water_volume_liters=50,
        status=BatchStatus.FERMENTING,
        measurements=BatchMeasurements(
            pre_boil_og=1.048,
            pre_boil_ph=5.4,
            post_boil_og=1.054,
            post_boil_ph=5.2,
            fermentor_volume_liters=36,
            final_og=1.053,
        ),
        notes="Primer lote con agua embotellada nueva.",
        created_at="2026-04-08T09:00:00"
    ),
}

# Contadores para simular auto-increment de IDs (sustituiremos por DB en Fase 2)
next_recipe_id = 3
next_batch_id = 2
