# -*- mode: python ; coding: utf-8 -*-
import os
import sys

from pathlib import Path
from pylibdmtx import pylibdmtx
from pyzbar import pyzbar

block_cipher = None


a = Analysis(['Main.py'],
             pathex=[],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             hooksconfig={},
             runtime_hooks=[],
             excludes=['_bootlocale'],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)

a.binaries += TOC([
    (Path(dep._name).name, dep._name, 'BINARY')
    for dep in pylibdmtx.EXTERNAL_DEPENDENCIES + pyzbar.EXTERNAL_DEPENDENCIES
])

pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)

exe = EXE(pyz,
          a.scripts, 
          [],
          exclude_binaries=True,
          name='QRCodeAttendance',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=False,
          disable_windowed_traceback=False,
          target_arch=None,
          codesign_identity=None,
          entitlements_file=None )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas, 
               strip=False,
               upx=True,
               upx_exclude=[],
               name='Main')
