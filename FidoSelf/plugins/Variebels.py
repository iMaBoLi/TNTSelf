from FidoSelf import client

VARIEBELS = {
    "TIME": "Use For Replace With Time String ( Ex: 23:59 )",
    "DATE": "Use For Replace With Date String ( Ex: 2222/22/22 )",
    "HEART": "Use For Replace With Random Heart ( Ex: ❤️ )",
    "FIRSTNAME": "Use For Replace With First Name Of User",
    "MENTION": "Use For Replace With Mention Of User",
    "USERNAME": "Use For Replace With Username Of User",
    "TITLE": "Use For Replace With Chat Title",
    "CHATUSERNAME": "Use For Replace With Chat Username",
    "COUNT": "Use For Replace With Chat Members Count",
}

for Var in VARIEBELS:
    __INFO__ = {
        "Category": "Variebels",
        "Name": Var,
        "Info": {
            "Help": "The Variebel For Use In Messages And ...",
            "Commands": {
                Var: {
                    "Help": VARS[Var],
                },
            },
        },
    }
    client.functions.AddInfo(__INFO__)