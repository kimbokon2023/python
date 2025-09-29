# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['mirae_LC008_A최종.py'],
    pathex=[],
    binaries=[],
    datas=[('data', 'data'), ('ceiling_excel', 'ceiling_excel'), ('dimstyle', 'dimstyle')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='mirae_LC008_A최종',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='mirae_LC008_A최종',
)
