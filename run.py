from pathlib import Path
import os
import subprocess

"""
実行ファイルができる「filtan/build/exe.****/」フォルダから
「filtan」フォルダに移動してpipenv実行
"""
current_dir = Path.cwd()
os.chdir(current_dir.parents[1])

start = subprocess.run(['pipenv', 'run', 'filtan'], shell=True)
