import pandas as pd

from validator903.types import ErrorDefinition


def validate():
    error = ErrorDefinition(
        code="621",
        description="Mother’s field has been completed but date of birth shows that the mother is younger than her child.",
        affected_fields=["DOB", "MC_DOB"],
    )

    def _validate(dfs):
        if "Header" not in dfs:
            return {}
        else:
            header = dfs["Header"]

            header["MC_DOB"] = pd.to_datetime(
                header["MC_DOB"], format="%d/%m/%Y", errors="coerce"
            )
            header["DOB"] = pd.to_datetime(
                header["DOB"], format="%d/%m/%Y", errors="coerce"
            )
            mask = (header["MC_DOB"] > header["DOB"]) | header["MC_DOB"].isna()

            validation_error_mask = ~mask
            validation_error_locations = header.index[validation_error_mask]

            return {"Header": validation_error_locations.tolist()}

    return error, _validate


def test_validate():
    import pandas as pd

    fake_data = pd.DataFrame(
        {
            "DOB": [
                "01/12/2021",
                "19/02/2016",
                "31/01/2019",
                "31/01/2019",
                "31/01/2019",
            ],
            "MC_DOB": ["01/01/2021", "19/12/2016", "31/01/2019", pd.NA, "01/02/2019"],
        }
    )

    fake_dfs = {"Header": fake_data}

    error_defn, error_func = validate()

    result = error_func(fake_dfs)

    assert result == {"Header": [0, 2]}
