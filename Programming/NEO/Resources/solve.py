import re

def remove_ansi_escape_sequences(input_string):
    cleaned_string = re.sub('\x1b','',input_string)
    cleaned_string = re.sub('\[','',cleaned_string)
    cleaned_string = re.sub('\x00','',cleaned_string)
    return cleaned_string

with open('output.txt','r') as f:
    text = f.read()
    text_filtered = remove_ansi_escape_sequences(text)
    matches = re.findall("0;(\d+)H92m(.)",text_filtered)

fake_flag = "CSC{have_you_ever_had_a_dream_neo_that_you_were_so_sure_was_real?_hjldsn6349d}"
flag = list(fake_flag)
for match in matches:
    index, char = match
    flag[int(index)-1] = char
print(''.join(flag))
