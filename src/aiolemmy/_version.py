try:
    # as name is needed to avoid mypy complaining about a missing explicit export
    from ._scm_version import version as version  # noqa: PLC0414
except ImportError:
    version = "unknown"
