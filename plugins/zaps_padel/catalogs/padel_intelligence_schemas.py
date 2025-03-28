matches_list = {
    "fields": [
        {
            "name": "id",
            "type": "int64"
        },
        {
            "name": "tournament",
            "type": {
                "struct": [
                    {
                        "name": "category",
                        "type": {
                            "struct": [
                                {
                                    "name": "id",
                                    "type": "int64"
                                },
                                {
                                    "name": "name",
                                    "type": "string"
                                },
                                {
                                    "name": "tour",
                                    "type": {
                                        "struct": [
                                            {
                                                "name": "id",
                                                "type": "int64"
                                            },
                                            {
                                                "name": "name",
                                                "type": "string"
                                            }
                                        ]
                                    }
                                }
                            ]
                        }
                    },
                    {
                        "name": "description",
                        "type": "string"
                    },
                    {
                        "name": "endTime",
                        "type": "string"
                    },
                    {
                        "name": "goldenPoint",
                        "type": "bool"
                    },
                    {
                        "name": "id",
                        "type": "int64"
                    },
                    {
                        "name": "location",
                        "type": "string"
                    },
                    {
                        "name": "name",
                        "type": "string"
                    },
                    {
                        "name": "startTime",
                        "type": "string"
                    },
                    {
                        "name": "tiebreak",
                        "type": "bool"
                    },
                    {
                        "name": "tour",
                        "type": {
                            "struct": [
                                {
                                    "name": "id",
                                    "type": "int64"
                                },
                                {
                                    "name": "name",
                                    "type": "string"
                                }
                            ]
                        }
                    }
                ]
            }
        },
        {
            "name": "startTime",
            "type": "string"
        },
        {
            "name": "team1Left",
            "type": {
                "struct": [
                    {
                        "name": "active",
                        "type": "bool"
                    },
                    {
                        "name": "birthdate",
                        "type": "string"
                    },
                    {
                        "name": "brand",
                        "type": {
                            "struct": [
                                {
                                    "name": "id",
                                    "type": "int64"
                                },
                                {
                                    "name": "logo",
                                    "type": "string"
                                },
                                {
                                    "name": "name",
                                    "type": "string"
                                },
                                {
                                    "name": "sponsorActive",
                                    "type": "bool"
                                },
                                {
                                    "name": "url",
                                    "type": "string"
                                }
                            ]
                        }
                    },
                    {
                        "name": "country",
                        "type": "string"
                    },
                    {
                        "name": "gender",
                        "type": "string"
                    },
                    {
                        "name": "hand",
                        "type": "string"
                    },
                    {
                        "name": "id",
                        "type": "int64"
                    },
                    {
                        "name": "image",
                        "type": "string"
                    },
                    {
                        "name": "name",
                        "type": "string"
                    },
                    {
                        "name": "nickname",
                        "type": "string"
                    },
                    {
                        "name": "preferSide",
                        "type": "string"
                    },
                    {
                        "name": "publicVisible",
                        "type": "bool"
                    }
                ]
            }
        },
        {
            "name": "team1Right",
            "type": {
                "struct": [
                    {
                        "name": "active",
                        "type": "bool"
                    },
                    {
                        "name": "birthdate",
                        "type": "string"
                    },
                    {
                        "name": "brand",
                        "type": {
                            "struct": [
                                {
                                    "name": "id",
                                    "type": "int64"
                                },
                                {
                                    "name": "logo",
                                    "type": "string"
                                },
                                {
                                    "name": "name",
                                    "type": "string"
                                },
                                {
                                    "name": "sponsorActive",
                                    "type": "bool"
                                },
                                {
                                    "name": "url",
                                    "type": "string"
                                }
                            ]
                        }
                    },
                    {
                        "name": "country",
                        "type": "string"
                    },
                    {
                        "name": "gender",
                        "type": "string"
                    },
                    {
                        "name": "hand",
                        "type": "string"
                    },
                    {
                        "name": "id",
                        "type": "int64"
                    },
                    {
                        "name": "image",
                        "type": "string"
                    },
                    {
                        "name": "name",
                        "type": "string"
                    },
                    {
                        "name": "nickname",
                        "type": "string"
                    },
                    {
                        "name": "preferSide",
                        "type": "string"
                    },
                    {
                        "name": "publicVisible",
                        "type": "bool"
                    }
                ]
            }
        },
        {
            "name": "team2Left",
            "type": {
                "struct": [
                    {
                        "name": "active",
                        "type": "bool"
                    },
                    {
                        "name": "birthdate",
                        "type": "string"
                    },
                    {
                        "name": "brand",
                        "type": {
                            "struct": [
                                {
                                    "name": "id",
                                    "type": "int64"
                                },
                                {
                                    "name": "logo",
                                    "type": "string"
                                },
                                {
                                    "name": "name",
                                    "type": "string"
                                },
                                {
                                    "name": "sponsorActive",
                                    "type": "bool"
                                },
                                {
                                    "name": "url",
                                    "type": "string"
                                }
                            ]
                        }
                    },
                    {
                        "name": "country",
                        "type": "string"
                    },
                    {
                        "name": "gender",
                        "type": "string"
                    },
                    {
                        "name": "hand",
                        "type": "string"
                    },
                    {
                        "name": "id",
                        "type": "int64"
                    },
                    {
                        "name": "image",
                        "type": "string"
                    },
                    {
                        "name": "name",
                        "type": "string"
                    },
                    {
                        "name": "nickname",
                        "type": "string"
                    },
                    {
                        "name": "preferSide",
                        "type": "string"
                    },
                    {
                        "name": "publicVisible",
                        "type": "bool"
                    }
                ]
            }
        },
        {
            "name": "team2Right",
            "type": {
                "struct": [
                    {
                        "name": "active",
                        "type": "bool"
                    },
                    {
                        "name": "birthdate",
                        "type": "string"
                    },
                    {
                        "name": "brand",
                        "type": {
                            "struct": [
                                {
                                    "name": "id",
                                    "type": "int64"
                                },
                                {
                                    "name": "logo",
                                    "type": "string"
                                },
                                {
                                    "name": "name",
                                    "type": "string"
                                },
                                {
                                    "name": "sponsorActive",
                                    "type": "bool"
                                },
                                {
                                    "name": "url",
                                    "type": "string"
                                }
                            ]
                        }
                    },
                    {
                        "name": "country",
                        "type": "string"
                    },
                    {
                        "name": "gender",
                        "type": "string"
                    },
                    {
                        "name": "hand",
                        "type": "string"
                    },
                    {
                        "name": "id",
                        "type": "int64"
                    },
                    {
                        "name": "image",
                        "type": "string"
                    },
                    {
                        "name": "name",
                        "type": "string"
                    },
                    {
                        "name": "nickname",
                        "type": "string"
                    },
                    {
                        "name": "preferSide",
                        "type": "string"
                    },
                    {
                        "name": "publicVisible",
                        "type": "bool"
                    }
                ]
            }
        },
        {
            "name": "endTime",
            "type": "string"
        },
        {
            "name": "tiebreak",
            "type": "bool"
        },
        {
            "name": "goldenPoint",
            "type": "bool"
        },
        {
            "name": "matchRound",
            "type": {
                "struct": [
                    {
                        "name": "id",
                        "type": "int64"
                    },
                    {
                        "name": "name",
                        "type": "string"
                    }
                ]
            }
        },
        {
            "name": "loaded",
            "type": "bool"
        },
        {
            "name": "accessLevel",
            "type": "int64"
        }
    ]
}

matches_stats_lastpoints = {
    "fields": [
        {
            "name": "matchId",
            "type": "int64"
        },
        {
            "name": "last10Points",
            "type": {
                "list": "int64"
            }
        },
        {
            "name": "lastPointNumShots",
            "type": "int64"
        },
        {
            "name": "longestPoint",
            "type": "int64"
        },
        {
            "name": "rallyLengthAvg",
            "type": "string"
        }
    ]
}

matches_stats_player = {
    "fields": [
        {
            "name": "matchId",
            "type": "int64"
        },
        {
            "name": "team1Left",
            "type": {
                "struct": [
                    {
                        "name": "assists",
                        "type": "int64"
                    },
                    {
                        "name": "image",
                        "type": "string"
                    },
                    {
                        "name": "netRegains",
                        "type": "int64"
                    },
                    {
                        "name": "pErrors",
                        "type": "int64"
                    },
                    {
                        "name": "participation",
                        "type": "string"
                    },
                    {
                        "name": "pi",
                        "type": "double"
                    },
                    {
                        "name": "piHistory",
                        "type": {
                            "list": {
                                "list": "double"
                            }
                        }
                    },
                    {
                        "name": "piKp",
                        "type": "double"
                    },
                    {
                        "name": "player",
                        "type": "string"
                    },
                    {
                        "name": "returnTotal",
                        "type": "int64"
                    },
                    {
                        "name": "returnWon",
                        "type": "int64"
                    },
                    {
                        "name": "returnWonPercentage",
                        "type": "double"
                    },
                    {
                        "name": "rulos",
                        "type": "int64"
                    },
                    {
                        "name": "serverTotal",
                        "type": "int64"
                    },
                    {
                        "name": "serverWon",
                        "type": "int64"
                    },
                    {
                        "name": "serverWonPercentage",
                        "type": "double"
                    },
                    {
                        "name": "smashAttempts",
                        "type": "int64"
                    },
                    {
                        "name": "smashWinners",
                        "type": "int64"
                    },
                    {
                        "name": "uErrors",
                        "type": "int64"
                    },
                    {
                        "name": "winners",
                        "type": "int64"
                    }
                ]
            }
        },
        {
            "name": "team1Right",
            "type": {
                "struct": [
                    {
                        "name": "assists",
                        "type": "int64"
                    },
                    {
                        "name": "image",
                        "type": "string"
                    },
                    {
                        "name": "netRegains",
                        "type": "int64"
                    },
                    {
                        "name": "pErrors",
                        "type": "int64"
                    },
                    {
                        "name": "participation",
                        "type": "string"
                    },
                    {
                        "name": "pi",
                        "type": "double"
                    },
                    {
                        "name": "piHistory",
                        "type": {
                            "list": {
                                "list": "double"
                            }
                        }
                    },
                    {
                        "name": "piKp",
                        "type": "double"
                    },
                    {
                        "name": "player",
                        "type": "string"
                    },
                    {
                        "name": "returnTotal",
                        "type": "int64"
                    },
                    {
                        "name": "returnWon",
                        "type": "int64"
                    },
                    {
                        "name": "returnWonPercentage",
                        "type": "double"
                    },
                    {
                        "name": "rulos",
                        "type": "int64"
                    },
                    {
                        "name": "serverTotal",
                        "type": "int64"
                    },
                    {
                        "name": "serverWon",
                        "type": "int64"
                    },
                    {
                        "name": "serverWonPercentage",
                        "type": "double"
                    },
                    {
                        "name": "smashAttempts",
                        "type": "int64"
                    },
                    {
                        "name": "smashWinners",
                        "type": "int64"
                    },
                    {
                        "name": "uErrors",
                        "type": "int64"
                    },
                    {
                        "name": "winners",
                        "type": "int64"
                    }
                ]
            }
        },
        {
            "name": "team2Left",
            "type": {
                "struct": [
                    {
                        "name": "assists",
                        "type": "int64"
                    },
                    {
                        "name": "image",
                        "type": "string"
                    },
                    {
                        "name": "netRegains",
                        "type": "int64"
                    },
                    {
                        "name": "pErrors",
                        "type": "int64"
                    },
                    {
                        "name": "participation",
                        "type": "string"
                    },
                    {
                        "name": "pi",
                        "type": "double"
                    },
                    {
                        "name": "piHistory",
                        "type": {
                            "list": {
                                "list": "double"
                            }
                        }
                    },
                    {
                        "name": "piKp",
                        "type": "double"
                    },
                    {
                        "name": "player",
                        "type": "string"
                    },
                    {
                        "name": "returnTotal",
                        "type": "int64"
                    },
                    {
                        "name": "returnWon",
                        "type": "int64"
                    },
                    {
                        "name": "returnWonPercentage",
                        "type": "double"
                    },
                    {
                        "name": "rulos",
                        "type": "int64"
                    },
                    {
                        "name": "serverTotal",
                        "type": "int64"
                    },
                    {
                        "name": "serverWon",
                        "type": "int64"
                    },
                    {
                        "name": "serverWonPercentage",
                        "type": "double"
                    },
                    {
                        "name": "smashAttempts",
                        "type": "int64"
                    },
                    {
                        "name": "smashWinners",
                        "type": "int64"
                    },
                    {
                        "name": "uErrors",
                        "type": "int64"
                    },
                    {
                        "name": "winners",
                        "type": "int64"
                    }
                ]
            }
        },
        {
            "name": "team2Right",
            "type": {
                "struct": [
                    {
                        "name": "assists",
                        "type": "int64"
                    },
                    {
                        "name": "image",
                        "type": "string"
                    },
                    {
                        "name": "netRegains",
                        "type": "int64"
                    },
                    {
                        "name": "pErrors",
                        "type": "int64"
                    },
                    {
                        "name": "participation",
                        "type": "string"
                    },
                    {
                        "name": "pi",
                        "type": "double"
                    },
                    {
                        "name": "piHistory",
                        "type": {
                            "list": {
                                "list": "double"
                            }
                        }
                    },
                    {
                        "name": "piKp",
                        "type": "double"
                    },
                    {
                        "name": "player",
                        "type": "string"
                    },
                    {
                        "name": "returnTotal",
                        "type": "int64"
                    },
                    {
                        "name": "returnWon",
                        "type": "int64"
                    },
                    {
                        "name": "returnWonPercentage",
                        "type": "double"
                    },
                    {
                        "name": "rulos",
                        "type": "int64"
                    },
                    {
                        "name": "serverTotal",
                        "type": "int64"
                    },
                    {
                        "name": "serverWon",
                        "type": "int64"
                    },
                    {
                        "name": "serverWonPercentage",
                        "type": "double"
                    },
                    {
                        "name": "smashAttempts",
                        "type": "int64"
                    },
                    {
                        "name": "smashWinners",
                        "type": "int64"
                    },
                    {
                        "name": "uErrors",
                        "type": "int64"
                    },
                    {
                        "name": "winners",
                        "type": "int64"
                    }
                ]
            }
        }
    ]
}

matches_stats_resume = {
    "fields": [
        {
            "name": "id",
            "type": "string"
        },
        {
            "name": "matchId",
            "type": "int64"
        },
        {
            "name": "matchScoreId",
            "type": "int64"
        },
        {
            "name": "currentTeam1",
            "type": "string"
        },
        {
            "name": "currentTeam2",
            "type": "string"
        },
        {
            "name": "set1Team1",
            "type": "int64"
        },
        {
            "name": "set1Team2",
            "type": "int64"
        },
        {
            "name": "set2Team1",
            "type": "int64"
        },
        {
            "name": "set2Team2",
            "type": "int64"
        },
        {
            "name": "set3Team1",
            "type": "int64"
        },
        {
            "name": "set3Team2",
            "type": "int64"
        }
    ]
}

matches_stats_sets = {
    "fields": [
        {
            "name": "id",
            "type": "string"
        },
        {
            "name": "match",
            "type": {
                "struct": [
                    {
                        "name": "accessLevel",
                        "type": "int64"
                    },
                    {
                        "name": "endTime",
                        "type": "string"
                    },
                    {
                        "name": "goldenPoint",
                        "type": "bool"
                    },
                    {
                        "name": "id",
                        "type": "int64"
                    },
                    {
                        "name": "loaded",
                        "type": "bool"
                    },
                    {
                        "name": "matchRound",
                        "type": {
                            "struct": [
                                {
                                    "name": "categoryRounds",
                                    "type": {
                                        "list": "string"
                                    }
                                },
                                {
                                    "name": "id",
                                    "type": "int64"
                                },
                                {
                                    "name": "name",
                                    "type": "string"
                                }
                            ]
                        }
                    },
                    {
                        "name": "startTime",
                        "type": "string"
                    },
                    {
                        "name": "team1Left",
                        "type": {
                            "struct": [
                                {
                                    "name": "active",
                                    "type": "bool"
                                },
                                {
                                    "name": "birthdate",
                                    "type": "string"
                                },
                                {
                                    "name": "brand",
                                    "type": {
                                        "struct": [
                                            {
                                                "name": "id",
                                                "type": "int64"
                                            },
                                            {
                                                "name": "logo",
                                                "type": "string"
                                            },
                                            {
                                                "name": "name",
                                                "type": "string"
                                            },
                                            {
                                                "name": "sponsorActive",
                                                "type": "bool"
                                            },
                                            {
                                                "name": "url",
                                                "type": "string"
                                            }
                                        ]
                                    }
                                },
                                {
                                    "name": "country",
                                    "type": "string"
                                },
                                {
                                    "name": "gender",
                                    "type": "string"
                                },
                                {
                                    "name": "hand",
                                    "type": "string"
                                },
                                {
                                    "name": "id",
                                    "type": "int64"
                                },
                                {
                                    "name": "image",
                                    "type": "string"
                                },
                                {
                                    "name": "name",
                                    "type": "string"
                                },
                                {
                                    "name": "nickname",
                                    "type": "string"
                                },
                                {
                                    "name": "preferSide",
                                    "type": "string"
                                },
                                {
                                    "name": "publicVisible",
                                    "type": "bool"
                                },
                                {
                                    "name": "racket",
                                    "type": "string"
                                },
                                {
                                    "name": "sponsor",
                                    "type": "string"
                                }
                            ]
                        }
                    },
                    {
                        "name": "team1Right",
                        "type": {
                            "struct": [
                                {
                                    "name": "active",
                                    "type": "bool"
                                },
                                {
                                    "name": "birthdate",
                                    "type": "string"
                                },
                                {
                                    "name": "brand",
                                    "type": {
                                        "struct": [
                                            {
                                                "name": "id",
                                                "type": "int64"
                                            },
                                            {
                                                "name": "logo",
                                                "type": "string"
                                            },
                                            {
                                                "name": "name",
                                                "type": "string"
                                            },
                                            {
                                                "name": "sponsorActive",
                                                "type": "bool"
                                            },
                                            {
                                                "name": "url",
                                                "type": "string"
                                            }
                                        ]
                                    }
                                },
                                {
                                    "name": "country",
                                    "type": "string"
                                },
                                {
                                    "name": "gender",
                                    "type": "string"
                                },
                                {
                                    "name": "hand",
                                    "type": "string"
                                },
                                {
                                    "name": "id",
                                    "type": "int64"
                                },
                                {
                                    "name": "image",
                                    "type": "string"
                                },
                                {
                                    "name": "name",
                                    "type": "string"
                                },
                                {
                                    "name": "nickname",
                                    "type": "string"
                                },
                                {
                                    "name": "preferSide",
                                    "type": "string"
                                },
                                {
                                    "name": "publicVisible",
                                    "type": "bool"
                                },
                                {
                                    "name": "racket",
                                    "type": "string"
                                },
                                {
                                    "name": "sponsor",
                                    "type": "string"
                                }
                            ]
                        }
                    },
                    {
                        "name": "team2Left",
                        "type": {
                            "struct": [
                                {
                                    "name": "active",
                                    "type": "bool"
                                },
                                {
                                    "name": "birthdate",
                                    "type": "string"
                                },
                                {
                                    "name": "brand",
                                    "type": {
                                        "struct": [
                                            {
                                                "name": "id",
                                                "type": "int64"
                                            },
                                            {
                                                "name": "logo",
                                                "type": "string"
                                            },
                                            {
                                                "name": "name",
                                                "type": "string"
                                            },
                                            {
                                                "name": "sponsorActive",
                                                "type": "bool"
                                            },
                                            {
                                                "name": "url",
                                                "type": "string"
                                            }
                                        ]
                                    }
                                },
                                {
                                    "name": "country",
                                    "type": "string"
                                },
                                {
                                    "name": "gender",
                                    "type": "string"
                                },
                                {
                                    "name": "hand",
                                    "type": "string"
                                },
                                {
                                    "name": "id",
                                    "type": "int64"
                                },
                                {
                                    "name": "image",
                                    "type": "string"
                                },
                                {
                                    "name": "name",
                                    "type": "string"
                                },
                                {
                                    "name": "nickname",
                                    "type": "string"
                                },
                                {
                                    "name": "preferSide",
                                    "type": "string"
                                },
                                {
                                    "name": "publicVisible",
                                    "type": "bool"
                                },
                                {
                                    "name": "racket",
                                    "type": "string"
                                },
                                {
                                    "name": "sponsor",
                                    "type": "string"
                                }
                            ]
                        }
                    },
                    {
                        "name": "team2Right",
                        "type": {
                            "struct": [
                                {
                                    "name": "active",
                                    "type": "bool"
                                },
                                {
                                    "name": "birthdate",
                                    "type": "string"
                                },
                                {
                                    "name": "brand",
                                    "type": {
                                        "struct": [
                                            {
                                                "name": "id",
                                                "type": "int64"
                                            },
                                            {
                                                "name": "logo",
                                                "type": "string"
                                            },
                                            {
                                                "name": "name",
                                                "type": "string"
                                            },
                                            {
                                                "name": "sponsorActive",
                                                "type": "bool"
                                            },
                                            {
                                                "name": "url",
                                                "type": "string"
                                            }
                                        ]
                                    }
                                },
                                {
                                    "name": "country",
                                    "type": "string"
                                },
                                {
                                    "name": "gender",
                                    "type": "string"
                                },
                                {
                                    "name": "hand",
                                    "type": "string"
                                },
                                {
                                    "name": "id",
                                    "type": "int64"
                                },
                                {
                                    "name": "image",
                                    "type": "string"
                                },
                                {
                                    "name": "name",
                                    "type": "string"
                                },
                                {
                                    "name": "nickname",
                                    "type": "string"
                                },
                                {
                                    "name": "preferSide",
                                    "type": "string"
                                },
                                {
                                    "name": "publicVisible",
                                    "type": "bool"
                                },
                                {
                                    "name": "racket",
                                    "type": "string"
                                },
                                {
                                    "name": "sponsor",
                                    "type": "string"
                                }
                            ]
                        }
                    },
                    {
                        "name": "tiebreak",
                        "type": "bool"
                    },
                    {
                        "name": "tournament",
                        "type": {
                            "struct": [
                                {
                                    "name": "category",
                                    "type": "string"
                                },
                                {
                                    "name": "description",
                                    "type": "string"
                                },
                                {
                                    "name": "endTime",
                                    "type": "string"
                                },
                                {
                                    "name": "goldenPoint",
                                    "type": "bool"
                                },
                                {
                                    "name": "id",
                                    "type": "int64"
                                },
                                {
                                    "name": "location",
                                    "type": "string"
                                },
                                {
                                    "name": "name",
                                    "type": "string"
                                },
                                {
                                    "name": "startTime",
                                    "type": "string"
                                },
                                {
                                    "name": "tiebreak",
                                    "type": "bool"
                                },
                                {
                                    "name": "tour",
                                    "type": "string"
                                }
                            ]
                        }
                    }
                ]
            }
        },
        {
            "name": "setNum",
            "type": "int64"
        },
        {
            "name": "teamStats",
            "type": {
                "struct": [
                    {
                        "name": "breakPointsAttempts",
                        "type": {
                            "struct": [
                                {
                                    "name": "team1",
                                    "type": "int64"
                                },
                                {
                                    "name": "team2",
                                    "type": "int64"
                                }
                            ]
                        }
                    },
                    {
                        "name": "breakPointsWon",
                        "type": {
                            "struct": [
                                {
                                    "name": "team1",
                                    "type": "int64"
                                },
                                {
                                    "name": "team2",
                                    "type": "int64"
                                }
                            ]
                        }
                    },
                    {
                        "name": "goldenPointsAgainst",
                        "type": {
                            "struct": [
                                {
                                    "name": "team1",
                                    "type": "int64"
                                },
                                {
                                    "name": "team2",
                                    "type": "int64"
                                }
                            ]
                        }
                    },
                    {
                        "name": "goldenPointsWon",
                        "type": {
                            "struct": [
                                {
                                    "name": "team1",
                                    "type": "int64"
                                },
                                {
                                    "name": "team2",
                                    "type": "int64"
                                }
                            ]
                        }
                    },
                    {
                        "name": "matchId",
                        "type": "int64"
                    },
                    {
                        "name": "pointsWon",
                        "type": {
                            "struct": [
                                {
                                    "name": "team1",
                                    "type": "int64"
                                },
                                {
                                    "name": "team2",
                                    "type": "int64"
                                }
                            ]
                        }
                    },
                    {
                        "name": "team1",
                        "type": "string"
                    },
                    {
                        "name": "team2",
                        "type": "string"
                    },
                    {
                        "name": "uErrors",
                        "type": {
                            "struct": [
                                {
                                    "name": "team1",
                                    "type": "int64"
                                },
                                {
                                    "name": "team2",
                                    "type": "int64"
                                }
                            ]
                        }
                    },
                    {
                        "name": "winners",
                        "type": {
                            "struct": [
                                {
                                    "name": "team1",
                                    "type": "int64"
                                },
                                {
                                    "name": "team2",
                                    "type": "int64"
                                }
                            ]
                        }
                    }
                ]
            }
        },
        {
            "name": "lastPointsStats",
            "type": {
                "struct": [
                    {
                        "name": "last10Points",
                        "type": {
                            "list": "int64"
                        }
                    },
                    {
                        "name": "lastPointNumShots",
                        "type": "int64"
                    },
                    {
                        "name": "longestPoint",
                        "type": "int64"
                    },
                    {
                        "name": "matchId",
                        "type": "int64"
                    },
                    {
                        "name": "rallyLengthAvg",
                        "type": "double"
                    }
                ]
            }
        },
        {
            "name": "playerStats",
            "type": {
                "struct": [
                    {
                        "name": "matchId",
                        "type": "int64"
                    },
                    {
                        "name": "team1Left",
                        "type": {
                            "struct": [
                                {
                                    "name": "additionalPi",
                                    "type": "int64"
                                },
                                {
                                    "name": "assists",
                                    "type": "int64"
                                },
                                {
                                    "name": "image",
                                    "type": "string"
                                },
                                {
                                    "name": "netRegains",
                                    "type": "int64"
                                },
                                {
                                    "name": "pErrors",
                                    "type": "int64"
                                },
                                {
                                    "name": "participation",
                                    "type": "double"
                                },
                                {
                                    "name": "pi",
                                    "type": "double"
                                },
                                {
                                    "name": "piHistory",
                                    "type": {
                                        "list": {
                                            "list": "double"
                                        }
                                    }
                                },
                                {
                                    "name": "piKp",
                                    "type": "double"
                                },
                                {
                                    "name": "player",
                                    "type": "string"
                                },
                                {
                                    "name": "returnTotal",
                                    "type": "int64"
                                },
                                {
                                    "name": "returnWon",
                                    "type": "int64"
                                },
                                {
                                    "name": "returnWonPercentage",
                                    "type": "double"
                                },
                                {
                                    "name": "rulos",
                                    "type": "int64"
                                },
                                {
                                    "name": "serverTotal",
                                    "type": "int64"
                                },
                                {
                                    "name": "serverWon",
                                    "type": "int64"
                                },
                                {
                                    "name": "serverWonPercentage",
                                    "type": "double"
                                },
                                {
                                    "name": "smashAttempts",
                                    "type": "int64"
                                },
                                {
                                    "name": "smashWinners",
                                    "type": "int64"
                                },
                                {
                                    "name": "touchs",
                                    "type": "int64"
                                },
                                {
                                    "name": "uErrors",
                                    "type": "int64"
                                },
                                {
                                    "name": "winners",
                                    "type": "int64"
                                }
                            ]
                        }
                    },
                    {
                        "name": "team1Right",
                        "type": {
                            "struct": [
                                {
                                    "name": "additionalPi",
                                    "type": "int64"
                                },
                                {
                                    "name": "assists",
                                    "type": "int64"
                                },
                                {
                                    "name": "image",
                                    "type": "string"
                                },
                                {
                                    "name": "netRegains",
                                    "type": "int64"
                                },
                                {
                                    "name": "pErrors",
                                    "type": "int64"
                                },
                                {
                                    "name": "participation",
                                    "type": "double"
                                },
                                {
                                    "name": "pi",
                                    "type": "double"
                                },
                                {
                                    "name": "piHistory",
                                    "type": {
                                        "list": {
                                            "list": "double"
                                        }
                                    }
                                },
                                {
                                    "name": "piKp",
                                    "type": "double"
                                },
                                {
                                    "name": "player",
                                    "type": "string"
                                },
                                {
                                    "name": "returnTotal",
                                    "type": "int64"
                                },
                                {
                                    "name": "returnWon",
                                    "type": "int64"
                                },
                                {
                                    "name": "returnWonPercentage",
                                    "type": "double"
                                },
                                {
                                    "name": "rulos",
                                    "type": "int64"
                                },
                                {
                                    "name": "serverTotal",
                                    "type": "int64"
                                },
                                {
                                    "name": "serverWon",
                                    "type": "int64"
                                },
                                {
                                    "name": "serverWonPercentage",
                                    "type": "double"
                                },
                                {
                                    "name": "smashAttempts",
                                    "type": "int64"
                                },
                                {
                                    "name": "smashWinners",
                                    "type": "int64"
                                },
                                {
                                    "name": "touchs",
                                    "type": "int64"
                                },
                                {
                                    "name": "uErrors",
                                    "type": "int64"
                                },
                                {
                                    "name": "winners",
                                    "type": "int64"
                                }
                            ]
                        }
                    },
                    {
                        "name": "team2Left",
                        "type": {
                            "struct": [
                                {
                                    "name": "additionalPi",
                                    "type": "int64"
                                },
                                {
                                    "name": "assists",
                                    "type": "int64"
                                },
                                {
                                    "name": "image",
                                    "type": "string"
                                },
                                {
                                    "name": "netRegains",
                                    "type": "int64"
                                },
                                {
                                    "name": "pErrors",
                                    "type": "int64"
                                },
                                {
                                    "name": "participation",
                                    "type": "double"
                                },
                                {
                                    "name": "pi",
                                    "type": "double"
                                },
                                {
                                    "name": "piHistory",
                                    "type": {
                                        "list": {
                                            "list": "double"
                                        }
                                    }
                                },
                                {
                                    "name": "piKp",
                                    "type": "double"
                                },
                                {
                                    "name": "player",
                                    "type": "string"
                                },
                                {
                                    "name": "returnTotal",
                                    "type": "int64"
                                },
                                {
                                    "name": "returnWon",
                                    "type": "int64"
                                },
                                {
                                    "name": "returnWonPercentage",
                                    "type": "double"
                                },
                                {
                                    "name": "rulos",
                                    "type": "int64"
                                },
                                {
                                    "name": "serverTotal",
                                    "type": "int64"
                                },
                                {
                                    "name": "serverWon",
                                    "type": "int64"
                                },
                                {
                                    "name": "serverWonPercentage",
                                    "type": "double"
                                },
                                {
                                    "name": "smashAttempts",
                                    "type": "int64"
                                },
                                {
                                    "name": "smashWinners",
                                    "type": "int64"
                                },
                                {
                                    "name": "touchs",
                                    "type": "int64"
                                },
                                {
                                    "name": "uErrors",
                                    "type": "int64"
                                },
                                {
                                    "name": "winners",
                                    "type": "int64"
                                }
                            ]
                        }
                    },
                    {
                        "name": "team2Right",
                        "type": {
                            "struct": [
                                {
                                    "name": "additionalPi",
                                    "type": "int64"
                                },
                                {
                                    "name": "assists",
                                    "type": "int64"
                                },
                                {
                                    "name": "image",
                                    "type": "string"
                                },
                                {
                                    "name": "netRegains",
                                    "type": "int64"
                                },
                                {
                                    "name": "pErrors",
                                    "type": "int64"
                                },
                                {
                                    "name": "participation",
                                    "type": "double"
                                },
                                {
                                    "name": "pi",
                                    "type": "double"
                                },
                                {
                                    "name": "piHistory",
                                    "type": {
                                        "list": {
                                            "list": "double"
                                        }
                                    }
                                },
                                {
                                    "name": "piKp",
                                    "type": "double"
                                },
                                {
                                    "name": "player",
                                    "type": "string"
                                },
                                {
                                    "name": "returnTotal",
                                    "type": "int64"
                                },
                                {
                                    "name": "returnWon",
                                    "type": "int64"
                                },
                                {
                                    "name": "returnWonPercentage",
                                    "type": "double"
                                },
                                {
                                    "name": "rulos",
                                    "type": "int64"
                                },
                                {
                                    "name": "serverTotal",
                                    "type": "int64"
                                },
                                {
                                    "name": "serverWon",
                                    "type": "int64"
                                },
                                {
                                    "name": "serverWonPercentage",
                                    "type": "double"
                                },
                                {
                                    "name": "smashAttempts",
                                    "type": "int64"
                                },
                                {
                                    "name": "smashWinners",
                                    "type": "int64"
                                },
                                {
                                    "name": "touchs",
                                    "type": "int64"
                                },
                                {
                                    "name": "uErrors",
                                    "type": "int64"
                                },
                                {
                                    "name": "winners",
                                    "type": "int64"
                                }
                            ]
                        }
                    }
                ]
            }
        }
    ]
}

matches_stats_team = {
    "fields": [
        {
            "name": "matchId",
            "type": "int64"
        },
        {
            "name": "team1",
            "type": "string"
        },
        {
            "name": "team2",
            "type": "string"
        },
        {
            "name": "pointsWon",
            "type": {
                "struct": [
                    {
                        "name": "team1",
                        "type": "int64"
                    },
                    {
                        "name": "team2",
                        "type": "int64"
                    }
                ]
            }
        },
        {
            "name": "breakPointsAttempts",
            "type": {
                "struct": [
                    {
                        "name": "team1",
                        "type": "int64"
                    },
                    {
                        "name": "team2",
                        "type": "int64"
                    }
                ]
            }
        },
        {
            "name": "breakPointsWon",
            "type": {
                "struct": [
                    {
                        "name": "team1",
                        "type": "int64"
                    },
                    {
                        "name": "team2",
                        "type": "int64"
                    }
                ]
            }
        },
        {
            "name": "goldenPointsAgainst",
            "type": {
                "struct": [
                    {
                        "name": "team1",
                        "type": "int64"
                    },
                    {
                        "name": "team2",
                        "type": "int64"
                    }
                ]
            }
        },
        {
            "name": "goldenPointsWon",
            "type": {
                "struct": [
                    {
                        "name": "team1",
                        "type": "int64"
                    },
                    {
                        "name": "team2",
                        "type": "int64"
                    }
                ]
            }
        },
        {
            "name": "winners",
            "type": {
                "struct": [
                    {
                        "name": "team1",
                        "type": "int64"
                    },
                    {
                        "name": "team2",
                        "type": "int64"
                    }
                ]
            }
        },
        {
            "name": "uErrors",
            "type": {
                "struct": [
                    {
                        "name": "team1",
                        "type": "int64"
                    },
                    {
                        "name": "team2",
                        "type": "int64"
                    }
                ]
            }
        }
    ]
}
