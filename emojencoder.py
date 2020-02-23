import json
import time

import numpy as np
from PIL import Image
from imutils.video import VideoStream
from sklearn.neighbors import KNeighborsClassifier


def writeFile(image, filename="emojiRender.txt"):
    '''Write text to file'''
    with open(filename, "w") as out:
        out.write(image)


def convertImage(knn, emojis, image):
    shape = image.shape[:2]
    pixels = image.reshape(-1, 3)
    indices = knn.predict(pixels).astype(int)
    result = emojis[indices].reshape(shape)
    return '\n'.join(['\u2009'.join(line) for line in result])


def get_knn(colors):
    knn = KNeighborsClassifier(n_neighbors=1)
    knn.fit(X=colors, y=np.arange(len(colors)))
    return knn


def runConversion(webcam=1, video=0, toFile=0, downscale=20,
                  dictFile='emojiGamutPartitioned.json',
                  srcFile="default.png", outfile="emojiRender.txt"):
    '''Parses options for emoji conversion.'''
    with open(dictFile) as json_file:
        emojiDict = json.load(json_file)

    colors, emojis = [], []
    for batch in emojiDict:
        for *color, emoji in batch:
            colors.append(np.array(color))
            emojis.append(emoji)

    valid_colors = np.array(colors)
    emojis = np.array(emojis)
    knn = get_knn(valid_colors)
    if webcam:
        vs = VideoStream
        vs(src=0).start()
        if video:
            timeCount = []
            try:
                while True:
                    timex = time.time()
                    image = vs(src=0).read().astype(int)[::downscale, ::downscale]
                    print(convertImage(knn, emojis, image))
                    timeCount += [time.time() - timex]
                    print(sum(timeCount) / len(timeCount))
            except KeyboardInterrupt:
                print(sum(timeCount) / len(timeCount))
        else:
            image = (vs(src=0).read().astype(int))[::downscale, ::downscale]
            image = convertImage(knn, emojis, image)
            if toFile:
                writeFile(image, outfile)
            else:
                print(image)
        vs(src=0).stop()
    else:
        image = np.array(Image.open(srcFile))[::downscale, ::downscale][:, :, ::-1]
        image = convertImage(knn, emojis, image)
        if toFile:
            writeFile(image, outfile)
        else:
            print(image)


if __name__ == '__main__':
    runConversion(webcam=1, video=1, downscale=30)