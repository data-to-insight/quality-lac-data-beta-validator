import pandas as pd

from lac_validator.rule_engine import rule_definition


@rule_definition(
    code="SW01bSTG1",
    message="For each social worker episode, information should be complete",
    affected_fields=["SW_DECOM", "SW_ID", "SW_REASON"],
    tables=["SWEpisodes"],
)
def validate(dfs):
    if "SWEpisodes" not in dfs:
        return {}
    else:
        df = dfs["SWEpisodes"]

        # If <SW_DECOM> > = 1 April 2023 then at least one instance of each of the following items should be provided:
        # <SW_ID>, <SW_DECOM>, <SW_REASON>

        df["SW_DECOM"] = pd.to_datetime(
            df["SW_DECOM"], format="%d/%m/%Y", errors="coerce"
        )

        no_items = df["SW_ID"].isna() | df["SW_REASON"].isna()
        after_1_apr_23 = df["SW_DECOM"] >= pd.to_datetime("01/04/2023", dayfirst=True)
        no_decom = df["SW_DECOM"].isna()

        errors = df[(after_1_apr_23 & no_items) | no_decom]

        error_rows = errors.index.tolist()

        return {"SWEpisodes": error_rows}


def test_validate():
    import pandas as pd

    fake_swe = pd.DataFrame(
        [
            {
                "CHILD": "child1",
                "SW_ID": pd.NA,
                "SW_DECOM": "01/01/2024",
                "xx": "xx",
            },  # fail no ID
            {
                "CHILD": "child2",
                "SW_ID": "xx",
                "SW_DECOM": pd.NA,
                "xx": "xx",
            },  # fail no decom
            {
                "CHILD": "child3",
                "SW_ID": "xx",
                "SW_DECOM": "01/01/2024",
                "xx": pd.NA,
            },  # fail no reason
            {
                "CHILD": "child4",
                "SW_ID": "xx",
                "SW_DECOM": "01/01/1999",
                "xx": "xx",
            },  # ignore before apr 1 2023
            {
                "CHILD": "child5",
                "SW_ID": "xx",
                "SW_DECOM": "01/01/1999",
                "xx": pd.NA,
            },  # ignore before apr 1 2023
            {
                "CHILD": "child6",
                "SW_ID": "xx",
                "SW_DECOM": "01/01/1999",
                "xx": pd.NA,
            },  # ignore before apr 1 2023
            {
                "CHILD": "child7",
                "SW_ID": "xx",
                "SW_DECOM": "01/01/2024",
                "SW_REASON": pd.NA,
            },  # fail no reason
            {
                "CHILD": "child9",
                "SW_ID": "xx",
                "xx": "xx",
                "SW_REASON": pd.NA,
            },  # fail, no details or decom
        ]
    )

    fake_dfs = {"SWEpisodes": fake_swe}

    result = validate(fake_dfs)

    assert result == {"SWEpisodes": [0, 1, 2, 6, 7]}
