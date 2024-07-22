from io import BytesIO


output = BytesIO(b"")
instring = """FUNCTION animload_Bird_A_Resting
#00001    animload_bird_A
#00002  END FUNCTION
#00003  """
length = len(instring)

test_string = ""
position = 0
running = True

def next_token():
    global position
    while position < length and (instring[position] == '\n' or instring[position] == ' '):
        position += 1
    if position >= length:
        return False
    if length > (position + 40):
        test = instring[position:position+40]
    else:
        test = instring[position:length]

    if test.startswith("FUNCTION"):
        print("FUNCTION")
        command_integer("FUNCTION", 35)
    elif test.startswith("END FUNCTION"):
        print("END FUNCTION")
        command_integer("END FUNCTION", 36)
    elif test.startswith("#"):
        print("#")
        output.write((2).to_bytes(1, byteorder='little'))
        position += 1
        token = extract_token_at(position)
        result_byte = parse_long(token)
        output.write(result_byte)
    else:
        print("  EXTRACT TOKEN")
        token = extract_token_at(position)
        result_byte = parse_field(token)
        output.write(result_byte)
    return True

def command_word(word):
    global position
    position += len(word)

def command_integer(word, integer):
    command_word(word)
    output.write(integer.to_bytes(1, byteorder='little'))

def extract_token_at(pos):
    token = ""
    if instring[pos] not in "-0123456789":
        while instring[pos] != ' ' and instring[pos] != '\n' and instring[pos] != ';':
            token = token + instring[pos]
            pos += 1
    else:
        while instring[pos] in "-0123456789.E":
            token = token + instring[pos]
            pos += 1
    print(token)
    return token

def parse_long(token):
    global position
    number = int(token)
    result_byte = number.to_bytes(4, byteorder='little')
    position += len(token)
    return result_byte

def parse_field(token):
    global position
    result_byte = bytearray(22)
    result_byte.extend(map(ord, token))
    position += len(token)
    return result_byte

while running:
    running = next_token()
with open('sam.qb', "wb") as f:
    f.write(output.getbuffer())
