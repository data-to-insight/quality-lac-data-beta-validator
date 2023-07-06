import click
import importlib
import pytest
import json
import os
from pathlib import Path

import lac_validator.lac_validator_class as lac_class
import importlib
from lac_validator.utils import process_uploaded_files

from validator903.ingress import read_from_text
from validator903.report import Report

@click.group()
def cli():
    pass


# LIST
@cli.command(name="list")
@click.option(
    "--ruleset",
    "-r",
    default="lac2022_23",
    help="validation year, e.g lac2022_23",
)
def list_cmd(ruleset):
    """
    :param str ruleset: validation year whose version of rules should be run.

    :return cli output: list of rules in validation year.
    """
    module = importlib.import_module(f"lac_validator.rules.{ruleset}")
    ruleset_registry = getattr(module, "registry")
    for rule in ruleset_registry:
        click.echo(f"{rule.code}\t{rule.message}")


# TEST
@cli.command(name="test")
@click.option(
    "--ruleset",
    "-r",
    default="lac2022_23",
    help="validation year, e.g lac2022_23",
)
def test_cmd(ruleset):
    """
    Runs pytest of rules specified
    :param str ruleset: validation year whose rules should be run
    :return: classic pytest output
    """
    module = importlib.import_module(f"lac_validator.rules.{ruleset}")
    module_folder = Path(module.__file__).parent
    # May 2023. There are 288 rule files.
    test_files = [
        str(p.absolute()) for p in module_folder.glob("*.py") if p.stem != "__init__"
    ]
    pytest.main(test_files)


# TESTtest
@cli.command(name="testtest")
def test():
    with open("files_failed.json", "r") as f:
        failed_paths = json.load(f)
    pytest.main(failed_paths)


# TEST one rule
@cli.command(name="test_one_rule")
@click.argument("code", type=str, required=True)
@click.option(
    "--ruleset",
    "-r",
    default="lac2022_23",
    help="validation year, e.g lac2022_23",
)
def test_one_rule(code, ruleset):
    """
    Runs pytest of rules specified
    :param str ruleset: validation year whose rules should be run
    :return: classic pytest output
    """
    module = importlib.import_module(f"lac_validator.rules.{ruleset}")
    module_folder = Path(module.__file__).parent

    file_path = os.path.join(module_folder, f"rule_{code}.py")

    pytest.main([file_path])


# RUN
@cli.command(name="run")
@click.argument("p4a_path", type=click.File("rt"), required=True)
@click.argument("ad1_path", type=click.File("rt"), required=True)
@click.option(
    "--ruleset",
    "-r",
    default="lac2022_23",
    help="validation year e.g lac2022_23",
)
@click.option("--select", "-s", default=None)
def run_all(p4a_path, ad1_path, ruleset, select):
    """
    created with code from offlinedebug.py

    :param str ruleset: validation year.
    :param str select: code of specific rule that should be run.
    """
    # p4a_path = "tests\\fake_data\placed_for_adoption_errors.csv"
    # ad1_path = "tests\\fake_data\\ad1.csv"

    frontend_files_dict = {"This year":[p4a_path, ad1_path], "Prev year": [p4a_path]}
    files_list = process_uploaded_files(frontend_files_dict)

    # the rest of the metadata is added in read_from_text() when instantiating Validator
    metadata = {"collectionYear": "2022", "localAuthority": "E09000027"}
    module = importlib.import_module(f"lac_validator.rules.{ruleset}")
    ruleset_registry = getattr(module, "registry")

    v = lac_class.LacValidator(metadata=metadata, files=files_list, registry=ruleset_registry, selected_rules=None)
    results = v.ds_results

    r = Report(results, ruleset=ruleset_registry)
    # print(f"*****************Report******************")
    # print(r.report.columns) # defined frontend display in previous tool configuration.
    print(f"*****************Child error summary******************")
    print(r.child_summary.columns)
    print(f"****************Error counts******************")
    print(r.error_summary.columns)

    full_issue_df = lac_class.create_issue_df(r.report, r.error_report)
    print(f"*****************full issue df******************")
    print(full_issue_df.columns)


# XML to tables
@cli.command(name="xmltocsv")
@click.argument("p4a_path", type=click.File("rt"), required=True)
def xmltocsv(p4a_path):
    with open(p4a_path.name, "rb") as f:
        p4a_filetext = f.read()
    files_list = [
        dict(name=p4a_path.name, description="This year", file_content=p4a_filetext),
    ]

    data_files, _ = read_from_text(files_list)
    click.echo(data_files)


if __name__ == "__main__":
    cli()
