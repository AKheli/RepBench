from django import template

register = template.Library()





@register.simple_tag
def kt_portlet(title=None , id=None):
    html = f'<div class="kt-portlet">' \
           f'<div class="kt-portlet__head">'
    if title:
        html += f'<div class="kt-portlet__head-label">' \
                f'<h3 class="kt-portlet__head-title"><h2>{title}</h2></h3>' \
                f'</div>'
    html += f'</div>'
    return html


@register.simple_tag
def kt_toolbar(id=None):
    html =    f""" <div class="kt-portlet__head-toolbar"> </div>"""
    if title:
        html += f'<div class="kt-portlet__head-label">' \
                f'<h3 class="kt-portlet__head-title"><h2>{title}</h2></h3>' \
                f'</div>'
    html += f'</div>'
    return html


@register.simple_tag
def kt_portlet(title=None):
    html = f'<div class="kt-portlet">' \
           f'<div class="kt-portlet__head">'
    if title:
        html += f'<div class="kt-portlet__head-label">' \
                f'<h3 class="kt-portlet__head-title"><h2>{title}</h2></h3>' \
                f'</div>'
    html += f'</div>'
    return html