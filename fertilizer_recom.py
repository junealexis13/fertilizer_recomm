'''
SCRIPT FOR AUTOMATED FERTILIZER RECOMMENDATION SYSTEM:
By: June Alexis Santos
Date: 2026-02-12
for: Project SARAI and Project Sinag
'''

from enum import Enum

class Fertilizers(Enum):
    UREA_PRILLED = {
        "N": 46,
        "P": 0,
        "K": 0
    }
    UREA_GRANULAR = {
        "N": 46,
        "P": 0,
        "K": 0
    }
    AMMOSUL = {
        "N": 21,
        "P": 0,
        "K": 0
    }
    COMPLETE = {
        "N": 14,
        "P": 14,
        "K": 14
    }
    AMMOPHOS = {
        "N": 16,
        "P": 20,
        "K": 0
    }
    MURIATE_OF_POTASH = {
        "N": 0,
        "P": 0,
        "K": 60
    }
    DIAMMONIUM_PHOSPHATE = {
        "N": 18,
        "P": 46,
        "K": 0
    }   



class FertilizerUsed:
    '''Fertilizer object class used for recommendation'''
    def __init__(self):
        self.N = 0
        self.P = 0
        self.K = 0
        self.name = 'custom'

    def get_fert(self, fert_class: str, **kwargs):
        try:
            return Fertilizers[fert_class].value
        except KeyError:
            self.N = kwargs.get('N', 0)
            self.P = kwargs.get('P', 0)
            self.K = kwargs.get('K', 0)
            self.name = kwargs.get('name', 'custom')
            return self.custom_fert(**kwargs)

    def custom_fert(self, **kwargs):
        '''Creates an instance of a fertilizer custom used'''
        self.N = kwargs.get('N', 0)
        self.P = kwargs.get('P', 0)
        self.K = kwargs.get('K', 0)
        self.name = kwargs.get('name', 'custom')
        return {'N': self.N, 'P': self.P, 'K': self.K, 'name': self.name}



class FertilizerRecommendation:
    def __init__(self, fertilizer_required: dict, area: float):
        self.fertilizer_required = fertilizer_required
        self.area = area

        self.NPK = [self.fertilizer_required['N'], self.fertilizer_required['P'], self.fertilizer_required['K']]


    def solve_linear_system(self, A, b):
        """
        Solves Mx = b for x using Gauss-Jordan elimination.
        A is a list of lists (matrix). b is a list (vector).
        Returns x as a list, or None if singular.
        """
        n = len(b)
        M = [row[:] + [val] for row, val in zip(A, b)]

        for i in range(n):
            pivot_row = i
            v_max = abs(M[i][i])
            for k in range(i + 1, n):
                if abs(M[k][i]) > v_max:
                    v_max = abs(M[k][i])
                    pivot_row = k
            
            if pivot_row != i:
                M[i], M[pivot_row] = M[pivot_row], M[i]
            
            pivot = M[i][i]
            if abs(pivot) < 1e-10:
                return None

            for j in range(i, n + 1):
                M[i][j] /= pivot
            
            for k in range(n):
                if k != i:
                    factor = M[k][i]
                    for j in range(i, n + 1):
                        M[k][j] -= factor * M[i][j]
        
        return [row[n] for row in M]

    def requirement(self, fert_N, fert_P, fert_K, **kwargs):
        """
        Calculates fertilizer requirements using Linear Algebra to solve the system of equations.
        System: A * x = b
        Where:
           A = Matrix of fertilizer compositions (Cols=Fertilizers, Rows=Nutrients N,P,K)
           x = Vector of amounts needed for each fertilizer
           b = Vector of required nutrients (N, P, K)
        """
        c0 = [fert_N.get('N', 0)/100.0, fert_N.get('P', 0)/100.0, fert_N.get('K', 0)/100.0]
        c1 = [fert_P.get('N', 0)/100.0, fert_P.get('P', 0)/100.0, fert_P.get('K', 0)/100.0]
        # Col 2: Composition of fert_K
        c2 = [fert_K.get('N', 0)/100.0, fert_K.get('P', 0)/100.0, fert_K.get('K', 0)/100.0]

        A = [
            [c0[0], c1[0], c2[0]],
            [c0[1], c1[1], c2[1]],
            [c0[2], c1[2], c2[2]]
        ]

        b = [
            self.fertilizer_required['N'],
            self.fertilizer_required['P'],
            self.fertilizer_required['K']
        ]

        solution = self.solve_linear_system(A, b)

        if solution is None:
            # Fallback: step-down calculation
            # 1. Start with P (often the limiting factor in mixed fertilizers)
            req_p = self.fertilizer_required['P']
            if c1[1] > 0:
                p_amount = (req_p / c1[1])
            else:
                p_amount = 0
            
            # Deduct supplied nutrients from P choice
            rem_n = self.fertilizer_required['N'] - (p_amount * c1[0])
            rem_k = self.fertilizer_required['K'] - (p_amount * c1[2])

            # 2. Add K to meet remaining K requirement
            if c2[2] > 0:
                k_amount = max(0, rem_k) / c2[2]
            else:
                k_amount = 0
            
            # Deduct supplied nutrients from K choice
            rem_n -= (k_amount * c2[0])

            # 3. Add N to meet remaining N requirement
            if c0[0] > 0:
                n_amount = max(0, rem_n) / c0[0]
            else:
                n_amount = 0
            
            # Apply area
            n_amount *= self.area
            p_amount *= self.area
            k_amount *= self.area
        else:
            n_amount = max(0, solution[0]) * self.area
            p_amount = max(0, solution[1]) * self.area
            k_amount = max(0, solution[2]) * self.area

        # Calculate supplied nutrients
        supplied_n = (n_amount * c0[0] + p_amount * c1[0] + k_amount * c2[0])
        supplied_p = (n_amount * c0[1] + p_amount * c1[1] + k_amount * c2[1])
        supplied_k = (n_amount * c0[2] + p_amount * c1[2] + k_amount * c2[2])

        # Calculate oversupply
        oversupply_n = max(0, supplied_n - self.fertilizer_required['N'])
        oversupply_p = max(0, supplied_p - self.fertilizer_required['P'])
        oversupply_k = max(0, supplied_k - self.fertilizer_required['K'])
        
        # Determine if oversupply is significant (e.g. > 0.1 kg)
        oversupply_data = {
            'N': oversupply_n if oversupply_n > 0.1 else 0,
            'P': oversupply_p if oversupply_p > 0.1 else 0,
            'K': oversupply_k if oversupply_k > 0.1 else 0
        }

        return {
            'N': n_amount,
            'P': p_amount,
            'K': k_amount,
            'oversupply': oversupply_data
        }

if __name__ == "__main__":
    fert = FertilizerUsed()

    used_N = fert.custom_fert(N=46, P=0, K=0)
    used_K = fert.custom_fert(N=0, P=0, K=60)
    used_P = fert.custom_fert(N=14, P=14, K=14)

    required = FertilizerUsed().custom_fert(N=90, P=30, K=60)

    recom = FertilizerRecommendation(fertilizer_required=required, area=1)
    print(recom.requirement(fert_N=used_N, fert_P=used_P, fert_K=used_K))