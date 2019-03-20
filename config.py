from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class Config:
	@staticmethod
	def connect():
		"""
		Create session conect db
		If connect success return session else return False
		"""
		try:
			# Connection String
			engine = create_engine('postgresql+psycopg2://postgres:123456@localhost:5432/DatabaseForReStudy')
			# Create session
			session = sessionmaker(bind=engine)
			return session()
		except expression as identifier:
			print (identifier)
			return False