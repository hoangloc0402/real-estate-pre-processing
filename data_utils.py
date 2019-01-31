
# coding: utf-8

# In[41]:


import re
import glob
import string
import ast
import unicode_utils 
import unicodedata
from pyvi import ViTokenizer, ViPosTagger


# In[48]:


token = dict()
token['int'] = '<INT>'
token['float'] = '<FLOAT>'
token['number'] = '<number>'
token['space'] = ' '
token['blank'] = ''
token['dot'] = '.'
SPECIAL_CHARACTER = '0123456789%@$.,=+-!;/()*"&^:#|\n\t\''
SPECIAL_CHARACTER2 = '!"#$%&()*+,-./:;<=>?@[\]^_`{|}~ '
vietnamese_chars = ' ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyzÀÁÂÃÈÉÊÌÍÒÓÔÕÙÚÝ'
vietnamese_chars += 'àáâãèéêìíòóôõùúýĂăĐđĨĩŨũƠơƯưẠạẢảẤấẦầẨẩẪẫẬậẮắẰằẲẳẴẵẶặẸẹẺẻẼẽẾếỀềỂểỄễỆệ'
vietnamese_chars += 'ỈỉỊịỌọỎỏỐốỒồỔổỖỗỘộỚớỜờỞởỠỡỢợỤụỦủỨứỪừỬửỮữỰựỲỳỴỵỶỷỸỹ'


# In[1]:


def read_all_txt_file(directiry_path):
    txt_files = glob.glob(directiry_path + '/*.txt')
#     log_file = open(directiry_path + 'error_log.txt', 'w+')
    for file in txt_files:
#         try:
            text = open(file, 'r', encoding = 'utf-8').read()
            text = unicode_utils.compound2unicode(text)
#             print(file)
            yield text
#         except:
#             log_file.write(file)
#             continue


# In[ ]:


def txt2dict(text):
    return ast.literal_eval(text)


# In[3]:


# \w = [a-zA-Z0-9_]
# \s = [ \t\n\r\f\v]
# \d = [0-9]
def remove_special_char(text):    
    # remove special character (+-*/_...) with single space   
    text = re.sub('[^\w\s'+ vietnamese_chars +'\.\\\/]+|[_]+', token['space'], text)
    # remove multi space with single space   
    text = re.sub('\s+', token['space'], text)
    # remove multi dot with one dot   
    text = re.sub('\.+', token['dot'], text)
    return text


# In[2]:


def add_token(text):
    #remove number with num token
    text = re.sub('\d+',token['number'],text)
#     # remove float number with 'FLOAT'
#     text = re.sub('\d+[.,]\d+', token['float'], text)  
#     # remove int number with 'INT'   
#     text = re.sub('\d+', token['int'], text)
    return text


# In[45]:


def clean_text(text):
    text = re.sub("\u2013|\u2014", "-", text)
    text = re.sub("\u00D7", " x ", text)
    text = unicodedata.normalize('NFKC', text)
    
    for i in string.punctuation: #!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~
        text = text.replace(i, ' {} '.format(i))
        
    text = re.sub(r'[^{}\s\w]+'.format(string.punctuation), ' ', text)
    numbers = re.findall(r'\d+', text)
    text = re.sub(r'\d+', ' 0 ', text)
    # text = re.sub(r'0[ ]*[.,]+[ ]*0', '00', text)
    text = re.sub('[\n\r]+', ' | ', text)
    return re.sub(r'[ ]+', ' ', text), numbers


# In[46]:


def tokenize(text):
    return ViTokenizer.tokenize(text)


# In[47]:


def pos_tagging(text):
    tok = tokenize(text)
    return ViPosTagger.postagging(tok)

