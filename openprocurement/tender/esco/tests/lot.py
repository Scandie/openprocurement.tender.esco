# -*- coding: utf-8 -*-
import unittest

from openprocurement.api.tests.base import snitch

from openprocurement.tender.belowthreshold.tests.base import test_organization
from openprocurement.tender.belowthreshold.tests.lot import (
    TenderLotProcessTestMixin
)
from openprocurement.tender.belowthreshold.tests.lot_blanks import (
    create_tender_lot,
    patch_tender_lot,
    delete_tender_lot,
    tender_lot_guarantee,
    tender_lot_document,
    tender_features_invalid
)

from openprocurement.tender.openeu.tests.lot import TenderLotEdgeCasesTestMixin
from openprocurement.tender.openeu.tests.lot_blanks import (
    # TenderLotProcessTest
    one_lot_1bid,
    one_lot_2bid_1unqualified,
    one_lot_2bid,
    two_lot_2bid_1lot_del,
    one_lot_3bid_1del,
    one_lot_3bid_1un,
    two_lot_1can,
    two_lot_2bid_0com_1can,
    two_lot_2bid_2com_2win,
    two_lot_3bid_1win_bug,
)

from openprocurement.tender.esco.tests.base import (
    BaseESCOEUContentWebTest,
    test_tender_data,
    test_lots,
    test_bids,
)

from openprocurement.tender.esco.tests.lot_blanks import (
    create_tender_lot_invalid,
    patch_tender_lot_minValue,
    get_tender_lot,
    get_tender_lots,
    tender_min_value,
    # TenderLotFeatureBidderResourceTest
    create_tender_feature_bid_invalid,
    create_tender_feature_bid,
    # TenderLotBidResourceTest
    create_tender_bid_invalid,
    patch_tender_bid,
)


class TenderLotResourceTest(BaseESCOEUContentWebTest):

    initial_auth = ('Basic', ('broker', ''))
    test_lots_data = test_lots  # TODO: change attribute identifier
    initial_data = test_tender_data

    test_create_tender_lot_invalid = snitch(create_tender_lot_invalid)
    test_create_tender_lot = snitch(create_tender_lot)
    test_patch_tender_lot = snitch(patch_tender_lot)
    test_patch_tender_lot_minValue = snitch(patch_tender_lot_minValue)
    test_delete_tender_lot = snitch(delete_tender_lot)

    test_tender_lot_guarantee = snitch(tender_lot_guarantee)

    test_get_tender_lot = snitch(get_tender_lot)
    test_get_tender_lots = snitch(get_tender_lots)


class TenderLotEdgeCasesTest(BaseESCOEUContentWebTest, TenderLotEdgeCasesTestMixin):
    initial_auth = ('Basic', ('broker', ''))
    initial_lots = test_lots * 2
    initial_bids = test_bids
    test_author = test_organization


class TenderLotFeatureResourceTest(BaseESCOEUContentWebTest):
    initial_lots = 2 * test_lots
    # for passing test_tender_min_value while min value = 0
    initial_lots[0]['minValue'] = {"amount": 0}
    initial_lots[1]['minValue'] = {"amount": 0}
    initial_auth = ('Basic', ('broker', ''))
    initial_data = test_tender_data
    test_lots_data = test_lots
    invalid_feature_value = 0.4
    max_feature_value = 0.3
    sum_of_max_value_of_all_features = 0.3

    test_tender_min_value = snitch(tender_min_value)
    test_tender_features_invalid = snitch(tender_features_invalid)
    test_tender_lot_document = snitch(tender_lot_document)


class TenderLotBidResourceTest(BaseESCOEUContentWebTest):
    initial_lots = test_lots
    initial_auth = ('Basic', ('broker', ''))
    test_bids_data = test_bids  # TODO: change attribute identifier

    test_create_tender_bid_invalid = snitch(create_tender_bid_invalid)
    test_patch_tender_bid = snitch(patch_tender_bid)


class TenderLotFeatureBidResourceTest(BaseESCOEUContentWebTest):
    initial_lots = test_lots
    initial_auth = ('Basic', ('broker', ''))
    initial_data = test_tender_data
    test_bids_data = test_bids  # TODO: change attribute identifier

    def setUp(self):
        super(TenderLotFeatureBidResourceTest, self).setUp()
        self.lot_id = self.initial_lots[0]['id']
        response = self.app.patch_json('/tenders/{}?acc_token={}'.format(self.tender_id, self.tender_token), {"data": {
            "items": [
                {
                    'relatedLot': self.lot_id,
                    'id': '1'
                }
            ],
            "features": [
                {
                    "code": "code_item",
                    "featureOf": "item",
                    "relatedItem": "1",
                    "title": u"item feature",
                    "enum": [
                        {
                            "value": 0.01,
                            "title": u"good"
                        },
                        {
                            "value": 0.02,
                            "title": u"best"
                        }
                    ]
                },
                {
                    "code": "code_lot",
                    "featureOf": "lot",
                    "relatedItem": self.lot_id,
                    "title": u"lot feature",
                    "enum": [
                        {
                            "value": 0.01,
                            "title": u"good"
                        },
                        {
                            "value": 0.02,
                            "title": u"best"
                        }
                    ]
                },
                {
                    "code": "code_tenderer",
                    "featureOf": "tenderer",
                    "title": u"tenderer feature",
                    "enum": [
                        {
                            "value": 0.01,
                            "title": u"good"
                        },
                        {
                            "value": 0.02,
                            "title": u"best"
                        }
                    ]
                }
            ]
        }})
        self.assertEqual(response.status, '200 OK')
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(response.json['data']['items'][0]['relatedLot'], self.lot_id)

    test_create_tender_bid_invalid = snitch(create_tender_feature_bid_invalid)
    test_create_tender_bid = snitch(create_tender_feature_bid)


class TenderLotProcessTest(BaseESCOEUContentWebTest, TenderLotProcessTestMixin):
    setUp = BaseESCOEUContentWebTest.setUp
    test_lots_data = test_lots  # TODO: change attribute identifier
    test_bids_data = test_bids
    initial_data = test_tender_data

    days_till_auction_starts = 16

    test_1lot_1bid = snitch(one_lot_1bid)
    test_1lot_2bid_1unqualified = snitch(one_lot_2bid_1unqualified)
    test_1lot_2bid = snitch(one_lot_2bid)
    test_2lot_2bid_1lot_del = snitch(two_lot_2bid_1lot_del)
    test_1lot_3bid_1del = snitch(one_lot_3bid_1del)
    test_1lot_3bid_1un = snitch(one_lot_3bid_1un)
    test_2lot_1can = snitch(two_lot_1can)
    test_2lot_2bid_0com_1can = snitch(two_lot_2bid_0com_1can)
    test_2lot_2bid_2com_2win = snitch(two_lot_2bid_2com_2win)
    test_2lot_3bid_1win_bug = snitch(two_lot_3bid_1win_bug)


def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TenderLotResourceTest))
    suite.addTest(unittest.makeSuite(TenderLotEdgeCasesTest))
    suite.addTest(unittest.makeSuite(TenderLotFeatureResourceTest))
    suite.addTest(unittest.makeSuite(TenderLotBidResourceTest))
    suite.addTest(unittest.makeSuite(TenderLotFeatureBidResourceTest))
    suite.addTest(unittest.makeSuite(TenderLotProcessTest))
    return suite


if __name__ == '__main__':
    unittest.main(defaultTest='suite')
