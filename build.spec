# -*- mode: python ; coding: utf-8 -*-


block_cipher = None

data_files = [
    ('src\\config\\filter_config.json','config'),
    ('src\\config\\person_type.json','config'),
    ('src\\config\\weekly_config.json','config'),
	('src\\.env','.')
]
a = Analysis(['src\\main.py'],
             pathex=[],
             binaries=[],
             datas=data_files,
             hiddenimports=[],
             hookspath=[],
             hooksconfig={},
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)

exe = EXE(pyz,
          a.scripts, 
          [],
          exclude_binaries=True,
          name='NPTDailyVaccineGenerator',
          debug=False,
          bootloader_ignore_signals=False,
          strip=True,
          upx=True,
          console=False,
          disable_windowed_traceback=False,
          target_arch='x86_64',
          codesign_identity=None,
          entitlements_file=None,
          icon='src\\assets\\icon.ico'
          )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas, 
               strip=False,
               upx=True,
               upx_exclude=[],
               name='NPTDailyVaccineGenerator')