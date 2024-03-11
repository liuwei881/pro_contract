# coding=utf-8

import sqlite3
import datetime
from flask import Flask
from flask import request, jsonify, render_template

app = Flask(__name__)
conn = sqlite3.connect('/Users/liuwei/Downloads/星链/pro_contract/contract.db', check_same_thread=False)

# f = conn.execute("select * from main.project").fetchall()
# print(f)
# conn.commit()

@app.route("/", methods=['GET'])
def get_project():
    """
    获取项目信息
    :return:
    """
    list = conn.execute("select * from main.project").fetchall()
    return render_template('index.html',list=list)


@app.route("/project", methods=['GET', 'POST', 'PUT'])
def project():
    """
    创建项目
    :return:
    """
    if request.method == 'POST':
        pro_name = request.form.get('pro_name') # 项目名称
        c_project = request.form.get('c_project') # 立项
        research = request.form.get('research') # 可研
        start = request.form.get('start') # 初设
        create_time = datetime.datetime.now()
        comment = request.form.get('comment') # 备注
        try:
            # 插入项目表
            sql = f"INSERT INTO main.project ('pro_name', 'c_project', 'research', 'start', 'comment', 'create_time') " \
                f"VALUES ('{pro_name}', '{c_project}', '{research}', '{start}', '{comment}', '{create_time}')"
            conn.execute(sql)
            conn.commit()
        except Exception as ex:
            return jsonify({'result': f'插入项目表异常{ex}'})
    #     try:
    #         sql = f"INSERT INTO main.capital ('allow_file', 'allow_money') " \
    #               f"VALUES ('{allow_file}', '{allow_money}')"
    #         conn.execute(sql)
    #         conn.commit()
    #     except Exception as ex:
    #         return jsonify({'result': f'插入资金表异常{ex}'})
    #     try:
    #         sql = f"INSERT INTO main.contract ('contract_values', 'payment', 'allow_nopay', 'pay_time', 'clear_time', 'party_unit', 'name') " \
    #               f"VALUES ('{contract_values}', '{payment}', '{allow_nopay}', '{pay_time}', '{clear_time}', '{party_unit}', '{name}')"
    #         conn.execute(sql)
    #         conn.commit()
    #     except Exception as ex:
    #         return jsonify({'result': f'插入合同表异常{ex}'})
    #     try:
    #         sql = f"INSERT INTO main.capital_channel ('name')" \
    #               f"VALUES ('{capital_channel}')"
    #         conn.execute(sql)
    #         conn.commit()
    #     except Exception as ex:
    #         return jsonify({'result': f'插入资金渠道表异常{ex}'})
    #     try:
    #         # 插入项目表合同id，资金表id
    #         sql = f"SELECT id FROM contract WHERE name='{name}'"
    #         r = conn.execute(sql).fetchone()
    #         v = int(r[0])
    #         update_sql = f"UPDATE project SET contract_id={v} " \
    #                      f"WHERE pro_name='{pro_name}'"
    #         conn.execute(update_sql)
    #         conn.commit()
    #         # 插入资金表id
    #         sql = f"SELECT id FROM capital " \
    #               f"WHERE allow_file='{allow_file}'" \
    #               f"and allow_money='{allow_money}'"
    #         r = conn.execute(sql).fetchone()
    #         v = int(r[0])
    #         update_sql = f"UPDATE project SET capital_id={v} " \
    #                      f"WHERE pro_name='{pro_name}'"
    #         conn.execute(update_sql)
    #         conn.commit()
    #     except Exception as ex:
    #         return jsonify({'result': f'插入项目表资金, 合同id异常{ex}'})
    #     try:
    #         # 插入资金下达表项目id, 资金渠道id
    #         pass
    #     except Exception as ex:
    #         return jsonify({'result': f'插入资金下达表项目id, 资金渠道id异常{ex}'})
    #     try:
    #         # 插入合同表资金渠道id, 项目id
    #         pass
    #     except Exception as ex:
    #         return jsonify({'result': f'插入合同表资金渠道id, 项目id异常{ex}'})
    #     return jsonify({'result': 'ok'})
    elif request.method == 'GET':
        sql = f"SELECT * FROM main.project"
        list = conn.execute(sql).fetchall()
        return render_template('project.html', list=list)
    elif request.method == 'PUT':
        pass

    return "<p>Hello, World!</p>"

@app.route("/contract", methods=['GET', 'POST', 'PUT'])
def contract():
    """
    创建合同
    :return:
    """
    if request.method == 'POST':
        name = request.form.get('name') # 合同名
        capital_channel = request.form.get('capital_channel') # 资金渠道
        contract_values = request.form.get('contract_values') # 合同值
        payment = request.form.get('payment') # 已支付
        allow_nopay = request.form.get('allow_nopay') # 已申请未支付
        pay_time = request.form.get('pay_time') # 支付时间
        check_clear = request.form.get('check_clear') # 结算值
        party_unit = request.form.get('party_unit') # 乙方单位
        pro_name = request.form.get('project_name') # 项目名称
        try:
            # 插入合同表
            sql = f"INSERT INTO main.contract ('name', 'capital_channel', 'contract_values', 'payment', 'allow_nopay', 'pay_time', 'check_clear', 'party_unit') " \
                f"VALUES ('{name}', '{capital_channel}', '{contract_values}', '{payment}', '{allow_nopay}', '{pay_time}', '{check_clear}', '{party_unit}') returning id"
            contract_id = conn.execute(sql)
            conn.commit()
        except Exception as ex:
            return jsonify({'result': f'插入合同表异常{ex}'})
        try:
            # 插入project_contract表
            sql = f"SELECT id FROM main.project " \
                  f"WHERE pro_name='{pro_name}'"
            project_id = int(conn.execute(sql).fetchone()[0])
            insert_sql = f"INSERT INTO project_contract ('project_id', 'contract_id') " \
                         f"VALUES ({project_id}, {contract_id})"
            conn.execute(insert_sql)
            conn.commit()
        except Exception as ex:
            return jsonify({'result': f'插入project_contract表异常{ex}'})
    elif request.method == 'GET':
        pass
    elif request.method == 'PUT':
        pass
        return


@app.route("/capital", methods=['GET', 'POST', 'PUT'])
def capital():
    """
    资金下达
    :return:
    """
    if request.method == 'POST':
        allow_file = request.form.get('allow_file') # 批复文件
        allow_money = request.form.get('allow_money') # 下达金额
        capital_channel = request.form.get('capital_channel') # 资金渠道
        pro_name = request.form.get('project_name')  # 项目名称
        try:
            # 插入资金表
            sql = f"INSERT INTO main.capital ('allow_file', 'allow_money', 'capital_channel') " \
                f"VALUES ('{allow_file}', '{allow_money}', '{capital_channel}')"
            conn.execute(sql)
            conn.commit()
        except Exception as ex:
            return jsonify({'result': f'插入资金表异常{ex}'})
        try:
            # 插入project_capital表
            sql = f"SELECT id FROM main.project " \
                  f"WHERE pro_name='{pro_name}'"
            capital_id = int(conn.execute(sql).fetchone()[0])
            insert_sql = f"INSERT INTO project_capital ('project_id', 'capital_id') " \
                         f"VALUES ({project_id}, {capital_id})"
            conn.execute(insert_sql)
            conn.commit()
        except Exception as ex:
            return jsonify({'result': f'插入project_contract表异常{ex}'})
    elif request.method == 'GET':
        pass
    elif request.method == 'PUT':
        pass
    return


@app.route("/capital_channel", methods=['GET', 'POST', 'PUT'])
def capital_channel():
    """
    资金渠道, 留出接口, 以后可能用到
    :return:
    """
    if request.method == 'POST':
        name = request.form.get('name') # 渠道名称
        conn.execute(f"INSERT INTO capital_channel VALUES {name}")
        conn.commit()
        return jsonify({"name": name})
    elif request.method == 'GET':
        result = conn.execute("SELECT * from main.capital_channel").fetchall()
        return render_template('channel.html', result=result)
    elif request.method == 'PUT':
        pass

if __name__ == '__main__':
    app.run()