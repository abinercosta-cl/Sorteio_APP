# -*- mode: python ; coding: utf-8 -*-

# Importar bibliotecas para encontrar caminhos dinamicamente
import os
import customtkinter

# Encontra o caminho da biblioteca customtkinter no Windows
# O caminho é relativo ao venv
customtkinter_path = os.path.join('venv', 'Lib', 'site-packages', 'customtkinter')

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    # Adiciona os arquivos de dados
    datas=[
        ('icone_sorteio.ico', '.'),
        ('sorteio.db', '.'),
        (customtkinter_path, 'customtkinter')
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
    a.binaries,
    a.datas,
    [],
    name='SorteioApp',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False, # Importante para não abrir um terminal
    onedir=True,   # Importante para criar uma pasta
    icon='icone_sorteio.ico'
)