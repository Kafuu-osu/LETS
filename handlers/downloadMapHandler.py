import tornado.gen
import tornado.web

from common.web import requestsManager
from common.sentry import sentry
from common.log import logUtils as log
from common.iputils import ipInfo

MODULE_NAME = "direct_download"
class handler(requestsManager.asyncRequestHandler):
    """
    Handler for /d/
    """
    @tornado.web.asynchronous
    @tornado.gen.engine
    @sentry.captureTornado
    def asyncGet(self, bid):
        try:
            noVideo = bid.endswith("n")
            if noVideo:
                bid = bid[:-1]
            bid = int(bid)

            log.info("[osu!direct] download id {}, {}".format(bid, "novideo" if noVideo else "full"))

            if ipInfo.getIpAera(self.request.remote_ip) == "CN":
                url = "https://txy1.sayobot.cn/beatmaps/download/{}/{}?server=null".format("novideo" if noVideo else "full", bid)
            else:
                url = "https://osu.gatari.pw/d/{}{}".format(bid, "?novideo" if noVideo else "")


            log.info("[osu!direct] download url {} selected".format(url))
            self.set_status(302, "Moved Temporarily")
            self.add_header("Location", url)
            self.add_header("Cache-Control", "no-cache")
            self.add_header("Pragma", "no-cache")
            self.add_header("referer", "https://kafuu.pro")
        except ValueError:
            self.set_status(400)
            self.write("Invalid set id")
