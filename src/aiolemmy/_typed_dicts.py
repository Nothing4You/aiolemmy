from __future__ import annotations

import sys
from typing import TYPE_CHECKING, Literal, TypedDict

if sys.version_info >= (3, 11):
    from typing import NotRequired
else:
    from typing_extensions import NotRequired

if TYPE_CHECKING:
    from aiolemmy._enum_types import ListingType, SortType


class GetApiV3CommentReportListParams(TypedDict):
    comment_id: NotRequired[int | None]
    community_id: NotRequired[int | None]
    limit: NotRequired[int | None]
    page: NotRequired[int | None]
    unresolved_only: NotRequired[Literal["true", "false"] | None]


class GetApiV3PostReportListParams(TypedDict):
    community_id: NotRequired[int | None]
    limit: NotRequired[int | None]
    page: NotRequired[int | None]
    post_id: NotRequired[int | None]
    unresolved_only: NotRequired[Literal["true", "false"] | None]


class GetApiV3PrivateMessageReportListParams(TypedDict):
    limit: NotRequired[int | None]
    page: NotRequired[int | None]
    unresolved_only: NotRequired[Literal["true", "false"] | None]


class GetApiV3PostListParams(TypedDict):
    community_id: NotRequired[int | None]
    community_name: NotRequired[str | None]
    disliked_only: NotRequired[Literal["true", "false"] | None]
    liked_only: NotRequired[Literal["true", "false"] | None]
    limit: NotRequired[int | None]
    page: NotRequired[int | None]
    page_cursor: NotRequired[str | None]
    saved_only: NotRequired[Literal["true", "false"] | None]
    show_hidden: NotRequired[Literal["true", "false"] | None]
    show_nsfw: NotRequired[Literal["true", "false"] | None]
    show_read: NotRequired[Literal["true", "false"] | None]
    sort: NotRequired[SortType | None]
    type_: NotRequired[ListingType | None]


class GetApiV3UserParams(TypedDict):
    community_id: NotRequired[int | None]
    limit: NotRequired[int | None]
    page: NotRequired[int | None]
    person_id: NotRequired[int | None]
    saved_only: NotRequired[Literal["true", "false"] | None]
    sort: NotRequired[SortType | None]
    username: NotRequired[str | None]


class GetApiV3ModlogParams(TypedDict):
    comment_id: NotRequired[int | None]
    community_id: NotRequired[int | None]
    limit: NotRequired[int | None]
    mod_person_id: NotRequired[int | None]
    other_person_id: NotRequired[int | None]
    page: NotRequired[int | None]
    person_id: NotRequired[int | None]
    type_: NotRequired[ListingType | None]
