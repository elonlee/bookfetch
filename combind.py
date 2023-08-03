import shutil

index = 13
count = 69
output_file = f'output/output.txt'

with open(output_file, 'w', encoding='utf-8') as f:
    for i in range(index, count):
        src = f'output/{i}.txt'
        print(src)
        with open(src, 'r', encoding='utf-8') as fsrc:
            shutil.copyfileobj(fsrc, f)
            f.writelines("\r\n")
