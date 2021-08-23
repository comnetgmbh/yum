# Yum Check


## Description
This check checks for available updates via yum or dnf on RedHat and derivatives.
The check receives the data via an agent-plugin.

The check becomes critical if kernel updates require a reboot.
It becomes warning state if there are any updates available.
This state can be overridden via a WATO rule.
