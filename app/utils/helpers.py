import re
import unicodedata


def slugify(text: str) -> str:
    """将文本转换为URL友好的slug"""
    # 转换为小写
    text = text.lower()
    
    # 移除重音符号
    text = unicodedata.normalize('NFKD', text)
    text = ''.join([c for c in text if not unicodedata.combining(c)])
    
    # 替换非字母数字字符为连字符
    text = re.sub(r'[^a-z0-9]+', '-', text)
    
    # 移除首尾的连字符
    text = text.strip('-')
    
    # 如果slug为空，使用默认值
    if not text:
        text = 'untitled'
    
    return text