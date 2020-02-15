from django import template
from django.template import RequestContext

from core.models import *

register = template.Library()


@register.inclusion_tag(filename='core/tags/menu.html', takes_context=True)
def draw_menu(context: RequestContext, menu_title: str) -> dict:
    points = MenuPoint.objects.filter(menu__title=menu_title)
    current_url_name = context.request.resolver_match.view_name
    if not points.filter(url_name=current_url_name).exists():
        # No active menu point: display only first-level points.
        points = points.filter(depth=0)
    else:
        # Menu point is active: display its children and ancestors with their siblings.
        ancestors_and_their_siblings = MenuPoint.objects.filter(parent__in=Relation.objects.filter(
            descendant__url_name=current_url_name).values_list('ancestor', flat=True))
        points = points.filter(depth=0).union(ancestors_and_their_siblings,
                                              MenuPoint.objects.filter(parent__url_name=current_url_name))
    return {'points': points}
