# -*- coding: utf-8 -*-
from datetime import timedelta

from openprocurement.api.utils import get_now

# TenderContractResourceTest


def patch_tender_contract(self):
    response = self.app.get('/tenders/{}/contracts'.format(self.tender_id))
    contract = response.json['data'][0]

    fake_contractID = "myselfID"
    fake_items_data = [{"description": "New Description"}]
    fake_suppliers_data = [{"name": "New Name"}]

    response = self.app.patch_json('/tenders/{}/contracts/{}?acc_token={}'.format(self.tender_id, contract['id'], self.tender_token), {
        "data": {"contractID": fake_contractID, "items": fake_items_data, "suppliers": fake_suppliers_data}})

    response = self.app.get('/tenders/{}/contracts/{}'.format(self.tender_id, contract['id']))
    self.assertNotEqual(fake_contractID, response.json['data']['contractID'])
    self.assertNotEqual(fake_items_data, response.json['data']['items'])
    self.assertNotEqual(fake_suppliers_data, response.json['data']['suppliers'])

    response = self.app.patch_json('/tenders/{}/contracts/{}?acc_token={}'.format(self.tender_id, contract['id'], self.tender_token),
                                   {"data": {"value": {"currency": "USD"}}}, status=403)
    self.assertEqual(response.status, '403 Forbidden')
    self.assertEqual(response.json['errors'][0]["description"], "Can\'t update currency for contract value")

    response = self.app.patch_json('/tenders/{}/contracts/{}?acc_token={}'.format(self.tender_id, contract['id'], self.tender_token),
                                   {"data": {"value": {"valueAddedTaxIncluded": False}}}, status=403)
    self.assertEqual(response.status, '403 Forbidden')
    self.assertEqual(response.json['errors'][0]["description"],
                     "Can\'t update valueAddedTaxIncluded for contract value")

    response = self.app.patch_json('/tenders/{}/contracts/{}?acc_token={}'.format(self.tender_id, contract['id'], self.tender_token),
                                   {"data": {
                                       "value": {
                                           "annualCostsReduction": 300.6,
                                           "yearlyPayments": 0.9,
                                           "contractDuration": 6
                                       }
                                   }}, status=403)
    self.assertEqual(response.status, '403 Forbidden')
    self.assertEqual(response.json['errors'][0]["description"],
                     "Value amount should be equal to awarded amount (698.444)")

    response = self.app.patch_json('/tenders/{}/contracts/{}?acc_token={}'.format(self.tender_id, contract['id'], self.tender_token),
                                   {"data": {
                                       "value": {
                                           "annualCostsReduction": 751.5,
                                           "yearlyPayments": 0.9,
                                           "contractDuration": 10
                                       }
                                   }})
    self.assertEqual(response.status, '200 OK')
    #  XXX: Useless check, because contract.value.amount should be strictly equal to award.amount.value and patch request will not return any data
    # self.assertEqual(response.json['data']['value']['amount'], 698.444)

    response = self.app.patch_json('/tenders/{}/contracts/{}?acc_token={}'.format(self.tender_id, contract['id'], self.tender_token),
                                   {"data": {"status": "active"}}, status=403)
    self.assertEqual(response.status, '403 Forbidden')
    self.assertEqual(response.content_type, 'application/json')
    self.assertIn("Can't sign contract before stand-still period end (", response.json['errors'][0]["description"])

    self.set_status('complete', {'status': 'active.awarded'})

    token = self.initial_bids_tokens[self.initial_bids[0]['id']]
    response = self.app.post_json('/tenders/{}/awards/{}/complaints?acc_token={}'.format(
        self.tender_id, self.award_id, token),
        {'data': {'title': 'complaint title', 'description': 'complaint description', 'author': self.supplier_info}})
    self.assertEqual(response.status, '201 Created')
    complaint = response.json['data']
    owner_token = response.json['access']['token']

    response = self.app.patch_json(
        '/tenders/{}/awards/{}/complaints/{}?acc_token={}'.format(self.tender_id, self.award_id, complaint['id'],
                                                                  owner_token), {"data": {"status": "pending"}})
    self.assertEqual(response.status, '200 OK')

    tender = self.db.get(self.tender_id)
    for i in tender.get('awards', []):
        i['complaintPeriod']['endDate'] = i['complaintPeriod']['startDate']
    self.db.save(tender)

    response = self.app.patch_json('/tenders/{}/contracts/{}?acc_token={}'.format(self.tender_id, contract['id'], self.tender_token),
                                   {"data": {"dateSigned": i['complaintPeriod']['endDate']}}, status=422)
    self.assertEqual(response.status, '422 Unprocessable Entity')
    self.assertEqual(response.json['errors'], [{u'description': [
        u'Contract signature date should be after award complaint period end date ({})'.format(
            i['complaintPeriod']['endDate'])], u'location': u'body', u'name': u'dateSigned'}])

    one_hour_in_furure = (get_now() + timedelta(hours=1)).isoformat()
    response = self.app.patch_json('/tenders/{}/contracts/{}?acc_token={}'.format(self.tender_id, contract['id'], self.tender_token),
                                   {"data": {"dateSigned": one_hour_in_furure}}, status=422)
    self.assertEqual(response.status, '422 Unprocessable Entity')
    self.assertEqual(response.json['errors'], [
        {u'description': [u"Contract signature date can't be in the future"], u'location': u'body',
         u'name': u'dateSigned'}])

    custom_signature_date = get_now().isoformat()
    response = self.app.patch_json('/tenders/{}/contracts/{}?acc_token={}'.format(self.tender_id, contract['id'], self.tender_token),
                                   {"data": {"dateSigned": custom_signature_date}})
    self.assertEqual(response.status, '200 OK')

    response = self.app.patch_json('/tenders/{}/contracts/{}?acc_token={}'.format(self.tender_id, contract['id'], self.tender_token),
                                   {"data": {"status": "active"}}, status=403)
    self.assertEqual(response.status, '403 Forbidden')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['errors'][0]["description"], "Can't sign contract before reviewing all complaints")

    response = self.app.patch_json(
        '/tenders/{}/awards/{}/complaints/{}?acc_token={}'.format(self.tender_id, self.award_id, complaint['id'],
                                                                  owner_token), {"data": {
            "status": "stopping",
            "cancellationReason": "reason"
        }})
    self.assertEqual(response.status, '200 OK')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['data']["status"], "stopping")

    authorization = self.app.authorization
    self.app.authorization = ('Basic', ('reviewer', ''))
    response = self.app.patch_json(
        '/tenders/{}/awards/{}/complaints/{}'.format(self.tender_id, self.award_id, complaint['id']), {'data': {
            'status': 'stopped'
        }})
    self.assertEqual(response.status, '200 OK')
    self.assertEqual(response.json['data']["status"], "stopped")

    self.app.authorization = authorization
    response = self.app.patch_json('/tenders/{}/contracts/{}?acc_token={}'.format(self.tender_id, contract['id'], self.tender_token),
                                   {"data": {"status": "active"}})
    self.assertEqual(response.status, '200 OK')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['data']["status"], "active")

    response = self.app.patch_json('/tenders/{}/contracts/{}?acc_token={}'.format(
        self.tender_id, contract['id'], self.tender_token), {"data": {
        "value": {
            "annualCostsReduction": 780.5,
            "yearlyPayments": 0.9,
            "contractDuration": 10
        },
        "contractID": "myselfID",
        "title": "New Title",
        "items": [{"description": "New Description"}],
        "suppliers": [{"name": "New Name"}]}}, status=403)
    self.assertEqual(response.status, '403 Forbidden')
    self.assertEqual(response.json['errors'][0]["description"],
                     "Can't update contract in current (complete) tender status")

    response = self.app.patch_json('/tenders/{}/contracts/{}?acc_token={}'.format(self.tender_id, contract['id'], self.tender_token),
                                   {"data": {"status": "active"}}, status=403)
    self.assertEqual(response.status, '403 Forbidden')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['errors'][0]["description"],
                     "Can't update contract in current (complete) tender status")

    response = self.app.patch_json('/tenders/{}/contracts/{}?acc_token={}'.format(self.tender_id, contract['id'], self.tender_token),
                                   {"data": {"status": "pending"}}, status=403)
    self.assertEqual(response.status, '403 Forbidden')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['errors'][0]["description"],
                     "Can't update contract in current (complete) tender status")

    response = self.app.patch_json('/tenders/{}/contracts/some_id'.format(self.tender_id),
                                   {"data": {"status": "active"}}, status=404)
    self.assertEqual(response.status, '404 Not Found')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['status'], 'error')
    self.assertEqual(response.json['errors'], [
        {u'description': u'Not Found', u'location':
            u'url', u'name': u'contract_id'}
    ])

    response = self.app.patch_json('/tenders/some_id/contracts/some_id', {"data": {"status": "active"}}, status=404)
    self.assertEqual(response.status, '404 Not Found')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['status'], 'error')
    self.assertEqual(response.json['errors'], [
        {u'description': u'Not Found', u'location':
            u'url', u'name': u'tender_id'}
    ])

    response = self.app.get('/tenders/{}/contracts/{}'.format(self.tender_id, contract['id']))
    self.assertEqual(response.status, '200 OK')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['data']["status"], "active")
    self.assertEqual(response.json['data']["value"]['amount'], 698.444)


def contract_items_without_quantity_deliveryDate(self):
    auth = self.app.authorization
    self.app.authorization = ('Basic', ('token', ''))
    response = self.app.post_json('/tenders/{}/contracts'.format(
        self.tender_id),
        {'data': {'title': 'contract title', 'description': 'contract description', 'awardID': self.award_id, "items": [
            {
                "description": u"футляри до державних нагород",
                "description_en": u"Cases for state awards",
                "classification": {
                    "scheme": u"CPV",
                    "id": u"44617100-9",
                    "description": u"Cartons"
                },
                "additionalClassifications": [
                    {
                        "scheme": u"ДКПП",
                        "id": u"17.21.1",
                        "description": u"папір і картон гофровані, паперова й картонна тара"
                    }
                ],
                "unit": {
                    "name": u"item",
                    "code": u"44617100-9"
                },
                "quantity": 5,
                "deliveryDate": {
                    "startDate": (get_now() + timedelta(days=2)).isoformat(),
                    "endDate": (get_now() + timedelta(days=5)).isoformat()
                },

                "deliveryAddress": {
                    "countryName": u"Україна",
                    "postalCode": "79000",
                    "region": u"м. Київ",
                    "locality": u"м. Київ",
                    "streetAddress": u"вул. Банкова 1"
                }
            }
        ]}})
    self.assertEqual(response.status, '201 Created')
    self.assertEqual(response.content_type, 'application/json')
    contract = response.json['data']

    for item in contract['items']:
        self.assertNotIn('deliveryDate', item)
        self.assertNotIn('quantity', item)

    response = self.app.patch_json('/tenders/{}/contracts/{}'.format(self.tender_id, contract['id']),
        {"data": {'status': 'pending', "items": [{'quantity': 10,
                             "deliveryDate": {
                                 "startDate": (get_now() + timedelta(days=12)).isoformat(),
                                 "endDate": (get_now() + timedelta(days=15)).isoformat()
                             }}]}})
    self.assertEqual(response.status, '200 OK')

    response = self.app.get('/tenders/{}/contracts/{}'.format(self.tender_id, contract['id']))
    self.assertEqual(response.content_type, 'application/json')
    contract = response.json['data']

    for item in contract['items']:
        self.assertNotIn('deliveryDate', item)
        self.assertNotIn('quantity', item)

    self.app.authorization = auth

    response = self.app.post_json('/tenders/{}/contracts?acc_token={}'.format(
        self.tender_id, self.tender_token),
        {'data': {'title': 'contract title', 'description': 'contract description',
                  'awardID': self.award_id}}, status=403)
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.status, '403 Forbidden')
    self.assertEqual(response.json['errors'][0]["description"], "Forbidden")
