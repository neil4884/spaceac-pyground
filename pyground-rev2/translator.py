from myserial import *


if __name__ == '__main__':
    with open('F433.TXT', 'r') as file_from:
        with open('F433.CSV', 'w') as file:
            file.writelines('')

        for line in file_from.readlines():
            x = strip(line)
            argz = ConvertComma(x)
            argz.write_csv('F433.CSV')

    with open('F868.TXT', 'r') as file_from:
        with open('F868.CSV', 'w') as file:
            file.writelines('')

        for line in file_from.readlines():
            x = strip(line)
            argz = ConvertComma(x)
            argz.write_csv('F868.CSV')

    with open('F915.TXT', 'r') as file_from:
        with open('F915.CSV', 'w') as file:
            file.writelines('')

        for line in file_from.readlines():
            x = strip(line)
            argz = ConvertComma(x)
            argz.write_csv('F915.CSV')

