from FidoSelf import client

def check_cmd(text):
    commands = client.DB.get_key("SELFCOMMANDS") or []
    for command in commands:
        search = re.search(command, text)
        if search:
            return True
    return False