python装饰器
python装饰器的应用一般用于对其他函数在运行之前，加载一些动作，提高代码复用率。一般的装饰器使用都是介绍函数和函数之间的装饰器应用，少有介绍在类中使用装饰器，今天这篇文章我们主要聚焦在类中使用装饰器。我们考虑这样一种情况，我们需要对数据库中一些表进行数据重置工作。需要先清空数据表，如果预置数据的表过多，每个函数中就都需要增加这个数据清除函数。代码冗余度很高。如果我们使用装饰器来每次在重置数据表中的数据时，先进行表的数据清除。接下来我们看下实际的代码，我们先来新建一个数据预置类。

import pymysql
import traceback
import contextlib
import functools


# 清空数据表
def db_table_clear(func):
    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        table_name = args[0]
        try:
            truncate_table_sql = """truncate table {}""".format(table_name)
            cursor.execute(truncate_table_sql)
        except Exception as e:
            traceback.print_exec(e)
        func(self, *args, **kwargs)
     return wrapper

class PresetDatabase(object):
    """
    数据库表数据预置
	"""
    def __init__(self, config):
        self.config = config
    
    @contextlib.contextmanager
    def conn_db(self):
        conn = pymysql.connect(**config)
        cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
        try:
            yield cursor
        except Exception as e:
            traceback.print_exec(e)
        finally:
            conn.commit()
            cursor.close()
            conn.close()
            
	@db_table_clear
    def reset_table1(self, table_name):
        with self.conn_db() as cursor:
            # 具体业务逻辑
            # ...省略
上述代码中，我们使用@db_table_clear这个注解，就可以实现每次重置数据表前，可以先进行数据表的清理工作。这段中的db_table_clear装饰函数，增加一个self参数就可以实现在类中使用类外的装饰器。
