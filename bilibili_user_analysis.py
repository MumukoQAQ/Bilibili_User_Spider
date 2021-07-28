import pandas as pd
from matplotlib import pyplot  as plt
from wordcloud import WordCloud

data = pd.read_csv('./userdata.csv')
all = len(data)

def level():
    '''
    账号活跃情况分析
    0 - 1级为僵尸账号
    2 - 4级为正常账号
    5 - 6级为活跃账号
    '''
    plt.rcParams['font.sans-serif'] = ['SimHei']

    zero_two = data[data.loc[:,'等级'] <= 1]
    zero_two_num = len(zero_two)

    three_four = data[(data.loc[:,'等级'] >= 2) & (data.loc[:,'等级'] <= 4)]
    three_four_num = len(three_four)

    five_six = data[(data.loc[:, '等级'] >= 5) & (data.loc[:, '等级'] <= 6)]
    five_six_num = len(five_six)
    level_x = [zero_two_num,three_four_num,five_six_num]
    level_lab = ['僵尸账号','正常账号','活跃账号']

    plt.pie(x=level_x,labels=level_lab,autopct='%0.2f',pctdistance=0.8,colors=['grey',None,'red'])
    plt.axis('equal')
    plt.legend(loc="upper right", fontsize=10, bbox_to_anchor=(1.1, 1.05), borderaxespad=0.3)
    plt.title('账号情况')
    plt.show()

    #各个等级所占的人数

    level_y = data['等级'].value_counts(sort=False)
    bar_lab = ['0级','1级','2级','3级','4级','5级','6级']

    plt.bar(bar_lab,height=level_y,width=0.5,color=['grey','grey','green','blue','orange','yellow','red'])
    plt.xticks(range(len(bar_lab)),bar_lab,size='small')

    plt.xlabel('等级')
    plt.ylabel('数量')
    plt.title('等级数量图')
    for a, b in zip(range(len(bar_lab)),level_y):
        plt.text(a, b + 0.05, '%.0f' % b, ha='center', va='bottom', fontsize=10)
    plt.show()

    plt.pie(x=level_y, labels=bar_lab, autopct='%0.2f',colors=['grey',None,'green','blue','orange','yellow','red'],pctdistance=0.8)
    plt.axis('equal')
    plt.legend(loc="upper right", fontsize=10, bbox_to_anchor=(1.1, 1.05), borderaxespad=0.3)
    plt.title('等级占比')
    plt.show()

def sex():

    '''
    统计性别数据
    '''

    sex_data = data['性别'].value_counts().to_dict()

    plt.pie(x=[sex_data['男'],sex_data['女']],labels=['男','女'],colors=[None,'pink'],autopct='%0.2f',pctdistance=0.8,labeldistance=0.9)
    plt.axis('equal')
    plt.legend(loc="upper right", fontsize=10, bbox_to_anchor=(1.1, 1.05), borderaxespad=0.3)
    plt.title('性别占比')
    plt.show()

    sex_x = [sex_data[i] for i in sex_data]
    sex_lable = [i for i in sex_data]

    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.pie(x=sex_x,labels=sex_lable,autopct='%0.2f',pctdistance=0.8,colors=['grey',None,'pink'])
    plt.axis('equal')
    plt.legend(loc="upper right", fontsize=10, bbox_to_anchor=(1.1, 1.05), borderaxespad=0.3)
    plt.title('性别数据')
    plt.show()

def vip():

    vip_table = data[data.loc[:,'是否开通会员'] == '是']
    year_vip = data[(data.loc[:,'是否开通会员'] == '是') & (data.loc[:,'是否是年费会员'] == '是')]

    vip_x = [all - len(vip_table),len(vip_table)]
    vip_lable = ['非会员','会员']

    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.pie(vip_x, labels=vip_lable, autopct='%0.2f', pctdistance=0.8,colors=['grey','red'])
    plt.axis('equal')
    plt.legend(loc="upper right", fontsize=10, bbox_to_anchor=(1.1, 1.05), borderaxespad=0.3)
    plt.title('会员情况')
    plt.show()

    '''
    会员中年份会员占比
    '''
    year_vip_x = [len(vip_table) - len(year_vip),len(year_vip)]
    year_vip_lable = ['普通会员','年费会员']
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.pie(year_vip_x, labels=year_vip_lable, autopct='%0.2f', pctdistance=0.8,colors=[None,'red'])
    plt.axis('equal')
    plt.legend(loc="upper right", fontsize=10, bbox_to_anchor=(1.1, 1.05), borderaxespad=0.3)
    plt.title('年费会员占比情况')
    plt.show()


def level_vip():
    '''
    每个等级中vip的数量情况
    '''

    vip_table = data[data.loc[:, '是否开通会员'] == '是']
    year_vip = data[(data.loc[:, '是否开通会员'] == '是') & (data.loc[:, '是否是年费会员'] == '是')]

    level_num = [0,1,2,3,4,5,6]

    bar_lab = ['0级', '1级', '2级', '3级', '4级', '5级', '6级']

    vip_g_key = []
    vip_g_value = []

    for key,value in list(vip_table.groupby('等级')):
        vip_g_key.append(key)
        vip_g_value.append(len(value))

    def add_defect(k_num,v_num):
        for i, j in enumerate(level_num):
            if j not in k_num:
                k_num.insert(i,j)
                v_num.insert(i,0)
    
    if len(level_num) != len(vip_g_key):
        add_defect(vip_g_key,vip_g_value)

    yvip_g_key = []
    yvip_g_value = []

    for key,value in list(year_vip.groupby('等级')):
        yvip_g_key.append(key)
        yvip_g_value.append(len(value))

    if len(yvip_g_key) != len(level_num):
        add_defect(yvip_g_key,yvip_g_value)

    ord_vip = [j - yvip_g_value[i]  for i,j in enumerate(vip_g_value)]

    x = list(range(len(bar_lab)))
    vip_x = [i + 0.3 for i in x]
    y_vip_x = [i + 0.6 for i in x]

    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.subplots(dpi=300)
    plt.bar(bar_lab,vip_g_value,width=0.3,label='总会员数')
    plt.bar(vip_x,ord_vip, width=0.3,label='普通会员数',color='orange')
    plt.bar(y_vip_x, yvip_g_value, width=0.3,label='年费会员数',color='red')

    plt.xticks(bar_lab)
    plt.legend(loc='upper left',fontsize=8, bbox_to_anchor=(1.1, 1.05), borderaxespad=0.4)
    plt.xlabel('等级')
    plt.ylabel('数量')
    plt.title('各个等级中会员数量情况',fontsize=14)

    for i,j in zip(range(len(bar_lab)),vip_g_value):
        plt.text(i, j + 0.05, '%.0f' % j, ha='center', va='bottom', fontsize=8)

    for i,j in zip(vip_x,ord_vip):
        plt.text(i, j + 0.05, '%.0f' % j, ha='center', va='bottom', fontsize=8)

    for i,j in zip(y_vip_x,yvip_g_value):
        plt.text(i, j + 0.05, '%.0f' % j, ha='center', va='bottom', fontsize=8)
    plt.show()

def CiYun():
    up = data[data.loc[:, '关注的UP主'] != '未关注UP主']
    words = []
    for c in up['关注的UP主'].values:
        for uname in c.split('|'):
            if uname != ' ':
                words.append(uname.strip()+' ')
 
    with open('./up_words.txt', 'w', encoding='utf-8') as f:
        f.writelines(words)
        print('UP主词语数据保存完成...')
    
    print('正在生成词云图...')
    f = open('./up_words.txt', 'r', encoding='utf-8').read()
    w = WordCloud(
        font_path="C:/Windows/Fonts/simhei.ttf", #字体路径
        background_color='white',
        max_words=5000,       #展示的词语数量，如爬取的数据较少可适当减少
        width=1800,
        height=1600,
        max_font_size=80,
        scale=5,
        mask=plt.imread('./bjt.jpg') #背景图路径
    ).generate(f)
    w.to_file('词云图.png')
    plt.subplots(figsize=(12, 8), dpi=500)
    plt.imshow(w, interpolation='bilinear')
    plt.axis("off")
    plt.show()

level_vip()
vip()
level()
sex()
CiYun()
