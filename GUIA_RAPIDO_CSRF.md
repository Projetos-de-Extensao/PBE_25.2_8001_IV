# 🔧 GUIA RÁPIDO: Corrigir Erro 403 CSRF no Heroku

## ⏱️ Tempo de Execução: ~5 minutos

### ❌ Sintoma do Problema
```
Erro ao fazer login como Professor/Monitor/Admin em produção:
Forbidden (403) - CSRF verification failed
```

---

## ✅ Solução em 3 Passos

### Passo 1: Configurar Variáveis de Ambiente

Execute UM dos dois métodos abaixo:

#### Método A: Usar Script Automatizado (RECOMENDADO)
```bash
chmod +x fix_csrf_heroku.sh
./fix_csrf_heroku.sh
```

#### Método B: Comandos Manuais
```bash
# Substitua "seu-app-name" pelo nome da sua app no Heroku
# Substitua "seu-dominio.herokuapp.com" pelo domínio real

heroku config:set \
  ALLOWED_HOSTS=localhost,127.0.0.1,seu-dominio.herokuapp.com \
  CSRF_TRUSTED_ORIGINS=https://seu-dominio.herokuapp.com \
  DEBUG=False \
  SECURE_SSL_REDIRECT=True \
  CSRF_COOKIE_SECURE=True \
  SESSION_COOKIE_SECURE=True \
  --app seu-app-name
```

### Passo 2: Deploy das Alterações
```bash
git add meuprojeto/settings.py
git commit -m "fix: Corrigir CSRF em produção"
git push heroku main
```

### Passo 3: Validar a Correção
```bash
# Monitorar logs
heroku logs --tail

# Testar login em:
# https://seu-dominio.herokuapp.com/login/

# Com usuários:
# Professor: professor.teste / professor123
# Monitor: monitor.teste / monitor123
# Admin: admin / admin123
```

---

## 🎯 O Que Foi Alterado

### `meuprojeto/settings.py`

```python
# ✅ Novo (linha ~25)
CSRF_TRUSTED_ORIGINS = config(
    'CSRF_TRUSTED_ORIGINS',
    default='https://seu-dominio.herokuapp.com',
    cast=Csv()
)

# ✅ Atualizado (linha ~160)
if not DEBUG:
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')  # ← NOVO
    CSRF_COOKIE_SAMESITE = 'Lax'  # ← NOVO
    # ... resto das configurações
```

---

## 🆘 Troubleshooting

| Sintoma | Solução |
|---------|---------|
| Ainda recebe 403 CSRF | Reiniciar dyno: `heroku restart --app seu-app` |
| Variáveis não salvaram | Verificar: `heroku config:get ALLOWED_HOSTS --app seu-app` |
| Login funciona em dev, não em prod | Deletar cache: `CTRL+SHIFT+DEL` no navegador |
| Precisa ver erros detalhados | Temporário: `heroku config:set DEBUG=True --app seu-app` |

---

## ✨ Resultado Esperado

✅ **Login bem-sucedido para:**
- Professor ✓
- Monitor ✓
- Admin ✓
- Aluno ✓

---

**Documentação Completa:** Ver arquivo `CORRECAO_ERRO_CSRF_403.md`
