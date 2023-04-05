"""
A build script which can be used to compile animations and build the website.
"""
from ctypes import cast
import inspect
import os
import subprocess
import argparse
import sys
import pathlib
import importlib
import re

from thefuzz import process, fuzz

# prevent manim from printing
sys.stdout = open(os.devnull, "w")
import manim as mn

sys.stdout = sys.__stdout__


"""
The process for parsing files, paths, and sources is as follows.

The user specifies a path like this:
level1/level2/level3
or this:
level1/

files:
end.py

scenes:
MyScene OtherScene

The output is the path to the file.
We collect all scenes and call manim build on them.
We're fine determining a list of scenes per file.

To handle each possible type of input, we begin by collecting all possible paths (which do not end in paths).
fuzzy matching paths requires collecting each level in the process - false, we simply collect all possible paths
and get the best one for the given input.
We tokenize around slashes and do not use a sort ratio matcher.

We collect paths
We collect file names and map them to paths
We collect scenes and map them to file names

We can then fuzz around our requirements as needed.
"""

source_path = pathlib.Path("website")

quality_folder_lookup = {"l": "480p15", "h": "1080p60"}


def get_all_file_paths() -> list[pathlib.Path]:
    """Searches source_path for all potential files. Returns a mapping of file names to their paths."""
    return [
        file_path
        for file_path in source_path.glob("**/*.py")
        if file_path.name != "conf.py"
    ]


def get_all_paths() -> list[pathlib.Path]:
    """Searches source_path for all possible paths, including sub-paths, and returns them.

    This function is used to collect paths for matching with the -p option.
    The paths include paths to all files.
    """
    return [path for path in source_path.glob("**") if path.name != "conf.py"]


def get_all_scenes(file_paths: list[pathlib.Path]) -> dict[str, pathlib.Path]:
    """Searches source_path for all possible scenes.

    Returns a mapping of scenes to their files.
    Duplicate scenes and files are not explicitly handled.
    """
    return dict(
        [
            (scene_name, file_path)
            for file_path in file_paths
            for scene_name in get_scene_names(file_path)
        ]
    )


def get_scene_names(file_path: pathlib.Path) -> list[str]:
    module_path = str(file_path).replace("/", ".").removesuffix(".py")
    module = importlib.import_module(module_path)
    return [
        name
        for name, cls in module.__dict__.items()
        if inspect.isclass(cls) and issubclass(cls, mn.Scene)
    ]


# def get_python_file_paths(path: str | None = None) -> list[str]:
#     if path is not None:
#         path = os.path.join(source_path, path)
#     else:
#         path = source_path

#     file_paths = []
#     for dir_path, _, file_names in os.walk(path):
#         file_paths.extend(
#             [os.path.join(dir_path, file_name) for file_name in file_names]
#         )

#     return [
#         file_path
#         for file_path in file_paths
#         if os.path.splitext(file_path)[1] == ".py"
#         and file_path != "{}/conf.py".format(source_path)
#     ]


def move_output(quality: str, file_path: pathlib.Path, scene_name: str) -> None:
    """Moves produced files from media to the appropriate location in website."""
    quality_folder = quality_folder_lookup[quality]

    path, sub_folder = os.path.split(file_path)

    # -p suppresses errors
    subprocess.run("mkdir -p {}/media".format(path), shell=True)

    # for scene in scenes:
    move_command = "mv media/videos/{sub_folder}/{quality_folder}/{scene_name}.mp4 {path}/media/.".format(
        sub_folder=sub_folder.removesuffix(".py"),
        scene_name=scene_name,
        quality_folder=quality_folder,
        path=path,
    )
    subprocess.run(move_command, shell=True)


def get_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Builds animations.",
    )
    parser.add_argument(
        "--production",
        action="store_true",
        help="whether to build production versions of animations",
    )
    parser.add_argument(
        "-f",
        "--file",
        nargs="*",
        default=None,
        help="python files to build",
    )
    parser.add_argument(
        "-p",
        "--path",
        nargs="*",
        default=None,
        help='paths relative to "/{}" which are recursively searched for files'.format(
            source_path
        ),
    )
    parser.add_argument(
        "-s",
        "--scene",
        nargs="*",
        help="a list of scenes to render",
    )
    parser.add_argument(
        "-m",
        "--make",
        action="store_true",
        help="whether to make the website after building",
    )
    return parser


def fuzzy_search(targets: list[str], values: list[str]) -> list[str]:
    parsed_targets = dict([(target, split_capital_case(target)) for target in targets])

    matches = []
    for value in values:
        parsed_value = split_capital_case(value)
        _, score, target_name = process.extractOne(  # type: ignore
            parsed_value, parsed_targets, scorer=fuzz.token_sort_ratio  # type: ignore
        )

        if score < 95:
            print("Found {} for input {} (score: {})".format(target_name, value, score))
        # print("Inputs:", parsed_targets)
        # print("Query:", parsed_value)
        matches.append(target_name)
    return matches


def split_capital_case(input: str) -> str:
    parsed = re.search("[^A-Z]*", input)
    matches: list[str] = []
    if parsed is not None:
        matches.append(parsed.group(0))

    end = re.findall("[A-Z][^A-Z]*", input)
    matches.extend(end)
    if matches[-1].lower() == "scene":
        matches.pop()
    return " ".join(matches)


def main():
    args = get_arg_parser().parse_args()

    quality = "h" if args.production else "l"

    target_paths = get_all_file_paths()
    if args.path is not None:
        all_paths = get_all_paths()
        for path in args.path:
            # filter target_paths based on paths in args.path
            pass

    if args.file is not None:
        # we use a dict so we can split names into sequences
        target_names = [path.name for path in target_paths]
        results = fuzzy_search(target_names, args.file)
        target_paths = [path for path in target_paths if path.name in results]

    scenes = get_all_scenes(target_paths)
    if args.scene is not None:
        results = fuzzy_search(list(scenes.keys()), args.scene)
        scenes = dict([(k, v) for k, v in scenes.items() if k in results])

    for scene_name, file_path in scenes.items():
        manim_command = (
            "manim render -v ERROR -q{quality} {file_path} {scene_names}".format(
                quality=quality,
                file_path=file_path,
                scene_names=scene_name,  # " ".join(scene_names),
            )
        )

        print("Rendering {} - {}".format(file_path, scene_name))
        subprocess.run(manim_command, shell=True)
        move_output(quality, file_path, scene_name)

    if args.make:
        subprocess.run("make html", shell=True)


if __name__ == "__main__":
    main()
