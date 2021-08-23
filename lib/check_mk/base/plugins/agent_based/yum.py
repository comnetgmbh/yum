#!/usr/bin/env python3
#
# Check_MK YUM Plugin - Check for upgradeable packages.
#
# Copyright 2015, Henri Wahl <h.wahl@ifw-dresden.de>
# Copyright 2018, Moritz Schlarb <schlarbm@uni-mainz.de>
#
# Based on:
#
# Check_MK APT-NG Plugin - Check for upgradeable packages.
#
# Copyright 2012, Stefan Schlesinger <sts@ono.at>
# Copyright 2015, Karsten Schoeke <karsten.schoeke@geobasis-bb.de>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#
# Example Agent Output:
#
# <<<yum>>>
# yes
# 4

from .agent_based_api.v1 import (
    register,
    Service,
    Result,
    State,
    Metric,
    render
)

yum_default_levels = {
    "reboot_req" : 2,
    "normal": 1,
    "security": 2,
    "last_update_state": 0,
    "last_update_time_diff": (60*24*60*60),
}

register.agent_section(
    name="yum",
)


def discovery_yum(section):
    if len(section) > 0:
        yield Service(item=None, parameters={})


# the check function
def check_yum(params, section):
    level        = 0
    msg          = ''
    reboot_req   = 'no'
    packages     = -1
    security_packages = -1
    # Parse the agent output
    if len(section) > 0:
        reboot_req = section[0][0]
        if reboot_req not in ('yes', 'no'):
            reboot_req = ''

    if len(section) > 1:
        try:
            packages = int(section[1][0])
        except:
            packages = -1

        try:
            security_packages = int(section[2][0])
        except:
            security_packages = -1

        try:
            last_update_timestamp = int(section[3][0])
        except:
            last_update_timestamp = -1

        if last_update_timestamp > 0:
            last_update = ", last update was run at %s" % render.datetime(last_update_timestamp)
        else:
            last_update = ""

        if packages < 0 and security_packages < 0:
            level = 3
            msg = 'No package information available' + str(packages)

        elif packages > 0 and security_packages > 0:
            level = 1
            if packages == 1:
                s = ''
            else:
                s = 's'
            if security_packages == 1:
                s_p = ''
            else:
                s_p = 's'

            msg = "%s security update%s and %s update%s available%s" % (security_packages, s_p, packages, s, last_update)

        elif packages > 0 and security_packages <= 0:
            level = 1
            if packages == 1:
                s = ''
            else:
                s = 's'
            msg = '%s update%s available%s' % (packages, s, last_update)

        elif security_packages > 0 and packages <= 0:
            level = 1
            if security_packages == 1:
                s = ''
            else:
                s = 's'
            msg = "%d security updates available%s" % (security_updates, s, last_update)

        packages = packages + security_packages

        if packages >= 0:
            yield Metric("count", packages)

    if (reboot_req == "yes") and (level == 0):
        # fallback for < 2.0.6
        if params is None:
            level = 2
        else:
            level = params["reboot_req"]
        msg = "reboot required"

    if level > 0:
        yield Result(state=State(level), summary="%s" % msg)
    else:
        yield Result(state=State(level), summary="All packages are up to date%s" % last_update)

register.check_plugin(
    name="yum",
    service_name="YUM Updates",
    discovery_function=discovery_yum,
    check_function=check_yum,
    check_ruleset_name="yum",
    check_default_parameters=yum_default_levels,
)

