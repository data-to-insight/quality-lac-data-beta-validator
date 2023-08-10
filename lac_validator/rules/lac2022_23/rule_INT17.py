import pandas as pd

from lac_validator.rule_engine import rule_definition
from lac_validator.fixtures import fake_INT_header, fake_INT_file


@rule_definition(
code="INT17",
message="Internal Check: DOB in Reviews is different to DOB in Header.",
affected_fields=["DOB"],
)
def validate(dfs):
    
        if "Header" not in dfs or "Reviews" not in dfs:
            return {}
        else:
            header = dfs["Header"]
            file = dfs["Reviews"]

            header["DOB"] = pd.to_datetime(
                header["DOB"], format="%d/%m/%Y", errors="coerce"
            )
            file["DOB"] = pd.to_datetime(
                file["DOB"], format="%d/%m/%Y", errors="coerce"
            )

            file["index_file"] = file.index

            merged = header.merge(
                file[["CHILD", "DOB", "index_file"]],
                on="CHILD",
                indicator=True,
                how="right",
                suffixes=["_header", "_file"],
            )

            mask = (
                (merged["DOB_header"] != merged["DOB_file"])
                & (merged["DOB_header"].notna() & merged["DOB_file"].notna())
                & (merged["_merge"] != "right_only")
            )
            eps_error_locations = merged.loc[mask, "index_file"]
            return {"Reviews": eps_error_locations.unique().tolist()}

    


def test_validate():
    
    fake_dfs = {"Header": fake_INT_header.copy(), "Reviews": fake_INT_file.copy()}
    result = validate(fake_dfs)
    assert result == {"Reviews": [2]}