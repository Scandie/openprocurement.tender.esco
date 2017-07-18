# -*- coding: utf-8 -*-
from copy import deepcopy


# TenderBidResourceTest


def create_tender_bid_invalid(self):
    response = self.app.post_json('/tenders/some_id/bids', {
        'data': {'tenderers': [self.author_data], "value": {"amount": 500}}}, status=404)
    self.assertEqual(response.status, '404 Not Found')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['status'], 'error')
    self.assertEqual(response.json['errors'], [
        {u'description': u'Not Found', u'location':
            u'url', u'name': u'tender_id'}
    ])

    request_path = '/tenders/{}/bids'.format(self.tender_id)
    response = self.app.post(request_path, 'data', status=415)
    self.assertEqual(response.status, '415 Unsupported Media Type')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['status'], 'error')
    self.assertEqual(response.json['errors'], [
        {u'description':
             u"Content-Type header should be one of ['application/json']", u'location': u'header',
         u'name': u'Content-Type'}
    ])

    response = self.app.post(
        request_path, 'data', content_type='application/json', status=422)
    self.assertEqual(response.status, '422 Unprocessable Entity')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['status'], 'error')
    self.assertEqual(response.json['errors'], [
        {u'description': u'No JSON object could be decoded',
         u'location': u'body', u'name': u'data'}
    ])

    response = self.app.post_json(request_path, 'data', status=422)
    self.assertEqual(response.status, '422 Unprocessable Entity')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['status'], 'error')
    self.assertEqual(response.json['errors'], [
        {u'description': u'Data not available',
         u'location': u'body', u'name': u'data'}
    ])

    response = self.app.post_json(request_path, {'not_data': {}}, status=422)
    self.assertEqual(response.status, '422 Unprocessable Entity')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['status'], 'error')
    self.assertEqual(response.json['errors'], [
        {u'description': u'Data not available',
         u'location': u'body', u'name': u'data'}
    ])

    response = self.app.post_json(request_path, {'data': {
        'invalid_field': 'invalid_value'}}, status=422)
    self.assertEqual(response.status, '422 Unprocessable Entity')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['status'], 'error')
    self.assertEqual(response.json['errors'], [
        {u'description': u'Rogue field', u'location':
            u'body', u'name': u'invalid_field'}
    ])

    response = self.app.post_json(request_path, {
        'data': {'tenderers': [{'identifier': 'invalid_value'}]}}, status=422)
    self.assertEqual(response.status, '422 Unprocessable Entity')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['status'], 'error')
    self.assertEqual(response.json['errors'], [
        {u'description': {u'identifier': [
            u'Please use a mapping for this field or Identifier instance instead of unicode.']}, u'location': u'body',
            u'name': u'tenderers'}
    ])

    response = self.app.post_json(request_path, {
        'data': {'tenderers': [{'identifier': {}}]}}, status=422)
    self.assertEqual(response.status, '422 Unprocessable Entity')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['status'], 'error')
    self.assertEqual(response.json['errors'], [
        {u'description': [u'This field is required.'], u'location': u'body', u'name': u'selfEligible'},
        {u'description': [u'This field is required.'], u'location': u'body', u'name': u'selfQualified'},
        {u'description': [
            {u'contactPoint': [u'This field is required.'],
             u'identifier': {u'scheme': [u'This field is required.'], u'id': [u'This field is required.']},
             u'name': [u'This field is required.'],
             u'address': [u'This field is required.']}
        ], u'location': u'body', u'name': u'tenderers'}
    ])

    response = self.app.post_json(request_path, {'data': {'selfEligible': False, 'tenderers': [{
        'name': 'name', 'identifier': {'uri': 'invalid_value'}}]}}, status=422)
    self.assertEqual(response.status, '422 Unprocessable Entity')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['status'], 'error')
    self.assertEqual(response.json['errors'], [
        {u'description': [u'Value must be one of [True].'], u'location': u'body', u'name': u'selfEligible'},
        {u'description': [u'This field is required.'], u'location': u'body', u'name': u'selfQualified'},
        {u'description': [{
            u'contactPoint': [u'This field is required.'],
            u'identifier': {u'scheme': [u'This field is required.'],
                            u'id': [u'This field is required.'],
                            u'uri': [u'Not a well formed URL.']},
            u'address': [u'This field is required.']}],
            u'location': u'body', u'name': u'tenderers'}
    ])

    response = self.app.post_json(request_path, {'data': {'selfEligible': True, 'selfQualified': True,
                                                          'tenderers': [self.author_data]}}, status=422)
    self.assertEqual(response.status, '422 Unprocessable Entity')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['status'], 'error')
    self.assertEqual(response.json['errors'], [
        {u'description': [u'This field is required.'], u'location': u'body', u'name': u'value'}
    ])

    response = self.app.post_json(request_path, {'data': {
        'selfEligible': True, 'selfQualified': True,
        'tenderers': [self.author_data], 'value': {}}}, status=422)
    self.assertEqual(response.status, '422 Unprocessable Entity')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['status'], 'error')
    self.assertEqual(response.json['errors'], [
        {u'location': u'body', u'name': u'value',
         u'description': {u'contractDuration': [u'This field is required.'],
                          u'annualCostsReduction': [u'This field is required.'],
                          u'yearlyPayments': [u'This field is required.']}}
    ])

    response = self.app.post_json(request_path, {'data': {
        'selfEligible': True, 'selfQualified': True,
        'tenderers': [self.author_data], 'value': {'amount': 500}}}, status=422)
    self.assertEqual(response.status, '422 Unprocessable Entity')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['status'], 'error')
    self.assertEqual(response.json['errors'], [
        {u'location': u'body', u'name': u'value',
         u'description': {u'contractDuration': [u'This field is required.'],
                          u'annualCostsReduction': [u'This field is required.'],
                          u'yearlyPayments': [u'This field is required.']}}
    ])

    response = self.app.post_json(request_path, {'data': {
        'selfEligible': True, 'selfQualified': True, 'tenderers': [self.author_data],
        'value': {'contractDuration': 0}}}, status=422)
    self.assertEqual(response.status, '422 Unprocessable Entity')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['status'], 'error')
    self.assertEqual(response.json['errors'], [
        {u'location': u'body', u'name': u'value',
         u'description': {u'annualCostsReduction': [u'This field is required.'],
                          u'yearlyPayments': [u'This field is required.'],
                          u'contractDuration': [u'Int value should be greater than 1.']}}
    ])

    response = self.app.post_json(request_path, {'data': {
        'selfEligible': True, 'selfQualified': True, 'tenderers': [self.author_data],
        'value': {'contractDuration': 20}}}, status=422)
    self.assertEqual(response.status, '422 Unprocessable Entity')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['status'], 'error')
    self.assertEqual(response.json['errors'], [
        {u'location': u'body', u'name': u'value',
         u'description': {u'annualCostsReduction': [u'This field is required.'],
                          u'yearlyPayments': [u'This field is required.'],
                          u'contractDuration': [u'Int value should be less than 15.']}}
    ])

    response = self.app.post_json(request_path, {'data': {
        'selfEligible': True, 'selfQualified': True, 'tenderers': [self.author_data],
        'value': {'yearlyPayments': 0}}}, status=422)
    self.assertEqual(response.status, '422 Unprocessable Entity')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['status'], 'error')
    self.assertEqual(response.json['errors'], [
        {u'location': u'body', u'name': u'value',
         u'description': {u'contractDuration': [u'This field is required.'],
                          u'annualCostsReduction': [u'This field is required.'],
                          u'yearlyPayments': [u'Float value should be greater than 0.8.']}}
    ])

    response = self.app.post_json(request_path, {'data': {
        'selfEligible': True, 'selfQualified': True, 'tenderers': [self.author_data],
        'value': {'yearlyPayments': 1}}}, status=422)
    self.assertEqual(response.status, '422 Unprocessable Entity')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['status'], 'error')
    self.assertEqual(response.json['errors'], [
        {u'location': u'body', u'name': u'value',
         u'description': {u'contractDuration': [u'This field is required.'],
                          u'annualCostsReduction': [u'This field is required.'],
                          u'yearlyPayments': [u'Float value should be less than 0.9.']}}
    ])
    # create bid with given value.amount
    # comment this test while minValue = 0
    # response = self.app.post_json('/tenders/{}/bids'.format(self.tender_id), {'data': {
    #     'selfEligible': True, 'selfQualified': True, 'tenderers': [self.author_data],
    #     'value': {'contractDuration': 6,
    #               'annualCostsReduction': 300.6,
    #               'yearlyPayments': 0.9,
    #               'amount': 1000}}}, status=422)
    # self.assertEqual(response.status, '422 Unprocessable Entity')
    # self.assertEqual(response.content_type, 'application/json')
    # self.assertEqual(response.json['status'], 'error')
    # self.assertEqual(response.json['errors'], [
    #     {u'location': u'body', u'name': u'value',
    #      u'description': [u'value of bid should be greater than minValue of tender']}
    # ])


def create_tender_bid(self):
    response = self.app.post_json('/tenders/{}/bids'.format(self.tender_id),
                                  {'data': self.test_bids_data[0]})
    self.assertEqual(response.status, '201 Created')
    self.assertEqual(response.content_type, 'application/json')
    bid = response.json['data']
    self.assertEqual(bid['tenderers'][0]['name'],
                     self.test_bids_data[0]['tenderers'][0]['name'])
    self.assertIn('id', bid)
    self.assertIn(bid['id'], response.headers['Location'])
    self.assertIn('value', bid)
    self.assertEqual(bid['value']['contractDuration'], 10)
    self.assertEqual(bid['value']['annualCostsReduction'], 751.5)
    self.assertEqual(bid['value']['yearlyPayments'], 0.9)
    self.assertEqual(bid['value']['amount'], 698.444)

    for status in ('active', 'unsuccessful', 'deleted', 'invalid'):
        data = deepcopy(self.test_bids_data[0])
        data.update({'status': status})
        response = self.app.post_json('/tenders/{}/bids'.format(self.tender_id),
                                      {'data': data}, status=403)
        self.assertEqual(response.status, '403 Forbidden')

    self.set_status('complete')

    response = self.app.post_json('/tenders/{}/bids'.format(self.tender_id), {'data': {
        'selfEligible': True, 'selfQualified': True, 'tenderers': [self.author_data],
        'value': {'contractDuration': 10,
                  'annualCostsReduction': 751.5,
                  'yearlyPayments': 0.9}}}, status=403)
    self.assertEqual(response.status, '403 Forbidden')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['errors'][0]["description"], "Can't add bid in current (complete) tender status")


def patch_tender_bid(self):
    response = self.app.post_json('/tenders/{}/bids'.format(self.tender_id),
                                  {'data': self.test_bids_data[0]})
    self.assertEqual(response.status, '201 Created')
    self.assertEqual(response.content_type, 'application/json')
    bid = response.json['data']
    bid_token = response.json['access']['token']

    # Comment this test while minValue = 0
    # response = self.app.patch_json('/tenders/{}/bids/{}?acc_token={}'.format(self.tender_id, bid['id'], bid_token), {'data': {
    #     'value': {'contractDuration': 6,
    #               'annualCostsReduction': 300.6,
    #               'yearlyPayments': 0.9}
    # }}, status=422)
    # self.assertEqual(response.status, '422 Unprocessable Entity')
    # self.assertEqual(response.content_type, 'application/json')
    # self.assertEqual(response.json['status'], 'error')
    # self.assertEqual(response.json['errors'], [
    #     {u'location': u'body', u'name': u'value',
    #      u'description': [u'value of bid should be greater than minValue of tender']}
    # ])

    response = self.app.patch_json('/tenders/{}/bids/{}?acc_token={}'.format(self.tender_id, bid['id'], bid_token),
                                   {"data": {'tenderers': [{"name": u"Державне управління управлінням справами"}]}})
    self.assertEqual(response.status, '200 OK')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['data']['date'], bid['date'])
    self.assertNotEqual(response.json['data']['tenderers'][0]['name'], bid['tenderers'][0]['name'])

    response = self.app.patch_json('/tenders/{}/bids/{}?acc_token={}'.format(self.tender_id, bid['id'], bid_token),
                                   {"data": {"value": {"amount": 500}, 'tenderers': self.test_bids_data[0]['tenderers']}})
    self.assertEqual(response.status, '200 OK')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['data']['date'], bid['date'])
    self.assertEqual(response.json['data']['value'], bid['value'])
    self.assertEqual(response.json['data']['tenderers'][0]['name'], bid['tenderers'][0]['name'])
    self.assertNotEqual(response.json['data']['value']['amount'], 500)

    response = self.app.patch_json('/tenders/{}/bids/some_id?acc_token={}'.format(self.tender_id, bid_token),
                                   {"data": {"value": {"amount": 400}}}, status=404)
    self.assertEqual(response.status, '404 Not Found')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['status'], 'error')
    self.assertEqual(response.json['errors'], [
        {u'description': u'Not Found', u'location':
            u'url', u'name': u'bid_id'}
    ])

    response = self.app.patch_json('/tenders/some_id/bids/some_id', {"data": {"value": {"amount": 400}}}, status=404)
    self.assertEqual(response.status, '404 Not Found')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['status'], 'error')
    self.assertEqual(response.json['errors'], [
        {u'description': u'Not Found', u'location':
            u'url', u'name': u'tender_id'}
    ])

    for status in ('invalid', 'active', 'unsuccessful', 'deleted', 'draft'):
        response = self.app.patch_json('/tenders/{}/bids/{}?acc_token={}'.format(self.tender_id, bid['id'], bid_token),
                                       {'data': {'status': status}}, status=403)
        self.assertEqual(response.status, '403 Forbidden')
        self.assertEqual(response.json['errors'][0]["description"], "Can't update bid to ({}) status".format(status))

    response = self.app.patch_json('/tenders/{}/bids/{}?acc_token={}'.format(self.tender_id, bid['id'], bid_token),
                                   {"data": {"value": {"amount": 400}}})
    self.assertEqual(response.status, '200 OK')
    self.assertEqual(response.content_type, 'application/json')

    self.set_status('complete')

    response = self.app.get('/tenders/{}/bids/{}'.format(self.tender_id, bid['id']))
    self.assertEqual(response.status, '200 OK')
    self.assertEqual(response.content_type, 'application/json')
    self.assertNotEqual(response.json['data']["value"]["amount"], 400)

    response = self.app.patch_json('/tenders/{}/bids/{}?acc_token={}'.format(self.tender_id, bid['id'], bid_token),
                                   {"data": {"value": {"amount": 400}}}, status=403)
    self.assertEqual(response.status, '403 Forbidden')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['errors'][0]["description"], "Can't update bid in current (complete) tender status")


def delete_tender_bidder(self):
    response = self.app.post_json('/tenders/{}/bids'.format(
        self.tender_id), {'data': {'selfEligible': True, 'selfQualified': True,
                                   'tenderers': self.test_bids_data[0]['tenderers'], "value": self.test_bids_data[0]['value']}})
    self.assertEqual(response.status, '201 Created')
    self.assertEqual(response.content_type, 'application/json')
    bid = response.json['data']
    bid_token = response.json['access']['token']

    response = self.app.delete('/tenders/{}/bids/{}?acc_token={}'.format(self.tender_id, bid['id'], bid_token))
    self.assertEqual(response.status, '200 OK')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['data']['id'], bid['id'])
    self.assertEqual(response.json['data']['status'], 'deleted')
    # deleted bid does not contain bid information
    self.assertFalse('value' in response.json['data'])
    self.assertFalse('tenderers' in response.json['data'])
    self.assertFalse('date' in response.json['data'])

    # try to add documents to bid
    for doc_resource in ['documents', 'financial_documents', 'eligibility_documents', 'qualification_documents']:
        response = self.app.post('/tenders/{}/bids/{}/{}?acc_token={}'.format(
            self.tender_id, bid['id'], doc_resource, bid_token),
            upload_files=[('file', 'name_{}.doc'.format(doc_resource[:-1]), 'content')], status=403)
        self.assertEqual(response.status, '403 Forbidden')
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(response.json['errors'][0]["description"], "Can't add document to 'deleted' bid")

    revisions = self.db.get(self.tender_id).get('revisions')
    self.assertTrue(any([i for i in revisions[-2][u'changes'] if i['op'] == u'remove' and i['path'] == u'/bids']))
    self.assertTrue(
        any([i for i in revisions[-1][u'changes'] if i['op'] == u'replace' and i['path'] == u'/bids/0/status']))

    response = self.app.delete('/tenders/{}/bids/some_id'.format(self.tender_id), status=404)
    self.assertEqual(response.status, '404 Not Found')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['status'], 'error')
    self.assertEqual(response.json['errors'], [
        {u'description': u'Not Found', u'location':
            u'url', u'name': u'bid_id'}
    ])

    response = self.app.delete('/tenders/some_id/bids/some_id', status=404)
    self.assertEqual(response.status, '404 Not Found')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['status'], 'error')
    self.assertEqual(response.json['errors'], [
        {u'description': u'Not Found', u'location':
            u'url', u'name': u'tender_id'}
    ])

    # create new bid
    response = self.app.post_json('/tenders/{}/bids'.format(
        self.tender_id), {'data': {'selfEligible': True, 'selfQualified': True,
                                   'tenderers': self.test_bids_data[0]['tenderers'], "value": self.test_bids_data[0]['value']}})
    self.assertEqual(response.status, '201 Created')
    bid = response.json['data']
    bid_token = response.json['access']['token']

    # update tender. we can set value that is less than a value in bid as
    # they will be invalidated by this request
    response = self.app.patch_json('/tenders/{}?acc_token={}'.format(self.tender_id, self.tender_token), {"data": {
                                                                                                                  "description": "new description"
                                                                                                                  }
                                                                                                          })
    self.assertEqual(response.status, '200 OK')
    self.assertEqual(response.json['data']["description"], "new description")

    # check bid 'invalid' status
    response = self.app.get('/tenders/{}/bids/{}?acc_token={}'.format(self.tender_id, bid['id'], bid_token))
    self.assertEqual(response.status, '200 OK')
    self.assertEqual(response.json['data']['status'], 'invalid')

    # try to delete 'invalid' bid
    response = self.app.delete('/tenders/{}/bids/{}?acc_token={}'.format(self.tender_id, bid['id'], bid_token))
    self.assertEqual(response.status, '200 OK')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['data']['id'], bid['id'])
    self.assertEqual(response.json['data']['status'], 'deleted')

    response = self.app.post_json('/tenders/{}/bids'.format(
        self.tender_id), {'data': {'selfEligible': True, 'selfQualified': True,
                                   'tenderers': self.test_bids_data[0]['tenderers'],
                                   "value": {
                                       "annualCostsReduction": 950,
                                       "yearlyPayments": 0.9,
                                       "contractDuration": 7
                                   }}
                          })
    response = self.app.post_json('/tenders/{}/bids'.format(
        self.tender_id), {'data': {'selfEligible': True, 'selfQualified': True,
                                   'tenderers': self.test_bids_data[1]['tenderers'],
                                   "value": {
                                       "annualCostsReduction": 950,
                                       "yearlyPayments": 0.9,
                                       "contractDuration": 8
                                   }}
                          })

    # switch to active.pre-qualification
    self.set_status('active.pre-qualification', {"id": self.tender_id, 'status': 'active.tendering'})
    self.app.authorization = ('Basic', ('chronograph', ''))
    response = self.app.patch_json('/tenders/{}'.format(
        self.tender_id), {"data": {"id": self.tender_id}})
    self.assertEqual(response.json['data']['status'], 'active.pre-qualification')

    # qualify bids
    response = self.app.get('/tenders/{}/qualifications'.format(self.tender_id))
    self.app.authorization = ('Basic', ('token', ''))
    for qualification in response.json['data']:
        response = self.app.patch_json('/tenders/{}/qualifications/{}'.format(
            self.tender_id, qualification['id']), {"data": {"status": "active", "qualified": True, "eligible": True}})
        self.assertEqual(response.status, "200 OK")

    # switch to active.pre-qualification.stand-still
    response = self.app.patch_json('/tenders/{}?acc_token={}'.format(
        self.tender_id, self.tender_token), {"data": {"status": 'active.pre-qualification.stand-still'}})
    self.assertEqual(response.json['data']['status'], 'active.pre-qualification.stand-still')

    # switch to active.auction
    self.set_status('active.auction', {"id": self.tender_id, 'status': 'active.pre-qualification.stand-still'})
    self.app.authorization = ('Basic', ('chronograph', ''))
    response = self.app.patch_json('/tenders/{}'.format(
        self.tender_id), {"data": {"id": self.tender_id}})
    self.assertEqual(response.json['data']['status'], "active.auction")

    # switch to qualification
    self.app.authorization = ('Basic', ('auction', ''))
    response = self.app.get('/tenders/{}/auction'.format(self.tender_id))
    auction_bids_data = response.json['data']['bids']
    response = self.app.post_json('/tenders/{}/auction'.format(self.tender_id),
                                  {'data': {'bids': auction_bids_data}})
    self.assertEqual(response.status, "200 OK")
    response = self.app.get('/tenders/{}'.format(self.tender_id))
    self.assertEqual(response.json['data']['status'], "active.qualification")

    # get awards
    response = self.app.get('/tenders/{}/awards'.format(self.tender_id))
    # get pending award
    award_id = [i['id'] for i in response.json['data'] if i['status'] == 'pending'][0]

    self.app.authorization = ('Basic', ('token', ''))
    self.app.patch_json('/tenders/{}/awards/{}?acc_token={}'.format(
        self.tender_id, award_id, self.tender_token),
        {"data": {"status": "active", "qualified": True, "eligible": True}})
    self.assertEqual(response.status, "200 OK")
    response = self.app.get('/tenders/{}'.format(self.tender_id))
    self.assertEqual(response.json['data']['status'], "active.awarded")

    # time travel
    tender = self.db.get(self.tender_id)
    for i in tender.get('awards', []):
        i['complaintPeriod']['endDate'] = i['complaintPeriod']['startDate']
    self.db.save(tender)

    # sign contract
    response = self.app.get('/tenders/{}'.format(self.tender_id))
    contract_id = response.json['data']['contracts'][-1]['id']
    self.app.authorization = ('Basic', ('token', ''))
    self.app.patch_json('/tenders/{}/contracts/{}?acc_token={}'.format(
        self.tender_id, contract_id, self.tender_token), {"data": {"status": "active"}})
    response = self.app.get('/tenders/{}'.format(self.tender_id))
    self.assertEqual(response.json['data']['status'], 'complete')

    # finished tender does not show deleted bid info
    response = self.app.get('/tenders/{}'.format(self.tender_id))
    self.assertEqual(response.status, '200 OK')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(len(response.json['data']['bids']), 4)
    bid_data = response.json['data']['bids'][1]
    self.assertEqual(bid_data['id'], bid['id'])
    self.assertEqual(bid_data['status'], 'deleted')
    self.assertFalse('value' in bid_data)
    self.assertFalse('tenderers' in bid_data)
    self.assertFalse('date' in bid_data)


def deleted_bid_is_not_restorable(self):
    response = self.app.post_json('/tenders/{}/bids'.format(
        self.tender_id), {'data': self.test_bids_data[0]})
    self.assertEqual(response.status, '201 Created')
    self.assertEqual(response.content_type, 'application/json')
    bid = response.json['data']
    bid_token = response.json['access']['token']

    response = self.app.delete('/tenders/{}/bids/{}?acc_token={}'.format(self.tender_id, bid['id'], bid_token))
    self.assertEqual(response.status, '200 OK')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['data']['id'], bid['id'])
    self.assertEqual(response.json['data']['status'], 'deleted')

    # try to restore deleted bid
    response = self.app.patch_json('/tenders/{}/bids/{}?acc_token={}'.format(self.tender_id, bid['id'], bid_token),
                                   {"data": {
                                       'status': 'pending',
                                   }}, status=403)
    self.assertEqual(response.status, '403 Forbidden')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['errors'][0]["description"], "Can't update bid in (deleted) status")

    response = self.app.get('/tenders/{}/bids/{}?acc_token={}'.format(self.tender_id, bid['id'], bid_token))
    self.assertEqual(response.status, '200 OK')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['data']['status'], 'deleted')


def bid_Administrator_change(self):
    response = self.app.post_json('/tenders/{}/bids'.format(
        self.tender_id), {'data': self.test_bids_data[0]})
    self.assertEqual(response.status, '201 Created')
    self.assertEqual(response.content_type, 'application/json')
    bid = response.json['data']

    self.app.authorization = ('Basic', ('administrator', ''))
    response = self.app.patch_json('/tenders/{}/bids/{}'.format(self.tender_id, bid['id']), {"data": {
        'selfEligible': True, 'selfQualified': True,
        'tenderers': [{"identifier": {"id": "00000000"}}],
        "value": {"amount": 400}
    }})
    self.assertEqual(response.status, '200 OK')
    self.assertEqual(response.content_type, 'application/json')
    self.assertNotEqual(response.json['data']["value"]["amount"], 400)
    self.assertEqual(response.json['data']["tenderers"][0]["identifier"]["id"], "00000000")


def bids_activation_on_tender_documents(self):
    bids_access = {}

    # submit bids
    for _ in range(2):
        response = self.app.post_json('/tenders/{}/bids'.format(
            self.tender_id), {'data': self.test_bids_data[0]})
        self.assertEqual(response.status, '201 Created')
        self.assertEqual(response.content_type, 'application/json')
        bids_access[response.json['data']['id']] = response.json['access']['token']

    # check initial status
    for bid_id, token in bids_access.items():
        response = self.app.get('/tenders/{}/bids/{}?acc_token={}'.format(self.tender_id, bid_id, token))
        self.assertEqual(response.status, '200 OK')
        self.assertEqual(response.json['data']['status'], 'pending')

    response = self.app.post('/tenders/{}/documents?acc_token={}'.format(
        self.tender_id, self.tender_token), upload_files=[('file', u'укр.doc', 'content')])
    self.assertEqual(response.status, '201 Created')
    self.assertEqual(response.content_type, 'application/json')

    for bid_id, token in bids_access.items():
        response = self.app.get('/tenders/{}/bids/{}?acc_token={}'.format(self.tender_id, bid_id, token))
        self.assertEqual(response.status, '200 OK')
        self.assertEqual(response.json['data']['status'], 'invalid')

    # activate bids
    for bid_id, token in bids_access.items():
        response = self.app.patch_json('/tenders/{}/bids/{}?acc_token={}'.format(self.tender_id, bid_id, token),
                                       {'data': {'status': 'pending'}})
        self.assertEqual(response.status, '200 OK')
        self.assertEqual(response.json['data']['status'], 'pending')


def bids_invalidation_on_tender_change(self):
    bids_access = {}

    # submit bids
    for data in self.test_bids_data:
        response = self.app.post_json('/tenders/{}/bids'.format(
            self.tender_id), {'data': data})
        self.assertEqual(response.status, '201 Created')
        self.assertEqual(response.content_type, 'application/json')
        bids_access[response.json['data']['id']] = response.json['access']['token']

    # check initial status
    for bid_id, token in bids_access.items():
        response = self.app.get('/tenders/{}/bids/{}?acc_token={}'.format(self.tender_id, bid_id, token))
        self.assertEqual(response.status, '200 OK')
        self.assertEqual(response.json['data']['status'], 'pending')

    # update tender. we can set value that is less than a value in bids as
    # they will be invalidated by this request
    response = self.app.patch_json('/tenders/{}?acc_token={}'.format(self.tender_id, self.tender_token), {"data":
        {
            "description": "new description"}
    })
    self.assertEqual(response.status, '200 OK')
    self.assertEqual(response.json['data']["description"], "new description")

    # check bids status
    for bid_id, token in bids_access.items():
        response = self.app.get('/tenders/{}/bids/{}?acc_token={}'.format(self.tender_id, bid_id, token))
        self.assertEqual(response.status, '200 OK')
        self.assertEqual(response.json['data']['status'], 'invalid')
    # try to add documents to bid
    for doc_resource in ['documents', 'financial_documents', 'eligibility_documents', 'qualification_documents']:
        response = self.app.post('/tenders/{}/bids/{}/{}?acc_token={}'.format(
            self.tender_id, bid_id, doc_resource, token),
            upload_files=[('file', 'name_{}.doc'.format(doc_resource[:-1]), 'content')], status=403)
        self.assertEqual(response.status, '403 Forbidden')
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(response.json['errors'][0]["description"], "Can't add document to 'invalid' bid")

    # check that tender status change does not invalidate bids
    # submit one more bid. check for invalid value first
    # comment test while minValue = 0
    # response = self.app.post_json('/tenders/{}/bids'.format(self.tender_id), {'data': self.test_bids_data[0]},
    #                               status=422)
    # self.assertEqual(response.status, '422 Unprocessable Entity')
    # self.assertEqual(response.content_type, 'application/json')
    # self.assertEqual(response.json['status'], 'error')
    # self.assertEqual(response.json['errors'], [
    #     {u'description': [u'value of bid should be greater than minValue of tender'], u'location': u'body',
    #      u'name': u'value'}
    # ])
    # and submit valid bid
    data = deepcopy(self.test_bids_data[0])
    data['value'] = {
        "annualCostsReduction": 950,
        "yearlyPayments": 0.9,
        "contractDuration": 8
    }
    response = self.app.post_json('/tenders/{}/bids'.format(self.tender_id), {'data': data})
    self.assertEqual(response.status, '201 Created')
    valid_bid_id = response.json['data']['id']
    valid_bid_token = response.json['access']['token']
    valid_bid_date = response.json['data']['date']

    response = self.app.post_json('/tenders/{}/bids'.format(
        self.tender_id), {'data': {'selfEligible': True, 'selfQualified': True,
                                   'tenderers': self.test_bids_data[1]['tenderers'],
                                   "value": {
                                       "annualCostsReduction": 950,
                                       "yearlyPayments": 0.9,
                                       "contractDuration": 7
                                   }}})

    # switch to active.pre-qualification
    self.set_status('active.pre-qualification', {"id": self.tender_id, 'status': 'active.tendering'})
    self.app.authorization = ('Basic', ('chronograph', ''))
    response = self.app.patch_json('/tenders/{}'.format(
        self.tender_id), {"data": {"id": self.tender_id}})
    self.assertEqual(response.json['data']['status'], 'active.pre-qualification')

    # qualify bids
    response = self.app.get('/tenders/{}/qualifications'.format(self.tender_id))
    self.app.authorization = ('Basic', ('token', ''))
    for qualification in response.json['data']:
        response = self.app.patch_json('/tenders/{}/qualifications/{}'.format(
            self.tender_id, qualification['id']),
            {"data": {"status": "active", "qualified": True, "eligible": True}})
        self.assertEqual(response.status, "200 OK")
    response = self.app.get(
        '/tenders/{}/bids/{}?acc_token={}'.format(self.tender_id, valid_bid_id, valid_bid_token))
    self.assertEqual(response.json['data']['status'], 'active')

    # switch to active.pre-qualification.stand-still
    response = self.app.patch_json('/tenders/{}'.format(
        self.tender_id), {"data": {"status": 'active.pre-qualification.stand-still'}})
    self.assertEqual(response.json['data']['status'], 'active.pre-qualification.stand-still')

    # switch to active.auction
    self.set_status('active.auction', {"id": self.tender_id, 'status': 'active.pre-qualification.stand-still'})
    self.app.authorization = ('Basic', ('chronograph', ''))
    response = self.app.patch_json('/tenders/{}'.format(
        self.tender_id), {"data": {"id": self.tender_id}})
    self.assertEqual(response.json['data']['status'], "active.auction")

    # switch to qualification
    self.app.authorization = ('Basic', ('auction', ''))
    response = self.app.get('/tenders/{}/auction'.format(self.tender_id))
    auction_bids_data = response.json['data']['bids']
    response = self.app.post_json('/tenders/{}/auction'.format(self.tender_id),
                                  {'data': {'bids': auction_bids_data}})
    self.assertEqual(response.status, "200 OK")
    response = self.app.get('/tenders/{}'.format(self.tender_id))
    self.assertEqual(response.json['data']['status'], "active.qualification")
    # tender should display all bids
    self.assertEqual(len(response.json['data']['bids']), 4)
    self.assertEqual(response.json['data']['bids'][2]['date'], valid_bid_date)
    # invalidated bids should show only 'id' and 'status' fields
    for bid in response.json['data']['bids']:
        if bid['status'] == 'invalid':
            self.assertTrue('id' in bid)
            self.assertFalse('value' in bid)
            self.assertFalse('tenderers' in bid)
            self.assertFalse('date' in bid)

    # invalidated bids stay invalidated
    for bid_id, token in bids_access.items():
        response = self.app.get('/tenders/{}/bids/{}'.format(self.tender_id, bid_id))
        self.assertEqual(response.status, '200 OK')
        self.assertEqual(response.json['data']['status'], 'invalid')
        # invalidated bids displays only 'id' and 'status' fields
        self.assertFalse('value' in response.json['data'])
        self.assertFalse('tenderers' in response.json['data'])
        self.assertFalse('date' in response.json['data'])

    # and valid bid is not invalidated
    response = self.app.get('/tenders/{}/bids/{}'.format(self.tender_id, valid_bid_id))
    self.assertEqual(response.status, '200 OK')
    self.assertEqual(response.json['data']['status'], 'active')
    # and displays all his data
    self.assertTrue('value' in response.json['data'])
    self.assertTrue('tenderers' in response.json['data'])
    self.assertTrue('date' in response.json['data'])

    # check bids availability on finished tender
    self.set_status('complete')
    response = self.app.get('/tenders/{}'.format(self.tender_id))
    self.assertEqual(response.status, '200 OK')
    self.assertEqual(len(response.json['data']['bids']), 4)
    for bid in response.json['data']['bids']:
        if bid['id'] in bids_access:  # previously invalidated bids
            self.assertEqual(bid['status'], 'invalid')
            self.assertFalse('value' in bid)
            self.assertFalse('tenderers' in bid)
            self.assertFalse('date' in bid)
        else:  # valid bid
            self.assertEqual(bid['status'], 'active')
            self.assertTrue('value' in bid)
            self.assertTrue('tenderers' in bid)
            self.assertTrue('date' in bid)


def deleted_bid_do_not_locks_tender_in_state(self):
    bids = []
    bids_tokens = []
    for bid_annual_cost_reduction in (800, 750):
        response = self.app.post_json('/tenders/{}/bids'.format(
            self.tender_id), {'data': {'selfEligible': True, 'selfQualified': True,
                                       'tenderers': [self.author_data],
                                       "value": {
                                           "annualCostsReduction": bid_annual_cost_reduction,
                                           "yearlyPayments": 0.9,
                                           "contractDuration": 10
                                       }}})
        self.assertEqual(response.status, '201 Created')
        self.assertEqual(response.content_type, 'application/json')
        bids.append(response.json['data'])
        bids_tokens.append(response.json['access']['token'])

    # delete first bid
    response = self.app.delete(
        '/tenders/{}/bids/{}?acc_token={}'.format(self.tender_id, bids[0]['id'], bids_tokens[0]))
    self.assertEqual(response.status, '200 OK')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['data']['id'], bids[0]['id'])
    self.assertEqual(response.json['data']['status'], 'deleted')

    response = self.app.post_json('/tenders/{}/bids'.format(
        self.tender_id), {'data': {'selfEligible': True, 'selfQualified': True,
                                   'tenderers': [self.author_data],
                                   "value": {
                                       "annualCostsReduction": 950,
                                       "yearlyPayments": 0.9,
                                       "contractDuration": 10
                                   }}})

    # switch to active.pre-qualification
    self.set_status('active.pre-qualification', {"id": self.tender_id, 'status': 'active.tendering'})
    self.app.authorization = ('Basic', ('chronograph', ''))
    response = self.app.patch_json('/tenders/{}'.format(
        self.tender_id), {"data": {"id": self.tender_id}})
    self.assertEqual(response.json['data']['status'], 'active.pre-qualification')

    # qualify bids
    response = self.app.get('/tenders/{}/qualifications'.format(self.tender_id))
    self.app.authorization = ('Basic', ('token', ''))
    for qualification in response.json['data']:
        response = self.app.patch_json('/tenders/{}/qualifications/{}'.format(
            self.tender_id, qualification['id']),
            {"data": {"status": "active", "qualified": True, "eligible": True}})
        self.assertEqual(response.status, "200 OK")

    # switch to active.pre-qualification.stand-still
    response = self.app.patch_json('/tenders/{}'.format(
        self.tender_id), {"data": {"status": 'active.pre-qualification.stand-still'}})
    self.assertEqual(response.json['data']['status'], 'active.pre-qualification.stand-still')

    # switch to active.auction
    self.set_status('active.auction',
                    {"id": self.tender_id, 'status': 'active.pre-qualification.stand-still'})
    self.app.authorization = ('Basic', ('chronograph', ''))
    response = self.app.patch_json('/tenders/{}'.format(
        self.tender_id), {"data": {"id": self.tender_id}})
    self.assertEqual(response.json['data']['status'], "active.auction")

    # switch to qualification
    self.app.authorization = ('Basic', ('auction', ''))
    response = self.app.get('/tenders/{}/auction'.format(self.tender_id))
    auction_bids_data = response.json['data']['bids']
    response = self.app.post_json('/tenders/{}/auction'.format(self.tender_id),
                                  {'data': {'bids': auction_bids_data}})
    self.assertEqual(response.status, "200 OK")
    response = self.app.get('/tenders/{}'.format(self.tender_id))
    self.assertEqual(response.json['data']['status'], "active.qualification")

    # check bids
    response = self.app.get('/tenders/{}'.format(self.tender_id))
    self.assertEqual(response.status, '200 OK')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(len(response.json['data']['bids']), 3)
    self.assertEqual(response.json['data']['bids'][0]['status'], 'deleted')
    self.assertEqual(response.json['data']['bids'][1]['status'], 'active')
    self.assertEqual(response.json['data']['bids'][2]['status'], 'active')

# TenderBidFeaturesResourceTest


def features_bid_invalid(self):
    data = deepcopy(self.test_bids_data[0])
    response = self.app.post_json('/tenders/{}/bids'.format(self.tender_id), {'data': data}, status=422)
    self.assertEqual(response.status, '422 Unprocessable Entity')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['status'], 'error')
    self.assertEqual(response.json['errors'], [
        {u'description': [u'This field is required.'], u'location': u'body', u'name': u'parameters'}
    ])
    data["parameters"] = [
        {
            "code": "OCDS-123454-AIR-INTAKE",
            "value": 0.1,
        }
    ]
    response = self.app.post_json('/tenders/{}/bids'.format(self.tender_id), {'data': data}, status=422)
    self.assertEqual(response.status, '422 Unprocessable Entity')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['status'], 'error')
    self.assertEqual(response.json['errors'], [
        {u'description': [u'All features parameters is required.'], u'location': u'body', u'name': u'parameters'}
    ])
    data["parameters"].append({
        "code": "OCDS-123454-AIR-INTAKE",
        "value": 0.1,
    })
    response = self.app.post_json('/tenders/{}/bids'.format(self.tender_id), {'data': data}, status=422)
    self.assertEqual(response.status, '422 Unprocessable Entity')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['status'], 'error')
    self.assertEqual(response.json['errors'], [
        {u'description': [u'Parameter code should be uniq for all parameters'], u'location': u'body', u'name': u'parameters'}
    ])
    data["parameters"][1]["code"] = "OCDS-123454-YEARS"
    data["parameters"][1]["value"] = 0.2
    response = self.app.post_json('/tenders/{}/bids'.format(self.tender_id), {'data': data}, status=422)
    self.assertEqual(response.status, '422 Unprocessable Entity')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['status'], 'error')
    self.assertEqual(response.json['errors'], [
        {u'description': [{u'value': [u'value should be one of feature value.']}], u'location': u'body', u'name': u'parameters'}
    ])


def features_bid(self):
    bid_data = deepcopy(self.test_bids_data[0])
    bid_data.update({
        "parameters": [
            {
                "code": i["code"],
                "value": 0.1,
            }
            for i in self.initial_data['features']
        ]
    })
    for i in [bid_data] * 2:
        response = self.app.post_json('/tenders/{}/bids'.format(self.tender_id), {'data': i})
        i['status'] = "pending"
        self.assertEqual(response.status, '201 Created')
        self.assertEqual(response.content_type, 'application/json')
        bid = response.json['data']
        bid.pop(u'date')
        bid.pop(u'id')
        self.assertEqual(set(bid), set(i))


def patch_and_put_document_into_invalid_bid(self):
    doc_id_by_type = {}
    for doc_resource in ['documents', 'financial_documents', 'eligibility_documents', 'qualification_documents']:
        response = self.app.post('/tenders/{}/bids/{}/{}?acc_token={}'.format(
            self.tender_id, self.bid_id, doc_resource, self.bid_token), upload_files=[('file', 'name_{}.doc'.format(doc_resource[:-1]), 'content')])

        self.assertEqual(response.status, '201 Created')
        self.assertEqual(response.content_type, 'application/json')
        doc_id = response.json["data"]['id']
        self.assertIn(doc_id, response.headers['Location'])
        self.assertEqual('name_{}.doc'.format(doc_resource[:-1]), response.json["data"]["title"])
        key = response.json["data"]["url"].split('?')[-1]
        doc_id_by_type[doc_resource] = {'id': doc_id, 'key': key}

    # update tender. we can set value that is less than a value in bids as
    # they will be invalidated by this request
    response = self.app.patch_json('/tenders/{}?acc_token={}'.format(self.tender_id, self.tender_token), {"data":
            {"description": "new description"}
    })
    self.assertEqual(response.status, '200 OK')
    self.assertEqual(response.json['data']["description"], "new description")

    for doc_resource in ['documents', 'financial_documents', 'eligibility_documents', 'qualification_documents']:
        doc_id = doc_id_by_type[doc_resource]['id']
        response = self.app.patch_json('/tenders/{}/bids/{}/{}/{}?acc_token={}'.format(
            self.tender_id, self.bid_id, doc_resource, doc_id, self.bid_token), { "data": {
                'confidentiality': 'buyerOnly',
                'confidentialityRationale': 'Only our company sells badgers with pink hair.',
            }}, status=403)
        self.assertEqual(response.status, '403 Forbidden')
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(response.json['errors'][0]["description"], "Can't update document data for 'invalid' bid")
        response = self.app.put('/tenders/{}/bids/{}/{}/{}?acc_token={}'.format(
            self.tender_id, self.bid_id, doc_resource, doc_id, self.bid_token), 'updated', content_type='application/msword', status=403)
        self.assertEqual(response.status, '403 Forbidden')
        self.assertEqual(response.json['errors'][0]["description"], "Can't update document in 'invalid' bid")
