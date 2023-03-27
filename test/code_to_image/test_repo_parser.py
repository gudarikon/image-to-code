"""
Check that repo_parser finds files that:
1. are in a mentioned directory (../src)
2. end with a specified postfix (.py)

Other files are ignored
"""
from src.code_to_image.repo_parser import *


def test_parse_repo(project_path):
    repo_files = parse_repo(str(project_path / "src" / "code_to_image"), [".py"])
    files_ending_with_py = [key for key in repo_files.keys() if key.endswith(".py")]
    files_in_specific_folder = [key for key in repo_files.keys() if
                                key.index("code_to_image") != -1]

    assert (len(files_ending_with_py) == len(repo_files.keys()))
    assert (len(files_in_specific_folder) == len(repo_files.keys()))


def test_wrong_postfix_ignored(resources_path):
    repo_files = parse_repo(str(resources_path), [".py"])

    assert (len(repo_files) == 0)
