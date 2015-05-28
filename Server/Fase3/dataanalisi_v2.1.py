# -*- coding: utf-8 -*-

import psycopg2
import sys

def getTuples():
	counter = conn.cursor()
	idC = conn.cursor()
	max_id = conn.cursor()

	idC.execute('SELECT last_analized FROM last_id_analized_v2')
	max_id.execute("SELECT MAX(id) FROM cleaned_tweets")
	max_id.execute("UPDATE last_id_analized_v2 SET last_analized = %s",(max_id.fetchone()))

	id = idC.fetchone()

	query = "SELECT nation, year, month, prog_lang, COUNT(id) FROM cleaned_tweets WHERE id > {0} GROUP BY nation, year, month, prog_lang".format(id[0])
	counter.execute(query)


	tuples = counter.fetchall()

	counter.close()
	idC.close()
	max_id.close()

	return(tuples)

def setTuples(tuples):
	statesC = conn.cursor()
	placer = conn.cursor()
	
	statesC.execute("SELECT nation_orig_lang, nation_eng_lang FROM nations")
	
	states_tmp = statesC.fetchall()
	states = {}
	for st in states_tmp:
		states[st[0]] = st[1]

	for tuple in tuples:
		query = "SELECT * FROM stats_v2 WHERE year = {0} AND month = {1} AND nation = '{2}' AND prog_lang = '{3}'".format(tuple[1], tuple[2], states[tuple[0]], tuple[3])
		placer.execute(query)
		checker = placer.fetchall()
		if not checker:
			query = "INSERT INTO stats_v2 (nation, prog_lang, tweets, year, month) VALUES ('{0}','{1}',0,{2},{3})".format(states[tuple[0]], tuple[3], tuple[1], tuple[2])
			placer.execute(query)
		query = "UPDATE stats_v2 SET tweets = tweets + {0} WHERE nation = '{1}' AND year = {2} AND month = {3} AND prog_lang = '{4}'".format(tuple[4], states[tuple[0]], tuple[1], tuple[2], tuple[3])
		placer.execute(query)
	
	statesC.close()
	placer.close()

	return("Cycle ended")

if __name__ == '__main__':
	try:
		conn = psycopg2.connect(user='twitter', password='tsacs3m', dbname='dati', host='52.16.148.22', port=5432)
		print(setTuples(getTuples()))
	except:
		e = sys.exc_info()[0]
		print("Error -----> :" + str(e))
	finally:
		conn.commit()
		conn.close()