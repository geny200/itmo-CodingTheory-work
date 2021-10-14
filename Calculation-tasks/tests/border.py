import unittest

from tools.border import gr_find_k_by_n_d, gr_find_d_by_n_k, vg_find_d_by_n_k, vg_find_k_by_n_d


class BorderTest(unittest.TestCase):

    def test_border(self):
        for n in range(20):
            for k in range(15):
                if not (n >= k > 0):
                    continue
                d = gr_find_d_by_n_k(n, k)
                self.assertLessEqual(d, n, f'Gr(n = {n}, k = {k}, d_eval = {d}): '
                                           f'Calculated d = {d} shoul be less than or equal to n = {n}')
                k_eval = gr_find_k_by_n_d(n, d)
                self.assertLessEqual(k, k_eval, f'Gr(n = {n}, k = {k}, d_eval = {d}): '
                                                f'Calculated k = {k_eval} should be more then or equal to K = {k}')

        for n in range(20):
            for k in range(15):
                if not (n >= k > 0):
                    continue
                d = vg_find_d_by_n_k(n, k)
                self.assertLessEqual(d, n, f'VG(n = {n}, k = {k}, d_eval = {d}): '
                                           f'Calculated d = {d} shoul be less than or equal to n = {n}')
                k_eval = vg_find_k_by_n_d(n, d)
                self.assertLessEqual(k, k_eval, f'VG(n = {n}, k = {k}, d_eval = {d}): '
                                                f'Calculated k = {k_eval} should be more then or equal to K = {k}')


if __name__ == '__main__':
    unittest.main()
