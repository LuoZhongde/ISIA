# 使用python的selenium库进行数据抓取 (Используйте библиотеку селена Python для понимания данных)
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import time
import csv
import random

# 启动浏览器 (Начните браузер)
driver = webdriver.Edge()
# 最大化浏览器窗口 (Максимизировать окно браузера)
driver.maximize_window()
# 访问网址 (Посетите URL)
driver.get('https://www.jd.com')
time.sleep(90) # 登录账号 (Входная учетная запись)
# 通过CSS选择器查找元素，输入关键字后回车 (Найдите элемент через селектор CSS, введите ключевое слово после ввода ключевого слова)
driver.find_element(By.CSS_SELECTOR, '#key').send_keys('冬季外套')
# 回车搜索 (Вернуть поиск)
driver.find_element(By.CSS_SELECTOR, '#key').send_keys(Keys.ENTER)


# 滚动页面函数,javascript (Функция поверхности катящейся страницы, JavaScript)
def drop_down():
  for x in range(20):
    js = "window.scrollBy(0, " + str(x * 200) + ");"
    driver.execute_script(js)
    time.sleep(1)

# 创建一个空列表用于存储商品数据 (Создайте пустой список для хранения данных о продукте)
commodity_data = []

#由于遇到反网络爬虫程序，设置检测元素，以等待手动操作 （Установите элемент обнаружения на ожидание ручного действия из-за обнаружения программы защиты от веб-сканирования.）
def find_brand():
  max_attempts = 1500  # 最大尝试次数
  attempts = 0
  while attempts < max_attempts:
    try:
      brand_element = driver.find_element(By.XPATH, '//ul[@id="parameter-brand"]/li')
      return brand_element.text
    except NoSuchElementException:
      print("未找到品牌元素，正在尝试重新检索...")
      time.sleep(90)  # 可以根据需要调整等待时间
      attempts += 1
  print("达到最大尝试次数，未能找到品牌元素")
  return None


def get_commodity_info():
  # 获取所有商品数据对应标签 (Получите соответствующий тег всех данных продукта)
  lis = driver.find_elements(By.CSS_SELECTOR, '.gl-item')
  # for循环遍历 (для прохождения)
  for li in lis:
    title = li.find_element(By.CSS_SELECTOR, '.p-name a em').text  # 标题 (заголовок)
    price = li.find_element(By.CSS_SELECTOR, '.p-price strong i').text  # 价格 (цена)
    # 定位商品标签元素，click()点击进入详情页 (Размещение элементов метки продукта, нажмите () Нажмите, чтобы ввести страницу сведений)
    li.find_element(By.CSS_SELECTOR, '.p-name em').click()
    # 获取窗口句柄 (Получить ручку окон)
    windows = driver.window_handles
    # 切换窗口，windows[-1]最右边窗口 (Переключение окна, Windows [-1] в дальнем правом окне)
    driver.switch_to.window(windows[-1])
    time.sleep(1)
    '''
    driver.refresh()
    driver.implicitly_wait(10)
    time.sleep(random.uniform(1, 10))
    '''
    #title = driver.find_element(By.CSS_SELECTOR, '.sku-name').text  # 标题 (заголовок)
    #price = driver.find_element(By.CSS_SELECTOR, '.price').text  # 价格 (цена)
    #brand = driver.find_element(By.XPATH, '//ul[@id="parameter-brand"]/li').text # 品牌

    brand = find_brand()  # 品牌
    count = driver.find_element(By.CSS_SELECTOR, '.count').text  # 评论 (Комментарий)
    # 商品详情信息 (Информация о деталях продукта)
    info = driver.find_elements(By.CSS_SELECTOR, '.parameter2 li')

    # 创建一个空字典 (Создать пустой словарь)
    product_dict = {}
    # 遍历商品信息列表 (Список списка товаров)
    for i in info:
      # 使用字符串分割，以":"为分隔符 (Используйте строку для разделения, используйте ":" В качестве разделителя)
      info_list = i.text.split("：", 1)
      # 去除前后空格 (Снимите передние и задние пространства)
      key = info_list[0].strip()
      value = info_list[1].strip()
      # 将当前键值对添加到字典中 (Добавьте значение текущего ключа в словарь)
      product_dict.update({key: value})

    #打开评分页面 (Откройте страницу оценки)
    driver.find_element(By.XPATH, '//li[@data-tab="trigger" and contains(@clstag, "shangpinpingjia")]').click()
    rating = driver.find_element(By.CLASS_NAME, 'percent-con').text  # 评分

    dit_commodity_data = {
      'title': title,
      'price': price,
      'count': count,
      'rating': rating,
      'brand': brand,
      'info_dict': product_dict
    }
    print(title, price, count, rating, brand, product_dict)

    # 将商品数据添加到列表中 (Добавить данные продукта в список)
    commodity_data.append(dit_commodity_data)
    #关闭窗口 (закройте окно)
    driver.close()
    driver.switch_to.window(windows[0])


#翻页 (Страницы)
for page in range(1,2):
  # 等待元素加载 (Нагрузка элемента ожидания)
  driver.implicitly_wait(10)
  drop_down()
  time.sleep(5)
  get_commodity_info()
  driver.implicitly_wait(10)
  #点击下一页 (Нажмите на следующую страницу)
  driver.find_element(By.CSS_SELECTOR, '.pn-next').click()

# 关闭浏览器 (Закрыть браузер)
driver.quit()

# 将商品数据保存到CSV文件中 (Сохранить данные продукта в файле CSV)
csv_file_path = '京东冬季外套数据1.0.csv'
csv_columns = ['title', 'price', 'count', 'rating', 'brand', 'info_dict']

with open(csv_file_path, 'w', encoding='utf-8', newline='') as csv_file:
    writer = csv.DictWriter(csv_file, fieldnames=csv_columns)
    writer.writeheader()
    for data in commodity_data:
        writer.writerow(data)

print(f"数据已保存到 {csv_file_path} 文件中")







