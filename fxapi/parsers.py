from selenium import webdriver
from time import sleep
from bs4 import BeautifulSoup
import requests, csv, os
from progress.bar import IncrementalBar
from . import utils

EXP_LIST_DIR_PATH 	= os.getenv("EXPIRATIONS_LIST_DIR_PATH")
EXP_LIST_FILE_PATH 	= os.getenv("EXPIRATIONS_LIST_FILE_PATH")
REVERSE_SYMBOLS		= ("CAD" , "CHF" , "JPY")

class DownloadExpirationsList:

	def __init__(self):
		self.display = None
		self.driver = None

	def _display_start(self):
		self._display_stop()
		try:
			self.display = Display(visible=0, size=(1920, 1080))
			self.display.start()
		except:
			print('Start without virtual display')

	def _display_stop(self):
		try:
			self.display.stop()
		except:
			pass

	def _webdriver_start(self):
		fp = webdriver.FirefoxProfile()
		fp.set_preference("browser.download.folderList",2)
		fp.set_preference("browser.download.manager.showWhenStarting",False)
		fp.set_preference("browser.download.dir", EXP_LIST_DIR_PATH)
		fp.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/csv")
		fp.set_preference("plugin.disable_full_page_plugin_for_types", "application/csv")
		driver = webdriver.Firefox(fp)
		driver.maximize_window()
		driver.implicitly_wait(15)
		self.driver = driver

	def _webdriver_stop(self):
		try:
			self.driver.quit()
		except:
			pass

	def open(self):
		self._display_start()
		self._webdriver_start()

	def close(self):
		self._webdriver_stop()
		self._display_stop()

	def download(self):
		data_set = {}
		symbol_index = '0'
		bar = IncrementalBar('Downloading ', max = 12)

		self.driver.get('https://www.cmegroup.com/tools-information/quikstrike/options-calendar.html')
		first_window=self.driver.window_handles[0]
		bar.next()
		sleep(5)
		self.driver.get('https://cmegroup-tools.quikstrike.net/User/QuikStrikeView.aspx?viewitemid=IntegratedCMEOptionExpirationCalendar')
		bar.next()
		sleep(5)
		self.driver.find_element_by_xpath('//a[@id="MainContent_ucViewControl_IntegratedCMEOptionExpirationCalendar_ucViewControl_hlCMEProducts"]').click()
		bar.next()
		sleep(5)
		for handle in self.driver.window_handles:
			if handle != first_window:
				second_window = handle
				self.driver.switch_to_window(handle)
				self.driver.find_element_by_xpath('//a[@id="ctl00_cphMain_lvTabs_ctrl3_lbTab"]').click()
				bar.next()
				sleep(2)
				self.driver.find_element_by_xpath('//a[@id="cphMain_ucProductBrowser_ucProductFilter_ucTrigger_lnkTrigger"]').click()
				bar.next()
				sleep(2)
				self.driver.find_element_by_xpath('//input[@id="cphMain_ucProductBrowser_ucProductFilter_ucGroupList_rblGroups_4"]').click()
				bar.next()
				sleep(2)
				self.driver.find_element_by_xpath('//input[@id="cphMain_ucProductBrowser_ucProductFilter_ucContractTypeList_rblContractType_1"]').click()
				bar.next()
				sleep(2)
				self.driver.find_element_by_xpath('//input[@id="cphMain_ucProductBrowser_ucProductFilter_btnApply"]').click()
				bar.next()
				sleep(2)
				self.driver.find_element_by_xpath('//a[@id="cphMain_ucProductBrowser_ucProductActions_ucTrigger_lnkTrigger"]').click()
				bar.next()
				sleep(2)
				self.driver.find_element_by_xpath('//a[@id="cphMain_ucProductBrowser_ucProductActions_lnkShowExpirations"]').click()
				bar.next()
				sleep(2)
				iframe = self.driver.find_element_by_xpath('//iframe[@id="mainFrame"]')
				self.driver.switch_to_frame(iframe)
				bar.next()
				sleep(2)
				self.driver.find_element_by_xpath('//a[@id="ctl03_ucExport_lnkTrigger"]').click()
				bar.next()
				sleep(5)
				self.driver.quit()
				self._display_stop()
				bar.finish()
				

class ParseExpirationsList:

	def __init__(self):
		pass

	def normalize_symbol_name(self, raw_name):
		parts_name 		= raw_name.split("/")
		if len(parts_name)<2:
			return 0
		normalize_name 	= parts_name[0]+parts_name[1]
		return normalize_name

	def parse(self):
		result = []
		with open(EXP_LIST_FILE_PATH, "r") as f_obj:
			reader = csv.reader(f_obj)
			for row in reader:
				second_col_elements = row[1].split(' ')
				if len(second_col_elements)>1:
					symbol_name = self.normalize_symbol_name(second_col_elements[0])
					if second_col_elements[1] == "Monthly" and second_col_elements[2]=="Options" and \
						(symbol_name!="EURCHF" and symbol_name!="EURGBP" and symbol_name!="EURJPY" and symbol_name!="NZDUSD"):
							filtered_monthly_data = [symbol_name, second_col_elements[1], row[2], row[5].split(' ')[0]]
							result.append(filtered_monthly_data)
					elif second_col_elements[1] == "Weekly" and second_col_elements[3]=="Options" and \
							(symbol_name!="EURCHF" and symbol_name!="EURGBP" and symbol_name!="EURJPY" and symbol_name!="NZDUSD"):
								filtered_weekly_data = [symbol_name, second_col_elements[2], row[2], row[5].split(' ')[0]]
								result.append(filtered_weekly_data)
		return result

class ParseSettleDataFromCme:
	MAIN_URL 			= 'https://www.cmegroup.com/tools-information/quikstrike/option-settlement.html'
	STRIKES_URL 		= 'https://cmegroup-tools.quikstrike.net/User/QuikStrikeView.aspx?pid={pid}&pf=61&viewitemid=IntegratedSettlementSheet'
	OPTION_TAB_ID		= 'ctl00_ucSelector_lvGroups_ctrl{option_index}_lbGroup'
	OPTION_GROUP_ID		= 'ctl00_ucSelector_lvGroups_ctrl{option_index}_ctl00_pnlExpirationGroupPopup'
	OPTION_UL_CLASS		= 'nav'
	OPTION_SPAN_CLASS	= 'item-name'
	ROW_QUANTITY_ID		= 'MainContent_ucViewControl_IntegratedSettlementSheet_ddlStrikeCount'
	ROW_QUANTITY_VALUE	= '25'
	MONTHLY_OPTION 		= 'Monthly'
	FRIDAY_OPTION 		= 'Friday'
	WEDNESDAY_OPTION 	= 'Wednesday'
	MONTHLY_INDEX		= 0
	FRIDAY_INDEX		= 2
	WEDNESDAY_INDEX		= 3

	def __init__(self, option):
		self.driver 		= webdriver.Firefox()
		self.symbol 		= option.symbol
		self.pid			= option.symbol.cme_pid
		self.cab			= option.symbol.cab
		self.option_type 	= option.option_type
		self.option_code 	= option.option_code

	def parse(self):
		url = self.STRIKES_URL.format(pid=self.pid)
		option_index = 0
		self.driver.get(self.MAIN_URL)
		sleep(3)
		self.driver.get(url)
		sleep(3)
		if self.option_type == self.MONTHLY_OPTION:
			option_index = self.MONTHLY_INDEX
		elif self.option_type == self.FRIDAY_OPTION:
			option_index = self.FRIDAY_INDEX
			if self.symbol.symbol != "JPYUSD":
				raw_code = self.option_code
				self.option_code = raw_code[1]+raw_code[2]+raw_code[0]+raw_code[3]+raw_code[4]
		elif self.option_type == self.WEDNESDAY_OPTION:
			option_index = self.WEDNESDAY_INDEX
		self.driver.find_element_by_xpath('//a[@id="'+ self.OPTION_TAB_ID.format(option_index=option_index) +'"]').click()
		sleep(3)
		soup = BeautifulSoup(self.driver.page_source, 'html.parser')
		div_list = soup.find('div', {'id': self.OPTION_GROUP_ID.format(option_index=option_index)})
		li_list = div_list.find('ul', {'class': self.OPTION_UL_CLASS}).find_all('li')
		for li in li_list:
			if li.find('span', {'class': self.OPTION_SPAN_CLASS}).text == self.option_code:
				put_strike	= 0
				call_strike = 0
				balance		= 0
				link_id = li.find('a').attrs['id']
				self.driver.find_element_by_xpath('//a[@id="'+ link_id +'"]').click()
				self.driver.find_element_by_xpath('//select[@id="'+ self.ROW_QUANTITY_ID +'"]/option[@value="'+ self.ROW_QUANTITY_VALUE +'"]').click()
				sleep(3)
				soup = BeautifulSoup(self.driver.page_source, 'html.parser')
				strikes_data = []
				table = soup.find('table', {'id': 'pricing-sheet'})
				for row in table.tbody.find_all('tr'):
					tds = row.find_all('td')
					tds = [td for td in tds if 'hide' not in td.attrs.get('class', [])]
					#strike_items = [float(tds[2].text.strip()), float(tds[3].text.strip()), float(tds[4].text.strip())]
					strike_items = [utils.str_to_numbers(tds[2].text), utils.str_to_numbers(tds[3].text), utils.str_to_numbers(tds[4].text)]
					strikes_data.append(strike_items)
				for strike_item in strikes_data:
					if strike_item[0] == self.cab:
						call_strike = strike_item[1]
						break
					else: 
						continue
				reverse_strikes_data = sorted(strikes_data, key=lambda item: item[1], reverse=True) 
				for strike_item in reverse_strikes_data:
					if strike_item[2] == self.cab:
						put_strike = strike_item[1]
						break
					else:
						continue
				balance = round((call_strike+put_strike)/2, 5)
				cab_data = {
					"call_strike"	:call_strike,
					"balance"		:balance,
					"put_strike"	:put_strike,
				}
				return cab_data
		return 0
		