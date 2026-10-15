"""Offline restore with integrity checks and preservation of previous contents."""
import argparse
import sqlite3
from datetime import datetime, timezone
from pathlib import Path


def restore(backup, database):
    backup = Path(backup).resolve(strict=True)
    database = Path(database).resolve()
    if backup == database:
        raise ValueError('Backup e destino devem ser distintos')
    source = sqlite3.connect(backup.as_uri() + '?mode=ro', uri=True)
    try:
        if source.execute('PRAGMA integrity_check').fetchone()[0] != 'ok':
            raise ValueError('Backup inválido')
        if database.exists():
            previous = database.with_name(database.name + '.before-restore-' + datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%f') + '.bak')
            current = sqlite3.connect(database)
            snapshot = sqlite3.connect(previous)
            try:
                current.backup(snapshot)
            finally:
                current.close()
                snapshot.close()
        target = sqlite3.connect(database)
        try:
            source.backup(target)
            if target.execute('PRAGMA integrity_check').fetchone()[0] != 'ok':
                raise ValueError('Restore inválido')
        finally:
            target.close()
    finally:
        source.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Pare app/worker antes do restore; o estado anterior será preservado.')
    parser.add_argument('--backup', required=True)
    parser.add_argument('--database', required=True)
    args = parser.parse_args()
    restore(args.backup, args.database)
    print('Restore verificado. Não inicialize a versão nova para validar rollback da versão anterior.')
