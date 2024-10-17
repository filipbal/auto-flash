# -*- mode: python ; coding: utf-8 -*-

import sys
import os
from PyInstaller.utils.hooks import collect_data_files

block_cipher = None

# Specify only the PyQt5 modules we need
pyqt5_modules = [
    'PyQt5.QtWidgets',
    'PyQt5.QtCore',
    'PyQt5.QtGui'
]

# Specify only the pywinauto modules we need
pywinauto_modules = [
    'pywinauto',
    'pywinauto.application',
    'pywinauto.keyboard'
]

a = Analysis(
    ['AutoFlash.py'],
    pathex=[],
    binaries=[],
    datas=collect_data_files('PyQt5', subdir='Qt/plugins/platforms') + 
           collect_data_files('PyQt5', subdir='Qt/plugins/styles'),
    hiddenimports=pyqt5_modules + pywinauto_modules,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['tkinter', 'PySide2', 'PIL'],
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
    name='AutoFlash',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # Change to True for easier debugging
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)