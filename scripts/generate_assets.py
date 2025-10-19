#!/usr/bin/python
import logging
from pathlib import Path
from typing import Callable

from PIL import Image

SOURCE_ASSETS: Path = Path(__file__).parent / "imgs"
TARGET_ASSETS: Path = Path(__file__).parent.parent / "assets"

log = logging.getLogger(__name__)


##### Header Generations #####
def _if_header(folder: Path) -> bool:
    required_files: list[str] = ["header_dark.png", "header_light.png"]

    for file in required_files:
        if not (folder / file).is_file():
            log.info("\t\tMissing required file: %s", file)
            return False

    return True


def _header(folder: Path) -> int:
    sizes: dict[str, tuple[int, int]] = {
        "hdpi": (194, 72),
        "mdpi": (129, 48),
        "xhdpi": (258, 96),
        "xxhdpi": (387, 144),
        "xxxhdpi": (516, 192),
    }
    variations: list[str] = [
        "custom_header",
        "yt_wordmark_header",
        "yt_premium_wordmark_header",
    ]
    files: list[str] = ["header_dark.png", "header_light.png"]

    destination: Path = TARGET_ASSETS / folder.stem / "header"
    destination.mkdir(exist_ok=True, parents=True)

    for file in files:
        mode: str = file.split("_", 1)[-1]
        for name, (w, h) in sizes.items():
            res_folder: Path = destination / ("drawable-" + name)
            res_folder.mkdir(exist_ok=True)

            img = Image.open(folder / file)
            img = img.resize((w, h), resample=Image.Resampling.LANCZOS)

            for variation in variations:
                out_path = res_folder / f"{variation}_{mode}"
                img.save(out_path)

        log.info("\t\tGenerated headers for mode: %s", mode)

    return 0


##### Icon Generations #####
def _if_icon(folder: Path) -> bool:
    required_files: list[str] = ["logo_background.png", "logo_foreground.png"]

    for file in required_files:
        if not (folder / file).is_file():
            log.info("\t\tMissing required file: %s", file)
            return False

    return True


def _icon(folder: Path) -> int:
    sizes: dict[str, tuple[int, int]] = {
        "hdpi": (162, 162),
        "mdpi": (108, 108),
        "xhdpi": (216, 216),
        "xxhdpi": (324, 324),
        "xxxhdpi": (432, 432),
    }
    variations: list[str] = [
        "revanced_adaptive_{}_custom.png",
        "adaptiveproduct_youtube_{}_color_108.png",
    ]
    variations_foreground: list[str] = [
        "ic_launcher_round.png",
        "ic_launcher.png",
    ]

    files: list[str] = ["logo_background.png", "logo_foreground.png"]

    destination: Path = TARGET_ASSETS / folder.stem / "icon"
    destination.mkdir(exist_ok=True, parents=True)

    for file in files:
        mode: str = file.split("_", 1)[-1].split(".")[0]
        for name, (w, h) in sizes.items():
            res_folder: Path = destination / ("mipmap-" + name)
            res_folder.mkdir(exist_ok=True)

            img = Image.open(folder / file)
            img = img.resize((w, h), resample=Image.Resampling.LANCZOS)

            for variation in variations:
                out_path = res_folder / variation.format(mode)
                img.save(out_path)

            if mode == "foreground":
                for variation in variations_foreground:
                    out_path = res_folder / variation
                    img.save(out_path)
        log.info("\t\tGenerated icons for mode: %s", mode)
    return 0


OPERATIONS: dict[str, list[Callable]] = {
    "Header": [_if_header, _header],
    "Icon": [_if_icon, _icon],
}


def main() -> int:
    logging.basicConfig(level=logging.INFO)

    for build_folder in SOURCE_ASSETS.iterdir():
        log.info("Processing build: %s", build_folder.name)
        for operation_name, (cond, func) in OPERATIONS.items():
            log.info("\tRunning operation: %s", operation_name)
            if cond(build_folder):
                log.info("\t\tCondition met, executing...")
                if ret_code := func(build_folder):
                    return ret_code
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
