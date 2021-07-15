if __name__ == '__main__':

    LAT1 = 15.3628845
    LON1 = 100.35495

    LAT2 = 15.380657
    LON2 = 100.345173

    n = 256

    with open('lat.csv', 'w') as file:
        file.writelines('')

    for i in range(256):
        out = LAT1 + (LAT2 - LAT1) * (i + 1) / n
        out2 = LON1 + (LON2 - LON1) * (i + 1) / n
        with open('lat.csv', 'a') as file:
            file.writelines(str(out2) + ',' + str(out) + '\n')
