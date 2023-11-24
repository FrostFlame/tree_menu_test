from django import template
from django.shortcuts import get_object_or_404
from django.utils.safestring import mark_safe

from menu.models import MenuItem
from menu.utils import draw

register = template.Library()


@register.simple_tag(takes_context=True)
def draw_menu(context, menu_name: str):
    menu_item = get_object_or_404(MenuItem, title=menu_name)
    tree = menu_item.get_tree()
    html_tree = draw(tree, context.request.build_absolute_uri(context.request.get_full_path()))

    return mark_safe(html_tree)
