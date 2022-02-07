with open('locations.list') as src:
    with open('ukraine_locations.list', mode='w') as new_file:
        line = src.readline()
        while line.strip() != '==============':
            line = src.readline()
            print(line)
        line = src.readline()
        while line.strip() != '':
            if 'Ukraine' in line:
                new_file.write(line)
                print(line)
            line = src.readline()
