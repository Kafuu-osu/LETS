import tornado.gen
import tornado.web

import requests
import json
from common.sentry import sentry
from common.web import requestsManager
from common.web import cheesegull
from constants import exceptions
from common.log import logUtils as log
from common.iputils import ipInfo

MODULE_NAME = "direct"
class handler(requestsManager.asyncRequestHandler):
    """
    Handler for /web/osu-search.php
    """
    @tornado.web.asynchronous
    @tornado.gen.engine
    @sentry.captureTornado
    def asyncGet(self):
        output = ""
        try:
            try:
                # Get arguments
                gameMode = self.get_argument("m", None)
                if gameMode != None:
                    gameMode = int(gameMode)
                if gameMode < 0 or gameMode > 3:
                    gameMode = None

                rankedStatus = self.get_argument("r", None)
                if rankedStatus != None:
                    rankedStatus = int(rankedStatus)

                query = self.get_argument("q", "")
                page = int(self.get_argument("p", "0"))
                if query.lower() not in ["newest", "top rated", "most played"]:
                    query = ""
            except ValueError:
                raise exceptions.invalidArgumentsException(MODULE_NAME)
            
            
            # in China Mainland, use sayobot mirror
            if True or ipInfo.getIpAera(self.request.remote_ip) == "CN":
                # Get data from sayobot API
                log.info("[sayobot] Requested osu!direct search: {}".format(query if query != "" else "index"))
                address = "https://api.sayobot.cn/beatmaplist?0=100&1={}&2={}&3=&5={}&6={}&4=63&7=1535&8=4095".format(
                    page * 100, 
                    2 if (query == "newest") else 1 if (query == "most played") else 4 if (query == "top rated") else 4,
                    15 if gameMode == None else gameMode + 1, 
                    31 if rankedStatus == None else { 4:31, 0:1, 7:1, 8:4, 3:2, 2:8, 5:16}.get(rankedStatus, 31)
                )
                log.info("[sayobot] address {}".format(address))
                response = requests.get(address)
                if response.status_code != 200:
                    log.error("ERROR WHEN: [sayobot] Requested osu!direct search, statusCode({})".format(response.status_code))
                    raise exceptions.noAPIDataError()
                if response.text in (None, 'null\n', ''):
                    log.error("ERROR WHEN: [sayobot] Requested osu!direct search, response text is null")
                    raise exceptions.noAPIDataError()
                searchData = json.loads(response.text)
                if searchData.get("status") != 0:
                    log.error("ERROR WHEN: [sayobot] Requested osu!direct search, sayobot status is invalid")
                    raise exceptions.noAPIDataError()
                mapSetDatas = searchData["data"]
                searchData = []
                for mapSet in mapSetDatas:
                    temp = { 
                        "ChildrenBeatmaps": [{
                            "BeatmapID": 0,
                            "ParentSetID": mapSet["sid"],
                            "DiffName": "[From Sayobot.cn mirror] {} Mode, Unknown Diffname, Unknown Info! But you can download it.".format('Unknown') if gameMode == None else ('std', 'taiko', 'ctb', 'mania')[gameMode],
                            "FileMD5": "",
                            "Mode": {1:0, 2:1, 4:2, 8:3}.get(mapSet.get("modes", 1), 0),
                            "BPM": 0,
                            "AR": 0,
                            "OD": 0,
                            "CS": 0,
                            "HP": 0,
                            "TotalLength": 0,
                            "HitLength": 0,
                            "Playcount": 0,
                            "Passcount": 0,
                            "MaxCombo": 0,
                            "DifficultyRating": 0
                        }]
                    }
                    temp["SetID"] = mapSet["sid"]
                    temp["RankedStatus"] = mapSet["approved"]
                    temp["LastUpdate"] = mapSet["lastupdate"]
                    temp["Favourites"] = mapSet["favourite_count"]
                    temp["Artist"] = mapSet["artist"]
                    temp["Title"] = mapSet["title"]
                    temp["Creator"] = mapSet["creator"]
                    temp["tags"] = ""
                    temp["Genre"] = 1
                    temp["Language"] = 1
                    temp["HasVideo"] = False
                    temp["Source"] = ""
                    temp["ApprovedDate"] = mapSet["lastupdate"]
                    temp["LastChecked"] = mapSet["lastupdate"]
                    searchData.append(temp)
                log.info("[sayobot] get osu!direct list completed")
            else:
                # use others (chessgull)
                # Get data from cheesegull API
                log.info("[cheesegull] Requested osu!direct search: {}".format(query if query != "" else "index"))
                searchData = cheesegull.getListing(rankedStatus=cheesegull.directToApiStatus(rankedStatus), page=page * 100, gameMode=gameMode, query=query)
                if searchData is None or searchData is None:
                    raise exceptions.noAPIDataError()


            # Write output
            output += "999" if len(searchData) == 100 else str(len(searchData))
            output += "\n"
            for beatmapSet in searchData:
                try:
                    output += cheesegull.toDirect(beatmapSet) + "\r\n"
                except ValueError:
                    # Invalid cheesegull beatmap (empty beatmapset, cheesegull bug? See Sentry #LETS-00-32)
                    pass
        except (exceptions.noAPIDataError, exceptions.invalidArgumentsException):
            output = "0\n"
        finally:
            self.write(output)

