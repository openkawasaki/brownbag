#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import json
import os
import codecs

import requests

import traceback

from dotenv import load_dotenv
import urllib.parse
import xml.etree.ElementTree as ET

# -----------------------------------
def write_json(filename, jsonData, indent=False):
    """
    JSONファイル書き込み
    """
    try:
        with codecs.open(filename, 'w', "utf-8") as f:
            if indent:
                json.dump(jsonData, f, sort_keys=True, indent=4, ensure_ascii=False)
            else:
                json.dump(jsonData, f, ensure_ascii=False)

    except IOError as e:
        traceback.print_exc()
        raise Exception('system error: {}'.format(e))

#-----------------------------------
def geocoding(addr):
    '''
    ジオコーディング
    :param addr:住所文字列
    :return:
    '''

    coordinates = []

    try:
        addr_enc = urllib.parse.quote(addr)

        # 東京大学空間情報科学研究センター
        # CSISシンプルジオコーディング実験
        # http://newspat.csis.u-tokyo.ac.jp/geocode/modules/geocode/index.php?content_id=1
        url = "http://geocode.csis.u-tokyo.ac.jp/cgi-bin/simple_geocode.cgi?charset=UTF8&addr=" + addr_enc

        # HTTP GET: 緯度経度取得
        read_data = requests.get(url)
        # 読み込みデータ取得
        xml_string = read_data.text

        # xmlデータを読み込みます
        root = ET.fromstring(xml_string)

        # candidate => longitude, latitude
        candidates = root.findall('candidate')
        for row in candidates:
            # 座標取得
            longitude = float(row.find("longitude").text)
            latitude  = float(row.find("latitude").text)
            coordinates.append({"longitude":longitude, "latitude":latitude})

    except Exception as e:
        traceback.print_exc()
        raise Exception('geocoding() error = {}'.format(e))

    return coordinates

#-----------------------------------
def csv2json(csvdata):
    '''
    CSV -> JSON 変換
    :param csvdata:
    :return:
    '''
    try:
        jsondata = []

        # ヘッダ読み込み
        keys = csvdata[0]
        # ヘッダ削除
        del csvdata[0]

        # CSVデータを一行ずつ読み込み
        for row in csvdata:
            data = {}
            for ii, key in enumerate(keys):
                # dictデータに設定
                #data[key] = row[ii]

                if key == '店名':
                    data["name"] = row[ii]
                elif key == '店舗概要':
                    data["description"] = row[ii]
                elif key == 'お店の住所':
                    data["addr"] = row[ii]
                    # 住所から緯度経度を取得
                    coordinates = geocoding(data["addr"])
                    data["lon"] = coordinates[0]["longitude"]
                    data["lat"] = coordinates[0]["latitude"]
                elif key == 'お弁当・メニュー情報':
                    data["menu"] = row[ii]
                elif key == 'テイクアウト（持ち帰り）に対応してますか？':
                    data["takeaway"] = row[ii]
                elif key == 'デリバリーサービス（出前・配達）に対応してますか？':
                    data["delivery"] = row[ii]
                elif key == 'お店の電話番号':
                    data["phone"] = row[ii]
                elif key == '営業時間':
                    data["opening_hours"] = row[ii]
                elif key == '定休日':
                    data["close_day"] = row[ii]
                elif key == '支払い方法':
                    data["payment"] = row[ii]
                elif key == 'ホームページ':
                    data["website"] = row[ii]
                elif key == 'SNS・その他リンク':
                    data["sns"] = row[ii]
                elif key == 'アクセス情報':
                    data["transportation"] = row[ii]
                elif key == 'カテゴリ':
                    data["category"] = row[ii]
                elif key == 'ジャンル':
                    data["genre"] = row[ii]
                elif key == 'その他、留意事項':
                    data["note"] = row[ii]
                elif key == '地域':
                    data["area"] = row[ii]
                elif key == 'ベジタリアン（vegetarian）、ビーガン（vegan）':
                    data["diet"] = row[ii]

            jsondata.append(data)

    except Exception as e:
        traceback.print_exc()
        raise Exception('csv2json() error = {}'.format(e))

    return jsondata

#-----------------------------------
def get_google_sheet():
    '''
    Googleスプレットシート読み込み
    :return: json data
    '''

    try:
        # アクセスキー取得
        API_KEY    = os.environ['API_KEY']    # Google API KEY
        SHEET_ID   = os.environ['SHEET_ID']   # Google spread sheet ID
        SHEET_NAME = os.environ['SHEET_NAME'] # sheet name

        # Google Sheets API URL
        url = 'https://sheets.googleapis.com/v4/spreadsheets/' + SHEET_ID + '/values/' + SHEET_NAME + '?key=' + API_KEY

        # HTTP GET: Google Sheets API Googleスプレットシート読み込み
        read_data = requests.get(url)
        # 読み込みデータ取得
        read_json = json.loads(read_data.text)
        # Googleスプレットシート データ部を取得
        csv_data  = read_json['values']
        # csv -> json変換
        json_data = csv2json(csv_data)

    except Exception as e:
        traceback.print_exc()
        raise Exception('get_google_sheet() error = {}'.format(e))

    return json_data

#-----------------------------------
def main():

    try:
        # 環境変数読み込み
        load_dotenv()

        # Googleスプレットシート読み込み
        json_data = get_google_sheet()

        # data.jsonファイル出力
        basedir  = os.path.dirname(os.path.abspath(__file__))
        filename = os.path.join(basedir, "data.json")
        write_json(filename, json_data, indent=False)

    except Exception as e:
        print('{}'.format(e))

#-------------------------------------------
if __name__ == "__main__":
    """
    main()
    """
    argv = sys.argv   # コマンドライン引数を格納したリストの取得
    argc = len(argv)  # 引数の個数

    main()
