# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.utils.translation import ugettext_lazy as _

from django.shortcuts import render
from django.http import JsonResponse

from .models import Level1BizGroup, Level2WorkGroup, Level3App, Level4AppCategory, Level5AppLink


# Create your views here.

# ================================ /portal/index ================================
def show_index(request):
    """
    show index.
    """
    return render(request, 'portal/index.html')


# ================================ /portal/app/id ================================
def show_app_default(request):
    """
    return json data for content right as default info.
    """
    default_content = {
        'title': _('Portal'),
        "data": []
    }
    return JsonResponse(default_content)


def get_links_by_id(id):
    """
    return json data in list for links filtered by id.
    """
    links = Level5AppLink.objects.filter(cat_id=id).order_by('link_name')
    tree_view_level5_nodes = []
    for n in links:
        node = {
            'name': n.link_name,
            'href': n.link_href,
            'img': '/media/{0}'.format(n.link_img if n.link_img_upload == '' else n.link_img_upload)
        }
        tree_view_level5_nodes.append(node)

    return tree_view_level5_nodes


def show_app(request, app_id):
    """
    return json data for app filtered by id.
    require: get_links_by_id.
    """
    this_app = Level3App.objects.get(app_id=app_id).app_name
    app_cat = Level4AppCategory.objects.filter(app__app_id=app_id).order_by('cat_rank')
    tree_view_level4_nodes = {
        'title': this_app,
        "data": []
    }
    for n in app_cat:
        tree_view_level4_nodes["data"].append({
            'id': this_app,
            'name': n.cat_name,
            'links': get_links_by_id(n.id)
        })

    return JsonResponse(tree_view_level4_nodes)


# ================================ /portal/show/tree ================================
def get_apps_by_id(id):
    """
    return json data in list for apps filtered by id.
    """
    work_groups = Level3App.objects.filter(wg__wg_id=id).filter(is_enabled=True).order_by('app_rank')
    tree_view_level3_nodes = []
    for n in work_groups:
        node = {
            'text': n.app_name,
            'href': '#appid_{0}'.format(n.app_id),
        }
        tree_view_level3_nodes.append(node)

    return tree_view_level3_nodes


def get_work_groups_by_id(id):
    """
    return json data in list for work groups filtered by id.
    """
    work_groups = Level2WorkGroup.objects.filter(bg__bg_id=id).order_by('wg_rank')
    tree_view_level2_nodes = []
    for n in work_groups:
        node = {
            'text': n.wg_name,
            'href': '#',
            'nodes': get_apps_by_id(n.wg_id)
        }
        if len(node['nodes']) == 0:
            continue
        tree_view_level2_nodes.append(node)

    return tree_view_level2_nodes


def show_tree(request):
    """
    return json data for treeview.
    require: get_work_groups_by_id, get_apps_by_id.
    """
    biz_groups = Level1BizGroup.objects.order_by('bg_rank')
    tree_view_level1_nodes = {
        'comment': "",
        "data": []
    }
    for n in biz_groups:
        node = {
            'text': n.bg_name,
            'href': '#',
            'nodes': get_work_groups_by_id(n.bg_id)
        }
        if len(node['nodes']) == 0:
            continue
        tree_view_level1_nodes['data'].append(node)

    return JsonResponse(tree_view_level1_nodes)


# ================================ /portal/show/navbar ================================
def show_nav(request):
    """
    return json data for navbar.
    require: get_apps_by_id.
    """
    biz_groups = Level1BizGroup.objects.order_by('bg_rank')
    nav_bar_level1_nodes = {
        'comment': "",
        "data": []
    }
    for b in biz_groups:
        work_groups = Level2WorkGroup.objects.filter(bg__bg_id=b.bg_id).filter(added_to_navbar=True).order_by('wg_rank')
        for n in work_groups:
            node = {
                'text': n.wg_name,
                'href': '#',
                'nodes': get_apps_by_id(n.wg_id)
            }
            if len(node['nodes']) == 0:
                continue
            nav_bar_level1_nodes['data'].append(node)

    return JsonResponse(nav_bar_level1_nodes)


# ================================ set default data for exp ================================
def set_default_app_cat_and_link(request):
    """
    set default link for each app.
    """
    apps = Level3App.objects.filter(is_enabled=True).order_by('app_name')

    for app in apps:
        count_error = 0
        try:
            (cat, status) = Level4AppCategory.objects.get_or_create(
                    cat_name='default({0})'.format(app.app_name),
                    app=app
            )
            print('cat={0}, status={1}'.format(cat.cat_name, status))

            href = 'http://nav.test.com/test?app={0}_{1}'.format(app.app_ename, app.app_id)
            (link, status) = Level5AppLink.objects.get_or_create(
                    link_name='default({0})'.format(app.app_name),
                    link_href=href,
                    cat=cat
            )
            print('link={0}, status={1}'.format(link.link_name, status))

        except Exception as e:
            print('[error]: {0}'.format(e))
            count_error += 1
            continue
        print('[count_error]: {0}'.format(count_error))

    return JsonResponse({'msg': 'OK'})