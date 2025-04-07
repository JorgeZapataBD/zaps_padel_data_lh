matches = {
    "fields": [
        {
            "name": "id",
            "type": "int64"
        },
        {
            "name": "self",
            "type": "string"
        },
        {
            "name": "name",
            "type": "string"
        },
        {
            "name": "round",
            "type": "int64"
        },
        {
            "name": "score",
            "type": {
                "list": {
                    "struct": [
                        {
                            "name": "team_1",
                            "type": "int64"
                        },
                        {
                            "name": "team_2",
                            "type": "int64"
                        }
                    ]
                }
            }
        },
        {
            "name": "played_at",
            "type": "string"
        },
        {
            "name": "category",
            "type": "string"
        },
        {
            "name": "duration",
            "type": "string"
        },
        {
            "name": "court",
            "type": "string"
        },
        {
            "name": "connections",
            "type": {
                "struct": [
                    {
                        "name": "players",
                        "type": "string"
                    },
                    {
                        "name": "stats",
                        "type": "string"
                    },
                    {
                        "name": "tournament",
                        "type": "string"
                    }
                ]
            }
        }
    ]
}

players = {
    "fields": [
        {
            "name": "id",
            "type": "int64"
        },
        {
            "name": "self",
            "type": "string"
        },
        {
            "name": "name",
            "type": "string"
        },
        {
            "name": "url",
            "type": "string"
        },
        {
            "name": "ranking",
            "type": "string"
        },
        {
            "name": "points",
            "type": "int64"
        },
        {
            "name": "height",
            "type": "int64"
        },
        {
            "name": "nationality",
            "type": "string"
        },
        {
            "name": "birthplace",
            "type": "string"
        },
        {
            "name": "birthdate",
            "type": "string"
        },
        {
            "name": "market_value",
            "type": "string"
        },
        {
            "name": "hand",
            "type": "string"
        },
        {
            "name": "side",
            "type": "string"
        },
        {
            "name": "connections",
            "type": {
                "struct": [
                    {
                        "name": "matches",
                        "type": "string"
                    }
                ]
            }
        }
    ]
}

seasons_tournaments = {
    "fields": [
        {
            "name": "id",
            "type": "int64"
        },
        {
            "name": "self",
            "type": "string"
        },
        {
            "name": "name",
            "type": "string"
        },
        {
            "name": "url",
            "type": "string"
        },
        {
            "name": "location",
            "type": "string"
        },
        {
            "name": "country",
            "type": "string"
        },
        {
            "name": "level",
            "type": "string"
        },
        {
            "name": "status",
            "type": "string"
        },
        {
            "name": "start_date",
            "type": "string"
        },
        {
            "name": "end_date",
            "type": "string"
        },
        {
            "name": "connections",
            "type": {
                "struct": [
                    {
                        "name": "matches",
                        "type": "string"
                    },
                    {
                        "name": "season",
                        "type": "string"
                    }
                ]
            }
        }
    ]
}
