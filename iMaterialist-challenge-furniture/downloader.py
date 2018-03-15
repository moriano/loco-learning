
import json
import requests
import concurrent.futures
import shutil
import os
train_raw = json.load(open('train.json'))

len(train_raw["annotations"])


def read_json(file_name):
    raw = json.load(open(file_name))
    images = raw["images"]
    annotations = raw["annotations"]
    
    results = {} # Key is label_id, value is a list of urls 
    
    image_id_to_label_id = {}
    for annotation_dict in annotations:
        label_id = annotation_dict["label_id"]
        this_image_id = annotation_dict["image_id"]
        results[label_id] = []
        image_id_to_label_id[this_image_id] = label_id
    
    for image_dict in images:        
        image_id = image_dict["image_id"]
        url = image_dict["url"]
        
        this_label_id = image_id_to_label_id[image_id]
        results[this_label_id] += url

    
    
    
    return results

results = read_json("train.json")


total_samples = 0
for label_id, images in results.items():
    total_samples += len(images)
    print(label_id, " has ", len(images), " examples")


def download_image(image, label_id, path_prefix="train/", msg = None):
    if msg:
        print(msg)
    request = requests.get(image, stream=True, headers={'Connection':'close'})
    if request.status_code == 200:
        
        dir_to_download = path_prefix + str(label_id) + "/"
        os.makedirs(dir_to_download,  exist_ok=True)
        path = dir_to_download + image.split("/")[-1]
        with open(path, 'wb') as f:
            request.raw.decode_content = True
            shutil.copyfileobj(request.raw, f)  
    else:
        print("Bummer! could not get image", image)



images_to_go = total_samples
with concurrent.futures.ThreadPoolExecutor(max_workers=50) as e:
    for label_id, images in results.items():
        for image in images:
            images_to_go -=1
            msg = None
            if images_to_go % 500 == 0:
                msg = "%d images to go" % images_to_go

            e.submit(download_image, image, label_id, msg=msg)
