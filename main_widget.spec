# -*- mode: python ; coding: utf-8 -*-

from image_processing_widget.defs import __version__


block_cipher = None

a = Analysis(
    ['image_processing_widget\\main_widget.py'],
    pathex=[],
    binaries=[],
    datas=[('image_processing_widget\\resource\\camera.svg', 'image_processing_widget\\resource')],
    hiddenimports=[],
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
    name=f"image-processing-widget-{__version__}",
    icon="image_processing_widget\\resource\\camera.ico",
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
)
