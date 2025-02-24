from __future__ import annotations

from typing import Literal

SortType = Literal[
    "Active",
    "Hot",
    "New",
    "Old",
    "TopDay",
    "TopWeek",
    "TopMonth",
    "TopYear",
    "TopAll",
    "MostComments",
    "NewComments",
    "TopHour",
    "TopSixHour",
    "TopTwelveHour",
    "TopThreeMonths",
    "TopSixMonths",
    "TopNineMonths",
    "Controversial",
    "Scaled",
]

ListingType = Literal[
    "All",
    "Local",
    "Subscribed",
    "ModeratorView",
]
