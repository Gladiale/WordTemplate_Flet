import sqlite3
import datetime

db_path = "./database/database.db" #テーブルを保存するファイル

#データベースファイルにコネクションを確立
con = sqlite3.connect(db_path)  
cur = con.cursor()  #カーソルインスタンスを作成

# テーブルを作成
# IPA (International Phonetic Alphabet)
cur.execute('''
            CREATE TABLE IF NOT EXISTS word_table (
              id INTEGER PRIMARY KEY AUTOINCREMENT,
              word TEXT,
              wordClass TEXT,
              IPA TEXT,
              phrase TEXT,
              others TEXT,
              experience TEXT,
              createAt timestamp,
              reviewAt timestamp
            )''')
con.close()


# データベースにデータを記入
def inset_data(word, wordClass, IPA, phrase, others, experience, createAt, reviewAt):
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute(
        'INSERT INTO word_table (word, wordClass, IPA, phrase, others, experience, createAt, reviewAt) VALUES (:word, :wordClass, :IPA, :phrase, :others, :experience, :createAt, :reviewAt)',
        {
            'word': word,
            'wordClass': wordClass,
            'IPA': IPA,
            'phrase': phrase,
            'others': others,
            'experience': experience,
            'createAt': createAt,
            'reviewAt': reviewAt
        })
    # コミットしないと登録が反映されない
    conn.commit()
    conn.close()


# データベースにデータを取得
# 参考(https://pynative.com/python-sqlite-date-and-datetime)
def get_allData(select_key):
    conn = sqlite3.connect(db_path, detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
    cur = conn.cursor()
    if select_key == "ALL":
        cur.execute('SELECT * FROM word_table ORDER BY id DESC')
    else:
        select_key_plusDay = select_key + datetime.timedelta(days=1)
        cur.execute('SELECT * FROM word_table WHERE createAt > ? AND createAt < ?', (select_key, select_key_plusDay))
    result = cur.fetchall()
    conn.close()
    return result


# 特定文字列, EXPのレコードを抽出
# https://www.ravness.com/posts/pythonsqlite
# https://3pysci.com/sqlite3-11/
def getData_byStr(str):
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    if str == "@LOW" or str == "@NORMAL" or str == "@HIGH":
        cur.execute('SELECT * FROM word_table WHERE experience = ?', (str,))
    else:
        cur.execute('SELECT * FROM word_table WHERE word LIKE ?', ('%' + str + '%',))
    result = cur.fetchall()
    conn.close()
    return result


# データベースからランダムなデータを取得
# https://ytyaru.hatenablog.com/entry/2022/07/19/000000
def getData_byRandom(select_key):
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    if select_key == "ALL":
        random_query = 'SELECT word, phrase FROM word_table WHERE id in (SELECT id FROM word_table ORDER BY RANDOM() LIMIT 7)'
        cur.execute(random_query)
    else:
        select_key_plusDay = select_key + datetime.timedelta(days=1)
        random_query = 'SELECT word, phrase FROM word_table WHERE id in (SELECT id FROM word_table WHERE createAt > ? AND createAt < ? ORDER BY RANDOM() LIMIT 7)'
        cur.execute(random_query, (select_key, select_key_plusDay))
    result = cur.fetchall()
    conn.close()
    return result


# 初入力の時間を取得
def get_firstDate():
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute('SELECT MIN(createAt) FROM word_table')
    result = cur.fetchone()[0]
    conn.close()
    return result


# 特定IDのデータを取得
def getData_byId(id):
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    # (id,)のidの後は,を付ける必要があります
    # 参考：https://stackoverflow.com/questions/11853167/parameter-unsupported-when-inserting-int
    cur.execute('SELECT * FROM word_table WHERE id = ?', (id,))
    result = cur.fetchone()
    conn.close()
    return result


# 特定IDのデータを更新
def update_byId(word, wordClass, IPA, phrase, others, id):
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    update_query = '''
        UPDATE word_table
        SET word = ?, wordClass = ?, IPA = ?, phrase = ?, others = ?
        WHERE id = ?;
        '''
    cur.execute(update_query, (word, wordClass, IPA, phrase, others, id))
    conn.commit()
    conn.close()


# 特定IDのEXPデータを更新
def updateEXP_byId(experience, id):
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    update_query = '''
        UPDATE word_table
        SET experience = ?
        WHERE id = ?;
        '''
    cur.execute(update_query, (experience, id))
    conn.commit()
    conn.close()


# 特定IDのレコードを削除
def delete_byId(id):
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute('DELETE FROM word_table WHERE id =?', (id,))
    conn.commit()
    conn.close()