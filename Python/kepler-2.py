
path_data = []
with open('path_data.txt', 'r') as f:
    for line in f:
        line = line.strip()
        if line.startswith('[') and line.endswith(']'):
            # Parse nested lists
            items = line[1:-1].split(',')
            nested_list = [float(item) for item in items]
            path_data.append(nested_list)
        else:
            path_data.append(float(line))
            