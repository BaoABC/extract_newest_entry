import requests
from bs4 import BeautifulSoup

def extract_newest_entry(url):
    """
    请求指定URL页面，查找页面中第一个表格，并返回表格中最新的一行数据（假设为最后一行）
    """
    try:
        response = requests.get(url)
        response.raise_for_status()
    except Exception as e:
        print(f"请求URL失败：{e}")
        return None

    soup = BeautifulSoup(response.text, 'html.parser')
    # 查找页面中的第一个表格
    table = soup.find('table')
    if not table:
        print("页面中没有找到表格")
        return None

    # 获取所有行（tr标签）
    rows = table.find_all('tr')
    if not rows:
        print("表格中没有数据行")
        return None

    # 如果表格第一行是表头（含有th标签），则数据行从第二行开始
    if rows[0].find_all('th'):
        data_rows = rows[1:]
    else:
        data_rows = rows

    if not data_rows:
        print("没有找到数据行")
        return None

    # 假设最新的数据在最后一行
    newest_row = data_rows[-1]
    # 提取该行中所有单元格的文本内容
    cells = newest_row.find_all(['td', 'th'])
    entry = [cell.get_text(strip=True) for cell in cells]
    return entry

if __name__ == '__main__':
    url = input("请输入包含表格的页面URL: ")
    newest_entry = extract_newest_entry(url)
    if newest_entry:
        print("最新的一行数据:", newest_entry)
    else:
        print("未能提取到最新数据")
