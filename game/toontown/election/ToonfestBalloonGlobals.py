from direct.interval.IntervalGlobal import *
from otp.nametag.NametagConstants import *
from pandac.PandaModules import *
from random import choice

BalloonBasePosition = [274, -263, 25]
#BalloonElectionPosition = [166.5, 64.0, 53.0] #Not needed in ToonFest
BalloonScale = 1.2

# Let's define all of Alec's speeches.
# There should be exactly 12 phrases for each to fit with the sequence.
# If you add another, make sure to add it to SlappySpeechChoices.
SlappySpeech1 = [
    'Hey how\'s it going?',
    'Welp, Ryno made me do the balloon trip thing so now we\'re doing it.',
    "So.... Buff Shark.",
    'He\'s pretty cool.',
    'His Flex move is a little too powerful for my tastes, however.',
    'And he keeps using it more and more every time I do a Mint.',
    "AND I KEEP GOING FUCKING SAD!!",
    "...",
    "Just be careful around Buff Shark. And the Pencil Breaker.",
    "Anyway, teleport somewhere else or use ~collisionsOff to leave the top!"
]

# Now we need to take those phrases and pick one to use
SlappySpeechChoices = [SlappySpeech1]
SlappySpeeches = choice(SlappySpeechChoices)

# Number of balloon flight paths. Change if you add more below.
NumBalloonPaths = 1

def generateFlightPaths(balloon):
    # This is quite messy imo... but I didn't have much time to think about it.
    # For each sequence, you basically copy and paste this whole section and edit
    # the sequence. When you add a new sequence here, you MUST edit the 
    # SLAPPY_BALLOON_NUM_PATHS constant.
    flightPaths = []
    flightPaths.append(
        Sequence(
            # Lift Off
            Wait(0.5),
            balloon.balloon.posHprInterval(1.5, Point3(232, -262, 27), (0, 2, 2)),
            balloon.balloon.posHprInterval(1.5, Point3(170, -252, 32), (0, -2, -2)),
            balloon.balloon.posHprInterval(8.0, Point3(178, -189, 37), (0, 0, 0)),
            balloon.balloon.posHprInterval(6.5, Point3(241, -146, 45), (5, 2, 2)),

            # To the tunnel we go
            balloon.balloon.posHprInterval(11.0, Point3(259, -95, 67), (180, -2, -2)),
            balloon.balloon.posHprInterval(5.5, Point3(252, -100, 95), (175, -4, 0)),

            # Lets drop a weight on the gag shop
            balloon.balloon.posHprInterval(10.0, Point3(204, -125, 110), (0, 2, -2)),
            balloon.balloon.posHprInterval(4.5, Point3(182, -141, 140), (-2, -2, 2)), 

            # Rats, we missed! Lets checkout the podium
            balloon.balloon.posHprInterval(21.5, Point3(198, -141, 175), (-70, 0, 0)),

            # Set her down; gently
            balloon.balloon.posHprInterval(15.0, Point3(196, -141, 205), (-25, 0, 0)),
            #Wait(5),
            #balloon.balloon.posHprInterval(15.0, Point3(274, -263, 25), (0, 0, 0)),
        )
    )

    # Return the flight paths back to the HotAirBalloon...
    return flightPaths

def generateToonFlightPaths(balloon):
    # This isn't all that great of a solution, but it stops jittering caused when we reparent the client to the balloon.
    # The downside is that it causes some minor latency for others, but not enough to care.
    toonFlightPaths = []
    toonFlightPaths.append(
        Sequence(
            # Lift Off
            Wait(0.5),
            base.localAvatar.posInterval(1.5, Point3(232, -262, 27)),
            base.localAvatar.posInterval(1.5, Point3(170, -252, 32)),
            base.localAvatar.posInterval(8.0, Point3(178, -189, 37)),
            base.localAvatar.posInterval(6.5, Point3(241, -146, 45)),

            # To the tunnel we go
            base.localAvatar.posInterval(11.0, Point3(259, -95, 67)),
            base.localAvatar.posInterval(5.5, Point3(252, -100, 95)),

            # Lets drop a weight on the gag shop
            base.localAvatar.posInterval(10.0, Point3(204, -125, 110)),
            base.localAvatar.posInterval(4.5, Point3(182, -141, 140)), 

            # Rats, we missed! Lets checkout the podium
            base.localAvatar.posInterval(21.5, Point3(198, -141, 175)),

            # Set her down; gently
            base.localAvatar.posInterval(15.0, Point3(196, -141, 205)),
        )
    )

    return toonFlightPaths

def generateSpeechSequence(balloon):
    # This is the interval for Slappy's phrases to say throughout the flight.
    # It shouldn't really be edited. Instead, add more phrases above with SlappySpeechX and SlappySpeechChoices.
    speechSequence = Sequence(
        Func(balloon.alec.setChatAbsolute, SlappySpeeches[0], CFSpeech | CFTimeout),
        Wait(9.5),
        Func(balloon.alec.setChatAbsolute, SlappySpeeches[1], CFSpeech | CFTimeout),
        Wait(9.5),
        Func(balloon.alec.setChatAbsolute, SlappySpeeches[2], CFSpeech | CFTimeout),
        Wait(9.5),
        Func(balloon.alec.setChatAbsolute, SlappySpeeches[3], CFSpeech | CFTimeout),
        Wait(9.5),
        Func(balloon.alec.setChatAbsolute, SlappySpeeches[4], CFSpeech | CFTimeout),
        Wait(9.5),
        Func(balloon.alec.setChatAbsolute, SlappySpeeches[5], CFSpeech | CFTimeout),
        Wait(9.5),
        Func(balloon.alec.setChatAbsolute, SlappySpeeches[6], CFSpeech | CFTimeout),
        Wait(9.5),
        Func(balloon.alec.setChatAbsolute, SlappySpeeches[7], CFSpeech | CFTimeout),
        Wait(9.5),
        Func(balloon.alec.setChatAbsolute, SlappySpeeches[8], CFSpeech | CFTimeout),
        Wait(9.5),
        Func(balloon.alec.setChatAbsolute, SlappySpeeches[9], CFSpeech | CFTimeout)
    )

    # Return the sequence back to the balloon to run
    return speechSequence
