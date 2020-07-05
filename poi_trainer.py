import cv2
import jsonlines
from pathlib import Path


data_file_input = jsonlines.open('/Users/janis/dev/garms_data/data_uk/asos_uk/img_data/img_items_asos_run20_9_valid.jsonl', 'r')
data_file_output = jsonlines.open('data/img_data/img_items_asos_run20_10b_roi.jsonl', 'w')
completed_outputs = [
    'data/img_data/img_items_asos_run20_10_roi.jsonl'
]
line_nr = 0
mouse_x = None
mouse_y = None
can_write = False


def on_click(event, x, y, p1, p2):
    global mouse_x
    global mouse_y
    global can_write
    if event == cv2.EVENT_LBUTTONDOWN:
        print(x, y)
        mouse_x = x
        mouse_y = y
        can_write = True


def write_data(data):
    global can_write
    if can_write == True:
        data_file_output.write(data)
        can_write = False


completed_hashes = set()
for completed_output in completed_outputs:
    completed_file = jsonlines.open(completed_output, 'r')
    for completed_line in completed_file:
        completed_hashes.add(completed_line['img_hash'])

for line in data_file_input:
    img_hash = line['img_hash']
    if img_hash not in completed_hashes:
        img_path = f'/Users/janis/dev/garms_data/data_uk/asos_uk/images/full/{img_hash}.jpg'
        check_file = Path(img_path)
        if check_file.exists():
            print(img_path)
            img = cv2.imread(img_path)
            orig_h = img.shape[0]
            orig_w = img.shape[1]
            if img.shape[0] > 1000:
                new_width = int(img.shape[1] * (1000 / img.shape[0]))
                img = cv2.resize(img, (new_width, 1000), interpolation=cv2.INTER_AREA)

            print('IMAGE SIZE')
            print(img.shape)
            img_h = img.shape[0]
            img_w = img.shape[1]
            cv2.putText(img, line['name'], (0, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, 234, 2)
            cv2.imshow("image", img)
            cv2.namedWindow('image')
            cv2.setMouseCallback('image', on_click)
            cv2.waitKey()
            print(f'mouse X: {mouse_x}')
            print(f'mouse Y: {mouse_y}')

            mouse_x_relative = mouse_x / img_w
            print(f'mouse_x_relative: {mouse_x_relative}')
            mouse_y_relative = mouse_y / img_h
            print(f'mouse_y_relative: {mouse_y_relative}')

            poi_data = {
                'img_w': orig_w,
                'img_h': orig_h,
                'poi_x_relative': mouse_x_relative,
                'poi_y_relative': mouse_y_relative,
                'poi_x_px': int(orig_w * mouse_x_relative),
                'poi_y_px': int(orig_h * mouse_y_relative)
            }
            print(poi_data)
            output_line = line
            output_line['poi_data'] = poi_data
            write_data(output_line)
            line_nr += 1
            print(f'LINE: {line_nr}')
            print('-----------------------------------------------------')
