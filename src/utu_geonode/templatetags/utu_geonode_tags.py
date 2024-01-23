
from django import template
from django.db.models import Q
from geonode.layers.models import Dataset
from geonode.base.models import Configuration
from geonode_mapstore_client.templatetags.get_menu_json import _is_mobile_device

register = template.Library()

@register.simple_tag()
def get_most_recently_added_featured_dataset():

    featured_dataset = Dataset.objects \
        .filter(Q(featured=True)) \
        .order_by('-date') \
        .values('id', 'title', 'thumbnail_url') \
        .first()

    return featured_dataset

@register.simple_tag(takes_context=True)
def get_custom_base_right_topbar_menu(context):

    is_mobile = _is_mobile_device(context)

    if is_mobile:
        return []

    home = {
        "type": "link",
        "href": "/",
        "label": "Home"
    }
    user = context.get('request').user
    about = {
            "label": "Community",
            "type": "dropdown",
            "items": [
                {
                    "type": "link",
                    "href": "https://blog.geonode.utu.fi/news-stories-events/",
                    "label": "News, Stories and Events",
                    "target": "_blank"
                },
                {
                    "type": "link",
                    "href": "/people/",
                    "label": "People"
                },
                {
                    "type": "link",
                    "href": "/groups/",
                    "label": "Groups"
                },
                {
                    "type": "link",
                    "href": "/about-us/",
                    "label": "About us"
                }
            ]
        }
    if user.is_authenticated and not Configuration.load().read_only:
        about['items'].extend([
            {
                "type": "divider"
            },
            {
                "type": "link",
                "href": "/invitations/geonode-send-invite/",
                "label": "Invite users"
            },
            {
                "type": "link",
                "href": "/admin/people/profile/add/",
                "label": "Add user"
            } if user.is_superuser else None,
            {
                "type": "link",
                "href": "/groups/create/",
                "label": "Create group"
            }if user.is_superuser else None,
        ])
    return [home, about]
