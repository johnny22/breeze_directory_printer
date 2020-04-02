from PIL import Image
import os

# This will edit all the photos in the INPUT_DIRECTORY and output a cropped and resized version to
# OUTPUT_DIRECTORY
#final width should be 250px
#final height should be 195px
CROP_RATIO = 10 
WIDTH = 1700
HEIGHT = 1326 
INPUT_DIRECTORY = "Images_from_office"
#INPUT_DIRECTORY = "Photo_work"
OUTPUT_DIRECTORY = "Resized_photos" 
pic_list = os.listdir(INPUT_DIRECTORY)
crop = False

def resize_photo(photo):
    """Receives PIL Image object, resizes, and returns."""
    new_photo = photo.resize((WIDTH, HEIGHT))
    return new_photo

def crop_photo_size(photo):
    """Receives PIL Image object and crops it."""
    width = photo.size[0]
    height = photo.size[1]
    new_width = width/CROP_RATIO 
    new_height = height/CROP_RATIO
    crop_tuple = (new_width, new_height, width-new_width, height-new_height)
    cropped_photo = photo.crop(crop_tuple)
    return cropped_photo
def crop_photo_aspect_only(photo):
    """Receives PIL Image object and crops the minimum amount to make the proper aspect."""
    width = photo.size[0]
    height = photo.size[1]+.0
    #print (photo.size, width/height)
    if width/height < 1.82:
        new_width = height*1.282
        diff = width - new_width
        crop_tuple = (diff/2, 0, new_width + diff/2, height)
        cropped = photo.crop(crop_tuple)
        return cropped
    
total = len(pic_list)
inc = 1
for picture in pic_list:
    print ('working on %d of %d.' % (inc, total))
    inc +=1
    in_path = os.path.abspath(INPUT_DIRECTORY + '/' + picture)
    out_path = os.path.abspath(INPUT_DIRECTORY + '/' + OUTPUT_DIRECTORY + '/')
    if not os.path.isdir(out_path):
        os.mkdir(out_path)
    if not os.path.isdir(in_path):
        photo = Image.open(in_path)
        photo = crop_photo_aspect_only(photo)
        new_photo = resize_photo(photo)
        new_photo.save(out_path + '/' + picture)
        if crop:
            #cropped = crop_photo_size(photo)
            aspect_cropped = crop_photo_aspect_only(photo)
            aspect_cropped.save(out_path + '/crop' + picture)





