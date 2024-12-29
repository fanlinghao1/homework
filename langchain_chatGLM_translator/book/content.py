
import pandas as  pd
from enum import Enum, auto
from PIL import Image as PILImage
from utils import LOG
from io import  StringIO
#import logging

# 创建一个日志记录器（Logger）对象，通常将其命名为 'LOG' 或者其他
#LOG = logging.getLogger(__name__)

#定义一个枚举里
class ContentType(Enum):
    TEXT = auto()  ##文本类的内容
    TABLE = auto() ##表格类的内容
    IMAGE = auto() ##图像类的内容

# 定义一个连接的类,并判断你传入的数据类型
class  Content:
    def __init__(self,content_type,original,translation = None):
        self.content_type  = content_type  #存储内容内型
        self.original = original  #存储原始内容
        self.translation = translation  #存储翻译内容
        self.status = False #存储状态值


    # 定义一个set_translation 的方法
    def  set_translation(self, translation, status):
        if not self.check_translation_type(translation):
            raise ValueError(f"Invalid translation type. Expected {self.content_type}, but got {type(translation)}")
        self.translation = translation
        self.status = status

    # 判断传入类型的状态
    def check_translation_type(self ,translation):
        if self.content_type == ContentType.TEXT and isinstance(translation, str):
            return True
        elif self.content_type == ContentType.TABLE and  isinstance(translation, list):
            return True
        elif self.content_type == ContentType.IMAGE and  isinstance(translation, PILImage.Image):
            return True
        return False

    #打印original的内容
    def __str__(self):
        return self.original


# 定义一个表内容处理的类
class TableContent(Content):
    def __init__(self,data,translation = None):
        df = pd.DataFrame(data)

        if len(data) != len(df) or len(data[0]) != len(df.columns):
            raise ValueError("The number of rows and columns in the extracted table data and DataFrame object do not match.")
        #调用父类构造函数：通过 super() 调用父类的构造函数，将数据的类型（表格类型）和 DataFrame 数据传递给父类进行初始化。
        super().__init__(ContentType.TABLE, df)

    def set_translation(self, translation, status):
        try:
            if not isinstance(translation,str):
                raise ValueError(f"Invalid translation type. Expected str, but got {type(translation)}")
            LOG.debug(f"[translation]\n{translation}")
            # Extract column names from the first set of brackets
            header = translation.split(']')[0][1:].split(', ')
            # Extract data rows from the remaining brackets
            data_rows = translation.split('] ')[1:]
            # Replace Chinese punctuation and split each row into a list of values
            data_rows = [row[1:-1].split(', ') for row in data_rows]
            # Create a DataFrame using the extracted header and data
            translated_df = pd.DataFrame(data_rows, columns=header)
            LOG.debug(f"[translated_df]\n{translated_df}")
            self.translation = translated_df
            self.status = status

        except Exception as e:
            LOG.error(f"An error occurred during table translation: {e}")
            self.translation = None
            self.status = False

    def __str__(self):
        return self.original.to_string(header = False,index = False)

    # 解析翻译的结果，如果翻译的结果为true 则translation 不然就是原文
    def iter_items(self,translated=False):
        target_df = self.translation if translated else self.original
        for row_idx, row in target_df.iterrows():
            for col_idx,item in enumerate(row):
                yield row_idx,col_idx,item


    #定义一个更新数据的方法
    def update_time(self,row_idx,col_idx,new_value,translated = False):
        target_df = self.translation if translated else self.original
        target_df.at[row_idx,col_idx,] = new_value

    def get_original_as_str(self):
        return self.original.to_string(header = False, index = False)








