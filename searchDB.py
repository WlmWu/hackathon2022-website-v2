import pymongo
import datetime
import pytz
import argparse
import json

from connMongoDB import ConnDB

class MongoDB(ConnDB):
    def __init__(self) -> None:
        super().__init__()
    
    def showAll(self) -> list:
        """
        Return all data in DB.
        """
        rlt=[]
        for i in self.col.find():
            rlt.append(i)
        return rlt

class DBSearcher():
    def __init__(self) -> None:
        self.db = MongoDB()
    
    def searching(self ,range: int, unit: str) -> list:
        """
        Return a list of data with time in range * unit.\n
        Each element in the list is a datum in DB.
        """
        unitDic = {'yr': 31104000, 'mon': 2592000, 'day': 86400, 'hr': 3600, 'min': 60}

        currtime = datetime.datetime.now(pytz.timezone('Asia/Taipei')).strftime("%Y/%m/%d %H:%M:%S")
        currtime = datetime.datetime.strptime(currtime, "%Y/%m/%d %H:%M:%S")
        alldata = self.db.showAll()
        result = [] if range > 0 and unit != '' else alldata
        if len(result) == 0:
            for d in alldata:
                dtime = datetime.datetime.strptime(d['time'], "%Y/%m/%d %H:%M:%S")
                tdiff = currtime - dtime
                if tdiff.total_seconds() > 0 and tdiff.total_seconds() < unitDic[unit]*range:
                    # d['img'] = str(d['img'])[2:-1]
                    # d.pop('_id')
                    result.append(d)

        return self.output(result)

    def output(self, result):
        for r in result:
            r['img'] = str(r['img'])[2:-1]
            r.pop('_id')
        
        return list(reversed(result))

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-r', dest='range', type=int, default=-1)
    parser.add_argument('-u', dest='unit', type=str, default='')
    args = parser.parse_args()

    srchr = DBSearcher()
    res = srchr.searching(args.range, args.unit)
    for r in res:
        print(res['msg'], res['time'], res['ip'])
