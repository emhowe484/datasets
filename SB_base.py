#ERIN HOWE 8/19/2026 
import pandas as pd

filePath = ''
df1 = pd.read_csv(filePath, usecols=['WORD', 'LENGTH'])
print(df1.info())

#create list of first letters to count each word by
df1['first'] = ''

for i in range(len(df1)):
    df1['first']= df1['WORD'].str[0]

backup1 = df1

#fix the categories so that they make more sense/ create bigger groups
df1['first'] = df1['first'].replace(['Q', 'R', 'S'], 'QRS')
df1['first'] = df1['first'].replace(['W', 'X', 'Y', 'Z'], 'WYZ')
df1['first'] = df1['first'].replace(['I', 'J', 'K'], 'IJK')
df1['first'] = df1['first'].replace(['U', 'V'], 'UV')
df1['first'] = df1['first'].replace(['N', 'O'], 'NO')

#actually creating the summary
print(df1['first'].value_counts())

#creating the mask column
df1["Mask"] = df1["WORD"].str.lower()

#finding and removing the accidental null value, because one of the words is 'None'
null_rows = df1[df1["WORD"].isna()]
print(null_rows)
df1= df1.dropna(subset=["WORD"])

#creating the actual mask
df1["Mask"] = df1["Mask"].apply(lambda w: "".join(dict.fromkeys(w)))

#subsets that can be useful for finding words with certain letters; vowels, n, y
#also can find the distribution of words across each first letter category
n_subset = df1[df1["Mask"].str.contains("n")]
a_subset = df1[df1["Mask"].str.contains("d")]
a_subset = df1[df1["Mask"].str.contains("a")]
e_subset = df1[df1["Mask"].str.contains("e")]
i_subset = df1[df1["Mask"].str.contains("i")]
o_subset = df1[df1["Mask"].str.contains("o")]
u_subset = df1[df1["Mask"].str.contains("u")]
y_subset = df1[df1["Mask"].str.contains("y")]

#get a subset of paragrams and perfect paragrams
para_subset = df1[df1["Mask"].str.len() == 7]
Ppara_subset = para_subset[para_subset["LENGTH"] == 7]

#useful
'''print(n_subset['first'].value_counts())
print(e_subset['first'].value_counts())
print(y_subset['first'].value_counts())
print(para_subset['first'].value_counts())
print(Ppara_subset['first'].value_counts())'''

#not useful
#print(a_subset['first'].value_counts())
#print(i_subset['first'].value_counts())
#print(u_subset['first'].value_counts())
#print(o_subset['first'].value_counts())

