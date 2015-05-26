# -*- coding: utf-8 -*-

import psycopg2

conn = psycopg2.connect(user='twitter', password='tsacs3m', dbname='dati', host='52.16.148.22', port=5432)

id_reader = conn.cursor()
counter = conn.cursor()
placer = conn.cursor()
updater = conn.cursor()
max_id = conn.cursor()

states = {
'Österreich':'austria',
'België':'belgium',
'Hrvatska':'croatia',
'Kibris':'cyprus',
'Ceská Republika':'czech_republic',
'Danmark':'denmark',
'Eesti':'estonia',
'Suomi':'finland',
'France':'france',
'Deutschland':'germany',
'Ελλάδα':'greece',
'Magyarország':'hungary',
'Ireland':'ireland',
'Italia':'italy',
'Latvia':'latvia	',
'Lietuva':'lithuania',
'Luxemburg':'luxembourg',
'Malta':'malta',
'Nederland':'netherlands',
'Polska':'poland',
'Portugal':'portugal',
'România':'romania',
'Slovensko':'slovakia',
'Slovenija':'slovenia',
'España':'spain',
'Sverige':'sweden',
'United Kingdom':'united_kingdom',
'България':'bulgaria'
}

langs = {
'java':0,
'c':0,
'cplusplus':0,
'csharp':0,
'javascriptphp':0,
'python':0,
'visual_basic':0,
'ruby':0,
'swift':0,
'html':0,	
'scala':0,
'obj_c':0}

id_reader.execute('SELECT last_analized FROM last_id_analized_v2')

last_id = id_reader.fetchone()
counter.execute("SELECT nation, prog_lang, COUNT(id), year, month FROM cleaned_tweets_v2 WHERE id > %s GROUP BY year, month, nation, prog_lang, year, month ORDER BY nation", (last_id))
max_id.execute("SELECT MAX(id) FROM cleaned_tweets_v2")
maxid = max_id.fetchone()

for tuple in counter:
	placer.execute("SELECT * FROM stats_v2 WHERE year = {0} AND month = {1} AND nation = '{2}'".format(tuple[3], tuple[4], tuple[0]))
	checker = placer.fetchall()
	if not checker:
		placer.execute("INSERT INTO stats_v2 (nation,java,c,cplusplus,csharp,javascript,php,python,visual_basic,ruby,swift,html,scala,obj_c,year, month) VALUES (%s,0,0,0,0,0,0,0,0,0,0,0,0,0,%s,%s)",(states[tuple[0]], tuple[3], tuple[4]))
	updater.execute("UPDATE stats_v2 SET {0} = {1} + {2} WHERE nation = '{3}' AND year = {4} AND month = {5}".format(tuple[1], tuple[1], tuple[2], tuple[0], tuple[3], tuple[4]))
	conn.commit()

max_id.execute("UPDATE last_id_analized_v2 SET last_analized = %s",(maxid))
conn.commit()
id_reader.close()
counter.close()
placer.close()
max_id.close()
updater.close()

#UPDATE stats SET java = java + 1 WHERE nation = 'italy' AND period = '2015-05'