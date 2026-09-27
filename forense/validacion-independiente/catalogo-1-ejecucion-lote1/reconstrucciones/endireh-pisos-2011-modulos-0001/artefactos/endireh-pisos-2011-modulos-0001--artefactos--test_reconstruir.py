"""Pruebas sintéticas de saltos, desconocidos y UPM de contribución cero."""
import unittest
import numpy as np
from reconstruir import recode, union, multiple_codes, estimate

class Rules(unittest.TestCase):
    def test_unknown_not_negative(self):
        y=union([recode(np.array([1,2,9,2])),recode(np.array([9,2,2,9]))])
        np.testing.assert_equal(y,[1,0,np.nan,np.nan])
    def test_annual_structural_skip(self):
        life=np.array([4,1,9]);year=np.array([np.nan,4,np.nan])
        np.testing.assert_equal(recode(np.where(life==4,4,year),(1,2,3),(4,)),[0,0,np.nan])
    def test_multiple_response_validity(self):
        x=multiple_codes([[np.nan,2,99,1],[np.nan,np.nan,np.nan,99]],[1],range(1,11))
        np.testing.assert_equal(x,[np.nan,0,np.nan,1])
    def test_full_frame_zero_contribution(self):
        # Cinco UPM contribuyen; sexta pertenece al marco aunque contribuye cero.
        y=np.tile([0.,1.],50);w=np.ones(100);ui=np.repeat(np.arange(5),20)
        mult=np.tile(np.ones(6),(200,1));mult[::2,0]=0;mult[::2,5]=2
        ans,reason=estimate(y,np.ones(100,bool),w,ui,mult)
        self.assertEqual(reason,'');self.assertEqual(ans[:3],(.5,.5,.5))
    def test_suppression(self):
        ans,reason=estimate(np.ones(99),np.ones(99,bool),np.ones(99),np.arange(99),np.ones((200,99)))
        self.assertIsNone(ans);self.assertIn('SUPRIMIDO',reason)

if __name__=='__main__':unittest.main()
