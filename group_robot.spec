# -*- mode: python -*-

block_cipher = None


a = Analysis(['web.py'],
             pathex=['C:\\Users\\Cheer.L\\Documents\\vs code\\py\\wx_group_robot'],
             binaries=[],
             datas=[],
             hiddenimports=['engineio.async_gevent'],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='group_robot_api',
          debug=False,
          strip=False,
          upx=True,
          runtime_tmpdir=None,
          console=True )
