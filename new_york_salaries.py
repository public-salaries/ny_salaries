import requests
from requests.adapters import HTTPAdapter
from scrapy import Selector
import csv
import os

# --------------------define variables-------------------
# OUTPUT_FILE = 'new_york.csv'
# START_BRANCH = 'New York City'
# START_PAGE = 0
# START_RESULT_ID = '0'


# -------------------------------------------------------

# --------------------define global functions------------

# -----------------------------------------------------------------------------------------------------------------------
class NewYorkScraper:
    def __init__(self,
                 base_url='http://seethroughny.net/tools/required/reports/payroll'
                 ):
        # define session object
        self.session = requests.Session()
        self.session.mount('https://', HTTPAdapter(max_retries=4))

        # set proxy
        # self.session.proxies.update({'http': 'http://127.0.0.1:40328'})

        # define urls
        self.base_url = base_url

        # set headers
        self.SetHeaders()

    def SetHeaders(self):
        headers = {
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'en-US,en;q=0.9',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            # 'Cookie': 'CONCRETE5=ee42a210ebd94606d24c357c8feccbc8; _ga=GA1.2.197499532.1515427958; _gid=GA1.2.1701455529.1515427958',
            'Host': 'seethroughny.net',
            'Origin': 'http://seethroughny.net',
            'Proxy-Connection': 'keep-alive',
            'Referer': 'http://seethroughny.net/payrolls',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest'
        }
        self.session.headers = headers

    def GetYearList(self):
        return [
            #'2008',
            #'2009',
            '2010',
            '2011',
            '2012',
            '2013',
            '2014',
            '2015',
            '2016',
            '2017'
        ]

    def GetBranchList(self):
        return [
            # 'Cities',
            'Counties',
            'New York City',
            'Public Authorities',
            'Schools'#,
            # 'Special Districts',
            # 'State - Executive',
            # 'State - Judicial',
            # 'State - Legislative',
            # 'Towns',
            # 'Villages'
        ]

    def GetPageData(self, year, branch, page, result_id, file_name):
        # set get data
        params = {}
        params['action'] = 'get'

        # set post data
        data = {}
        data['PayYear[]'] = year
        data['BranchName[]'] = branch
        data['SortBy'] = 'YTDPay DESC'
        data['current_page'] = page
        data['result_id'] = result_id
        data['url'] = '/tools/required/reports/payroll?action=get'
        data['nav_request'] = '0'

        # set url
        url = self.base_url

        # get request
        ret = self.session.post(url, params=params, data=data)

        if ret.status_code == 200:
            if len(ret.json()['html']) == 0: return -1

            # get trs for result and expand
            html = ret.json()['html']
            result_trs = Selector(text=html).xpath('//tr[contains(@id, "resultRow")]').extract()
            expand_trs = Selector(text=html).xpath('//tr[contains(@id, "expandRow")]').extract()

            for idx in range(0, len(result_trs)):
                result_tr = result_trs[idx]
                result_tds = Selector(text=result_tr).xpath('//td/text()').extract()
                # print(result_tds)
                expand_tr = expand_trs[idx]
                expand_tr = str(expand_tr).replace('<one year in service>\n        </one>', ')</div>\n')

                # expand_td_0 = Selector(text=expand_tr).xpath('//td[2]/div[1]/div[2]/text()').extract()
                # if len(expand_td_0) > 0: expand_td_0 = expand_td_0[0]
                # else:  expand_td_0 = ''

                expand_td_1 = Selector(text=expand_tr).xpath('//td[2]/div[2]/div[2]/text()').extract()
                if len(expand_td_1) > 0:
                    expand_td_1 = expand_td_1[0]
                else:
                    expand_td_1 = ''

                expand_td_2 = Selector(text=expand_tr).xpath('//td[2]/div[3]/div[2]/text()').extract()
                if len(expand_td_2) > 0:
                    expand_td_2 = expand_td_2[0]
                else:
                    expand_td_2 = ''

                expand_td_3 = Selector(text=expand_tr).xpath('//td[2]/div[4]/div[2]/text()').extract()
                if len(expand_td_3) > 0:
                    expand_td_3 = expand_td_3[0]
                else:
                    expand_td_3 = ''

                expand_td_4 = Selector(text=expand_tr).xpath('//td[2]/div[5]/div[2]/text()').extract()
                if len(expand_td_4) > 0:
                    expand_td_4 = expand_td_4[0]
                else:
                    expand_td_4 = ''

                expand_td_5 = Selector(text=expand_tr).xpath('//td[2]/div[6]/div[2]/text()').extract()
                if len(expand_td_5) > 0:
                    expand_td_5 = expand_td_5[0]
                else:
                    expand_td_5 = ''

                # get data
                data = [
                    result_tds[0],
                    result_tds[1],
                    result_tds[2],
                    result_tds[3],
                    expand_td_1,
                    expand_td_2,
                    expand_td_3,
                    expand_td_4,
                    expand_td_5
                ]

                # write data into output csv file
                self.WriteData(data, file_name)

            return ret.json()['result_id']
        else:
            print('fail to get page data')

    def WriteHeader(self, file_name):
        # set headers
        header_info = []
        header_info.append('name')
        header_info.append('employer_agency')
        header_info.append('total_pay')
        header_info.append('subagency_type')
        header_info.append('title')
        header_info.append('rate_of_pay')
        header_info.append('year')
        header_info.append('pay_basis')
        header_info.append('branch')

        # write header into output csv file
        writer = csv.writer(open(file_name, 'w'), delimiter=',', lineterminator='\n')
        writer.writerow(header_info)

    def WriteData(self, data, file_name):
        # write data into output csv file
        writer = csv.writer(open(file_name, 'a'), delimiter=',', lineterminator='\n')
        writer.writerow(data)

    def Start(self):
        # get year list
        print('getting year list')
        year_list = self.GetYearList()

        # get branch list
        print('getting branch list')
        branch_list = self.GetBranchList()

        # flag = False
        for year in year_list:
            for branch in branch_list:
                page = 0
                result_id = '0'

                # if START_BRANCH == branch:
                #     flag = True
                #     page = START_PAGE
                #     result_id = START_RESULT_ID
                #
                # if flag == False: continue

                print('processing for %s:%s ...' % (year, branch))
                file_name = year + '_' + branch + '.csv'

                # write header into output csv file
                if page == 0: self.WriteHeader(year + '/' + file_name)

                while (True):
                    # get data and save it into csv file
                    print('getting data for %s page %s:%s ...' % (page, year, branch))
                    result_id = self.GetPageData(year, branch, page, result_id, year + '/' + file_name)
                    print(result_id)

                    if int(result_id) <= 0: break

                    page += 1


# ------------------------------------------------------- main -------------------------------------------------------
def main():
    # create scraper object
    scraper = NewYorkScraper()

    # start to scrape
    scraper.Start()


if __name__ == '__main__':
    main()
