import re
import json
import boto3

DICTIONARY_TABLE_KEY = "english_word"
DICTIONARY_TABLE_NAME = 'english_thai_dict_v2'

dynamo = boto3.resource('api', region_name='ap-southeast-1')

pattern_ends_with_es = re.compile('([a-zA-Z]+?)(es$)')
pattern_ends_with_ss = re.compile('([a-zA-Z]+?)(ss$)')
pattern_ends_with_s = re.compile('([a-zA-Z]+?)(s$)')
pattern_ends_with_ed = re.compile('([a-zA-Z]+?)(ed$)')
pattern_ends_with_ing = re.compile('([a-zA-Z]+?)(ing$)')
pattern_ends_with_ies = re.compile('([a-zA-Z]+?)(ies$)')
pattern_ends_with_ied = re.compile('([a-zA-Z]+?)(ied$)')


def respond(err, res=None):
    return {
        'statusCode': '400' if err else '200',
        'body': err.message if err else json.dumps(res),
        'headers': {
            'Content-Type': 'application/json',
        },
    }


def lookup(search_terms):
    keys = []
    for search_term in search_terms:
        keys.append({DICTIONARY_TABLE_KEY: search_term})
    response = dynamo.batch_get_item(
        RequestItems={
            DICTIONARY_TABLE_NAME: {
                'Keys': keys
            }
        }
    )
    if 'Responses' in response and DICTIONARY_TABLE_NAME in response['Responses'] and len(response['Responses'][DICTIONARY_TABLE_NAME]) > 0:
        definitions = response['Responses'][DICTIONARY_TABLE_NAME]
        definitions.sort(key=lambda val: search_terms.index(val[DICTIONARY_TABLE_KEY]))
        return definitions[0]


def found(pattern, word):
    return len(pattern.findall(word)) > 0


def get_closest_search_terms(search_term):
    """
    :param search_term:
    :return closest_search_terms: list of closest search term that is the singular or present tense form of the given search_term
    """

    closest_search_terms = []
    if found(pattern_ends_with_ies, search_term) or found(pattern_ends_with_ied, search_term):
        closest_search_terms.append(search_term[:len(search_term) - 3] + "y")

    if not found(pattern_ends_with_ss, search_term) and found(pattern_ends_with_s, search_term):
        closest_search_terms.append(pattern_ends_with_s.findall(search_term)[0][0])

    if not found(pattern_ends_with_ss, search_term) and found(pattern_ends_with_es, search_term):
        closest_search_terms.append(pattern_ends_with_es.findall(search_term)[0][0])

    if found(pattern_ends_with_ed, search_term):
        closest_search_terms.append(search_term[:len(search_term) - 1])
        closest_search_terms.append(search_term[:len(search_term) - 2])
        closest_search_terms.append(search_term[:len(search_term) - 3])

    if found(pattern_ends_with_ing, search_term):
        closest_search_terms.append(search_term[:len(search_term) - 3] + "e")
        closest_search_terms.append(search_term[:len(search_term) - 3])
        closest_search_terms.append(search_term[:len(search_term) - 4])
    return closest_search_terms


def lambda_handler(event, context):
    print("Received event: " + json.dumps(event, indent=2))
    search_term = event['pathParameters']['search_term'].lower()
    definition = lookup([search_term])
    if definition is None:
        closest_search_terms = get_closest_search_terms(search_term)
        definition = lookup(closest_search_terms) if len(closest_search_terms) > 0 else None

    if definition is not None:
        data = {"found": True, "search_term": search_term, "closest_search_term": definition["english_word"],
                "definitions": list(definition["thai_definitions"])}
        return respond(None, data)
    else:
        return respond(None, {"found": False, "search_term": search_term})

if __name__ == "__main__":
    print(lambda_handler({"pathParameters": {"search_term": "launches"}}, None))
