import unittest
import sys
sys.path.append('../')
from licensing.data import licence_application
from licensing.data.licence_application import LicenceApplication
from licensing.data.location import Locations

class LicenceApplicationTest(unittest.TestCase):
    
    def setUp(self):
        self.visit = LicenceApplication.from_google_row('www.foo.com/apply-for-a-licence/licence-name/body/interaction-X','republic of test')
        
    def test_licence_extraction(self):
        self.assertEqual(self.visit.licence, 'licence-name')
        
    def test_body_extraction(self):
        self.assertEqual(self.visit.body, 'body')
        
    def test_interaction_extraction(self):
        self.assertEqual(self.visit.interaction, 'interaction')
        
    def test_location(self):
        self.assertEqual(self.visit.location, 'republic of test')
        
    def test_equality(self):
        another_application = LicenceApplication.from_google_row('www.foo.com/apply-for-a-licence/licence-name/body/interaction-X','republic of test')
        self.assertEqual(self.visit, another_application)


class LicenceApplicationBatchCreation(unittest.TestCase):
    
    def setUp(self):
        # url, country, visits
        self.stub_google_results_1 = [['/foo/bar/zap/boom','testopia','1'],['/foo/bar/zap/boom','test republic','2']]
        self.stub_google_results_2 = [['/foo/bar/zap/boom','testopia','1'],['not valid','test republic','1']]
    
    def test_batch_creation_of_licence_applications(self):
        licence_applications = licence_application.from_google_data(self.stub_google_results_1)
        #should create an application for each visit
        self.assertEqual(len(list(licence_applications)),3)
    

if __name__ == '__main__':
    unittest.main()
