import jieba

# open 内置函数 不需要引用 直接使用
# 开打文件西游记和python 文件放到同一个目录，可直接引用不需要路径
f = open('text.txt', 'r', encoding='utf-8')
# 查看文件的编码格式
print('文件的编码格式:' + f.encoding)
# 读取文件
txt = f.read()
# 关闭文件，良好的习惯
f.close()

# 使用精确模式对文本进行分词
#  使用结巴库把西游拆分成一个个的词组
words = jieba.lcut(txt)

# 通过键值对的形式存储词语及其出现的次数
# 大括号表示 python的字典类型对应，
# 键值对 key:value1 ,类似java的map对象和list
counts = {}

chiyun = []
for word in words:
    # == 1 单个词语不计算在内
    if len(word) < 2:
        continue
    else:
        # 遍历所有词语，每出现一次其对应的值加 1
        counts[word] = counts.get(word, 0) + 1

    # 将键值对转换成列表
items = list(counts.items())

# 根据词语出现的次数进行从大到小排序
items.sort(key=lambda x: x[1], reverse=True)
# 列标题 format
print("{0:<5}{1:<8}{2:<5}".format('序号', '词语', '频率'))
# 需要显示的范围  10即显示前10个，0到9
for i in range(10):
    word, count = items[i]
    print("{0:<5}{1:<8}{2:>5}".format(i + 1, word, count))