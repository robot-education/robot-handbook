"""
A build script which can be used to compile animations in "source".
Takes as arguments -p, for production, as well as -h for help.
If -p is omitted, output is optimized for compile speed.
A file may be specified, as well as an optional list of classes to compile within that file.
If no file is specified, the entire directory is compiled.
"""
import inspect
import os
import subprocess
import argparse
import sys
import importlib

from typing import List

# prevent manim from printing
sys.stdout = open(os.devnull, "w")
import manim as mn

sys.stdout = sys.__stdout__

source_path = "source"
quality_folder_lookup = {"l": "480p15", "h": "1080p60"}


def get_python_file_paths(path: str | None = None) -> List[str]:
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
        if os.path.splitext(file_path)[1] == ".py" and file_path != "source/conf.py"
    ]


def get_path(file_name: str) -> str | None:
    for dir_path, _, file_names in os.walk(source_path):
        if file_name in file_names:
            return os.path.join(dir_path, file_name)
    return None


def get_animation_names(file_path: str) -> List[str]:
    file_path = file_path.replace("/", ".").removesuffix(".py")
    module = importlib.import_module(file_path)
    return [
        name
        for name, cls in module.__dict__.items()
        if inspect.isclass(cls) and issubclass(cls, mn.Scene)
    ]


def move_output(quality: str, file_path: str, animations: List[str]) -> None:
    """Moves produced files from media to the appropriate location in source."""
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
        help='paths relative to "/source" which are recursively searched for files',
    )
    parser.add_argument(
        "-s",
        "--scene",
        nargs="*",
        help="a list of scenes to render",
    )
    return parser


def main():
    args = get_arg_parser().parse_args()

    quality = "h" if args.production else "l"

    file_paths = []
    if args.file == None and args.path is None:
        file_paths = get_python_file_paths()

    if args.path != None:
        for path in args.path:
            file_paths.extend(get_python_file_paths(path=path))

    if args.file != None:
        for file_name in args.file:
            file_path = get_path(file_name)
            if file_path is None:
                raise ValueError(
                    'Failed to find the specified file "{file_name}" in "/source". Aborting.'
                )
            file_paths.append(file_path)

    for file_path in file_paths:
        animation_names = get_animation_names(file_path)

        if args.scene is not None:
            animation_names = [name for name in animation_names if name in args.scene]

        manim_command = (
            "manim render -v ERROR -q{quality} {file_path} {animation_names}".format(
                quality=quality,
                file_path=file_path,
                animation_names=" ".join(animation_names),
            )
        )

        print("Rendering {}".format(file_path))
        subprocess.run(manim_command, shell=True)
        move_output(quality, file_path, animation_names)


if __name__ == "__main__":
    main()
