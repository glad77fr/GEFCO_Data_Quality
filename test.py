import re

val = "19 A Route de Mussig"

val2= "233dfm4f7Jf 3"

"""a = re.compile(r'^\d{2}')
b = re.compile(r'^\S+')
c = re.compile(r'(?:^\S+)(?:[a-z])')
d = re.compile(r'[a-z]+|[A-Z]+')"""
"e = re.compile(r'(?i)BIS | (?i)BIS ')"

#print(re.findall(r'(?:[a-z\s]+)',val))

print(re.findall(r'\d\s[A-Z]\s', val))
a = re.findall(r'\d\s[A-Z]\s', val)
print(a[0])
b = re.findall(r'[A-Z]', a[0])
print(b)
print(re.findall(r'((?i)[a-z])', val))


#print(a.findall(val))

