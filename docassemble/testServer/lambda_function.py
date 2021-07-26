import json
import os
import requests
import stripe

def lambda_handler(event, context):
    webhook_secret = os.environ['webhook_secret']
    stripe_secret = os.environ['stripe_secret']
    stripe_public = os.environ['stripe_public']
    signature = request.headers.get('stripe-signature')
    if webhook_secret:
        try:
            event = stripe.Webhook.construct_event(
                payload=request.data, sig_header=signature, secret=webhook_secret)
            event_data = event['data']
        except Exception as e:
            return e
    # Get the type of webhook event sent - used to check the status of PaymentIntents.
        event_type = event['type']
    else:
        event_data = request_data['data']
        event_type = request_data['type']
    data_object = event_data['object']
    try:
        start_data = json.loads(event['body'])
    except:
        return { 'statusCode': 400, 'body': json.dumps('Could not read JSON from the HTTP body') }
    key = os.environ['daapikey']
    root = os.environ['baseurl']
    i = os.environ['interview']
    r = requests.get(root + '/api/session/new', params={'key': key, 'i': i})
    if r.status_code != 200:
        return { 'statusCode': 400, 'body': json.dumps('Error creating new session at ' + root + '/api/session/new')}
    session = r.json()['session']
    r = requests.post(root + '/api/session/new', data={'key': key,
                                                   'i': i,
                                                   'session': session,
                                                   'variables': json.dumps({'start_data': start_data, 'event_data': event}),
                                                   'question': '1'})
    if r.status_code != 200:
        return { 'statusCode': 400, 'body': json.dumps('Error writing data to new session')}
    return { 'statusCode': 204, 'body': ''}