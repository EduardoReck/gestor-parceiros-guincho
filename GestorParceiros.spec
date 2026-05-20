# -*- mode: python ; coding: utf-8 -*-
import os
import glob

# Localiza o python DLL automaticamente a partir do executável Python em uso
import sys
_python_dir = os.path.dirname(sys.executable)
_dll_pattern = os.path.join(_python_dir, "python3*.dll")
_dll_matches = glob.glob(_dll_pattern)
_python_dll = _dll_matches[0] if _dll_matches else None

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[(_python_dll, '.')] if _python_dll else [],
    datas=[],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='GestorParceiros',
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
    icon='assets/icon.ico' if os.path.exists('assets/icon.ico') else None,
)
