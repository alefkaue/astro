"""Request boundary: CSRF, conservative execution gates and safe errors."""
import secrets

from flask import g, jsonify, request, session

from app.config import config


def install(app):
    app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024

    @app.before_request
    def protect():
        g.request_id = secrets.token_hex(12)
        if request.method in ('POST', 'PATCH', 'PUT', 'DELETE') and (session.get('uid') or request.path == '/api/login'):
            expected = session.get('csrf_token', '')
            supplied = request.headers.get('X-CSRF-Token', '')
            if not expected or not secrets.compare_digest(expected, supplied):
                return jsonify({'error': 'CSRF inválido', 'code': 'csrf_failed'}), 403
        origin = request.headers.get('Origin')
        if request.method in ('POST', 'PATCH', 'PUT', 'DELETE') and origin and origin != request.host_url.rstrip('/'):
            return jsonify({'error': 'Origem não permitida', 'code': 'origin_denied'}), 403
        if request.method in ('POST', 'PUT', 'PATCH'):
            body = request.get_json(silent=True)
            if body is None or not isinstance(body, dict):
                return jsonify({'error': 'Objeto JSON obrigatório', 'code': 'invalid_json'}), 400
            string_fields = ('name','client','status','note','notes','persona','plan','cycle','target','instructions','template')
            for key in string_fields:
                if key in body and (not isinstance(body[key], str) or len(body[key]) > 4000):
                    return jsonify({'error': f'Campo {key} inválido', 'code': 'invalid_input'}), 400
            for key in ('scan_id','finding_id','engagement_id'):
                if key in body and (type(body[key]) is not int or body[key] < 1):
                    return jsonify({'error': f'Campo {key} inválido', 'code': 'invalid_input'}), 400
            if 'scope' in body and (not isinstance(body['scope'], list) or len(body['scope']) > 256 or
                                    any(not isinstance(item, str) or len(item) > 128 for item in body['scope'])):
                return jsonify({'error': 'Escopo inválido', 'code': 'invalid_input'}), 400
            if 'hosts' in body and (not isinstance(body['hosts'], list) or len(body['hosts']) > 256 or
                                    any(not isinstance(item, str) for item in body['hosts'])):
                return jsonify({'error': 'Hosts inválidos', 'code': 'invalid_input'}), 400
        # Legacy scanners contain invasive checks, run in the web process and
        # cannot enforce scope revocation immediately before every connection.
        if request.path in ('/api/scan', '/api/autonomous/run', '/api/exploit_chain', '/api/auto_discover'):
            from app.auth.decorators import current_user
            if not current_user():
                return jsonify({'error': 'Não autenticado'}), 401
            if request.path in ('/api/scan', '/api/autonomous/run'):
                from app.auth.decorators import permission_required
                result = permission_required('scan:execute')(lambda: None)()
                if result is not None:
                    return result
            return jsonify({'error': 'Execução legada suspensa até worker/agente e controles P0',
                            'code': 'execution_disabled'}), 403

    @app.after_request
    def headers(response):
        response.headers['X-Request-ID'] = getattr(g, 'request_id', '')
        response.headers['X-Content-Type-Options'] = 'nosniff'
        response.headers['X-Frame-Options'] = 'DENY'
        response.headers['Referrer-Policy'] = 'same-origin'
        if request.path.startswith('/api/'):
            response.headers['Cache-Control'] = 'no-store'
        if response.is_json and response.status_code >= 400:
            body = response.get_json()
            if isinstance(body, dict):
                body.setdefault('code', f'http_{response.status_code}')
                body.setdefault('message', body.get('error', 'Falha na requisição'))
                body['request_id'] = getattr(g, 'request_id', '')
                response.set_data(app.json.dumps(body))
        return response

    @app.errorhandler(PermissionError)
    def denied(_error):
        return jsonify({'error': 'Recurso não encontrado'}), 404
