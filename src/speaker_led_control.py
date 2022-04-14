import vlc
import time
import RPi.GPIO as GPIO

'''
Run this script on RPi 2. This script will read the detected gesture from RPi 1 over GPIO.
It will then send the corresponding commands to the speaker and LED.

The plist variable must contain the names of all the songs in the songs folder.
If the name of the song is not in plist, then it will not be available to play.
'''


GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)  # numbering scheme

GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(27, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(22, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(24, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(4, GPIO.OUT)
GPIO.setup(5, GPIO.OUT)
GPIO.setup(6, GPIO.OUT)


# playlist of songs
plist = ['howLong.mp3', 'godIsAWoman.mp3', 'tillTheWorldEnds.mp3']
songIndex = 0
playlistLength = len(plist)

# play the first song
player = vlc.MediaPlayer(plist[0])
player.audio_set_volume(40)
player.play()

go = True


def volume_up(channel):
    print("up")
    # raise volume
    # if already at max volume, do nothing
    if player.audio_get_volume() < 100:
        player.audio_set_volume(player.audio_get_volume() + 20)
        GPIO.output(5, GPIO.HIGH)
        GPIO.output(4, GPIO.LOW)
        GPIO.output(6, GPIO.LOW)
        time.sleep(2)
        GPIO.output(4, GPIO.LOW)
        GPIO.output(5, GPIO.LOW)
        GPIO.output(6, GPIO.LOW)


def volume_down(channel):
    print("down")
    # lower volume
    # if already at min volume, do nothing
    if player.audio_get_volume() > 0:
        player.audio_set_volume(player.audio_get_volume() - 20)
        GPIO.output(4, GPIO.HIGH)
        GPIO.output(5, GPIO.LOW)
        GPIO.output(6, GPIO.LOW)
        time.sleep(2)
        GPIO.output(4, GPIO.LOW)
        GPIO.output(5, GPIO.LOW)
        GPIO.output(6, GPIO.LOW)


def play_pause(channel):
    print("pause")
    global go

    # turn off
    if(go):
        player.pause()
        go = False
        GPIO.output(6, GPIO.HIGH)
        GPIO.output(4, GPIO.LOW)
        GPIO.output(5, GPIO.LOW)
        time.sleep(2)
        GPIO.output(4, GPIO.LOW)
        GPIO.output(5, GPIO.LOW)
        GPIO.output(6, GPIO.LOW)
    else:
        player.play()
        go = True
        GPIO.output(6, GPIO.HIGH)
        GPIO.output(4, GPIO.LOW)
        GPIO.output(5, GPIO.LOW)
        time.sleep(2)
        GPIO.output(4, GPIO.LOW)
        GPIO.output(5, GPIO.LOW)
        GPIO.output(6, GPIO.LOW)


def next_song(channel):
    print("next")
    global player
    global songIndex
    # if at last song in playlist, go to beginning
    if songIndex == playlistLength - 1:
        currentVol = player.audio_get_volume()
        player.pause()
        player = vlc.MediaPlayer(plist[0])
        player.audio_set_volume(currentVol)
        player.play()
        songIndex = 0
        GPIO.output(5, GPIO.HIGH)
        GPIO.output(4, GPIO.LOW)
        GPIO.output(6, GPIO.HIGH)
        time.sleep(2)
        GPIO.output(4, GPIO.LOW)
        GPIO.output(5, GPIO.LOW)
        GPIO.output(6, GPIO.LOW)
    else:
        currentVol = player.audio_get_volume()
        player.pause()
        player = vlc.MediaPlayer(plist[songIndex + 1])
        player.audio_set_volume(currentVol)
        player.play()
        songIndex = songIndex + 1
        GPIO.output(5, GPIO.HIGH)
        GPIO.output(4, GPIO.LOW)
        GPIO.output(6, GPIO.HIGH)
        time.sleep(2)
        GPIO.output(4, GPIO.LOW)
        GPIO.output(5, GPIO.LOW)
        GPIO.output(6, GPIO.LOW)


def prev_song(channel):
    print("prev")
    global player
    global songIndex
    # if at first song in playlist, go to end
    if songIndex == 0:
        currentVol = player.audio_get_volume()
        player.pause()
        player = vlc.MediaPlayer(plist[playlistLength - 1])
        player.audio_set_volume(currentVol)
        player.play()
        songIndex = playlistLength - 1
        GPIO.output(4, GPIO.HIGH)
        GPIO.output(5, GPIO.LOW)
        GPIO.output(6, GPIO.HIGH)
        time.sleep(2)
        GPIO.output(4, GPIO.LOW)
        GPIO.output(5, GPIO.LOW)
        GPIO.output(6, GPIO.LOW)
    else:
        currentVol = player.audio_get_volume()
        player.pause()
        player = vlc.MediaPlayer(plist[songIndex - 1])
        player.audio_set_volume(currentVol)
        player.play()
        songIndex = songIndex - 1
        GPIO.output(4, GPIO.HIGH)
        GPIO.output(5, GPIO.LOW)
        GPIO.output(6, GPIO.HIGH)
        time.sleep(2)
        GPIO.output(4, GPIO.LOW)
        GPIO.output(5, GPIO.LOW)
        GPIO.output(6, GPIO.LOW)


GPIO.add_event_detect(22, GPIO.FALLING, callback=volume_up)
GPIO.add_event_detect(27, GPIO.FALLING, callback=volume_down)
GPIO.add_event_detect(17, GPIO.FALLING, callback=play_pause)
GPIO.add_event_detect(23, GPIO.FALLING, callback=next_song)
GPIO.add_event_detect(24, GPIO.FALLING, callback=prev_song)


# infinite loop
while True:
    """do nothing"""
