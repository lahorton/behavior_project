import json

json_string = open("bd.json").read()

parsed_bd = json.loads(json_string)

print(parsed_bd[0]['title']


# i = 0
# for i in parsed_bd:
#     behavior =parsed_bd[i]['title']
#     description = parsed_bd[i]['description']
#     print(behavior)
#     print(description)
#     i += 1
