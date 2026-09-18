"""Explicit parser for this study's bounded contract language; no fixtures or oracle."""
import re

def compile_contract(contract):
    header=contract.split('. ',1)[0]
    pairs=re.findall(r'([A-Za-z_]+) means (id|account|amount|status|revision|kind)\b',header)
    fields={meaning:column for column,meaning in pairs}
    if set(fields)!={'id','account','amount','status','revision','kind'} or len(pairs)!=6:
        raise ValueError('contract column declarations unsupported')
    def choose(yes,no):
        if (yes in contract)==(no in contract):
            raise ValueError('ambiguous or unsupported contract clause')
        return yes in contract
    major=choose('Amounts are decimal dollars.','Amounts are integer cents.')
    latest=choose('The highest revision wins per document.','The first occurrence wins per document.')
    negative=choose('Credit-kind values must become negative absolute amounts.',
                    'All amounts already carry their proper sign; preserve it even for credit-kind rows.')
    accepted=re.search(r'Accept statuses ([a-z, ]+) only\.',contract)
    if accepted is None:raise ValueError('no status contract')
    return {'fields':fields,'units':'major' if major else 'minor','dedup':'latest' if latest else 'first',
            'credit_negative':negative,'accept':accepted[1].split(', ')}
