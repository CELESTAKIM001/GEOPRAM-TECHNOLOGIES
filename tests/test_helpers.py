import sys, pathlib, unittest
sys.path.insert(0,str(pathlib.Path(__file__).resolve().parents[1]))
from geopram.security import hash_password, verify_password, secure_token
from geopram.documents import validate_invoice, validate_certificate
from geopram.maintenance import normalize_notice
class HelpersTest(unittest.TestCase):
 def test_password_hash_roundtrip(self):
  h=hash_password('correct-horse-battery-staple'); self.assertTrue(verify_password(h,'correct-horse-battery-staple')); self.assertFalse(verify_password(h,'wrong'))
 def test_token(self): self.assertGreaterEqual(len(secure_token()),40)
 def test_invoice(self): self.assertEqual(validate_invoice({'customer_name':'A','amount':'12.345'})['amount'],12.35)
 def test_invoice_negative(self):
  with self.assertRaises(ValueError): validate_invoice({'customer_name':'A','amount':-1})
 def test_certificate_required(self):
  with self.assertRaises(ValueError): validate_certificate({'recipient_name':'A'})
 def test_maintenance_scope(self): self.assertEqual(normalize_notice(True,scope='bad')['maintenance_scope'],'global')
if __name__=='__main__': unittest.main()
