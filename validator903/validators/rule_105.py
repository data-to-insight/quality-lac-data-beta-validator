import pandas as pd

from validator903.types import MissingMetadataError
from validator903.types import ErrorDefinition


def validate():
    error = ErrorDefinition(
        code="105",
        description="Data entry for Unaccompanied Asylum-Seeking Children (UASC) status of child is invalid or has not been completed.",
        affected_fields=["UASC"],
    )

    def _validate(dfs):
        if "Header" not in dfs:
            return {}
        else:
            try:
                file_format = dfs["metadata"]["file_format"]
            except KeyError as e:
                raise MissingMetadataError(*e.args)
            if file_format == "csv":
                return {}

            header = dfs["Header"]
            code_list = [0, 1]

            mask = ~pd.to_numeric(header["UASC"], errors="coerce").isin(code_list)
            error_locs = header.index[mask]

            return {"Header": error_locs.tolist()}

    return error, _validate


def test_validate():
    import pandas as pd

    fake_header = pd.DataFrame({"UASC": [0, 1, pd.NA, "", "0", "1", "2", 2]})
    error_defn, error_func = validate()

    fake_dfs = {"Header": fake_header, "metadata": {"file_format": "csv"}}
    result = error_func(fake_dfs)
    assert result == {}

    fake_dfs = {"Header": fake_header, "metadata": {"file_format": "xml"}}
    result = error_func(fake_dfs)
    assert result == {"Header": [2, 3, 6, 7]}
