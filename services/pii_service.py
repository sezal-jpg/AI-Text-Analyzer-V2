import os
import re
from dotenv import load_dotenv
from azure.core.credentials import AzureKeyCredential
from azure.ai.textanalytics import TextAnalyticsClient

load_dotenv()

CATEGORY_THRESHOLDS={"Email": 0.75,
    "PhoneNumber": 0.75,
    "CreditCardNumber": 0.80,
    "Person": 0.90,
    "Address": 0.85,
    "INPermanentAccount": 0.70,
    "INUniqueIdentificationNumber": 0.75,
    "BankAccountNumber": 0.80,}

IGNORED_CATEGORIES={"PersonType","DateTime"}

EMAIL_PATTERN=re.compile(   r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b",re.IGNORECASE)
PAN_PATTERN=re.compile(r"\b[A-Z]{3}[CPHFABTLJG][A-Z][0-9]{4}[A-Z]\b",re.IGNORECASE)
PHONE_PATTERN=re.compile(r"(?<!\d)(?:\+91[\s-]?)?[6-9]\d{9}(?!\d)")
CREDIT_CARD_PATTERN=re.compile(r"(?<!\d)(?:\d[ -]?){13,19}(?!\d)")
ACCOUNT_NUMBER_PATTERN=re.compile(r"(?<!\d)\d{8,18}(?!\d)")

DOB_PATTERN = re.compile(
    r"\b(?:dob|date\s+of\s+birth|birth\s+date)"
    r"\s*(?:[:#=\-]|is|was)\s*"
    r"(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})",
    re.IGNORECASE
)

PAN_CONTEXT_PATTERN = re.compile(
    r"\b(?:pan|pan\s+card|permanent\s+account\s+number)"
    r"\s*(?:number|no\.?)?"
    r"\s*(?:[:#=\-]|is)\s*"
    r"([A-Za-z0-9][A-Za-z0-9_-]{5,19})",
    re.IGNORECASE
)
AADHAAR_CONTEXT_PATTERN = re.compile(
    r"\b(?:aadhaar|aadhar|uid|unique\s+identification)"
    r"\s*(?:number|no\.?)?"
    r"\s*(?:[:#=\-]|is)\s*"
    r"((?:\d[\s-]?){11,14}\d)",
    re.IGNORECASE
)
ACCOUNT_CONTEXT_PATTERN = re.compile(
    r"\b(?:bank\s+account|account\s+number|account\s+no\.?|a\/c)"
    r"\s*(?:number|no\.?)?"
    r"\s*(?:[:#=\-]|is)\s*"
    r"(\d{8,18})\b",
    re.IGNORECASE
)
PHONE_CONTEXT_PATTERN=re.compile(  r"\b(?:phone|mobile|contact|telephone)"
    r"\s*(?:number|no\.?)?"
    r"\s*[:#=\-]?\s*"
    r"((?:\+91[\s-]?)?[6-9]\d{9})\b",re.IGNORECASE)

SECRET_CONTEXT_PATTERN = re.compile(
    r"\b(?:api[\s_-]*key|api[\s_-]*token|access[\s_-]*token|"
    r"auth[\s_-]*token|secret|secret[\s_-]*key|password|"
    r"private[\s_-]*key|client[\s_-]*secret)"
    r"\s*(?:is|are|=|:|->)?\s*"
    r"([A-Za-z0-9_\-./+=]{12,})",
    re.IGNORECASE
)

def get_client():

    endpoint = os.getenv("AZURE_LANGUAGE_ENDPOINT")
    key = os.getenv("AZURE_LANGUAGE_KEY")

    if not endpoint:
        raise ValueError(
            "AZURE_LANGUAGE_ENDPOINT is missing from .env"
        )

    if not key:
        raise ValueError(
            "AZURE_LANGUAGE_KEY is missing from .env"
        )

    return TextAnalyticsClient(
        endpoint=endpoint,
        credential=AzureKeyCredential(key)
    )
    
def get_threshold(category):
    """
    Return category-specific confidence threshold.
    Unknown categories use a conservative default.
    """
    return CATEGORY_THRESHOLDS.get(category,0.80)

def add_entity(entities,text,start,end,category,confidence,source):
    """
    Add a detected entity to the collection.
    """
    if start>=end:
        return
    
    entities.append({'text':text[start:end],
                    'category':category,
                    'confidence':confidence,
                    'offset':start,
                    'length':end-start,
                    'source':source,})
    
def ranges_overlap(start1,end1,start2,end2):
    return start1<end2 and start2 <end1   

def luhn_check(number):
    """
    Validate credit-card-like numbers using Luhn algorithm.
    """
    digits=re.sub(r"\D","",number)
    if not 13<=len(digits)<=19:
        return False
    
    total=0
    reverse_digits=digits[::-1]
    
    for index,digit in enumerate(reverse_digits):
        value=int(digit)
        
        if index %2 ==1:
            value*=2
            
            if value>9:
                value-=9
                
        total+=value
        
    return total %10==0

def detect_azure_pii(text):
    """
    Detect PII using Azure AI Language.

    We first request important privacy categories.
    If the installed SDK/service rejects the category filter,
    we fall back to Azure's normal PII detection and apply
    our application-level category policy afterward.
    """
    client=get_client()
    requested_categories=["default",
        "INPermanentAccount",
        "INUniqueIdentificationNumber",]      
    try:
        response=client.recognize_pii_entities([text],language='en',categories_filter=requested_categories)    
        
    except Exception:
        response=client.recognize_pii_entities([text],language='en')    
        
    result=response[0]      
    
    if result.is_error:
        raise ValueError(result.error.message) 
    entities=[]
    
    for entity in result.entities:
        category=entity.category
        confidence=entity.confidence_score
        
        if category in IGNORED_CATEGORIES:
            continue
        threshold=get_threshold(category)
        
        if confidence < threshold:
            continue
        
        entities.append({
            'text':entity.text,
            'category':category,
            'confidence':confidence,
            'offset':entity.offset,
            'length':entity.length,
            'source':'Azure AI Language',
        })
        
    return entities  

def detect_rule_based_pii(text):
    """
    Additional deterministic firewall layer.

    This catches important identifiers even when the Azure
    model doesn't recognize them.
    """
    entities=[]
    
    for match in EMAIL_PATTERN.finditer(text):
        add_entity(entities,text,match.start(),match.end(),'Email',1.0,'Deterministic Rule')
        
    for match in PAN_PATTERN.finditer(text):
        add_entity(entities,text,match.start(),match.end(),'INPermanentAccount',1.0,'PAN Validator')        
            
    for match in PAN_CONTEXT_PATTERN.finditer(text):
        value_start=match.start(1)
        value_end=match.end(1)
        value=text[value_start:value_end]
        
        cleaned=value.rstrip(".,;:")
        value_end=value_start+len(cleaned)
        
        if value_end > value_start:
           add_entity(entities,text,value_start,value_end,'PAN_Labeled_Identifier',1.0,'Context Rule')
           
    for match in AADHAAR_CONTEXT_PATTERN.finditer(text):
            value_start=match.start(1)
            value_end=match.end(1)
            add_entity(entities,text,value_start,value_end,'INUniqueIdentificationNumber',1.0,'Context Rule')       
               
    for match in DOB_PATTERN.finditer(text):
                value_start=match.start(1)
                value_end=match.end(1)
                add_entity(entities,text,value_start,value_end,'DateOfBirth',1.0,'Context Rule')       
                   
    for match in ACCOUNT_CONTEXT_PATTERN.finditer(text):
                value_start=match.start(1)
                value_end=match.end(1)
                add_entity(entities,text,value_start,value_end,'BankAccountNumber',1.0,'Context Rule')       
                
    for match in PHONE_CONTEXT_PATTERN.finditer(text):
                    value_start=match.start(1)
                    value_end=match.end(1)
                    add_entity(entities,text,value_start,value_end,'PhoneNumber',1.0,'Context Rule')   
                    
    for match in PHONE_PATTERN.finditer(text):  
        add_entity(entities,text,match.start(),match.end(),'PhoneNumber',0.90,'Pattern Rule')      
        
    for match in SECRET_CONTEXT_PATTERN.finditer(text):
          value_start = match.start(1)
          value_end = match.end(1)
          add_entity(
            entities,
            text,
            value_start,
            value_end,
            "SecretOrApiKey",
            1.0,
            "Secret Context Rule" )        
        
    for match in CREDIT_CARD_PATTERN.finditer(text):
        candidate=match.group()
        
        if luhn_check(candidate):
            add_entity(entities,text,match.start(),match.end(),'CreditCardNumber',1.0,'Luhn Validator')     
            
    return entities  


def merge_entities(entities):
    """
    Merge overlapping Azure + rule-based detections.

    If two detectors identify the same text, keep one entity
    and combine their source information.
    """
    if not entities:
        return []
    
    entities=sorted(entities,key=lambda x: (x['offset'], -x['length'] -x['confidence']))
    merged=[]
    
    for entity in entities:
        if not merged:
            merged.append(entity)
            continue
        previous=merged[-1]
        
        prev_start=previous['offset']
        prev_end=previous['offset']+previous['length']
        
        current_start=entity['offset']
        current_end=entity['offset']+entity['length']
        
        if ranges_overlap(prev_start,prev_end,current_start,current_end):
            if entity['length']> previous['length']:
               sources=set(previous['source'].split("+"))
               sources.update(entity['source'].split("+"))
               entity['source']="+".join(sorted(sources))
               merged[-1]=entity
        
            else:
              sources=set(previous['source'].split("+"))
              sources.update(entity['source'].split("+"))
              entity['source']="+".join(sorted(sources))  
            
        else:
           merged.append(entity)
        
    return merged  

def redact_text(text,entities):
    """
    Redact detected entities from the original text.

    Redaction happens from right to left so offsets remain valid.
    """
    redacted=text
    sorted_entities=sorted(entities,key=lambda x: x['offset'],reverse=True)
    for entity in sorted_entities:
        start=entity['offset']
        end=start+entity['length']
        replacement='*'*entity['length']
        redacted=(redacted[:start]+replacement+redacted[end:])
        
    return redacted

def scan_and_redact(text):
    """
    Main TextShield AI privacy firewall.

    Pipeline:

        Azure PII
             +
        Deterministic Rules
             ↓
        Merge / Deduplicate
             ↓
        Redaction
    """
    
    if not text or not text.strip():
        return {'redacted_text':text,
                'entities':[],
                'pii_detected':False,
                'pii_count':0,
                'detection_sources':[],}
        
    azure_entities=detect_azure_pii(text)    
    rule_entities=detect_rule_based_pii(text) 
    
    all_entities=azure_entities + rule_entities
    entities=merge_entities(all_entities)
    
    redacted_text=redact_text(text,entities)
    cleaned_entities=[]
    
    for entity in entities:
        cleaned_entities.append({'text':entity['text'],
                                'category':entity['category'],
                                'confidence':entity['confidence'],
                                'source':entity['source']})
        
    sources=sorted(set(entity['source'] for entity in entities))    
    
    return {
        'redacted_text':redacted_text,
        'entities':cleaned_entities,
        'pii_detected':len(entities) > 0,
        'pii_count': len(entities),
        'detection_sources':sources,
        
    }
    
            
            
              
            
                                     
                                             
                                 
                             
              
            
            
              
      
            
     
    



