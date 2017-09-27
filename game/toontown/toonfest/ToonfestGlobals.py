from direct.interval.IntervalGlobal import *
from otp.nametag.NametagConstants import *
from pandac.PandaModules import *
from random import choice
StandPieTypeAmount = [4, 20, 1]
Cog1PopupPoints = [[(218.4, -101.0, 8.5), -20],
 [(185.4, -266.7, 5.25), 113],
 [(294.7, -254.2, 27.7), 90],
 [(303.1, -546.9, 1.0), 26],
 [(121.6, 17.0, 4.7), -147]]
Cog2PopupPoints = [[(84.8, -240, 6.6), -265],
 [(392.5, -106.1, 9.7), -90],
 [(265.2, -312.4, 31.5), 190],
 [(33.0, -333.8, 8.4), 260],
 [(143.0, -155.8, 4.7), 0]]
Cog3PopupPoints = [[(337.4, 11.4, 9.7), 141],
 [(69.5, -88.1, 14.6), -80],
 [(158.0, -490.5, 1.0), -64],
 [(239.1, -404.8, 8.4), -350],
 [(-200.4, -95.5, 12.0), -227]]
CogHolePopupPoints = list(Cog1PopupPoints + Cog2PopupPoints + Cog3PopupPoints)
DaytimeCycle = 2400
NighttimeCycle = 1200
TrampolinePoints = [(100, -257, 4.6, -55),
 (202, -211, 4.6, 33),
 (340, -157, 9.8, 77),
 (186, 63, 4.5, 90),
 (169, -440, 0.94, 253),
 (43, 20, 21.1, -147)]
CannonPoints = [(122, -226, 5.2, 322, 0, 5),
 (42, -50, 20.3, -63, -5, 0),
 (117, 64, 10.3, 212, -8, -1),
 (286, 46, 4.5, 165, 0, 0),
 (313, -247, 28.9, 23, 0, 0),
 (367, -29, 27, 90, 10, 0)]
BalloonBaseProperties = [(285, -272, 25), -90, 1.0]
BalloonTowerProperties = [LPoint3f(212, -23, 207), 370, 1.0]
SlappySpeech1 = ['No, no! Blargghh, not another.',
 "I don't mean to offend very much -- I'm just not a fan of rides. ",
 '...or balloons...',
 '...or...heights...',
 'AHH! -- Sorry, just looked down.',
 "I didn't really volunteer for the job you see, it's just that...",
 'Well, you know what happened.',
 'Flippy insisted on having a balloon here in his memory.',
 "Oh boy, we're here. Looks like I get to go back down.",
 "Just press the ToonFest Teleport Button when you're ready to come back down!"]
SlappySpeech2 = ['Need a lift?',
 "I actually wouldn't recommend it.",
 'Say, do you know how many Toons go sad from balloon crashes each year?',
 "One. There's actually only been one. And he didn't really go sad from a crash.",
 'He worked with balloons though. So that counts.',
 "I've happened to notice that you haven't asked me to take you back down to the ground yet!",
 "I mean seriously, I'm telling you straightforward: We're not going to survive this ride.",
 "Listen, I didn't want to do this, but we're too high. This is just too high. For your own safety I'm taking us back--",
 "Oh, we're here. You know, that was just as bad as anticipated, and now I get to relive it all again. Hooray!",
 "Just press the ToonFest Teleport Button when you're ready to come back down!"]
SlappySpeech3 = ['Heeeeellllllooooo!',
 'Despite my serendipitous exclamation, I must inform you that I am actually quite terrified!',
 "Balloon rides aren't exactly my forte. I'm all about voting.",
 'Preferably votes that stay on the ground.',
 'You know, I could have been a Fisherman too. Great scenery. Slimey fish.',
 "On second thought, I couldn't handle fishing. Slime doesn't work well with my gloves.",
 'If they had an official ToonFest counter though? Oh man, that would be the dream.',
 "But no, instead I'm up here in the balloon.",
 "That's the last time I put my name into a ballot! No, just kidding. I love ballots.",
 "Just press the ToonFest Teleport Button when you're ready to come back down!"]
SlappySpeech5 = ['Another balloon ride. Just what my day needed!',
 'That was complete sarcasm, too. I actually have a mortal fear of heights.',
 "I've been living my nightmares all day today!",
 "I must say though, this ride isn't so bad yet. At least I'm not alone!",
 'You can see a lot from up here, actually. The mine, the mountains -- is that... A castle?',
 'Flippy really is going all out with the construction projects.',
 "WI can't say I like the color scheme though.",
 "Wowee, this is great! I'm actually pretty excited to head--",
 "Hang on - you're getting off here? No, you can't just leave me all the way up here!",
 "Just press the ToonFest Teleport Button when you're ready to come back down. Don't mind me, I'll just float here panicing!"]
SlappySpeechChoices = [SlappySpeech1,
 SlappySpeech2,
 SlappySpeech3,
 SlappySpeech5]
SlappySpeeches = choice(SlappySpeechChoices)
NumBalloonPaths = 1

def generateFlightPaths(balloon):
    flightPaths = []
    flightPaths.append(Sequence(Wait(0.5), balloon.balloon.posHprInterval(3.0, Point3(295, -265, 30), (-80, 2, 2), blendType='easeIn'), balloon.balloon.posHprInterval(10.0, Point3(310, -172, 55), (0, 0, 0)), balloon.balloon.posHprInterval(10.0, Point3(315, -64, 117), (50, 2, 2)), balloon.balloon.posHprInterval(16.0, Point3(302, 20, 160), (360, -2, 0)), balloon.balloon.posHprInterval(7.5, Point3(280, 55, 187), (390, 1, 2)), balloon.balloon.posHprInterval(8.0, Point3(210, -2, 210), (380, 1, 2)), balloon.balloon.posHprInterval(3.0, Point3(212, -23, 207), (370, 0, 0), blendType='easeOut')))
    return flightPaths


def generateToonFlightPaths(balloon):
    toonFlightPaths = []
    toonFlightPaths.append(Sequence(Wait(0.5), base.localAvatar.posInterval(3.0, Point3(295, -265, 30.3), blendType='easeIn'), base.localAvatar.posInterval(10.0, Point3(310, -172, 55.3)), base.localAvatar.posInterval(10.0, Point3(315, -64, 117.3)), base.localAvatar.posInterval(16.0, Point3(302, 20, 160.3)), base.localAvatar.posInterval(7.5, Point3(280, 55, 187.3)), base.localAvatar.posInterval(8.0, Point3(210, -2, 210.3)), base.localAvatar.posInterval(3.0, Point3(212, -23, 207.3), blendType='easeOut')))
    return toonFlightPaths


def generateSpeechSequence(balloon):
    speechSequence = Sequence(Func(balloon.driver.setChatAbsolute, SlappySpeeches[0], CFSpeech | CFTimeout), Wait(4), Func(balloon.driver.setChatAbsolute, SlappySpeeches[1], CFSpeech | CFTimeout), Wait(6), Func(balloon.driver.setChatAbsolute, SlappySpeeches[2], CFSpeech | CFTimeout), Wait(4), Func(balloon.driver.setChatAbsolute, SlappySpeeches[3], CFSpeech | CFTimeout), Wait(6), Func(balloon.driver.setChatAbsolute, SlappySpeeches[4], CFSpeech | CFTimeout), Wait(10), Func(balloon.driver.setChatAbsolute, SlappySpeeches[5], CFSpeech | CFTimeout), Wait(6), Func(balloon.driver.setChatAbsolute, SlappySpeeches[6], CFSpeech | CFTimeout), Wait(10), Func(balloon.driver.setChatAbsolute, SlappySpeeches[7], CFSpeech | CFTimeout), Wait(6), Func(balloon.driver.setChatAbsolute, SlappySpeeches[8], CFSpeech | CFTimeout), Wait(7), Func(balloon.driver.setChatAbsolute, SlappySpeeches[9], CFSpeech | CFTimeout))
    return speechSequence
