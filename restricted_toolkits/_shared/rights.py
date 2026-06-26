# -*- coding: utf-8 -*-
"""Rights status + the lawful-source guard shared by all toolkits."""

STATUSES = ('public-domain', 'cc0', 'open-license', 'in-copyright')

LAWFUL_SOURCE_NOTICE = (
    "This toolkit distributes only code, metadata, and structural signatures — never the\n"
    "work itself. To build a local copy you must supply a source you have lawfully obtained.\n"
    "It does NOT bypass DRM, paywalls, or logins, and does NOT scrape against any site's\n"
    "terms of service. It grants no license to any text.")


def network_fetch_allowed(manifest):
    """A network fetch is allowed ONLY for a source_option explicitly marked allowed:true
    (reserved for public-domain / clearly-licensed sources). Returns the option or None."""
    for opt in manifest.get('source_options', []):
        if opt.get('kind') == 'official-download' and opt.get('allowed') is True:
            return opt
    return None


def refuse_unless_user_file(args_input, manifest):
    """Guard for acquire: require a user-supplied file unless an allowed PD fetch exists."""
    if args_input:
        return
    if network_fetch_allowed(manifest):
        return
    raise SystemExit(
        "REFUSED: no --input given and no allowed public-domain fetch is configured.\n\n" +
        LAWFUL_SOURCE_NOTICE)
