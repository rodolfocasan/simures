# -*- mode: python ; coding: utf-8 -*-

import os
import sys

block_cipher = None

# Configuración específica para Linux - Versión corregida
project_dir = os.path.dirname(os.path.abspath(sys.argv[0]))  # <-- Cambio clave aquí

a = Analysis(
    ['main.py'],
    pathex=[project_dir],
    binaries=[],
    datas=[
        ('Storage/Icons/*.png', 'Storage/Icons'),
        ('_ascii.py', '.')
    ],
    hiddenimports=[
        'PyQt5.QtCore',
        'PyQt5.QtGui',
        'PyQt5.QtWidgets',
        'PyQt5.sip'
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['jupyter', 'pandas', 'scipy'],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    name='simures',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    icon=os.path.join(project_dir, 'Storage', 'Icons', 'favicon_01.png')  # Ruta absoluta
)