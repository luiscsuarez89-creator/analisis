import unittest

from electrocampos_api.client import normalize_records


class NormalizeRecordsTests(unittest.TestCase):
    def test_dict_rows(self):
        payload = {"results": [{"municipio": "Bogotá", "valor": "1.2"}]}
        df = normalize_records(payload)
        self.assertEqual(list(df.columns), ["municipio", "valor"])
        self.assertEqual(df.iloc[0]["municipio"], "Bogotá")

    def test_list_rows_with_columns(self):
        payload = {
            "data": [["Bogotá", 1.2]],
            "columns": [{"fieldName": "municipio"}, {"fieldName": "valor"}],
        }
        df = normalize_records(payload)
        self.assertEqual(list(df.columns), ["municipio", "valor"])
        self.assertAlmostEqual(df.iloc[0]["valor"], 1.2)


if __name__ == "__main__":
    unittest.main()
