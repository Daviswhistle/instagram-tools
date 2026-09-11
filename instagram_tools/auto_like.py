"""Public auto-like domain API."""

from .auto_like_engine import (
    AutoLikerError,
    BrowserClosedError,
    FollowingFeedScanner,
    FollowingFeedUnavailableError,
    InstagramRestrictionError,
    ScanSummary,
    normalize_post_key,
)

__all__ = [
    "AutoLikerError",
    "BrowserClosedError",
    "FollowingFeedScanner",
    "FollowingFeedUnavailableError",
    "InstagramRestrictionError",
    "ScanSummary",
    "normalize_post_key",
]
