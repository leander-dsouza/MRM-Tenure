import base64
image = open(r'/home/leander/Desktop/tennis.jpg', 'rb')
image_read = image.read()
image_64_encode = base64.encodestring(image_read)
image_64_decode = base64.decodestring(image_64_encode)
image_result = open(r'/home/leander/Desktop/tennis2decoded.jpg', 'wb') # create a writable image and write the decoding result
image_result.write(image_64_decode)
