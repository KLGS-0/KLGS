# 导入库
from flask import Flask, request, jsonify
import pandas as pd

app = Flask(__name__)

# 加载模型
# frequent_itemsets 通常包含 'support' 和 'itemsets' 列，且按 support 降序排列
frequent_itemsets = pd.read_pickle('./association_rules/frequent_itemsets.pkl')
rules = pd.read_pickle('./association_rules/rules.pkl')


@app.route("/")
def hello():
    return "Hello World!"


@app.route('/recommend', methods=['POST'])
def recommend():
    data = request.json.get('items', [])

    # 生成关联规则推荐
    recommendDations = []
    for idx, rule in rules.iterrows():
        antecedents = list(rule['antecedents'])
        consequents = list(rule['consequents'])
        # 检查前件是否跟输入匹配
        if set(antecedents).issubset(set(data)):
            recommendDations.extend(consequents)

    # 去重
    recommendDations = list(set(recommendDations) - set(data))

    # 当推荐内容为空时，返回一个热门的菜品
    if not recommendDations:
        # 获取 frequent_itemsets 中支持度最高的第一项
        # 假设 itemsets 列存储的是 frozenset，我们需要从中提取出商品名称
        top_item_set = frequent_itemsets.iloc[0]['itemsets']

        # 如果 itemsets 是集合（frozenset），将其转换为列表
        if isinstance(top_item_set, frozenset):
            recommendDations = list(top_item_set)
        else:
            # 如果不是集合（极少情况），直接放入列表
            recommendDations = [top_item_set]

    # 返回推荐结果
    return jsonify({'recommendDations': recommendDations})


if __name__ == "__main__":
    app.run(debug=True)