import sys, json
import logging
import rds_config
import pymysql
#rds settings
rds_host  = "fastest-finger-first-db.cuxtpaw3cpag.us-east-1.rds.amazonaws.com"
name = rds_config.db_username
password = rds_config.db_password
db_name = 'fastest_finger_first'

logger = logging.getLogger()
logger.setLevel(logging.INFO)

try:
	conn = pymysql.connect(rds_host, user=name, passwd=password, db=db_name, connect_timeout=15, autocommit=True)
except:
	logger.error("ERROR: Unexpected error: Could not connect to MySql instance.")
	sys.exit()

logger.info("SUCCESS: Connection to RDS mysql instance succeeded")

def handler(event, context):
	"""
	This function fetches content from mysql RDS instance
	"""
	print(event)
	with conn.cursor() as cur:
		command1 = """INSERT INTO `fastest_finger_first`.`registration_data` (Phone, UserName, QuestionNumber) VALUES ('{}','{}','{}') ON DUPLICATE KEY UPDATE QuestionNumber = '{}'""".format(event['phone'], event['name'], event['question'], event['question'])
		print('added to table1')
		cur.execute(command1)
		correct_answers = [0,1,4,1,1,2,3,4,4,2,3]
		if(correct_answers[int(event['question'])] == int(event['answer'])):
			command2 = """insert into user_info(UserName,Phone,QuestionNumber,Answer,TimeTaken) values ('{}','{}','{}','{}','{}');""".format(event['name'], event['phone'], event['question'], event['answer'], event['time'])
			try:
				cur.execute(command2)
				print('added a row')
				conn.commit()
			except:
				print('duplicate entery')
		else:
			print ('wrong answer')
		return "success!"