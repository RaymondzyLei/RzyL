from pathlib import Path

KEYWORDS = {
    "1": ["1", "测试", "test", "alpha"],
    "2": ["2", "实验", "experiment", "beta"],
    "3": ["3", "演示", "demo", "gamma"]
}
#`src\asserts\dawu\`下的图片文件名与"'KEYWORDS中的第一个对象'+'.jpg'"相同
def get_image_path(keyword: str) -> Path:
    return Path.cwd() / "src" / "asserts" / "dawu" / f"{keyword}.jpg"
