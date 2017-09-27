ThoughtPrefix = '.'

def isThought(message):
    return message and message.startswith(ThoughtPrefix)

def removeThoughtPrefix(message):
    if isThought(message):
        return message[len(ThoughtPrefix):]
    else:
        return message

def findAvatarName(id):
    info = base.cr.identifyAvatar(id)

    return info.getName() if info else ''
