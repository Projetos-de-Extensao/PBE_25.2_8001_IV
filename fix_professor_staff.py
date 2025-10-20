#!/usr/bin/env python
"""
Script para remover is_staff de professor.teste
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'meuprojeto.settings')
django.setup()

from django.contrib.auth.models import User

user = User.objects.get(username='professor.teste')
print(f'Antes:')
print(f'  is_staff: {user.is_staff}')
print(f'  is_superuser: {user.is_superuser}')

user.is_staff = False
user.save()

print(f'Depois:')
print(f'  is_staff: {user.is_staff}')
print(f'  is_superuser: {user.is_superuser}')
