import jsonlines
from pathlib import Path

input_paths = [
    'data/img_data/img_items_asos_run20_10b_roi.jsonl',
    'data/img_data/img_items_asos_run20_10_roi.jsonl',
    'data/img_data/img_items_topshop_run6_10_roi.jsonl'
]
output_file = jsonlines.open('data/poi_train_data_1.jsonl', 'w')

line_counter = 0
for input_path in input_paths:
    input_file = jsonlines.open(input_path, 'r')
    for input_line in input_file:
        label = [
            input_line['poi_data']['poi_x_relative'],
            input_line['poi_data']['poi_y_relative'],
        ]
        img_hash = input_line['img_hash']
        if 'asos' in input_path:
            path = f'/Users/janis/dev/garms_data/data_uk/asos_uk/images/full/{img_hash}.jpg'
        else:
            path = f'/Users/janis/dev/garms_experiment/poi_trainer/data/images/full/{img_hash}.jpg'

        check_file = Path(path)
        if not check_file.exists():
            raise Exception(f'Wrong path: {path}')

        output_line = {
            'path': path,
            'label': label
        }
        output_file.write(output_line)
        line_counter += 1
        print(f'LINE: {line_counter}')
