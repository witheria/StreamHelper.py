# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['D:\\com\\StreamHelper\\resources\\__init__.py'],
             pathex=['D:\\com\\Streamhelper'],
             binaries=[],
             datas=[('D:\\com\\StreamHelper\\resources\\uis\\', '.\\resources')],
             hiddenimports=['pyperclip'],
             hookspath=[],
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
          name='StreamHelper',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=False , uac_admin=True, icon='D:\\com\\StreamHelper\\resources\\images\\common\\icon2.ico')
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               upx_exclude=[],
               name='StreamHelper')
