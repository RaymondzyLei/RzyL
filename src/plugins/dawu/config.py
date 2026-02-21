from pathlib import Path

KEYWORDS={
    "Introduction_and_Simple_PendulumRE": ["单摆", "绪论", "单摆出门测", "绪论出门测"],
    "Mass_&_Density_MeasurementPRE": ["质量与密度的测量预习", "质量与密度的测量预习测", "质量和密度的测量预习测", "质量密度的测量预习测", "质量的测量预习测", "密度的测量预习测", "质量测量预习测", "密度测量预习测", "质量预习测", "密度预习测"],
    "Mass_&_Density_MeasurementRE": ["质量与密度的测量", "质量与密度的测量出门测", "质量和密度的测量出门测", "质量密度的测量出门测", "质量的测量出门测", "密度的测量出门测", "质量测量出门测", "密度测量出门测", "质量出门测", "密度出门测"],
    "Young's_Modulus_of_Steel_WirePRE": ["杨氏模量预习", "钢丝杨氏模量预习测", "杨氏模量预习测"],
    "Young's_Modulus_of_Steel_WireRE": ["杨氏模量", "钢丝杨氏模量出门测", "杨氏模量出门测"],
}
#`src\asserts\dawu\`下的图片文件名与"'KEYWORDS中的第一个对象'+'.jpg'"相同
def get_image_path(keyword: str) -> Path:
    return Path.cwd() / "src" / "asserts" / "dawu" / f"{keyword}.jpg"
