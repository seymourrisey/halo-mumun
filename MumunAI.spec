# -*- mode: python ; coding: utf-8 -*-

from PyInstaller.utils.hooks import collect_data_files

a = Analysis(
    ['main.py'],
    pathex=['.'],
    binaries=[],
    datas=[
        ('ui/style.kv', 'ui'),
        ('ui/assets/fonts/ModernDOS8x8.ttf', 'ui/assets/fonts'),
        ('ui/assets/icons/mic.png', 'ui/assets/icons'),
        ('ui/assets/icons/mic_pressed.png', 'ui/assets/icons'),
        ('ui/assets/icons/settings.png', 'ui/assets/icons'),
        ('ui/assets/mumun.png', 'ui/assets'),
        ('core/ai.py', 'core'),
        ('core/tts.py', 'core'),
        ('core/mic.py', 'core'),
        ('core/config.py', 'core'),
    ],
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
    [],
    exclude_binaries=True,
    name='MumunAI',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    icon='mumun-icon.ico',
)

coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='MumunAI',
)
