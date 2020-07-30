import tornado.gen
import tornado.web

from common.web import requestsManager

with open('templates/default.html', 'r', encoding='utf-8') as read_file:
	default_page = read_file.read()

class handler(requestsManager.asyncRequestHandler):
	@tornado.web.asynchronous
	@tornado.gen.engine
	def asyncGet(self):
		self.write(default_page)