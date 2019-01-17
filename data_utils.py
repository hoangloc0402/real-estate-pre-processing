
# coding: utf-8

# In[1]:


import re
import string
import unicodedata


# In[2]:


token = dict()
token['int'] = 'INT'
token['float'] = 'FLOAT'
token['space'] = ' '
token['blank'] = ''
vietnamese_chars = ' ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyzÀÁÂÃÈÉÊÌÍÒÓÔÕÙÚÝ'
vietnamese_chars += 'àáâãèéêìíòóôõùúýĂăĐđĨĩŨũƠơƯưẠạẢảẤấẦầẨẩẪẫẬậẮắẰằẲẳẴẵẶặẸẹẺẻẼẽẾếỀềỂểỄễỆệ'
vietnamese_chars += 'ỈỉỊịỌọỎỏỐốỒồỔổỖỗỘộỚớỜờỞởỠỡỢợỤụỦủỨứỪừỬửỮữỰựỲỳỴỵỶỷỸỹ'


# In[3]:


# \w = [a-zA-Z0-9_]
# \s = [ \t\n\r\f\v]
# \d = [0-9]
def remove_special_char(text):    
    # remove special character (+-*/_...) with single space   
    text = re.sub('[^\w\s'+ vietnamese_chars +'\.]+|[_]+', token['space'], text)   
    # remove multi space with single space   
    text = re.sub('\s+', token['space'], text)
    return text


# In[4]:


def add_token(text):
    # remove float number with 'FLOAT'
    text = re.sub('\d+[.,]\d+', token['float'], text)  
    # remove int number with 'INT'   
    text = re.sub('\d+', token['int'], text)
    return text


# In[5]:


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

