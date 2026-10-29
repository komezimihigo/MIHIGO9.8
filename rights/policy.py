from dataclasses import dataclass
@dataclass
class RightsDecision:
    allowed: bool
    reason: str

def validate_source(source_type: str, rights_confirmed: bool, attribution: str='') -> RightsDecision:
    """Fail closed: do not treat public availability as permission to reuse."""
    if source_type not in {'owned','public_domain','licensed'}: return RightsDecision(False,'Unknown source type')
    if not rights_confirmed: return RightsDecision(False,'Rights/permission must be confirmed before processing for publication')
    if source_type=='licensed' and not attribution.strip(): return RightsDecision(False,'Licensed source requires attribution details')
    return RightsDecision(True,'Rights declaration recorded; this is not independent legal verification')
