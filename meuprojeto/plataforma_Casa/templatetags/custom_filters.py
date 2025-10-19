from django import template

register = template.Library()


@register.filter
def filter_by_status(queryset, status):
    """
    Filtro customizado para filtrar objetos por status
    Uso: {{ pagamentos|filter_by_status:'Pendente' }}
    """
    if not queryset:
        return []
    
    try:
        return queryset.filter(status=status)
    except Exception:
        # Se o queryset não tiver o campo status ou não for um queryset
        # tenta filtrar como lista comum
        if isinstance(queryset, list):
            return [item for item in queryset if hasattr(item, 'status') and item.status == status]
        return queryset
