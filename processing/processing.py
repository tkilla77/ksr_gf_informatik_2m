with open('gemeinden.csv', encoding='latin1') as f:
    count = 0
    for line in f:
        values = line.split(',')
        print(line.strip())

    print(f'There are {count} VS towns')