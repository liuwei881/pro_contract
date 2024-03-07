# coding=utf-8

import sqlite3
from flask import Flask
from flask import request, jsonify, render_template

app = Flask(__name__)
conn = sqlite3.connect('/Users/liuwei/Downloads/星链/pro_contract/contract.db', check_same_thread=False)

# f = conn.execute("select * from main.project").fetchall()
# print(f)
# conn.commit()

@app.route("/project", methods=['GET'])
def get_project():
    """
    获取项目信息
    :return:
    """
    list = conn.execute("select * from main.project").fetchall()
    return render_template('index.html',list=list)

@app.route("/create_project", methods=['POST'])
def create_project():
    """
    创建项目
    :return:
    """
    pro_name = request.form.get('pro_name') # 项目名称
    c_project = request.form.get('c_project') # 立项
    research = request.form.get('research') # 可研
    start = request.form.get('start') # 初设
    create_time = request.form.get('create_time')
    modify_time = request.form.get('modify_time')
    allow_file = request.form.get('allow_file') # 批复文件
    allow_money = request.form.get('allow_money') # 允许资金
    capital_channel = request.form.get('capital_channel') # 资金渠道
    comment = request.form.get('comment') # 备注

    return "<p>Hello, World!</p>"

@app.route("/create_contract", methods=['POST'])
def contract():
    """
    创建合同
    :return:
    """
    name = request.form.get('name') # 合同名
    capital_channel = request.form.get('capital_channel') # 资金渠道
    contract_values = request.form.get('contract_values') # 合同值
    payment = request.form.get('payment') # 已支付
    allow_nopay = request.form.get('allow_nopay') # 已申请未支付
    pay_time = request.form.get('pay_time') # 支付时间
    check_clear = request.form.get('check_clear') # 结算值
    party_unit = request.form.get('party_unit') # 乙方单位
    return


@app.route("/capital", methods=['POST'])
def capital():
    """
    资金下达
    :return:
    """
    allow_file = request.form.get('allow_file') # 批复文件
    allow_money = request.form.get('allow_money') # 下达金额


