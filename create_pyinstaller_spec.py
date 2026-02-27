"""Generate PyInstaller spec file for gfootball."""
import os

import gfootball_engine
import gfootball

engine_path = os.path.dirname(gfootball_engine.__file__)
gfootball_path = os.path.dirname(gfootball.__file__)

print(f'Engine path: {engine_path}')
print(f'GFootball path: {gfootball_path}')

binaries = []
for f in os.listdir(engine_path):
    if f.endswith('.pyd') or f.endswith('.dll'):
        full = os.path.join(engine_path, f).replace('\\', '\\\\')
        binaries.append(f'("{full}", "gfootball_engine")')

data_dir = os.path.join(engine_path, 'data').replace('\\', '\\\\')
fonts_dir = os.path.join(engine_path, 'fonts').replace('\\', '\\\\')
scenarios_dir = os.path.join(gfootball_path, 'scenarios').replace('\\', '\\\\')

spec = f"""# -*- mode: python ; coding: utf-8 -*-
block_cipher = None

a = Analysis(
    ['launcher.py'],
    pathex=[],
    binaries=[{', '.join(binaries)}],
    datas=[
        ("{data_dir}", "gfootball_engine/data"),
        ("{fonts_dir}", "gfootball_engine/fonts"),
        ("{scenarios_dir}", "gfootball/scenarios"),
    ],
    hiddenimports=[
        'gfootball', 'gfootball.env', 'gfootball.env.football_env',
        'gfootball.env.football_action_set', 'gfootball.env.config',
        'gfootball.env.constants', 'gfootball.env.observation_preprocessing',
        'gfootball.env.observation_processor', 'gfootball.env.scenario_builder',
        'gfootball.env.wrappers', 'gfootball.env.players',
        'gfootball.scenarios', 'pygame', 'cv2', 'numpy', 'gymnasium',
        'psutil', 'six', 'absl', 'cloudpickle',
    ],
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='GFootball',
    debug=False,
    strip=False,
    upx=True,
    console=True,
    icon=None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    name='gfootball',
)
"""

with open('gfootball.spec', 'w') as f:
    f.write(spec)

print('Spec file created successfully')
