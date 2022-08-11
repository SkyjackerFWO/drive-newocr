import os
import json


#path = os.path.expanduser('./image')
path_image = "./train_images"
path_label = "./label"
train_list = "./train_list.txt"
FJoin = os.path.join


def GetFiles(path):
    """Output: file_list là danh sách tất cả các file trong path và trong tất cả các
       thư mục con bên trong nó. dir_list là danh sách tất cả các thư mục con
       của nó. Các output đều chứa đường dẫn đầy đủ."""

    folder_file, files, dir_list = [], [], []
    for dir, subdirs, files in os.walk(path):
        # print("dir ",dir)
        folder_file.extend([FJoin(dir, f) for f in files])
        files.extend([f for f in files])
        dir_list.extend([FJoin(dir, d) for d in subdirs])
    return folder_file, files, dir_list


def GetLabels(path):
    folder_files, files, _ = GetFiles(path)
    train_gts = "./train_gts"
    if not os.path.exists(train_gts):
        os.makedirs(train_gts)
    for folder_file in folder_files:
        with open(folder_file, 'r') as f:
            data = json.load(f)
        file_name = folder_file.lstrip(path)
        path_file_gts = train_gts+'/'+file_name.rstrip("json")+("png.txt")
        mainline = ""
        for element in data:
            box = element['box']
            """
            Ground truth cua repo DB yeu cau 8 elment tuong ung voi x1,y1,x2,y2,x3,y3,x4,y4 (A -> B -> C -> D)
            Ground truth cua VinAi cho 4 elment x1,y1,x3,y3 (A va C)
            The nen ta phai tinh chinh lai. Rat may data image la ban scan pdf the nen ta co the lam ntn
            x1,y1,x3,y1,x3,y3,x1,y3
            """
            box_str = f'{box[0]},{box[1]},{box[2]},{box[1]},{box[2]},{box[3]},{box[0]},{box[3]}'
            #box_str = ",".join(map(str, box))
            text = element['text']
            line = box_str + ","+text + "\n"
            mainline += line
        with open(path_file_gts, mode='w') as f:
            f.write(mainline)
    # print("hello")


        # print(file_gts)
GetLabels(path_label)

_, file_file, _ = GetFiles(path_image)
with open(train_list, mode='w') as f:
    f.write('\n'.join(file_file))
