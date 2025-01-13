from __future__ import annotations

import logging
import urllib.parse
from datetime import datetime
from typing import Any

import aiohttp.client

from ._version import version

logger = logging.getLogger(__name__)

PAGE_LIMIT_MAX = 50

MODLOG_TYPES = {
    "removed_posts": "mod_remove_post",
    "locked_posts": "mod_lock_post",
    "featured_posts": "mod_feature_post",
    "removed_comments": "mod_remove_comment",
    "removed_communities": "mod_remove_community",
    "banned_from_community": "mod_ban_from_community",
    "banned": "mod_ban",
    "added_to_community": "mod_add_community",
    "transferred_to_community": "mod_transfer_community",
    "added": "mod_add",
    "admin_purged_persons": "admin_purge_person",
    "admin_purged_communities": "admin_purge_community",
    "admin_purged_posts": "admin_purge_post",
    "admin_purged_comments": "admin_purge_comment",
    "hidden_communities": "mod_hide_community",
}

DEFAULT_USER_AGENT = f"aiolemmy/{version} (https://github.com/Nothing4You/aiolemmy)"


class Lemmy:
    _jwt: str | None = None

    def __init__(
        self,
        session: aiohttp.client.ClientSession,
        instance_base_url: str,
        *,
        user_agent: str | None = None,
        jwt: str | None = None,
    ) -> None:
        self._session = session
        self._common_headers = {
            "User-Agent": (
                user_agent if user_agent is not None else DEFAULT_USER_AGENT
            ),
        }

        if jwt is not None:
            self._jwt = jwt
            self._common_headers["authorization"] = f"Bearer {jwt}"

        if instance_base_url.endswith("/"):
            self._instance_base_url = instance_base_url[:-1]
        else:
            self._instance_base_url = instance_base_url

        self._domain = urllib.parse.urlsplit(self._instance_base_url).hostname

    async def _request(
        self,
        method: str,
        url: str,
        /,
        **kwargs: Any,
    ) -> aiohttp.client.ClientResponse:
        if "raise_for_status" not in kwargs:
            kwargs["raise_for_status"] = True

        if "headers" in kwargs:
            kwargs["headers"] = self._common_headers | kwargs["headers"]
        else:
            kwargs["headers"] = self._common_headers

        if "timeout" not in kwargs:
            kwargs["timeout"] = aiohttp.client.ClientTimeout(
                sock_connect=5,
            )

        return await self._session.request(
            method,
            url,
            **kwargs,
        )

    async def _get(
        self,
        url: str,
        /,
        **kwargs: Any,
    ) -> aiohttp.client.ClientResponse:
        return await self._request(
            "get",
            url,
            **kwargs,
        )

    async def _post(
        self,
        url: str,
        /,
        **kwargs: Any,
    ) -> aiohttp.client.ClientResponse:
        return await self._request(
            "post",
            url,
            **kwargs,
        )

    async def _put(
        self,
        url: str,
        /,
        **kwargs: Any,
    ) -> aiohttp.client.ClientResponse:
        return await self._request(
            "put",
            url,
            **kwargs,
        )

    async def list_communities(
        self,
        *,
        limit: int | None = None,
        page: int | None = None,
        show_nsfw: bool | None = None,
        sort: str | None = None,
        type_: str | None = None,
    ) -> aiohttp.ClientResponse:
        url = f"{self._instance_base_url}/api/v3/community/list"
        query: dict[str, int | str] = {}

        if limit is not None:
            query["limit"] = limit
        if page is not None:
            query["page"] = page
        if show_nsfw is not None:
            query["show_nsfw"] = str(show_nsfw).lower()
        if sort is not None:
            query["sort"] = sort
        if type_ is not None:
            query["type_"] = type_

        return await self._get(url, params=query, raise_for_status=False)

    async def list_posts(
        self,
        *,
        community_id: int | None = None,
        community_name: str | None = None,
        disliked_only: bool | None = None,
        liked_only: bool | None = None,
        limit: int | None = None,
        page: int | None = None,
        page_cursor: str | None = None,
        saved_only: bool | None = None,
        sort: str | None = None,
        type_: str | None = None,
    ) -> aiohttp.ClientResponse:
        url = f"{self._instance_base_url}/api/v3/post/list"
        query: dict[str, int | str] = {}

        if community_id is not None:
            query["community_id"] = community_id
        if community_name is not None:
            query["community_name"] = community_name
        if disliked_only is not None:
            query["disliked_only"] = str(disliked_only).lower()
        if liked_only is not None:
            query["liked_only"] = str(liked_only).lower()
        if limit is not None:
            query["limit"] = limit
        if page is not None:
            query["page"] = page
        if page_cursor is not None:
            query["page_cursor"] = page_cursor
        if saved_only is not None:
            query["saved_only"] = str(saved_only).lower()
        if sort is not None:
            query["sort"] = sort
        if type_ is not None:
            query["type_"] = type_

        return await self._get(url, params=query, raise_for_status=False)

    async def list_comments(
        self,
        *,
        community_id: int | None = None,
        community_name: str | None = None,
        disliked_only: bool | None = None,
        liked_only: bool | None = None,
        limit: int | None = None,
        max_depth: int | None = None,
        page: int | None = None,
        parent_id: int | None = None,
        post_id: int | None = None,
        saved_only: bool | None = None,
        sort: str | None = None,
        type_: str | None = None,
    ) -> aiohttp.ClientResponse:
        url = f"{self._instance_base_url}/api/v3/comment/list"
        query: dict[str, int | str] = {}

        if community_id is not None:
            query["community_id"] = community_id
        if community_name is not None:
            query["community_name"] = community_name
        if disliked_only is not None:
            query["disliked_only"] = str(disliked_only).lower()
        if liked_only is not None:
            query["liked_only"] = str(liked_only).lower()
        if limit is not None:
            query["limit"] = limit
        if max_depth is not None:
            query["max_depth"] = max_depth
        if page is not None:
            query["page"] = page
        if parent_id is not None:
            query["parent_id"] = parent_id
        if post_id is not None:
            query["post_id"] = post_id
        if saved_only is not None:
            query["saved_only"] = str(saved_only).lower()
        if sort is not None:
            query["sort"] = sort
        if type_ is not None:
            query["type_"] = type_

        return await self._get(url, params=query, raise_for_status=False)

    async def get_comment_reports(
        self,
        *,
        unresolved_only: bool = False,
        page: int = 1,
        limit: int | None = 20,
    ) -> dict[int, Any]:
        url = f"{self._instance_base_url}/api/v3/comment/report/list"
        query: dict[str, int | str] = {
            "page": page,
            "limit": (
                min(limit, PAGE_LIMIT_MAX) if limit is not None else PAGE_LIMIT_MAX
            ),
        }
        if unresolved_only:
            query["unresolved_only"] = "true"

        # report ids as keys to avoid double counting them
        reports: dict[int, Any] = {}

        # If viewing all reports, order by newest, but if viewing unresolved only, show the oldest first (FIFO)
        # https://github.com/LemmyNet/lemmy/blob/0.19.3/crates/db_views/src/comment_report_view.rs#L108

        j = None
        broken = False
        while not broken and (limit is None or len(reports) < limit):
            if j is not None:
                query["page"] += 1

            logger.debug("Retrieving comment reports page %s", query["page"])
            r = await self._get(url, params=query, raise_for_status=True)
            j = await r.json()

            if len(j["comment_reports"]) == 0:
                break

            for report in j["comment_reports"]:
                if limit is not None and len(reports) >= limit:
                    broken = True
                    break

                if report["comment_report"]["id"] not in reports:
                    reports[report["comment_report"]["id"]] = report

        logger.debug("Retrieved %s comment reports", len(reports))

        return reports

    async def get_post_reports(
        self,
        *,
        unresolved_only: bool = False,
        page: int = 1,
        limit: int | None = 20,
    ) -> dict[int, Any]:
        url = f"{self._instance_base_url}/api/v3/post/report/list"
        query: dict[str, int | str] = {
            "page": page,
            "limit": (
                min(limit, PAGE_LIMIT_MAX) if limit is not None else PAGE_LIMIT_MAX
            ),
        }
        if unresolved_only:
            query["unresolved_only"] = "true"

        # report ids as keys to avoid double counting them
        reports: dict[int, Any] = {}

        # If viewing all reports, order by newest, but if viewing unresolved only, show the oldest first (FIFO)
        # https://github.com/LemmyNet/lemmy/blob/0.19.3/crates/db_views/src/comment_report_view.rs#L108

        j = None
        broken = False
        while not broken and (limit is None or len(reports) < limit):
            if j is not None:
                query["page"] += 1

            logger.debug("Retrieving post reports page %s", query["page"])
            r = await self._get(url, params=query, raise_for_status=True)
            j = await r.json()

            if len(j["post_reports"]) == 0:
                break

            for report in j["post_reports"]:
                if limit is not None and len(reports) >= limit:
                    broken = True
                    break

                if report["post_report"]["id"] not in reports:
                    reports[report["post_report"]["id"]] = report

        logger.debug("Retrieved %s post reports", len(reports))

        return reports

    async def get_private_message_reports(
        self,
        *,
        unresolved_only: bool = False,
        page: int = 1,
        limit: int | None = 20,
    ) -> dict[int, Any]:
        url = f"{self._instance_base_url}/api/v3/private_message/report/list"
        query: dict[str, int | str] = {
            "page": page,
            "limit": (
                min(limit, PAGE_LIMIT_MAX) if limit is not None else PAGE_LIMIT_MAX
            ),
        }
        if unresolved_only:
            query["unresolved_only"] = "true"

        # report ids as keys to avoid double counting them
        reports: dict[int, Any] = {}

        # If viewing all reports, order by newest, but if viewing unresolved only, show the oldest first (FIFO)
        # https://github.com/LemmyNet/lemmy/blob/0.19.3/crates/db_views/src/comment_report_view.rs#L108

        j = None
        broken = False
        while not broken and (limit is None or len(reports) < limit):
            if j is not None:
                query["page"] += 1

            logger.debug("Retrieving private message reports page %s", query["page"])
            r = await self._get(url, params=query, raise_for_status=True)
            j = await r.json()

            if len(j["private_message_reports"]) == 0:
                break

            for report in j["private_message_reports"]:
                if limit is not None and len(reports) >= limit:
                    broken = True
                    break

                if report["private_message_report"]["id"] not in reports:
                    reports[report["private_message_report"]["id"]] = report

        logger.debug("Retrieved %s private message reports", len(reports))

        return reports

    async def resolve_comment_report(
        self,
        report_id: int,
        resolved: bool = True,
    ) -> Any:
        payload = {
            "report_id": report_id,
            "resolved": resolved,
        }

        r = await self._put(
            f"{self._instance_base_url}/api/v3/comment/report/resolve",
            json=payload,
        )

        return await r.json()

    async def resolve_post_report(
        self,
        report_id: int,
        resolved: bool = True,
    ) -> Any:
        payload = {
            "report_id": report_id,
            "resolved": resolved,
        }

        r = await self._put(
            f"{self._instance_base_url}/api/v3/post/report/resolve",
            json=payload,
        )

        return await r.json()

    async def resolve_private_message_report(
        self,
        report_id: int,
        resolved: bool = True,
    ) -> Any:
        payload = {
            "report_id": report_id,
            "resolved": resolved,
        }

        r = await self._put(
            f"{self._instance_base_url}/api/v3/private_message/report/resolve",
            json=payload,
        )

        return await r.json()

    async def get_registration_applications(
        self,
        *,
        unread_only: bool = False,
        page: int = 1,
        limit: int = 20,
    ) -> Any:
        params: dict[str, int | str] = {
            "page": page,
            "limit": limit,
        }
        if unread_only:
            params["unread_only"] = "true"

        r = await self._get(
            f"{self._instance_base_url}/api/v3/admin/registration_application/list",
            params=params,
        )

        return await r.json()

    # TODO: this should use list_posts()
    async def get_community_posts(
        self,
        community: str,
        count: int | None = 100,
        after: datetime | None = None,
    ) -> Any:
        url = f"{self._instance_base_url}/api/v3/post/list"
        query = {
            "limit": 20,
            "sort": "New",
            "type_": "All",
            "community_name": community,
        }

        posts: list[Any] = []

        j = None
        broken = False
        while count is None or len(posts) < count:
            if broken:
                break
            if j is not None:
                if "next_page" in j:
                    query["page_cursor"] = j["next_page"]
                elif "page" in query:
                    query["page"] += 1
                else:
                    query["page"] = 2

            r = await self._get(url, params=query, raise_for_status=False)

            if r.content_type == "text/plain":
                t = await r.text()
                # This should always have an error status
                r.raise_for_status()
                logger.warning("Invalid response while trying to retrieve posts: %r", t)
                return []

            if r.content_type == "text/html":
                logger.warning("unexpectedly received html from %s", url)
                t = await r.text()
                logger.warning("%r", t)
                return []

            j = await r.json()

            if "error" in j:  # noqa: SIM102
                # 0.19+ Community is not known to this instance
                # For removed and deleted communities we will just return an empty posts array
                if j["error"] == "unknown" and j["message"] == "Record not found":
                    logger.info(
                        "community %s does not exist on %s",
                        community,
                        self._domain,
                    )
                    return []

            if len(j["posts"]) == 0:
                logger.debug("received 0 posts")
                break

            for post in j["posts"]:
                if count is not None and len(posts) == count:
                    logger.debug("break; found enough posts at %s", count)
                    break

                if after is not None:
                    post_published = datetime.fromisoformat(post["post"]["published"])
                    if post_published <= after:
                        # community featured posts are listed at the top of the first page and may be older than desired
                        if post["post"]["featured_community"]:
                            continue

                        logger.debug(
                            "breaking; post %s from %s is older than %s",
                            post["post"]["ap_id"],
                            post_published,
                            after,
                        )
                        broken = True
                        break

                posts.append(post)

            logger.debug("added posts, now at %s", len(posts))

        return posts

    async def get_person_details(
        self,
        username: str | None = None,
        person_id: int | None = None,
        sort: str | None = None,
        limit: int | None = 20,
    ) -> Any:
        if username is None and person_id is None:
            raise Exception("username or person_id must be provided")

        if username is not None and person_id is not None:
            raise Exception("username and person_id must not both be provided")

        logger.debug(
            "Retrieving person details for %s",
            username if username is not None else person_id,
        )

        url = f"{self._instance_base_url}/api/v3/user"
        query = {
            "sort": sort if sort is not None else "New",
            "page": 1,
            "limit": (
                min(limit, PAGE_LIMIT_MAX) if limit is not None else PAGE_LIMIT_MAX
            ),
        }
        if username is not None:
            query["username"] = username
        if person_id is not None:
            query["person_id"] = person_id

        person_view = None
        moderates = None

        # content ids as keys to avoid double counting content if new content was added during pagination
        posts: dict[str, Any] = {}
        comments: dict[str, Any] = {}

        j = None
        broken = False
        while not broken and (
            limit is None or (len(posts) < limit and len(comments) < limit)
        ):
            if j is not None:
                query["page"] += 1

            logger.debug(
                "Retrieving %s page %s for %s",
                url,
                query["page"],
                username if username is not None else person_id,
            )
            r = await self._get(url, params=query, raise_for_status=True)
            j = await r.json()

            person_view = j["person_view"]
            moderates = j["moderates"]

            for post in j["posts"]:
                if limit is not None and len(posts) >= limit:
                    broken = True
                    break
                posts[post["post"]["id"]] = post

            for comment in j["comments"]:
                if limit is not None and len(comments) >= limit:
                    broken = True
                    break
                comments[comment["comment"]["id"]] = comment

            if len(j["posts"]) < query["limit"] and len(j["comments"]) < query["limit"]:  # type: ignore[operator]
                break

        return {
            "person_view": person_view,
            "moderates": moderates,
            "posts": posts,
            "comments": comments,
        }

    async def remove_post(
        self,
        post_id: int,
        removed: bool,
        reason: str | None = None,
    ) -> Any:
        payload: dict[str, int | bool | str] = {
            "post_id": post_id,
            "removed": removed,
        }
        if reason is not None:
            payload["reason"] = reason

        r = await self._post(
            f"{self._instance_base_url}/api/v3/post/remove",
            json=payload,
        )

        return await r.json()

    async def remove_comment(
        self,
        comment_id: int,
        removed: bool,
        reason: str | None = None,
    ) -> Any:
        payload: dict[str, int | bool | str] = {
            "comment_id": comment_id,
            "removed": removed,
        }
        if reason is not None:
            payload["reason"] = reason

        r = await self._post(
            f"{self._instance_base_url}/api/v3/comment/remove",
            json=payload,
        )

        return await r.json()

    async def report_post(
        self,
        post_id: int,
        reason: str,
    ) -> Any:
        r = await self._post(
            f"{self._instance_base_url}/api/v3/post/report",
            json={
                "post_id": post_id,
                "reason": reason,
            },
        )

        return await r.json()

    async def report_comment(
        self,
        comment_id: int,
        reason: str,
    ) -> Any:
        r = await self._post(
            f"{self._instance_base_url}/api/v3/comment/report",
            json={
                "comment_id": comment_id,
                "reason": reason,
            },
        )

        return await r.json()

    async def report_private_message(
        self,
        private_message_id: int,
        reason: str,
    ) -> Any:
        r = await self._post(
            f"{self._instance_base_url}/api/v3/private_message/report",
            json={
                "private_message_id": private_message_id,
                "reason": reason,
            },
        )

        return await r.json()

    async def ban_from_site(
        self,
        person_id: int,
        ban: bool | None = True,
        reason: str | None = None,
        expires: int | None = None,
        remove_data: bool | None = None,
    ) -> Any:
        payload: dict[str, int | bool | str] = {
            "person_id": person_id,
        }
        if ban is not None:
            payload["ban"] = ban
        if reason is not None:
            payload["reason"] = reason
        if expires is not None:
            payload["expires"] = expires
        if remove_data is not None:
            payload["remove_data"] = remove_data

        r = await self._post(
            f"{self._instance_base_url}/api/v3/user/ban",
            json=payload,
        )

        return await r.json()

    async def add_mod_to_community(
        self,
        community_id: int,
        person_id: int,
        added: bool = True,
    ) -> Any:
        payload: dict[str, int | bool] = {
            "added": added,
            "person_id": person_id,
            "community_id": community_id,
        }

        r = await self._post(
            f"{self._instance_base_url}/api/v3/community/mod",
            json=payload,
        )

        return await r.json()

    async def ban_from_community(
        self,
        person_id: int,
        community_id: int,
        ban: bool | None = True,
        reason: str | None = None,
        expires: int | None = None,
        remove_data: bool | None = None,
    ) -> Any:
        payload: dict[str, int | bool | str] = {
            "person_id": person_id,
            "community_id": community_id,
        }
        if ban is not None:
            payload["ban"] = ban
        if reason is not None:
            payload["reason"] = reason
        if expires is not None:
            payload["expires"] = expires
        if remove_data is not None:
            payload["remove_data"] = remove_data

        r = await self._post(
            f"{self._instance_base_url}/api/v3/community/ban_user",
            json=payload,
        )

        return await r.json()

    async def remove_community(
        self,
        community_id: int,
        removed: bool = True,
        reason: str | None = None,
    ) -> Any:
        payload: dict[str, int | bool | str] = {
            "community_id": community_id,
            "removed": removed,
        }

        if reason is not None:
            payload["reason"] = reason

        r = await self._post(
            f"{self._instance_base_url}/api/v3/community/remove",
            json=payload,
        )

        return await r.json()

    async def hide_community(
        self,
        community_id: int,
        hidden: bool = True,
        reason: str | None = None,
    ) -> Any:
        payload: dict[str, int | bool | str] = {
            "community_id": community_id,
            "hidden": hidden,
        }

        if reason is not None:
            payload["reason"] = reason

        r = await self._put(
            f"{self._instance_base_url}/api/v3/community/hide",
            json=payload,
        )

        return await r.json()

    async def get_modlog(
        self,
        community_id: int | None = None,
        mod_person_id: int | None = None,
        other_person_id: int | None = None,
        type_: str | None = None,
        limit: int | None = 20,
    ) -> dict[str, dict[int, Any]]:
        url = f"{self._instance_base_url}/api/v3/modlog"
        query: dict[str, int | str] = {
            "page": 1,
            "limit": (
                min(limit, PAGE_LIMIT_MAX) if limit is not None else PAGE_LIMIT_MAX
            ),
        }
        if community_id is not None:
            query["community_id"] = community_id
        if mod_person_id is not None:
            query["mod_person_id"] = mod_person_id
        if other_person_id is not None:
            query["other_person_id"] = other_person_id
        if type_ is not None:
            query["type_"] = type_

        # modlog record ids as keys by type to avoid double counting content if new content was added during pagination
        # modlog_reports[record_type][record_id]
        modlog_records: dict[str, dict[int, Any]] = {}

        # Lemmy returns modlog entries by descending published date

        j = None
        broken = False
        while not broken and (
            limit is None
            or all(len(records) < limit for records in modlog_records.values())
        ):
            if j is not None:
                query["page"] += 1

            logger.debug("Retrieving modlog page %s", query["page"])
            r = await self._get(url, params=query, raise_for_status=True)
            j = await r.json()

            for k in j:
                if k not in MODLOG_TYPES:
                    logger.warning("received unexpected key in modlog response: %s", k)
                    continue

                if k not in modlog_records:
                    modlog_records[k] = {}

                for record in j[k]:
                    if limit is not None and len(modlog_records[k]) >= limit:
                        broken = True
                        break
                    modlog_records[k][record[MODLOG_TYPES[k]]["id"]] = record

            if all(k in j and len(j[k]) < query["limit"] for k in MODLOG_TYPES):  # type: ignore[operator]
                break

        return modlog_records

    async def resolve_object(self, q: str, /) -> Any:
        r = await self._get(
            f"{self._instance_base_url}/api/v3/resolve_object",
            params={"q": q},
            raise_for_status=False,
        )
        return await r.json()

    async def get_federated_instances(self) -> Any:
        r = await self._get(
            f"{self._instance_base_url}/api/v3/federated_instances",
        )

        return await r.json()

    async def block_instance(self, instance_id: int, block: bool) -> Any:
        r = await self._post(
            f"{self._instance_base_url}/api/v3/site/block",
            json={
                "instance_id": instance_id,
                "block": block,
            },
        )

        return await r.json()

    async def get_site(self) -> Any:
        r = await self._get(
            f"{self._instance_base_url}/api/v3/site",
        )

        return await r.json()

    async def edit_site(self, **kwargs: Any) -> Any:
        r = await self._put(
            f"{self._instance_base_url}/api/v3/site",
            json=kwargs,
        )

        return await r.json()
