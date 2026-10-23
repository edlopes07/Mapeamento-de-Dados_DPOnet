import sqlite3
import json
from pathlib import Path

def mapear_banco(caminho):
    conexao = sqlite3.connect(caminho)

    tabelas = conexao.execute("""
        SELECT name, sql
        FROM sqlite_schema
        WHERE type = 'table'
          AND name NOT LIKE 'sqlite_%'
    """).fetchall()

    mapa = {}

    for nome_tabela, codigo in tabelas:
        colunas = conexao.execute(
            f'PRAGMA table_info("{nome_tabela}")'
        ).fetchall()

        mapa[nome_tabela] = {
            "codigo": codigo,
            "colunas": [
                {
                    "nome": coluna[1],
                    "tipo": coluna[2]
                }
                for coluna in colunas
            ]
        }

    conexao.close()
    return mapa

banco = "banco_teste_lgpd.db"
caminho = Path(__file__).resolve().parent / banco
resultado = mapear_banco(str(caminho))
print(json.dumps(resultado, indent=4, ensure_ascii=False))

