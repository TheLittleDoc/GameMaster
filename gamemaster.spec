# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(['gamemaster.pyw'],
             pathex=['C:\Python310\Lib\site-packages', 'C:\\Users\\TheLittleDoc\\Desktop\\GameMaster'],
             binaries=[],
             datas=[('icon.ico','.')],
             hiddenimports=[],
             hookspath=[],
             hooksconfig={},
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)

splash = Splash('splash.png',
             binaries=a.binaries,
             datas=a.datas,
             text_pos=(10, 375),
             text_size=12,
             text_color='black')

pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)

             
a.datas += [('header_alt.png','C:\\Users\\TheLittleDoc\\Desktop\\GameMaster\\header_alt.png', 'DATA')]
a.datas += [('doc.png','C:\\Users\\TheLittleDoc\\Desktop\\GameMaster\\doc.png', 'DATA')]
a.datas += [('discord.png','C:\\Users\\TheLittleDoc\\Desktop\\GameMaster\\discord.png', 'DATA')]
a.datas += [('github.png','C:\\Users\\TheLittleDoc\\Desktop\\GameMaster\\github.png', 'DATA')]
a.datas += [('kofi.png','C:\\Users\\TheLittleDoc\\Desktop\\GameMaster\\kofi.png', 'DATA')]
a.datas += [('LICENSE','C:\\Users\\TheLittleDoc\\Desktop\\GameMaster\\LICENSE', 'DATA')]

exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,  
          [],
          splash,
          name='gamemaster',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=False,
          disable_windowed_traceback=False,
          target_arch=None,
          codesign_identity=None,
          entitlements_file=None , icon="icon.ico")

coll = COLLECT(exe,
                
          splash.binaries)