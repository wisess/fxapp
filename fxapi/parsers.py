from selenium import webdriver
from time import sleep
from bs4 import BeautifulSoup
import requests, csv, os
from progress.bar import IncrementalBar

EXP_LIST_DIR_PATH 	= os.getenv("EXPIRATIONS_LIST_DIR_PATH")
EXP_LIST_FILE_PATH 	= os.getenv("EXPIRATIONS_LIST_FILE_PATH")
REVERSE_SYMBOLS		= ("CAD" , "CHF" , "JPY")

class DownloadExpirationsList:

	def __init__(self):
		fp = webdriver.FirefoxProfile()
		fp.set_preference("browser.download.folderList",2)
		fp.set_preference("browser.download.manager.showWhenStarting",False)
		fp.set_preference("browser.download.dir", EXP_LIST_DIR_PATH)
		fp.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/csv")
		fp.set_preference("plugin.disable_full_page_plugin_for_types", "application/csv")
		self.driver = webdriver.Firefox(fp)

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
		# bar = IncrementalBar('Parsing ', max = 1)
		# bar.next()
		# bar.finish()
		with open(EXP_LIST_FILE_PATH, "r") as f_obj:
			reader = csv.reader(f_obj)
			for row in reader:
				row_elements = row[1].split(' ')
				if len(row_elements)>1:
					symbol_name = self.normalize_symbol_name(row_elements[0])
					print(row_elements[2])