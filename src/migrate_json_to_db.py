"""
migrate_json_to_db.py
─────────────────────
Script de migração única: lê os arquivos JSON antigos (se existirem) e
importa os dados para o banco PostgreSQL.

Como rodar no Railway:
  railway run python src/migrate_json_to_db.py

Localmente (com DATABASE_URL configurado):
  DATABASE_URL="postgresql://..." python src/migrate_json_to_db.py
"""

import os
import json
import sys
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("migração")

_SRC = os.path.dirname(os.path.abspath(__file__))

def _ler_json(nome_arquivo):
    caminho = os.path.join(_SRC, nome_arquivo)
    if not os.path.exists(caminho):
        logger.info(f"  Arquivo não encontrado: {nome_arquivo} — pulando.")
        return None
    try:
        with open(caminho, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        logger.error(f"  Erro ao ler {nome_arquivo}: {e}")
        return None

def migrar_media(cur):
    dados = _ler_json("media_storage.json")
    if dados is None:
        return 0, 0
    videos  = dados.get("videos", [])
    imagens = dados.get("imagens", [])
    v_ok = i_ok = 0
    for item in videos:
        try:
            cur.execute(
                "INSERT INTO media (file_id, tipo, caption) VALUES (%s, 'video', %s) ON CONFLICT (file_id) DO NOTHING",
                (item["file_id"], item.get("caption", ""))
            )
            if cur.rowcount > 0:
                v_ok += 1
        except Exception as e:
            logger.warning(f"    Vídeo ignorado ({item.get('file_id','?')}): {e}")
    for item in imagens:
        try:
            cur.execute(
                "INSERT INTO media (file_id, tipo, caption) VALUES (%s, 'imagem', %s) ON CONFLICT (file_id) DO NOTHING",
                (item["file_id"], item.get("caption", ""))
            )
            if cur.rowcount > 0:
                i_ok += 1
        except Exception as e:
            logger.warning(f"    Imagem ignorada ({item.get('file_id','?')}): {e}")
    return v_ok, i_ok

def migrar_ranking(cur):
    dados = _ler_json("ranking.json")
    if dados is None:
        return 0
    ok = 0
    for user_id_str, info in dados.items():
        try:
            cur.execute("""
                INSERT INTO ranking (user_id, nome, pontos, msgs_hoje, ultimo_dia)
                VALUES (%s, %s, %s, %s, NULL)
                ON CONFLICT (user_id) DO UPDATE
                    SET nome   = EXCLUDED.nome,
                        pontos = GREATEST(ranking.pontos, EXCLUDED.pontos)
            """, (
                int(user_id_str),
                info.get("nome", "Membro"),
                int(info.get("pontos", 0)),
                0,
            ))
            ok += 1
        except Exception as e:
            logger.warning(f"    Ranking uid={user_id_str} ignorado: {e}")
    return ok

def migrar_oracao(cur):
    dados = _ler_json("pedidos_oracao.json")
    if dados is None:
        return 0
    if not isinstance(dados, list):
        logger.warning("  pedidos_oracao.json: formato inesperado.")
        return 0
    ok = 0
    for item in dados:
        try:
            cur.execute("""
                INSERT INTO oracao (nome, user_id, pedido, data, orado)
                VALUES (%s, %s, %s, %s, %s)
            """, (
                item.get("nome", "Membro"),
                int(item.get("user_id", 0)),
                item.get("pedido", ""),
                item.get("data", ""),
                bool(item.get("orado", False)),
            ))
            ok += 1
        except Exception as e:
            logger.warning(f"    Pedido oração ignorado: {e}")
    return ok

def migrar_aniversarios(cur):
    dados = _ler_json("aniversarios.json")
    if dados is None:
        return 0
    ok = 0
    for user_id_str, info in dados.items():
        try:
            cur.execute("""
                INSERT INTO aniversarios (user_id, nome, dia, mes)
                VALUES (%s, %s, %s, %s)
                ON CONFLICT (user_id) DO UPDATE
                    SET nome = EXCLUDED.nome,
                        dia  = EXCLUDED.dia,
                        mes  = EXCLUDED.mes
            """, (
                int(user_id_str),
                info.get("nome", "Membro"),
                int(info.get("dia", 1)),
                int(info.get("mes", 1)),
            ))
            ok += 1
        except Exception as e:
            logger.warning(f"    Aniversário uid={user_id_str} ignorado: {e}")
    return ok

def migrar_testemunhos(cur):
    dados = _ler_json("testemunhos.json")
    if dados is None:
        return 0
    if not isinstance(dados, list):
        logger.warning("  testemunhos.json: formato inesperado.")
        return 0
    ok = 0
    for item in dados:
        try:
            cur.execute("""
                INSERT INTO testemunhos (nome, user_id, texto, data, publicado)
                VALUES (%s, %s, %s, %s, %s)
            """, (
                item.get("nome", "Membro"),
                int(item.get("user_id", 0)),
                item.get("texto", ""),
                item.get("data", ""),
                bool(item.get("publicado", False)),
            ))
            ok += 1
        except Exception as e:
            logger.warning(f"    Testemunho ignorado: {e}")
    return ok

def migrar_avisos(cur):
    dados = _ler_json("avisos_usuarios.json")
    if dados is None:
        return 0
    ok = 0
    for user_id_str, qtd in dados.items():
        try:
            cur.execute("""
                INSERT INTO avisos (user_id, avisos, ultimo)
                VALUES (%s, %s, '')
                ON CONFLICT (user_id) DO UPDATE
                    SET avisos = GREATEST(avisos.avisos, EXCLUDED.avisos)
            """, (int(user_id_str), int(qtd)))
            ok += 1
        except Exception as e:
            logger.warning(f"    Aviso uid={user_id_str} ignorado: {e}")
    return ok

def main():
    logger.info("=" * 55)
    logger.info("  MIGRAÇÃO JSON → PostgreSQL — Avivamento AD Bot")
    logger.info("=" * 55)

    sys.path.insert(0, _SRC)
    try:
        from database import init_db, db
    except ImportError as e:
        logger.error(f"Não foi possível importar database.py: {e}")
        sys.exit(1)

    logger.info("Inicializando banco de dados...")
    try:
        init_db()
        logger.info("  ✅ Tabelas prontas.")
    except Exception as e:
        logger.error(f"  ❌ Falha ao inicializar banco: {e}")
        sys.exit(1)

    resultados = {}

    try:
        with db() as cur:
            logger.info("\n📦 Migrando mídia (media_storage.json)...")
            v, i = migrar_media(cur)
            resultados["Vídeos"] = v
            resultados["Imagens"] = i

            logger.info("🏆 Migrando ranking (ranking.json)...")
            resultados["Ranking"] = migrar_ranking(cur)

            logger.info("🙏 Migrando pedidos de oração (pedidos_oracao.json)...")
            resultados["Orações"] = migrar_oracao(cur)

            logger.info("🎂 Migrando aniversários (aniversarios.json)...")
            resultados["Aniversários"] = migrar_aniversarios(cur)

            logger.info("🌟 Migrando testemunhos (testemunhos.json)...")
            resultados["Testemunhos"] = migrar_testemunhos(cur)

            logger.info("⚠️  Migrando avisos (avisos_usuarios.json)...")
            resultados["Avisos"] = migrar_avisos(cur)

    except Exception as e:
        logger.error(f"Erro fatal durante migração: {e}")
        sys.exit(1)

    logger.info("\n" + "=" * 55)
    logger.info("  RESULTADO DA MIGRAÇÃO")
    logger.info("=" * 55)
    for chave, qtd in resultados.items():
        icone = "✅" if qtd > 0 else "⏭️ "
        logger.info(f"  {icone} {chave}: {qtd} registro(s) importado(s)")
    logger.info("=" * 55)
    logger.info("Migração concluída! O bot já pode ser iniciado.")

if __name__ == "__main__":
    main()
