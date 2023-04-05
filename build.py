"""
A build script which can be used to compile animations and build the website.
"""
import inspect
import os
import subprocess
import argparse
import sys
import importlib

import fuzzywuzzy as fuzz

# prevent manim from printing
sys.stdout = open(os.devnull, "w")
import manim as mn

sys.stdout = sys.__stdout__

source_path = "website"
quality_folder_lookup = {"l": "480p15", "h": "1080p60"}

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


def get_all_file_paths() -> dict[str, str]:
    """Searches source_path for all potential files. Returns a mapping of file names to paths."""
    return {}


def get_all_paths() -> list[str]:
    """Searches source_path for all possible file paths. Returns a list of paths."""
    return []


def get_all_scenes() -> dict[str, str]:
    """Searches source_path for all possible scenes. Returns a mapping of scenes to paths."""
    return {}


def get_python_file_paths(path: str | None = None) -> list[str]:
    if path is not None:
        path = os.path.join(source_path, path)
    else:
        path = source_path

    file_paths = []
    for dir_path, _, file_names in os.walk(path):
        file_paths.extend(
            [os.path.join(dir_path, file_name) for file_name in file_names]
        )

    return [
        file_path
        for file_path in file_paths
        if os.path.splitext(file_path)[1] == ".py"
        and file_path != "{}/conf.py".format(source_path)
    ]


def get_path(file_name: str) -> str | None:
    for dir_path, _, file_names in os.walk(source_path):
        if file_name in file_names:
            return os.path.join(dir_path, file_name)
    return None


def get_animation_names(file_path: str) -> list[str]:
    file_path = file_path.replace("/", ".").removesuffix(".py")
    module = importlib.import_module(file_path)
    return [
        name
        for name, cls in module.__dict__.items()
        if inspect.isclass(cls) and issubclass(cls, mn.Scene)
    ]


def move_output(quality: str, file_path: str, animations: list[str]) -> None:
    """Moves produced files from media to the appropriate location in website."""
    quality_folder = quality_folder_lookup[quality]
    path, sub_folder = os.path.split(file_path)

    # -p suppresses errors
    subprocess.run("mkdir -p {}/media".format(path), shell=True)

    for animation in animations:
        move_command = "mv media/videos/{sub_folder}/{quality_folder}/{animation}.mp4 {path}/media/.".format(
            sub_folder=sub_folder.removesuffix(".py"),
            animation=animation,
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


def main():
    args = get_arg_parser().parse_args()

    quality = "h" if args.production else "l"

    file_paths = []
    if args.file is None and args.path is None:
        file_paths = get_python_file_paths()

    # paths are harvested without fuzzy matching, as that's tricky to do
    if args.path is not None:
        for path in args.path:
            file_paths.extend(get_python_file_paths(path=path))

    # file_paths is now a list of desired search paths

    # look for files
    if args.file is not None:
        for file_name in args.file:
            file_path = get_path(file_name)
            if file_path is None:
                raise ValueError(
                    'Failed to find the specified file "{}" in "/{}". Aborting.'.format(
                        file_name, file_path
                    )
                )
            file_paths.append(file_path)

    all_scene_names = []
    for file_path in file_paths:
        scene_names = get_animation_names(file_path)
        all_scene_names.extend(scene_names)

        # look for scenes
        if args.scene is not None:
            scene_names = [name for name in all_scene_names if name in args.scene]
            if scene_names == []:
                continue

        manim_command = (
            "manim render -v ERROR -q{quality} {file_path} {animation_names}".format(
                quality=quality,
                file_path=file_path,
                animation_names=" ".join(scene_names),
            )
        )

        print("Rendering {}".format(file_path))
        subprocess.run(manim_command, shell=True)
        move_output(quality, file_path, scene_names)

        if args.make:
            subprocess.run("make html", shell=True)


if __name__ == "__main__":
    main()
