# import jieba
# from wordcloud import WordCloud
# import matplotlib.pyplot as plt
# import numpy as np
from PIL import Image
#
# def seg_sentence(sentence):
#     sentence_seged = jieba.cut(sentence.strip())  #strip()用来消除前后的空格
#     outstr = ''
#     for word in sentence_seged:
#         if word != '\t':
#             outstr += word
#             outstr += " " #去掉制表符并用空格分隔各词
#     return outstr.strip()
#
#
# # # 创建停用词list
# # def stopwordslist(filepath):
# #     stopwords = [line.strip() for line in open(filepath, 'r', encoding='utf-8').readlines()]
# #     return stopwords
# #
# #
# # def seg_sentence(sentence):
# #    sentence_seged = jieba.cut(sentence.strip())
# #    stopwords = stopwordslist('./stop.txt')  # 这里加载停用词的路径
# #    outstr = ''
# #    for word in sentence_seged:
# #        if word not in stopwords: # 判断如果不是停用词
# #            if word != '\t':
# #                outstr += word
# #                outstr += " "
# #    return outstr
#
#
# inputs = open('test.txt', 'r', encoding='utf-8') # 原始的中文文档
# outputs = open('output.txt', 'w', encoding='utf-8') # 分词过后的中文文档
# for line in inputs:
#     line_seg = seg_sentence(line)  # 对每个句子进行分词
#     outputs.write(line_seg + '\n')  # 将处理过后的文件进行保存
# outputs.close()
# inputs.close()
# mask = np.array(Image.open("111.jpg")) # 模板图片
# inputs = open('output.txt', 'r', encoding='utf-8')
# mytext=inputs.read()
# wordcloud=WordCloud(mask=mask, width=3000, height=3000, background_color="white", margin=1,
#                     max_words=300, min_font_size=10, max_font_size=None, repeat=False,
#                     font_path="0606.ttf").generate(mytext) #生成云图
# wordcloud.to_file('wordcloud.jpg')
# inputs.close()

# import numpy as np
# import matplotlib.pyplot as plt
# from wordcloud import WordCloud
#
# text = "缪邦燕是猪猪"
#
# x, y = np.ogrid[:300, :300]
#
# mask = (x - 150) ** 2 + (y - 150) ** 2 > 130 ** 2
# mask = 255 * mask.astype(int)
# # mask = np.array(Image.open("111.jpg")) # 模板图片
#
# wc = WordCloud(background_color="white", repeat=True, mask=mask,font_path="0606.ttf")
# wc.generate(text)
#
# plt.axis("off")
# plt.imshow(wc, interpolation="bilinear")
# plt.show()


i = 13 // 3

print(i)