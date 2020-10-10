class Document():

    WELCOME_STR = 'Welcome! The context for this book is {}.'

    def __init__(self, title, author, context):
        print('init function called')
        self.title = title
        self.author = author
        self.__context = context

    # 类函数
    @classmethod
    def create_empty_book(cls, title, author):
        return cls(title=title, author=author, context='nothing')

    def get_context_length(self):
        return len(self.__context)

    # 静态函数
    @staticmethod
    def get_welcome(context):
        return Document.WELCOME_STR.format(context)


if __name__ == '__main__':
    empty_book = Document.create_empty_book("helfafa afafadf afadfaafd fadafefaf", "prefsifiafa dafa daffadf")
    print(empty_book.get_context_length())
    print(empty_book.get_welcome("welcome"))

