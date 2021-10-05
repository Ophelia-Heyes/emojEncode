# emojEncode 🖥️

This script takes a variety of image inputs and outputs and emoji representation.

To use, import **emojencoder.py** and use the function **emojencoder.runConversion()**

## runConversion ✨

The main function, **runConversion**, takes input from either an image file or a webcam feed. Currently, it can only accept video from the webcam, not from video files.

  ### Arguments:

  ### webcam 🕸️
  Set to **True** to use a webcam feed as input. If **False**, it will use a source file instead. Defaults to **True**.

  ### video 📹
  Set to **True** to output a video stream from the webcam. When using video mode, the only output are terminal prints for each frame. Defaults to **False**.

  ### toFile 🗄️
  Set to **True** to output to a file. If **False**, it will print the output to the terminal instead. Defaults to **False**.

  ### downscale ↕️
  This is the integer with which to divide the source resolution. Set to 1 to output at the original image resolution. It's recomended to keep this number higher, especially when rendering video, as the conversion takes a lot of processing time. Defaults to **20**

  ### srcFile ℹ️
  The source image filename to be converted, if not using the webcam feature. It will accept any three channel RGB image.

  ### outfile 🥧
  The filename to write to if not outputting the emojis to the terminal. The default is **"emojiRender.txt"**

