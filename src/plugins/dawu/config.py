from pathlib import Path
from .keywords import KEYWORDS

#`src\asserts\dawu\`下的图片文件名与"'KEYWORDS中的第一个对象'+'.jpg'"相同
def get_image_path(keyword: str) -> Path:
    return Path.cwd() / "src" / "asserts" / "dawu" / f"{keyword}.jpg"
