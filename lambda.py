import boto3
import json
import datetime


if __name__ == '__main__':
    with open('config.json') as f:
        kwag = json.load(f)

        today = datetime.datetime.now()
        str_date = today - datetime.timedelta(days=1)
        end_date = today

        client = boto3.client('ce', **kwag)
        kk = dict()
        tp = dict()
        tp['Start'] = str_date.strftime('%Y-%m-%d')
        tp['End'] = end_date.strftime('%Y-%m-%d')
        print(tp)
        kk['TimePeriod'] = tp
        kk['Granularity'] = 'DAILY'
        kk['Metrics'] = ['UnblendedCost']
        gb = list()
        gb.append({"Type": "DIMENSION","Key": "SERVICE"})
        gb.append({"Type": "DIMENSION","Key": "REGION"})
        kk['GroupBy'] = gb
        rr = client.get_cost_and_usage(**kk)

        for dd in rr['ResultsByTime']:
            print(dd['TimePeriod']['End'])
            for ddd in dd['Groups']:
                ammount = float(ddd['Metrics']['UnblendedCost']['Amount'])
                if ammount > 0:
                    print('%s(%s)' % (ddd['Keys'][0], ddd['Keys'][1]))
                    print('$ %s' % ddd['Metrics']['UnblendedCost']['Amount'])