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


def read_emoji_file(path='emojiGamutPartitioned.json'):
    with open(path) as json_file:
        emojiDict = json.load(json_file)

    colors, emojis = [], []
    for batch in emojiDict:
        for *color, emoji in batch:
            colors.append(np.array(color))
            emojis.append(emoji)

    return [np.array(x) for x in (colors, emojis)]


def downscale_image(img: Image.Image, coeff) -> np.ndarray:
    size = np.array(img.size)
    new_size = np.round(size / coeff).astype(int)
    return np.array(img.resize(new_size))


def runConversion(webcam=1, video=0, toFile=0, downscale=20,
                  srcFile="default.png", outfile="emojiRender.txt"):
    colors, emojis = read_emoji_file()
    knn = KNeighborsClassifier(n_neighbors=1)
    knn.fit(X=colors, y=np.arange(len(colors)))

    if webcam:
        vs = VideoStream
        vs(src=0).start()
        if video:
            timeCount = []
            try:
                while True:
                    timex = time.time()
                    image = Image.fromarray(vs(src=0).read().astype('uint8'))
                    image = downscale_image(image, downscale)
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
        image = downscale_image(Image.open(srcFile), downscale)
        image = convertImage(knn, emojis, image)
        if toFile:
            writeFile(image, outfile)
        else:
            print(image)


if __name__ == '__main__':
    runConversion(webcam=1, video=1, downscale=30)
