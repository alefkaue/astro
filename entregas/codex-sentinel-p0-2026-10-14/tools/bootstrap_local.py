"""Create a local organization owner interactively, without default passwords."""
import getpass
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app import create_app, db
from app.config import config


def main():
    if config.ENVIRONMENT != 'development' or config.DEMO:
        raise SystemExit('Bootstrap apenas em development, DEMO=false')
    name = input('Organização: ').strip()
    email = input('Email do owner: ').strip().lower()
    password = getpass.getpass('Senha (mínimo 12 caracteres): ')
    if not name or '@' not in email or len(password) < 12:
        raise SystemExit('Nome, email e senha forte obrigatórios')
    if password != getpass.getpass('Confirmar senha: '):
        raise SystemExit('Senhas diferentes')
    create_app()
    if db.get_user_by_email(email):
        raise SystemExit('Email já cadastrado; nenhuma organização criada')
    account_id = db.create_account(name)
    user_id = db.create_user(email, name, password, 'owner', account_id)
    print(f'Organização {account_id} e owner {user_id} criados. Execução real permanece bloqueada.')


if __name__ == '__main__':
    main()
