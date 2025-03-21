import requests
from bs4 import BeautifulSoup
from flask import Flask, request, jsonify

app = Flask(__name__)

def extract_newest_entry_from_html(html):
    """
    从 HTML 内容中提取第一个表格的最新数据行（假设最新数据为最后一行）
    
    参数:
        html (str): 网页的 HTML 内容
        
    返回:
        list: 最新一行数据中各单元格的文本列表
        
    异常:
        ValueError: 当页面中未找到表格或数据行时抛出异常
    """
    soup = BeautifulSoup(html, 'html.parser')
    # 查找页面中的第一个表格
    table = soup.find('table')
    if not table:
        raise ValueError("页面中未找到表格数据")
    
    # 获取所有表格行
    rows = table.find_all('tr')
    if not rows:
        raise ValueError("表格中没有数据行")
    
    # 判断首行是否为表头（存在<th>标签），若是则数据行从第二行开始
    data_rows = rows[1:] if rows[0].find_all('th') else rows
    if not data_rows:
        raise ValueError("没有找到数据行")
    
    # 假设最新数据在最后一行
    newest_row = data_rows[-1]
    cells = newest_row.find_all(['td', 'th'])
    return [cell.get_text(strip=True) for cell in cells]

@app.route('/', methods=['GET'])
def index():
    """
    HTTP GET 接口
    请求示例: GET /?url=https://example.com/page-with-table
    返回:
        JSON 格式，包含最新一行数据或错误信息
    """
    url = request.args.get('url')
    if not url:
        return jsonify({"error": "缺少 url 参数"}), 400

    try:
        # 获取目标页面内容
        response = requests.get(url)
        response.raise_for_status()
        # 提取最新数据行
        newest_entry = extract_newest_entry_from_html(response.text)
        return jsonify({"newest_entry": newest_entry})
    except requests.RequestException as e:
        return jsonify({"error": f"请求目标页面失败: {e}"}), 500
    except ValueError as ve:
        return jsonify({"error": str(ve)}), 400
    except Exception as ex:
        return jsonify({"error": f"未知错误: {ex}"}), 500

if __name__ == '__main__':
    # 本地调试时启动 Flask 服务
    app.run(debug=True)
