with open('locations.list') as src:
    with open('lite.list', mode='w') as new_file:
        line = src.readline()
        while line.strip() != '==============':
            line = src.readline()
            print(line)
        i = 1
        while line.strip != '':
            line = src.readline()
            if i % 20 == 0:
                new_file.write(line)
                print(line)
            i += 1