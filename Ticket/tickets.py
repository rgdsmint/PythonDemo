import requests
from stations import station_code, code_station, stationsChineseName
from prettytable import PrettyTable
import time
import colorama
from colorama import Fore
import platform
'''
此程序意在练手和方便自己
直接运行即可使用
使用方式运行即可看到
'''


class SearchTicket:
    '''
    查票程序
    '''

    def __init__(self):
        '''接受所查票的参数 : 车票类型 起始车站 日期'''
        self.trainOption = input(
            '-d动车 -g高铁 -k快速 -t特快 -z直达\n请输入您要查询的车次类型(如:-dg PS:默认全选) :')
        # 如果没有填参数或者参数错误 则按默认执行
        if len(self.trainOption
               ) == 0 or self.trainOption not in '-dgktz' and len(
                   self.trainOption) != 0:
            self.trainOption = '-dgktz'  # 默认全选 (-dgktz)
            print('\t输入有误 已按默认类型执行')

        self.fromStation = input('请输入您出发的城市(如:南京 PS:默认南京) :')
        # 如果参数错误(不在站点名称里面 则按默认执行)
        if self.fromStation not in stationsChineseName:
            self.fromStation = '南京'  # 默认南京
            print('\t输入有误 已按默认起始点执行')

        self.toStation = input('请输入您要前往的城市(如:上海 PS:默认上海) :')
        # 如果参数错误(不在站点名称里面 则按默认执行)
        if self.toStation not in stationsChineseName:
            self.toStation = '上海'  # 默认上海
            print('\t输入有误 已按默认终止点执行')

        self.Date = input('请输入日期(如:2018-05-09 PS:默认日期为当天) :')
        # 如果参数错误(不为正确日期格式 则按默认时间执行))
        if self.is_valid_date(self.Date):
            pass
        else:
            self.Date = time.strftime('%Y-%m-%d')  # 默认日期为当天
            print('\t输入有误 已按默认时间执行')
        self.train = self.trains()

    def is_valid_date(self, str):
        '''判断是否是一个有效的日期字符串'''
        if len(str) == 10:
            try:
                time.strptime(str, "%Y-%m-%d")
                return True
            except:
                return False
        else:
            return False

    def searchTrain(self):
        '''处理信息 得出官网信息 并写成列表'''
        arguments = {
            'option': self.trainOption,
            'from_station': station_code.get(self.fromStation, None),
            'to_station': station_code.get(self.toStation, None),
            'date': self.Date
        }
        self.options = ''.join([key for key in arguments['option']])
        url = 'https://kyfw.12306.cn/otn/leftTicket/query?\
leftTicketDTO.train_date={}\
&leftTicketDTO.from_station={}&\
leftTicketDTO.to_station={}\
&purpose_codes=ADULT'.format(arguments['date'], arguments['from_station'],
                             arguments['to_station'])
        requests.urllib3.disable_warnings()
        r = requests.get(url, verify=False)
        try:
            self.raw_trains = r.json()['data']['result']
        except:
            exit('输入有误')

    def trains(self):
        '''解析信息 得出各参数'''
        v_system = platform.system()  # 获取操作系统信息(因为Windows需要特殊处理)
        if v_system == 'Windows':  # 如果系统为Windows 则作处理
            colorama.init(autoreset=True)
        for item in self.raw_trains:
            data_list = item.split('|')
            trainNum = data_list[3]
            initial = trainNum[0].lower()
            if not self.options or initial in self.options:
                from_station_code = data_list[6]
                to_station_code = data_list[7]
                from_station_name = code_station.get(from_station_code)
                to_station_name = code_station.get(to_station_code)
                start_time = data_list[8]
                arrive_time = data_list[9]
                time_duration = data_list[10]
                business_seat = data_list[32] or '--'  # 商务座
                first_seat = data_list[31] or '--'  # 一等座
                second_seat = data_list[30] or '--'  # 二等座
                high_sort_sleep = data_list[21] or '--'  # 高级软卧
                sort_sleep = data_list[23] or '--'  # 软卧
                move_slepp = data_list[33] or '--'  # 动卧
                hard_sleep = data_list[28] or '--'  # 硬卧
                sort_seat = data_list[24] or '--'  # 软座
                hard_seat = data_list[29] or '--'  # 硬座
                no_seat = data_list[26] or '--'  # 无座
                other_seat = data_list[22] or '--'  # 其它
                train = [
                    trainNum, '\n'.join([
                        Fore.RED + from_station_name + Fore.RESET,
                        Fore.GREEN + to_station_name + Fore.RESET
                    ]), '\n'.join([
                        Fore.RED + start_time + Fore.RESET,
                        Fore.GREEN + arrive_time + Fore.RESET
                    ]), time_duration, business_seat, first_seat, second_seat,
                    high_sort_sleep, sort_sleep, move_slepp, hard_sleep,
                    sort_seat, hard_seat, no_seat, other_seat
                ]

                yield train

    def pretty_print(self):
        '''将得到的车票相关数据可视化'''
        pt = PrettyTable()
        article = '车次 站点 时间 历时  商务座 一等座 二等座 高级软卧 软卧 动卧 硬卧 软座 硬座 无座 其他'.split()
        pt._set_field_names(article)
        for train in self.train:
            pt.add_row(train)
        print(pt)


if __name__ == '__main__':
    '''运行程序增加循环以重复查询'''
    while True:
        st = SearchTicket()
        st.searchTrain()
        st.pretty_print()
        # 询问是否继续
        message = input('是否继续?[y/n] (PS:默认为n): ')
        # 如果不是'y' 则退出
        if message != 'y':
            exit('程序已结束')
