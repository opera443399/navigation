# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.apps import AppConfig


class PortalConfig(AppConfig):
    name = 'portal'


# for img in $(ls media/icons/);do echo $img |awk -F'.' '{print "    (#icons/"$0"#, #"$1"#),"}' |sed "s/#/'/g";done
CHOICES_ICONS = (
    ('icons/analysis.png', 'analysis'),
    ('icons/bandwidth.png', 'bandwidth'),
    ('icons/bastion.png', 'bastion'),
    ('icons/default.svg', 'default'),
    ('icons/email.png', 'email'),
    ('icons/it.png', 'it'),
    ('icons/log.png', 'log'),
    ('icons/network.png', 'network'),
    ('icons/nginx.png', 'nginx'),
    ('icons/oa.png', 'oa'),
    ('icons/ops.png', 'ops'),
    ('icons/publish.png', 'publish'),
    ('icons/security.png', 'security'),
    ('icons/server.png', 'server'),
    ('icons/smokeping.png', 'smokeping'),
    ('icons/statistic.png', 'statistic'),
    ('icons/tool.png', 'tool'),
    ('icons/web.png', 'web'),
    ('icons/wiki.png', 'wiki'),
    ('icons/zabbix.png', 'zabbix'),
)