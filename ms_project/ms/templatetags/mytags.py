from django import template
register = template.Library()


# 自定义过滤器
@register.filter(name='truncate_chars')
def truncate_chars(value, a):
    if value.__len__() > int(a):
        return '%s...'% value[0:int(a)]
    else:
        return value
