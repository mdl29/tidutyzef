"""some error codes for the game"""

USERNAME_NOT_SET = {"object": "error", "errorCode" : 0,
                    "desc": "You should have an username and a team before any operation"}
TEAM_ERROR = {"object": "error", "errorCode" : 1,
              "desc": "this team doesn't exist"}
USERNAME_ALREADY_IN_USE = {"object": "error", "errorCode" : 2,
                           "desc": "username already in use in your team"}
JSON_ERROR = {"object": "error", "errorCode" : 3,
              "desc": "the JSON can't be load"}
UNKNOW_OBJECT = {"object": "error", "errorCode" : 4,
                 "desc": "the object is not set or isn't recognized"}
USERNAME_ALREADY_SET = {"object": "error", "errorCode" : 5,
                        "desc": "you can't change your username"}
