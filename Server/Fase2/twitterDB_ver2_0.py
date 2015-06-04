import tweepy
import psycopg2
 
auth = tweepy.AppAuthHandler(token, secret)
  
api = tweepy.API(auth, wait_on_rate_limit=True,
                   wait_on_rate_limit_notify=True)
  
if (not api):
	print ("Can't Authenticate")
	sys.exit(-1)

langs = {"javascript":"javascript",
		"csharp":"csharp",
		"java":"java",
		"cplusplus":"cplusplus OR cpp",
		"python":"python",
		"visual_basic":"visual basic OR visualbasic",
		"ruby":"ruby",
		"swift":"swift",
		"c":"c language OR c programming OR c developer",
		"html":"html",
		"scala":"scala",
		"obj_c":"Objective-C OR ObjC OR Obj-C"}

conn = psycopg2.connect(user='', password='',
                            dbname='', host='',
                            port=)
curs = conn.cursor()

for key, value in langs.items():
	print (key + " tweets...")
	for status in tweepy.Cursor(api.search, q=value, rpp = 100).items(100):
	curs.execute('INSERT INTO eutweets (content, prog_lang, created_at, nation, id_str) VALUES (%s, %s, %s, %s, %s)', (status.text, key, status.created_at.date(), status.place.country, status.id_str))
	conn.commit()
curs.close()
conn.close()