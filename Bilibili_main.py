import requests as rs
import re
import pandas as pd
import random
import time
import math
from uid_creat import Generate

class Bili():
    def __init__(self):
        self.uids = open('./uid.txt', 'r').read().strip(',').split(',')
        self.urls = ['https://api.bilibili.com/x/space/acc/info?mid={}&jsonp=jsonp'.format(i) for i in self.uids]
        self.info_url = []
        self.UID = []
        self.name = []
        self.sex = []
        self.sign = []
        self.vip = []
        self.year_vip = []
        self.level = []
        self.gz = []
        self.fs = []
        self.gzup = []
        self.tags = []
        self.yc_count = 0
        self.c = 0
        self.ua = open('./user_agents.txt').read().replace('"', '').split('\n')
        self.User_data = {
            'UID': self.UID,
            '主页': self.info_url,
            '等级': self.level,
            '昵称': self.name,
            '性别': self.sex,
            '关注数': self.gz,
            '粉丝数': self.fs,
            '关注的UP主': self.gzup,
            '关注的标签':self.tags,
            '个性签名': self.sign,
            '是否开通会员': self.vip,
            '是否是年费会员': self.year_vip
        }
        for url in self.urls:
            self.get_data(url)

        self.Generating_tables()

    def get_data(self, url):
        headers = {'user-agent': random.choice(self.ua) }
        self.c += 1
        print(f'正在爬取第{self.c}个   URl:{url}')
        print(f'目前一共有{self.yc_count}个异常UID')

        try:
            time.sleep(0.3)
            res = rs.get(url, headers=headers).json()
            if res['code'] == 0:
                self.UID.append(res['data']['mid'])
                self.info_url.append(f"https://space.bilibili.com/{res['data']['mid']}")
                self.name.append(res['data']['name'])
                self.sex.append(res['data']['sex'])
                self.sign.append(res['data']['sign'])
                self.level.append(res['data']['level'])

                if res['data']['vip']['status'] == 0:
                    self.vip.append('否')
                    self.year_vip.append('否')
                elif res['data']['vip']['status'] == 1 and res['data']['vip']['type'] != 2:
                    self.vip.append('是')
                    self.year_vip.append('否')
                elif res['data']['vip']['status'] == 1 and res['data']['vip']['type'] == 2:
                    self.year_vip.append('是')
                    self.vip.append('是')
                else:
                    self.vip.append('否')
                    self.year_vip.append('否')

                follower_url = 'https://api.bilibili.com/x/relation/stat?vmid={}&jsonp=jsonp'.format(res['data']['mid'])
                f = rs.get(follower_url, headers=headers).json()
                if f['code'] == -412:
                    self.gz.append('请求被拦截')
                    self.fs.append('请求被拦截')
                    print('关注数请求已被拦截... 暂停30分钟...')
                    time.sleep(30 * 60)
                else:
                    self.gz.append(f['data']['following'])
                    self.fs.append(f['data']['follower'])

                follower_code = rs.get('https://api.bilibili.com/x/relation/followings?vmid={}&pn=1&ps=50&order=desc&order_type=&jsonp=jsonp'.format(res['data']['mid'])).json()
                if follower_code['code'] == 0:
                    total = 250 if follower_code['data']['total'] > 250 else follower_code['data']['total']
                    if total != 0:
                       try:
                           pn = math.ceil(total / 50)
                           unames = ''
                           for p in range(1, pn + 1):
                               follow_up_url = 'https://api.bilibili.com/x/relation/followings?vmid={}&pn={}&ps=50&order=desc&order_type=&jsonp=jsonp'.format(res['data']['mid'], p)
                               up_name = rs.get(follow_up_url).json()['data']['list']
                               for uname in up_name:
                                   unames += uname['uname'] + ' | '
                           self.gzup.append(unames)
                       except:
                           self.gzup('请求被拦截')
                           print('关注UP字段请求已被拦截...')
                    else:
                        self.gzup.append('未关注UP主')
                elif follower_code['code'] == 22115:
                    self.gzup.append('用户已设置隐私，无法查看')
                elif follower_code['code'] == -412:
                    print('关注UP字段请求已被拦截 暂停30分钟......')
                    self.gzup.append('请求被拦截')
                    time.sleep(30 * 60)
                else:
                    print(f"未知问题 UID:{res['data']['mid']} 主页URL:{self.info_url[-1]}")
                    self.gzup.append('未知错误')

                tag = rs.get('https://api.bilibili.com/x/space/tag/sub/list?vmid={}&jsonp=jsonp'.format(res['data']['mid'])).json()
                if tag['code'] == 0:
                    tag_names = ''
                    for tag_name in tag['data']['tags']:
                        tag_names += tag_name['tag_name'] + ' | '
                    self.tags.append(tag_names)
                elif tag['code'] == 53013:
                    self.tags.append('用户隐私设置未公开')
                else:
                    self.tags.append('未知错误')
                    print('关注标签请求未知错误 URL: https://api.bilibili.com/x/space/tag/sub/list?vmid={}&jsonp=jsonp'.format(res['data']['mid']))

            elif res['code'] == -412:
                print('请求已被拦截......')
                print('休息半小时.....')
                self.Log()
                print('-' * 50)
                time.sleep(30 * 60)

            elif res['code'] == -404:
                print("当前用户没有数据: apiurl: {} https://space.bilibili.com/{}".format(url,re.findall('\d+',url)[0]))
                self.yc_count += 1

            else:
                print("未知错误: api url: {} https://space.bilibili.com/{}".format(url, re.findall('\d+', url)[0]))

            self.Log()
            print('-' * 50)

        except:
            print("未知错误...  apiurl: {}  https://space.bilibili.com/{}".format(url,re.findall('\d+',url)[0]))
            self.Log()
            self.yc_count += 1
            print('-' * 50)

    def Generating_tables(self):
        self.Log()
        self.df = pd.DataFrame(self.User_data)
        print('正在生成表格...')
        self.df.set_index(['UID'], inplace=True)
        self.df.to_csv('./userdata.csv', encoding='utf-8')
        print(f'表格生成完成...一共有{self.yc_count}个url没有数据')

    def Log(self):
        print(f'''数据情况:
 ID字段长度:{len(self.UID)}
 主页字段长度: {len(self.info_url)}
 性别字段长度: {len(self.sex)}
 等级字段长度：{len(self.level)}
 名字字段长度: {len(self.name)}
 关注字段长度：{len(self.gz)}
 粉丝字段长度: {len(self.fs)}
 会员字段长度: {len(self.vip)}
 年费会员字段长度: {len(self.year_vip)}
 关注up字段长度: {len(self.gzup)}
 关注标签字段长度: {len(self.tags)}
 个性签名字段长度: {len(self.sign)}''')

if __name__ == '__main__':
    Generate(n=1000)    #要爬多少条数据 修改n的参数，默认100
    Bili()

