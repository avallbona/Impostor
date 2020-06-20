"""template tags for impostor."""

from django import template
from impostor.models import ImpostorLog

register = template.Library()


@register.simple_tag
def get_impersonated_as(request):
    """return the impersonated_as template tag to include into the main template.

    :param request:
    :return:
    """
    try:
        impersonated_as = ImpostorLog.objects.get(token=request.session['impostor_token'])
    except (ImpostorLog.DoesNotExist, KeyError):
        impersonated_as = None

    return impersonated_as
