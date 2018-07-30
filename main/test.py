# with open("test_map.txt", "a+") as f:
    # print(f)
f=open("test_map.txt")
content = f.readline()
# print(content)
while content:
    print(content)
    content = content.split(',')
    #     # print(line)
    for key_value in content:
        key_value = key_value.split(':')
        key = key_value[0]
        value = key_value[1]
        print("key:" + key)
        print("value:" + value)
    content = f.readline()
    # for line in f:
    #     line = line.split(',')
    #     print(line)
    #     for key_value in line:
    #         key_value = key_value.split(':')
    #         key = key_value[0]
    #         value = key_value[1]
    #         print("key:" + key)
    #         print("value:" + value)
