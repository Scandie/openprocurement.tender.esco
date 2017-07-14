# -*- coding: utf-8 -*-
import os
from copy import deepcopy

from openprocurement.tender.openeu.tests.base import (
    BaseTenderWebTest,
    test_features_tender_data as base_eu_test_features_data,
    test_tender_data as base_eu_test_data,
    test_lots as base_eu_lots,
    test_bids as base_eu_bids,
)

NBU_DISCOUNT_RATE = 0.22

test_tender_data = deepcopy(base_eu_test_data)
test_tender_data['procurementMethodType'] = "esco.EU"
test_tender_data['NBUdiscountRate'] = NBU_DISCOUNT_RATE

test_tender_data['minValue'] = test_tender_data['value']
del test_tender_data['value']

test_features_tender_data = deepcopy(base_eu_test_features_data)
test_features_tender_data['procurementMethodType'] = "esco.EU"
test_features_tender_data['NBUdiscountRate'] = NBU_DISCOUNT_RATE

test_features_tender_data['minValue'] = test_features_tender_data['value']
del test_features_tender_data['value']

test_lots = deepcopy(base_eu_lots)
test_lots[0]['minValue'] = test_lots[0]['value']
del test_lots[0]['value']

test_bids = deepcopy(base_eu_bids)
for bid in test_bids:
    bid['value'] = {'yearlyPayments': 0.9,
                       'annualCostsReduction': 751.5,
                       'contractDuration': 10}


class BaseESCOWebTest(BaseTenderWebTest):
    relative_to = os.path.dirname(__file__)
    initial_data = None
    initial_status = None
    initial_bids = None
    initial_lots = None
    initial_auth = ('Basic', ('broker', ''))
    docservice = False



class BaseESCOContentWebTest(BaseESCOWebTest):
    """ ESCO Content Test """
    initialize_initial_data = True

    def setUp(self):
        super(BaseESCOContentWebTest, self).setUp()
        if self.initial_data and self.initialize_initial_data:
            self.create_tender()


class BaseESCOEUContentWebTest(BaseESCOContentWebTest):
    """ ESCO EU Content Test """

    initial_data = test_tender_data
