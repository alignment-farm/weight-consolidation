"""Controller-only generation and independent oracle, never imported in workers."""
import random

FIELDS = [
 dict(zip(['id','account','amount','status','revision','kind'],names.split()))
 for names in ['invoice customer gross state version type',
               'document client value stage revision category',
               'ref buyer amount status seq kind',
               'number account balance flag update class']]

def case(split, i):
    rng = random.Random({'source':401,'development':907,'evaluation':1801,'confirmation':2801}[split]+i)
    family = i%4
    fields = FIELDS[family]
    changed = split in ['evaluation','confirmation'] and i >= 6
    # Dev and evaluation recombine units/revision/credit/status across vocabularies.
    variant = family if split == 'source' else i+1
    major = variant%2 == 0
    latest = variant%3 != 0
    negative = variant%3 != 1
    accept = ['posted'] if not changed else ['posted','settled']
    if changed:
        latest = not latest
        negative = not negative
    cfg = {'fields':fields,'units':'major' if major else 'minor',
           'dedup':'latest' if latest else 'first','credit_negative':negative,'accept':accept}
    contract = ('Columns: '+', '.join(f'{v} means {k}' for k,v in fields.items())+'. '+
        ('Amounts are decimal dollars.' if major else 'Amounts are integer cents.')+' '+
        ('The highest revision wins per document.' if latest else 'The first occurrence wins per document.')+' '+
        ('Credit-kind values must become negative absolute amounts.' if negative else 'All amounts already carry their proper sign; preserve it even for credit-kind rows.')+' '+
        'Accept statuses '+', '.join(accept)+' only. All other statuses are excluded. Unknown accounts are quarantined. '+
        ('This revised contract supersedes old examples; retain every other obligation.' if changed else 'Apply this current contract.'))
    prefix = f'{split}-{i}'
    a,b,c,d = [rng.randint(100,9000) for _ in range(4)]
    # canonical input sequence: credit, duplicate changing state, unknown, void, settled.
    raw = [(f'{prefix}-A','c1',a,'posted',1,'sale'),
           (f'{prefix}-B','c2',b,'posted',1,'credit'),
           (f'{prefix}-A','c1',c,'void',2,'sale'),
           (f'{prefix}-C','missing',d,'posted',1,'sale'),
           (f'{prefix}-D','c2',a,'void',1,'sale'),
           (f'{prefix}-E','c1',-b,'settled',1,'credit')]
    rows = []
    for doc,account,value,status,revision,kind in raw:
        amount = f'{value/100:.2f}' if major else str(value)
        rows.append(dict(zip(fields.values(),[doc,account,amount,status,revision,kind])))
    task = {'job':prefix,'contract':contract,'rows':rows,'accounts':{'c1':'account-1','c2':'account-2'}}
    # Oracle is built from canonical facts with integer arithmetic, not transform.py.
    chosen = [raw[2] if latest else raw[0],raw[1],*raw[3:]]
    records, quarantine, excluded = [],[],[]
    for doc,account,value,status,revision,kind in sorted(chosen):
        if status not in accept: excluded.append(doc)
        elif account == 'missing': quarantine.append(doc)
        else: records.append({'id':doc,'account':task['accounts'][account],
                              'minor':-abs(value) if negative and kind=='credit' else value})
    expected = {'job':prefix,'records':records,'quarantine':quarantine,'excluded':excluded,
                'total_minor':sum(r['minor'] for r in records)}
    return {'id':prefix,'split':split,'changed':changed,'task':task,'config':cfg,'expected':expected}

def grade(case, artifact, status):
    components = {key:artifact.get(key)==value for key,value in case['expected'].items()}
    return {'complete':status=='succeeded' and all(components.values()),'components':components}
