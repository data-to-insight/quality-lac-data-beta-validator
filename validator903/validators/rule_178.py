from validator903.types import ErrorDefinition


def validate():
    error = ErrorDefinition(
        code="178",
        description="Placement provider code is not a valid code.",
        affected_fields=["PLACE_PROVIDER"],
    )

    def _validate(dfs):
        if "Episodes" not in dfs:
            return {}

        episodes = dfs["Episodes"]

        code_list_placement_provider = ["PR0", "PR1", "PR2", "PR3", "PR4", "PR5"]
        code_list_placement_with_no_provider = ["T0", "T1", "T2", "T3", "T4", "Z1"]

        place_provider_needed_and_correct = episodes["PLACE_PROVIDER"].isin(
            code_list_placement_provider
        ) & ~episodes["PLACE"].isin(code_list_placement_with_no_provider)

        place_provider_not_provided = episodes["PLACE_PROVIDER"].isna()

        place_provider_not_needed = episodes["PLACE_PROVIDER"].isna() & episodes[
            "PLACE"
        ].isin(code_list_placement_with_no_provider)

        mask = (
            place_provider_needed_and_correct
            | place_provider_not_provided
            | place_provider_not_needed
        )

        validation_error_mask = ~mask
        validation_error_locations = episodes.index[validation_error_mask]

        return {"Episodes": validation_error_locations.tolist()}

    return error, _validate


def test_validate():
    import pandas as pd

    fake_data = pd.DataFrame(
        {
            "PLACE_PROVIDER": ["PR0", "PR1", "", pd.NA, "", pd.NA],
            "PLACE": ["U1", "T0", "U2", "Z1", "T1", pd.NA],
        }
    )

    fake_dfs = {"Episodes": fake_data}

    error_defn, error_func = validate()

    result = error_func(fake_dfs)

    assert result == {"Episodes": [1, 2, 4]}
