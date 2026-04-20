#!/usr/bin/env python3

"""Stage the submitter's Kerberos credential in the current HTCondor schedd."""

from __future__ import annotations

import sys


try:
    import htcondor2 as htcondor
except ImportError:
    import htcondor


def main() -> int:
    try:
        htcondor.Credd().add_user_cred(htcondor.CredTypes.Kerberos, None)
    except Exception as exc:
        print(
            "Failed to stage Kerberos credentials for HTCondor submission: "
            f"{exc}",
            file=sys.stderr,
        )
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
