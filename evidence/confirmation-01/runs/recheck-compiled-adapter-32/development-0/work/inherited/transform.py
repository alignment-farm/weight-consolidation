"""Reusable invoice normalization. No contract interpretation or evaluator imports."""
from decimal import Decimal

def reconcile(task, config):
    fields = config['fields']
    if set(fields) != {'id','account','amount','status','revision','kind'}:
        raise ValueError('fields must map id/account/amount/status/revision/kind')
    if config['units'] not in ['minor','major'] or config['dedup'] not in ['first','latest']:
        raise ValueError('units minor/major and dedup first/latest required')
    if type(config['credit_negative']) is not bool or not isinstance(config['accept'], list):
        raise ValueError('credit_negative boolean and accept list required')
    by_id = {}
    for row in task['rows']:
        key = row[fields['id']]
        if key not in by_id or (config['dedup']=='latest' and int(row[fields['revision']]) > int(by_id[key][fields['revision']])):
            by_id[key] = row
    records, quarantine, excluded = [], [], []
    for key,row in sorted(by_id.items()):
        if row[fields['status']] not in config['accept']:
            excluded.append(key)
            continue
        account = task['accounts'].get(row[fields['account']])
        if account is None:
            quarantine.append(key)
            continue
        value = Decimal(str(row[fields['amount']])) * (100 if config['units']=='major' else 1)
        if value != value.to_integral_value():
            raise ValueError('nonintegral minor units')
        if config['credit_negative'] and row[fields['kind']]=='credit':
            value = -abs(value)
        records.append({'id':key,'account':account,'minor':int(value)})
    return {'job':task['job'],'records':records,'quarantine':quarantine,'excluded':excluded,
            'total_minor':sum(r['minor'] for r in records)}
