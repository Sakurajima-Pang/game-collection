# -*- mode: python ; coding: utf-8 -*-
import sys
from pathlib import Path

block_cipher = None

base_path = Path(SPECPATH)

a = Analysis(
    ['main.py'],
    pathex=[str(base_path)],
    binaries=[],
    datas=[
        ('plugins', 'plugins'),
        ('data', 'data'),
        ('interfaces', 'interfaces'),
        ('core', 'core'),
        ('ui', 'ui'),
    ],
    hiddenimports=[
        'tkinter',
        'tkinter.ttk',
        'tkinter.messagebox',
        'tkinter.filedialog',
        'game.plugins.game2048',
        'game.plugins.gomoku',
        'game.plugins.huarongdao',
        'game.plugins.game2048.plugin',
        'game.plugins.gomoku.plugin',
        'game.plugins.huarongdao.plugin',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='GameCollection',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,
)
