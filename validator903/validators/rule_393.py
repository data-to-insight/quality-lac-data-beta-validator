from validator903.types import ErrorDefinition


def validate():
    error = ErrorDefinition(
        code="393",
        description="Child is looked after but mother field is not completed.",
        affected_fields=["MOTHER"],
    )

    def _validate(dfs):
        if "Header" not in dfs or "Episodes" not in dfs:
            return {}
        else:
            header = dfs["Header"]
            episodes = dfs["Episodes"]

            header_female = header[header["SEX"].astype(str) == "2"]

            applicable_episodes = episodes[
                ~episodes["LS"].str.upper().isin(["V3", "V4"])
            ]

            error_mask = (
                header_female["CHILD"].isin(applicable_episodes["CHILD"])
                & header_female["MOTHER"].isna()
            )

            error_locations = header_female.index[error_mask]

            return {"Header": error_locations.to_list()}

    return error, _validate


def test_validate():
    import pandas as pd

    fake_data = pd.DataFrame(
        {
            "CHILD": ["101", "102", "103", "104", "105"],
            "SEX": ["2", "1", "2", "2", "2"],
            "MOTHER": ["1", pd.NA, "0", pd.NA, pd.NA],
        }
    )

    fake_data_episodes = pd.DataFrame(
        {
            "CHILD": ["101", "102", "103", "104", "105"],
            "LS": ["C2", "C2", "c2", "C1", "v4"],
        }
    )

    fake_dfs = {"Header": fake_data, "Episodes": fake_data_episodes}

    error_defn, error_func = validate()

    result = error_func(fake_dfs)

    assert result == {"Header": [3]}
