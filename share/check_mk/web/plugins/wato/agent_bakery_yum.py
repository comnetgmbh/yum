#!/usr/bin/env python3
# -*- encoding: utf-8; py-indent-offset: 4 -*-
from cmk.gui.cee.plugins.wato.agent_bakery.rulespecs.utils import RulespecGroupMonitoringAgentsAgentPlugins
from cmk.gui.i18n import _
from cmk.gui.valuespec import (
    Dictionary,
    Alternative,
    Age,
    FixedValue
)

from cmk.gui.plugins.wato import (
    HostRulespec,
    rulespec_registry
)


def _valuespec_agent_config_yum():
    return Alternative(
        title=_("YUM (Community Version) updates (Linux)"),
        help=_("This will deploy the agent plugin <tt>yum</tt>. This will activate the "
               "check <tt>yum</tt> on RedHat based hosts and monitor pending normal and security updates."),
        style="dropdown",
        elements=[
            Dictionary(
                title=_("Deploy the YUM plugin"),
                elements=[
                    ("interval",
                     Age(title="Interval for checking updates"),
                     ),
                ],
                optional_keys=False,
            ),
            FixedValue(None, title=_("Do not deploy the YUM plugin"), totext=_("(disabled)")),
        ],
        default_value={"interval": 129600, },
    )


rulespec_registry.register(
    HostRulespec(
        name="agent_config:yum",
        group=RulespecGroupMonitoringAgentsAgentPlugins,
        valuespec=_valuespec_agent_config_yum
    ))

