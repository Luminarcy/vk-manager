import os
import vk
import json
from flask import render_template, request, send_from_directory, session, Blueprint

abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)
os.chdir("..")

# vk
with open('config.json') as json_file:
    data = json.load(json_file)
    for p in data['keys']:
        TOKEN = p['vk_token']

bp = Blueprint('vk_user_subscriptions', __name__, url_prefix='/')


def name_resolver(name, api):
    vk_id = api.utils.resolveScreenName(screen_name=name, v=5.103)
    user_id = int(vk_id['object_id'])
    print("User id:", user_id)
    return user_id


def get_subscriptions(user_id, api):
    first = api.users.getSubscriptions(user_id=user_id,
                                       v=5.103, extended=1, count=200)
    data = first["items"]
    count = first["count"] // 200
    for i in range(1, count + 1):
        data = data + api.users.getSubscriptions(user_id=user_id,
                                                 v=5.103, extended=1, count=200, offset=i * 200)["items"]
    return data


def filter_data(data, data_filters=None):
    if data_filters is None:
        data_filters = ['id', 'name']
    res = []
    for item in data:
        if item['type'] == 'page':
            filtered_item = {your_key: item[your_key] for your_key in data_filters}
            if list(filtered_item)[0] == 'name':
                desired_order_list = data_filters
                filtered_item = {k: filtered_item[k] for k in desired_order_list}
            res.append(filtered_item)
    return res


def make_file(data, filename="data.csv", field_separator="\u0009", line_separator="\n"):
    line = ""
    file_to_open = "reports/"+filename
    with open(file_to_open, "w", encoding='utf16') as file:
        for item in data:
            for key in item.keys():
                if key == 'id':
                    string_part = "https://vk.com/public" + str(item[key]) + field_separator
                else:
                    string_part = str(item[key]) + field_separator
                line += string_part
            line += line_separator
        file.write(line)


def make_html(data, field_separator="", line_separator=""):
    line = """<table border="1"><tr><th>Group Link</th><th>Group Name</th></tr>"""
    for item in data:
        line += "<tr>"
        for key in item.keys():
            line += "<td>"
            if key == 'id':
                string_part = "https://vk.com/public" + str(item[key]) + field_separator
            else:
                string_part = str(item[key]) + field_separator
            line += string_part
            line += "</td>"
        line += line_separator
        line += "</tr>"
    line += "</table>"
    return line


def filter_profile_link(link):
    vk_name = link.split('/')[-1]
    return vk_name


def process_request(text):
    vk_session = vk.Session(access_token=TOKEN)
    api = vk.API(vk_session)

    name = filter_profile_link(text)
    user_id = name_resolver(name, api)

    user_groups = get_subscriptions(user_id, api)
    user_groups_with_id = filter_data(user_groups)

    filename = str(user_id) + "_groups"
    csv_filename = filename + ".csv"
    make_file(user_groups_with_id, filename=csv_filename)

    html_table = make_html(user_groups_with_id)
    html = html_table

    return html, csv_filename


@bp.route('/vkgroups')
def index():
    return render_template('vkgroups.html')


@bp.route('/report', methods=['POST', 'GET'])
def report():
    if request.method == 'POST' and request.form.get('profile') is not None:
        text = request.form['text']
        if len(text.split('/')) < 3:
            return render_template('404.html'), 404
        data = process_request(text)
        html = data[0]
        session['csv_filename'] = data[1]
        return render_template("report.html", html=html)
    if request.method == 'POST' and request.form.get('download') is not None:
        csv_filename = session.get('csv_filename', None)
        return send_from_directory(directory='reports', filename=csv_filename, as_attachment=True)
    return render_template('404.html'), 404