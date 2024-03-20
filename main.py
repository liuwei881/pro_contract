# coding=utf-8

import sqlite3
import datetime
import xlrd
import os
from datetime import datetime
from xlrd import xldate_as_tuple
from flask import Flask
from flask import request, jsonify, render_template, redirect, url_for
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = './'
ALLOWED_EXTENSIONS = {'xlsx'}

app = Flask(__name__)
conn = sqlite3.connect('/Users/liuwei/Downloads/星链/pro_contract/contract.db', check_same_thread=False)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/", methods=['GET'])
def start():
    """
    开始页面
    :return:
    """
    return render_template('index.html')


@app.route("/project/<int:page>", methods=['GET', 'POST'])
@app.route("/project/", methods=['GET', 'POST'])
def project(page=1):
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
        return render_template('project.html')
    elif request.method == 'GET':
        limit = 10
        offset = 5 * int(page) - 5
        sql = f"SELECT p.id, p.pro_name, p.c_project, " \
              f"p.research, p.start, " \
              f"p.create_time, p.comment, " \
              f"c.name, lc.name, c.contract_values," \
              f"c.payment, c.allow_nopay, c.pay_time, c.final_value," \
              f"c.party_unit FROM " \
              f"project p LEFT JOIN project_contract pc ON " \
              f"pc.project_id=p.id LEFT JOIN contract c ON c.id=pc.contract_id " \
              f"LEFT JOIN project_capital pp ON pp.project_id=p.id " \
              f"LEFT JOIN capital cp ON cp.id=pp.capital_id " \
              f"LEFT JOIN project_channel tc ON tc.project_id=p.id " \
              f"LEFT JOIN channel lc ON lc.id=tc.channel_id " \
              f"ORDER BY p.id DESC LIMIT {limit} offset {offset}"
        list = conn.execute(sql).fetchall()
        total = len(list)
        return render_template('project.html', list=list, total=total)

@app.route("/search_project/", methods=['GET', 'POST'])
def search_project():
    """
    项目搜索
    :return:
    """
    searchKey = request.form.get("searchKey")
    limit = 10
    page = 1
    offset = 5 * int(page) - 5
    if searchKey:
        sql = f"SELECT p.id, p.pro_name, p.c_project, " \
              f"p.research, p.start, p.create_time, p.comment, " \
              f"c.name, lc.name as channel, c.contract_values," \
              f"c.payment, c.allow_nopay, c.pay_time, c.final_value," \
              f"c.party_unit FROM " \
              f"project p LEFT JOIN project_contract pc ON " \
              f"pc.project_id=p.id LEFT JOIN contract c ON c.id=pc.contract_id " \
              f"LEFT JOIN project_capital pp ON pp.project_id=p.id " \
              f"LEFT JOIN capital cp ON cp.id=pp.capital_id " \
              f"LEFT JOIN project_channel tc ON tc.project_id=p.id " \
              f"LEFT JOIN channel lc ON lc.id=tc.channel_id " \
              f"WHERE p.pro_name like '%{searchKey}%'" \
              f"ORDER BY p.id DESC LIMIT {limit} offset {offset}"
        list = conn.execute(sql).fetchall()
        total = len(list)
    else:
        sql = f"SELECT p.pro_name, p.c_project, " \
              f"p.research, p.start, p.create_time, " \
              f"p.comment, c.name, lc.name as channel, c.contract_values," \
              f"c.payment, c.allow_nopay, c.pay_time, c.final_value," \
              f"c.party_unit FROM " \
              f"project p LEFT JOIN project_contract pc ON " \
              f"pc.project_id=p.id LEFT JOIN contract c ON c.id=pc.contract_id " \
              f"LEFT JOIN project_capital pp ON pp.project_id=p.id " \
              f"LEFT JOIN capital cp ON cp.id=pp.capital_id " \
              f"LEFT JOIN project_channel tc ON tc.project_id=p.id " \
              f"LEFT JOIN channel lc ON lc.id=tc.channel_id " \
              f"ORDER BY p.id DESC LIMIT {limit} offset {offset}"
        list = conn.execute(sql).fetchall()
        total = len(list)
    return render_template('project.html', list=list, total=total)

@app.route("/edit_project/<int:id>/", methods=['POST'])
def edit_project(id):
    """
    编辑项目
    :return:
    """
    if request.method == 'POST':
        c_project = request.form.get('c_project') # 立项
        research = request.form.get('research') # 可研
        start = request.form.get('start') # 初设
        modify_time = datetime.datetime.now()
        comment = request.form.get('comment') # 备注
        try:
            # 修改项目表
            sql = f"UPDATE project SET " \
                  f"c_project='{c_project}', research='{research}'," \
                  f"start='{start}', modify_time='{modify_time}'," \
                  f"comment='{comment}'" \
                  f"WHERE id={id}"
            conn.execute(sql)
            conn.commit()
        except Exception as ex:
            return jsonify({'result': f'修改项目表异常{ex}'})
    return redirect("/project/")


@app.route("/contract/<int:page>", methods=['GET','POST'])
@app.route("/contract/", methods=['GET','POST'])
def contract(page=1):
    """
    创建合同
    :return:
    """
    if request.method == 'POST':
        name = request.form.get('name') # 合同名
        channel = request.form.get('channel') # 资金渠道
        contract_values = request.form.get('contract_values') # 合同值
        payment = request.form.get('payment') # 已支付
        allow_nopay = request.form.get('allow_nopay') # 已申请未支付
        pay_time = request.form.get('pay_time') # 支付时间
        final_value = request.form.get('final_value') # 结算值
        party_unit = request.form.get('party_unit') # 乙方单位
        pro_name = request.form.get('pro_name') # 项目名称
        try:
            # 插入合同表
            sql = f"INSERT INTO main.contract ('name', 'contract_values', 'payment', 'allow_nopay', 'pay_time', 'final_value', 'party_unit') " \
                f"VALUES ('{name}', '{contract_values}', '{payment}', '{allow_nopay}', '{pay_time}', '{final_value}', '{party_unit}') returning id"
            contract_id = conn.execute(sql).lastrowid
            conn.commit()
        except Exception as ex:
            return jsonify({'result': f'插入合同表异常{ex}'})
        try:
            # 插入project_contract表
            sql = f"SELECT id FROM main.project " \
                  f"WHERE pro_name='{pro_name}'"
            project_id = conn.execute(sql).fetchone()[0]
            insert_sql = f"INSERT INTO project_contract ('project_id', 'contract_id') " \
                         f"VALUES ({project_id}, {contract_id})"
            conn.execute(insert_sql)
            conn.commit()
        except Exception as ex:
            return jsonify({'result': f'插入project_contract表异常{ex}'})
        try:
            # 插入contract_channel表
            sql = f"SELECT id FROM main.channel " \
                  f"WHERE name='{channel}'"
            channel_id = conn.execute(sql).fetchone()[0]
            insert_sql = f"INSERT INTO contract_channel ('channel_id', 'contract_id') " \
                         f"VALUES ({channel_id}, {contract_id})"
            conn.execute(insert_sql)
            conn.commit()
        except Exception as ex:
            return jsonify({'result': f'插入contract_channel表异常{ex}'})
    elif request.method == 'GET':
        limit = 10
        offset = 5 * int(page) - 5
        sql = f"SELECT c.id, p.pro_name, lc.name as channel, c.name, " \
              f"c.contract_values, " \
              f"c.payment, c.allow_nopay, " \
              f"c.pay_time, c.final_value, c.party_unit FROM " \
              f"contract c LEFT JOIN project_contract pc ON " \
              f"pc.contract_id=c.id LEFT JOIN project p ON p.id=pc.project_id " \
              f"LEFT JOIN contract_channel tc ON tc.contract_id=c.id " \
              f"LEFT JOIN channel lc ON lc.id=tc.channel_id " \
              f"ORDER BY c.id DESC LIMIT {limit} offset {offset}"
        list = conn.execute(sql).fetchall()
        count_sql = f"SELECT SUM(contract_values) FROM contract"
        count = conn.execute(count_sql).fetchall()
        depart_sql = f"SELECT lc.name, SUM(c.payment) " \
              f"FROM contract c LEFT JOIN contract_channel tc ON tc.contract_id=c.id " \
              f"LEFT JOIN channel lc ON lc.id=tc.channel_id " \
              f"Group by lc.name "
        depart = conn.execute(depart_sql).fetchall()
        total = len(list)
        return render_template('/contract.html', list=list, count=count, depart=depart, total=total)
    return redirect("/contract/")


@app.route("/edit_contract/<int:id>/", methods=['POST'])
def edit_contract(id):
    """
    修改合同
    :return:
    """
    if request.method == 'POST':
        name = request.form.get('name') # 合同名
        contract_values = request.form.get('contract_values') # 合同值
        payment = request.form.get('payment') # 已支付
        allow_nopay = request.form.get('allow_nopay') # 已申请未支付
        pay_time = request.form.get('pay_time') # 支付时间
        final_value = request.form.get('final_value') # 结算值
        party_unit = request.form.get('party_unit') # 乙方单位
        try:
            # 修改合同表
            sql = f"UPDATE contract SET " \
                  f"name='{name}'," \
                  f"contract_values='{contract_values}', payment='{payment}'," \
                  f"allow_nopay='{allow_nopay}', pay_time='{pay_time}'," \
                  f"final_value='{final_value}', party_unit='{party_unit}' " \
                  f"WHERE id={id}"
            conn.execute(sql)
            conn.commit()
        except Exception as ex:
            return jsonify({'result': f'修改合同表异常{ex}'})
    return redirect('/contract/')


@app.route("/search_contract/", methods=['GET', 'POST'])
def search_contract():
    """
    合同搜索
    :return:
    """
    searchKey = request.form.get("searchKey")
    limit = 10
    page = 1
    offset = 5 * int(page) - 5
    count_sql = f"SELECT SUM(contract_values) FROM contract"
    count = conn.execute(count_sql).fetchall()
    depart_sql = f"SELECT lc.name, SUM(c.payment) " \
                 f"FROM contract c LEFT JOIN contract_channel tc ON tc.contract_id=c.id " \
                 f"LEFT JOIN channel lc ON lc.id=tc.channel_id " \
                 f"Group by lc.name "
    depart = conn.execute(depart_sql).fetchall()
    try:
        if searchKey:
            sql = f"SELECT c.id, p.pro_name, lc.name as channel, " \
                f"c.name, c.contract_values, " \
                f"c.payment, c.allow_nopay, c.pay_time, c.final_value, " \
                f"c.party_unit FROM " \
                f"contract c LEFT JOIN project_contract pc ON " \
                f"pc.contract_id=c.id LEFT JOIN project p ON p.id=pc.project_id " \
                f"LEFT JOIN contract_channel tc ON tc.contract_id=c.id " \
                f"LEFT JOIN channel lc ON lc.id=tc.channel_id " \
                f"WHERE c.name like '%{searchKey}%' " \
                f"OR p.pro_name like '%{searchKey}%' " \
                f"OR lc.name like '%{searchKey}%' " \
                f"ORDER BY p.id DESC LIMIT {limit} offset {offset}"
            list = conn.execute(sql).fetchall()
            total = len(list)
        else:
            sql = f"SELECT c.id, p.pro_name, lc.name as channel " \
                f"c.name, c.contract_values," \
                f"c.payment, c.allow_nopay, c.pay_time, c.final_value," \
                f"c.party_unit FROM " \
                f"contract c LEFT JOIN project_contract pc ON " \
                f"pc.contract_id=c.id LEFT JOIN project p ON p.id=pc.project_id " \
                f"LEFT JOIN contract_channel tc ON tc.contract_id=c.id " \
                f"LEFT JOIN channel lc ON lc.id=tc.channel_id " \
                f"ORDER BY p.id DESC LIMIT {limit} offset {offset}"
            list = conn.execute(sql).fetchall()
            total = len(list)
    except Exception as ex:
        return jsonify({'result': f'搜索合同表异常{ex}'})
    return render_template('contract.html', list=list, total=total, count=count, depart=depart)


@app.route("/capital/<int:page>", methods=['GET','POST'])
@app.route("/capital/", methods=['GET', 'POST'])
def capital(page=1):
    """
    资金下达
    :return:
    """
    if request.method == 'POST':
        allow_file = request.form.get('allow_file') # 批复文件
        allow_money = request.form.get('allow_money') # 下达金额
        channel = request.form.get('channel') # 资金渠道
        pro_name = request.form.get('pro_name')  # 项目名称
        try:
            # 插入资金表
            sql = f"INSERT INTO main.capital ('allow_file', 'allow_money') " \
                f"VALUES ('{allow_file}', '{allow_money}') returning id"
            capital_id = conn.execute(sql).lastrowid
            conn.commit()
        except Exception as ex:
            return jsonify({'result': f'插入资金表异常{ex}'})
        try:
            # 插入project_capital表
            sql = f"SELECT id FROM main.project " \
                  f"WHERE pro_name='{pro_name}'"
            project_id = conn.execute(sql).fetchone()[0]
            insert_sql = f"INSERT INTO project_capital ('project_id', 'capital_id') " \
                         f"VALUES ({project_id}, {capital_id})"
            conn.execute(insert_sql)
            conn.commit()
        except Exception as ex:
            return jsonify({'result': f'插入project_capital表异常{ex}'})
        try:
            # 插入capital_channel表
            sql = f"SELECT id FROM main.channel " \
                  f"WHERE name='{channel}'"
            channel_id = conn.execute(sql).fetchone()[0]
            insert_sql = f"INSERT INTO capital_channel ('channel_id', 'capital_id') " \
                         f"VALUES ({channel_id}, {capital_id})"
            conn.execute(insert_sql)
            conn.commit()
        except Exception as ex:
            return jsonify({'result': f'插入资金渠道表异常{ex}'})
    elif request.method == 'GET':
        limit = 10
        offset = 5 * int(page) - 5
        sql = f"SELECT c.id, p.pro_name, " \
              f"c.allow_file, c.allow_money, lc.name FROM " \
              f"capital c LEFT JOIN project_capital pc ON " \
              f"pc.capital_id=c.id LEFT JOIN project p ON p.id=pc.project_id " \
              f"LEFT JOIN capital_channel cc ON cc.capital_id=c.id " \
              f"LEFT JOIN channel lc ON lc.id=cc.channel_id " \
              f"ORDER BY c.id DESC LIMIT {limit} offset {offset}"
        list = conn.execute(sql).fetchall()
        count_sql = f"SELECT SUM(allow_money) FROM capital"
        count = conn.execute(count_sql).fetchall()
        depart_sql = f"SELECT lc.name, SUM(c.allow_money) FROM " \
              f"capital c LEFT JOIN capital_channel cc ON cc.capital_id=c.id " \
              f"LEFT JOIN channel lc ON lc.id=cc.channel_id " \
              f"GROUP BY lc.name"
        depart = conn.execute(depart_sql).fetchall()
        total = len(list)
        return render_template('/capital.html', list=list, count=count, depart=depart, total=total)
    return redirect("/capital/")


@app.route("/edit_capital/<int:id>/", methods=['POST'])
def edit_capital(id):
    """
    编辑下达
    :return:
    """
    if request.method == 'POST':
        allow_file = request.form.get('allow_file') # 批复文件
        allow_money = request.form.get('allow_money') # 下达金额
        try:
            # 插入资金表
            sql = f"UPDATE capital SET " \
                  f"allow_file='{allow_file}', allow_money='{allow_money}' " \
                  f"WHERE id={id}"
            conn.execute(sql)
            conn.commit()
        except Exception as ex:
            return jsonify({'result': f'插入资金表异常{ex}'})
    return redirect("/capital/")


@app.route("/pay/<int:id>/", methods=['POST'])
def pay(id):
    """
    点击从已申请未支付到已支付
    :param id:
    :return:
    """
    allow = request.form.get('allow')
    if allow:
        try:
            sql = f"SELECT c.payment, c.allow_nopay FROM contract c " \
                f"WHERE c.id={id}"
            payment, allow_nopay = conn.execute(sql).fetchall()[0]
            if float(allow) > float(allow_nopay):
                return jsonify({'result': f'必须小于{allow_nopay}'})
            allow_no = float(allow_nopay) - float(allow) # 要更改的值
            count_value = float(payment) + float(allow)
            update_sql = f"UPDATE contract SET " \
                        f"allow_nopay={allow_no}, payment={count_value} " \
                        f"WHERE contract.id={id}"
            conn.execute(update_sql)
            conn.commit()
        except Exception as ex:
            return jsonify({'result': f'点击从已申请未支付到已支付异常{ex}'})
    else:
        return jsonify({'result': f'必须输入金额'})
    return redirect("/contract/")


@app.route("/upload_contract/", methods=['POST'])
def upload_contract():
    """
    上传合同批量插入
    :return:
    """
    if 'file' not in request.files:
        return jsonify({'result': 'nofile'})
    file = request.files.get('file')
    if file.filename == '':
        return jsonify({'result': 'nofile'})
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        wb = xlrd.open_workbook(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        sh = wb.sheet_by_name('Sheet1')
        for i in range(1, sh.nrows):
            data = sh.row_values(i)
            name, channel, contract_values, \
                payment, allow_nopay, pay_time, \
                final_value, party_unit, pro_name = data[0], data[1], \
                data[2], data[3], data[4], datetime(*xldate_as_tuple(data[5], 0)).date(), data[6], data[7], data[8]
            try:
                sql = f"INSERT INTO main.contract ('name', 'contract_values', 'payment', 'allow_nopay', 'pay_time', 'final_value', 'party_unit') " \
                    f"VALUES ('{name}', '{contract_values}', '{payment}', '{allow_nopay}', '{pay_time}', '{final_value}', '{party_unit}') returning id"
                contract_id = conn.execute(sql).lastrowid
                conn.commit()
            except Exception as ex:
                return jsonify({'result': f'批量插入合同表异常{ex}'})
            try:
                sql = f"SELECT id FROM main.project " \
                    f"WHERE pro_name='{pro_name}'"
                project_id = conn.execute(sql).fetchone()[0]
                insert_sql = f"INSERT INTO project_contract ('project_id', 'contract_id') " \
                         f"VALUES ({project_id}, {contract_id})"
                conn.execute(insert_sql)
                conn.commit()
            except Exception as ex:
                return jsonify({'result': f'批量插入project_contract表异常{ex}'})
            try:
                sql = f"SELECT id FROM main.channel " \
                      f"WHERE name='{channel}'"
                channel_id = conn.execute(sql).fetchone()[0]
                insert_sql = f"INSERT INTO contract_channel ('channel_id', 'contract_id') " \
                             f"VALUES ({channel_id}, {contract_id})"
                conn.execute(insert_sql)
                conn.commit()
            except Exception as ex:
                return jsonify({'result': f'批量插入contract_channel表异常{ex}'})
    return redirect("/contract/")

@app.route("/upload_capital/", methods=['POST'])
def upload_capital():
    """
    上传资金下达批量插入
    :return:
    """
    if 'file' not in request.files:
        return jsonify({'result': 'nofile'})
    file = request.files.get('file')
    if file.filename == '':
        return jsonify({'result': 'nofile'})
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        wb = xlrd.open_workbook(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        sh = wb.sheet_by_name('Sheet1')
        for i in range(1, sh.nrows):
            data = sh.row_values(i)
            allow_file, allow_money, \
                channel_name, pro_name = data[0], str(data[1]), \
                data[2], data[3]
            try:
                sql = f"INSERT INTO main.capital ('allow_file', 'allow_money') " \
                      f"VALUES ('{allow_file}', '{allow_money}') returning id"
                capital_id = conn.execute(sql).lastrowid
                conn.commit()
            except Exception as ex:
                return jsonify({'result': f'插入资金表异常{ex}'})
            try:
                # 插入capital_channel表
                sql = f"SELECT id FROM main.channel " \
                      f"WHERE name='{channel_name}'"
                channel_id = conn.execute(sql).fetchone()[0]
                insert_sql = f"INSERT INTO capital_channel ('channel_id', 'capital_id') " \
                             f"VALUES ({channel_id}, {capital_id})"
                conn.execute(insert_sql)
                conn.commit()
            except Exception as ex:
                return jsonify({'result': f'插入capital_channel表异常{ex}'})
            try:
                # 插入project_capital表
                sql = f"SELECT id FROM main.project " \
                      f"WHERE pro_name='{pro_name}'"
                project_id = conn.execute(sql).fetchone()[0]
                insert_sql = f"INSERT INTO project_capital ('project_id', 'capital_id') " \
                             f"VALUES ({project_id}, {capital_id})"
                conn.execute(insert_sql)
                conn.commit()
            except Exception as ex:
                return jsonify({'result': f'插入project_capital表异常{ex}'})
    return redirect("/capital/")

@app.route("/channel/<int:page>", methods=['GET','POST'])
@app.route("/channel/", methods=['GET', 'POST'])
def channel(page=1):
    """
    资金渠道
    :return:
    """
    if request.method == 'POST':
        name = request.form.get('name')  # 资金渠道
        pro_name = request.form.get('pro_name') # 项目名称
        try:
            # 插入资金渠道表
            sql = f"INSERT INTO main.channel ('name') " \
                f"VALUES ('{name}') returning id"
            channel_id = conn.execute(sql).lastrowid
            conn.commit()
        except Exception as ex:
            return jsonify({'result': f'插入资金渠道异常{ex}'})
        try:
            # 插入project_channel表
            sql = f"SELECT id FROM main.project " \
                f"WHERE pro_name='{pro_name}'"
            project_id = conn.execute(sql).fetchone()[0]
            insert_sql = f"INSERT INTO project_channel ('project_id', 'channel_id') " \
                        f"VALUES ({project_id}, {channel_id})"
            conn.execute(insert_sql)
            conn.commit()
        except Exception as ex:
            return jsonify({'result': f'插入project_channel表异常{ex}'})
    elif request.method == 'GET':
        limit = 10
        offset = 5 * int(page) - 5
        sql = f"SELECT cc.id, p.pro_name, cc.name FROM " \
            f"channel cc LEFT JOIN project_channel pc ON " \
            f"pc.channel_id=cc.id LEFT JOIN project p ON p.id=pc.project_id " \
            f"ORDER BY cc.id DESC LIMIT {limit} offset {offset}"
        list = conn.execute(sql).fetchall()
        total = len(list)
        return render_template('/channel.html', list=list, total=total)
    return redirect("/channel/")

@app.route("/edit_channel/<int:id>/", methods=['POST'])
def edit_channel(id):
    """
    编辑资金渠道
    :return:
    """
    if request.method == 'POST':
        name = request.form.get('name') # 资金渠道名称
        try:
            # 插入资金渠道表
            sql = f"UPDATE channel SET name='{name}' WHERE id={id}"
            conn.execute(sql)
            conn.commit()
        except Exception as ex:
            return jsonify({'result': f'插入资金渠道表异常{ex}'})
    return redirect("/channel/")


@app.route("/upload_channel/", methods=['POST'])
def upload_channel():
    """
    批量上传渠道
    :return:
    """
    if 'file' not in request.files:
        return jsonify({'result': 'nofile'})
    file = request.files.get('file')
    if file.filename == '':
        return jsonify({'result': 'nofile'})
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        wb = xlrd.open_workbook(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        sh = wb.sheet_by_name('Sheet1')
        for i in range(1, sh.nrows):
            data = sh.row_values(i)
            pro_name, channel = data[0], data[1]
            try:
                sql = f"INSERT INTO main.channel ('name') " \
                      f"VALUES ('{channel}') returning id"
                channel_id = conn.execute(sql).lastrowid
                conn.commit()
            except Exception as ex:
                return jsonify({'result': f'插入资金渠道表异常{ex}'})
            try:
                # 插入project_channel表
                sql = f"SELECT id FROM main.project " \
                      f"WHERE pro_name='{pro_name}'"
                project_id = conn.execute(sql).fetchone()[0]
                insert_sql = f"INSERT INTO project_channel ('project_id', 'channel_id') " \
                             f"VALUES ({project_id}, {channel_id})"
                conn.execute(insert_sql)
                conn.commit()
            except Exception as ex:
                return jsonify({'result': f'插入project_channel表异常{ex}'})
    return redirect("/channel/")

@app.route("/search_channel/", methods=['GET', 'POST'])
def search_channel():
    """
    资金渠道搜索
    :return:
    """
    searchKey = request.form.get("searchKey")
    limit = 10
    page = 1
    offset = 5 * int(page) - 5
    try:
        if searchKey:
            sql = f"SELECT cc.id, p.pro_name, cc.name FROM " \
                f"channel cc LEFT JOIN project_channel pc ON " \
                f"pc.channel_id=cc.id LEFT JOIN project p ON p.id=pc.project_id " \
                f"WHERE cc.name like '%{searchKey}%' OR p.pro_name like '%{searchKey}%'" \
                f"ORDER BY p.id DESC LIMIT {limit} offset {offset}"
            list = conn.execute(sql).fetchall()
            total = len(list)
        else:
            sql = f"SELECT cc.id, p.pro_name, cc.name FROM " \
                f"channel cc LEFT JOIN project_channel pc ON " \
                f"pc.channel_id=cc.id LEFT JOIN project p ON p.id=cc.project_id " \
                f"ORDER BY p.id DESC LIMIT {limit} offset {offset}"
            list = conn.execute(sql).fetchall()
            total = len(list)
    except Exception as ex:
        return jsonify({'result': f'搜索资金渠道表异常{ex}'})
    return render_template('channel.html', list=list, total=total)


if __name__ == '__main__':
    app.run()