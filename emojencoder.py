import json
import time
import numpy as np
from numpy import mean
from PIL import Image
from imutils.video import VideoStream


def nearestColor(subjects, query):
    '''finds nearest matching color to query color
       from a given dictionary of colors'''
    return subjects[min(subjects,
                    key=lambda subject: sum((s - q) * (s - q) for s,
                                            q in zip(subject, query)))]


def writeFile(image, filename="emojiRender.txt"):
    '''Write text to file'''
    file = open(filename, "w")
    file.write(image)
    file.close()


def convertImage(emojiDict, part, image):
    '''Returns an emoji representation for a given '''
    asc = [[nearestColor(emojiDict[int(mean(px)//part)],
                         tuple(px))[-1] for px in lin][::-1] for lin in image]
    return '\n'.join(['\u2009'.join(line) for line in asc])


def runConversion(webcam=1, video=0, toFile=0, downscale=20,
                  dictFile='emojiGamutPartitioned.json',
                  srcFile="default.png", outfile="emojiRender.txt"):
    '''Parses options for emoji conversion.'''
    with open(dictFile) as json_file:
        emojiDict = json.load(json_file)
    emojiDict = [dict(zip([tuple(x[0:3]) for x in y],
                          [x[3] for x in y])) for y in emojiDict]
    part = 256/len(emojiDict)
    if webcam:
        vs = VideoStream
        vs(src=0).start()
        if video:
            try:
                timeCount = []
                while True:
                    timex = time.time()
                    image = vs(src=0).read().astype(int)[::downscale,
                                                         ::downscale]
                    print(convertImage(emojiDict, part, image,))
                    timeCount += [time.time()-timex]
                    print(sum(timeCount)/len(timeCount))
            except KeyboardInterrupt:
                pass
        else:
            image = (vs(src=0).read().astype(int))[::downscale, ::downscale]
            image = convertImage(emojiDict, part, image)
            if toFile:
                writeFile(image, outfile)
            else:
                print(image)
        vs(src=0).stop()
    else:
        image = np.array(Image.open(srcFile))[::downscale,
                                              ::downscale][:, :, ::-1]
        image = convertImage(emojiDict, part, image)
        if toFile:
            writeFile(image, outfile)
        else:
            print(image)


if __name__ == '__main__':
    runConversion(webcam=1, video=0, downscale=20)
