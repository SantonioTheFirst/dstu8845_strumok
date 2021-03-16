# -*- coding: utf-8 -*-

import config
from config import np

class dstu8848:
    def __init__(self, key, iv, key_size = 64):
        self.strumok_alpha_mul = config.strumok_alpha_mul
        self.strumok_alphainv_mul = config.strumok_alphainv_mul
        self.T0 = config.T0
        self.T1 = config.T1
        self.T2 = config.T2
        self.T3 = config.T3
        self.T4 = config.T4
        self.T5 = config.T5
        self.T6 = config.T6
        self.T7 = config.T7
        
        self.S = np.zeros(16, dtype = np.uint64)
        self.r = np.zeros(2, dtype = np.uint64)
        self.key = key
        self.iv = iv
        self.key_size = key_size
        
        if key_size == 32:
            self.S[0] = np.bitwise_xor(self.key[3], self.iv[0])
            self.S[1] = self.key[2]
            self.S[2] = np.bitwise_xor(self.key[1], self.iv[1])
            self.S[3] = np.bitwise_xor(self.key[0], self.iv[2])
            self.S[4] = self.key[3]
            self.S[5] = np.bitwise_xor(self.key[2], self.iv[3])
            self.S[6] = np.bitwise_not(self.key[1])
            self.S[7] = np.bitwise_not(self.key[0])
            self.S[8] = self.key[3]
            self.S[9] = self.key[2]
            self.S[10] = np.bitwise_not(self.key[1])
            self.S[11] = self.key[0]
            self.S[12] = self.key[3]
            self.S[13] = np.bitwise_not(self.key[2])
            self.S[14] = self.key[1]
            self.S[15] = np.bitwise_not(self.key[0])
            
        elif (key_size == 64):
            # print(type(self.key[7]), type(self.iv[0]), self.key[7], self.iv[0])
            self.S[0] = np.bitwise_xor(self.key[7], self.iv[0])
            # print(self.S[0])
            self.S[1] = self.key[6]
            self.S[2] = self.key[5]
            self.S[3] = np.bitwise_xor(self.key[4], self.iv[1])
            self.S[4] = self.key[3]
            self.S[5] = np.bitwise_xor(self.key[2], self.iv[2])
            self.S[6] = self.key[1]
            self.S[7] = np.bitwise_not(self.key[0])
            self.S[8] = np.bitwise_xor(self.key[4], self.iv[3])
            self.S[9] = np.bitwise_not(self.key[6])
            self.S[10] = self.key[5]
            self.S[11] = np.bitwise_not(self.key[7])
            self.S[12] = self.key[3]
            self.S[13] = self.key[2]
            self.S[14] = np.bitwise_not(self.key[1])
            self.S[15] = self.key[0]
        else:
            pass
#             return 0

        for i in range(2):
            # print('iteration', i)
            outfrom_fsm = np.uint64(0)
            fsmtmp = np.uint64(0)

            outfrom_fsm = np.bitwise_xor((self.r[0] + self.S[15]), self.r[1])
            # print("RRRR", self.S[0], np.left_shift(np.uint64(self.S[0]), np.uint64(8)), np.right_shift(np.uint64(self.S[0]), np.uint64(56)))
            self.S[0] = np.bitwise_xor(np.bitwise_xor(self.a_mul(self.S[0]), self.S[13]), np.bitwise_xor(self.ainv_mul(self.S[11]), outfrom_fsm))
            # print('S[0] in loop a_mul', self.S[0])
            # print('r1 and S[13]', self.r[1], self.S[13])
            fsmtmp = self.r[1] + self.S[13]
            # print("FSMTMP_1", fsmtmp)
            self.r[1] = self.T(self.r[0])
            self.r[0] = fsmtmp

            outfrom_fsm = np.bitwise_xor((self.r[0] + self.S[0]), self.r[1])
            self.S[1] = np.bitwise_xor(np.bitwise_xor(np.bitwise_xor(self.a_mul(self.S[1]), self.S[14]), self.ainv_mul(self.S[12])), outfrom_fsm)
            # print('S[1] in loop a_mul', self.S[1])
            # print('r1 and S[14]', self.r[1], self.S[14])
            fsmtmp = self.r[1] + self.S[14]
            # print('FSMTMP_2', fsmtmp)
            self.r[1] = self.T(self.r[0])
            self.r[0] = fsmtmp

            outfrom_fsm = np.bitwise_xor((self.r[0] + self.S[1]),  self.r[1])
            self.S[2] = np.bitwise_xor(np.bitwise_xor(np.bitwise_xor(self.a_mul(self.S[2]), self.S[15]), self.ainv_mul(self.S[13])), outfrom_fsm)
            # print('S[2] in loop a_mul', self.S[2])
            # print('r1 and S[15]', self.r[1], self.S[15])
            fsmtmp = self.r[1] + self.S[15]
            self.r[1] = self.T(self.r[0])
            self.r[0] = fsmtmp

            outfrom_fsm = np.bitwise_xor((self.r[0] + self.S[2]), self.r[1])
            self.S[3] = np.bitwise_xor(np.bitwise_xor(np.bitwise_xor(self.a_mul(self.S[3]), self.S[0]), self.ainv_mul(self.S[14])), outfrom_fsm)
            # print('S[3] in loop a_mul', self.S[3])
            # print('r1 and S[0]', self.r[1], self.S[0])
            fsmtmp = self.r[1] + self.S[0]
            self.r[1] = self.T(self.r[0])
            self.r[0] = fsmtmp

            outfrom_fsm = np.bitwise_xor((self.r[0] + self.S[3]), self.r[1])
            self.S[4] = np.bitwise_xor(np.bitwise_xor(np.bitwise_xor(self.a_mul(self.S[4]), self.S[1]), self.ainv_mul(self.S[15])), outfrom_fsm)
            # print('S[4] in loop a_mul', self.S[4])
            # print('r1 and S[1]', self.r[1], self.S[1])
            fsmtmp = self.r[1] + self.S[1]
            self.r[1] = self.T(self.r[0])
            self.r[0] = fsmtmp

            outfrom_fsm = np.bitwise_xor((self.r[0] + self.S[4]), self.r[1])
            self.S[5] = np.bitwise_xor(np.bitwise_xor(np.bitwise_xor(self.a_mul(self.S[5]), self.S[2]), self.ainv_mul(self.S[0])), outfrom_fsm)
            # print('S[5] in loop a_mul', self.S[5])
            # print('r1 and S[2]', self.r[1], self.S[2])
            fsmtmp = self.r[1] + self.S[2]
            self.r[1] = self.T(self.r[0])
            self.r[0] = fsmtmp

            outfrom_fsm = np.bitwise_xor((self.r[0] + self.S[5]), self.r[1])
            self.S[6] = np.bitwise_xor(np.bitwise_xor(np.bitwise_xor(self.a_mul(self.S[6]), self.S[3]), self.ainv_mul(self.S[1])), outfrom_fsm)
            # print('S[6] in loop a_mul', self.S[6])
            # print('r1 and S[3]', self.r[1], self.S[3])
            fsmtmp = self.r[1] + self.S[3]
            self.r[1] = self.T(self.r[0])
            self.r[0] = fsmtmp

            outfrom_fsm = np.bitwise_xor((self.r[0] + self.S[6]), self.r[1])
            self.S[7] = np.bitwise_xor(np.bitwise_xor(np.bitwise_xor(self.a_mul(self.S[7]), self.S[4]), self.ainv_mul(self.S[2])), outfrom_fsm)
            # print('S[7] in loop a_mul', self.S[7])
            # print('r1 and S[4]', self.r[1], self.S[4])
            fsmtmp = self.r[1] + self.S[4]
            self.r[1] = self.T(self.r[0])
            self.r[0] = fsmtmp

            outfrom_fsm = np.bitwise_xor((self.r[0] + self.S[7]), self.r[1])
            self.S[8] = np.bitwise_xor(np.bitwise_xor(np.bitwise_xor(self.a_mul(self.S[8]), self.S[5]), self.ainv_mul(self.S[3])), outfrom_fsm)
            # print('S[8] in loop a_mul', self.S[8])
            # print('r1 and S[5]', self.r[1], self.S[5])
            fsmtmp = self.r[1] + self.S[5]
            self.r[1] = self.T(self.r[0])
            self.r[0] = fsmtmp

            outfrom_fsm = np.bitwise_xor((self.r[0] + self.S[8]), self.r[1])
            self.S[9] = np.bitwise_xor(np.bitwise_xor(np.bitwise_xor(self.a_mul(self.S[9]), self.S[6]), self.ainv_mul(self.S[4])), outfrom_fsm)
            # print('S[9] in loop a_mul', self.S[9])
            # print('r1 and S[6]', self.r[1], self.S[6])
            fsmtmp = self.r[1] + self.S[6]
            self.r[1] = self.T(self.r[0])
            self.r[0] = fsmtmp

            outfrom_fsm = np.bitwise_xor((self.r[0] + self.S[9]), self.r[1])
            self.S[10] = np.bitwise_xor(np.bitwise_xor(np.bitwise_xor(self.a_mul(self.S[10]), self.S[7]), self.ainv_mul(self.S[5])), outfrom_fsm)
            # print('S[10] in loop a_mul', self.S[10])
            # print('r1 and S[7]', self.r[1], self.S[7])
            fsmtmp = self.r[1] + self.S[7]
            self.r[1] = self.T(self.r[0])
            self.r[0] = fsmtmp

            outfrom_fsm = np.bitwise_xor((self.r[0] + self.S[10]), self.r[1])
            self.S[11] = np.bitwise_xor(np.bitwise_xor(np.bitwise_xor(self.a_mul(self.S[11]), self.S[8]), self.ainv_mul(self.S[6])), outfrom_fsm)
            # print('S[11] in loop a_mul', self.S[11])
            # print('r1 and S[8]', self.r[1], self.S[8])
            fsmtmp = self.r[1] + self.S[8]
            self.r[1] = self.T(self.r[0])
            self.r[0] = fsmtmp

            outfrom_fsm = np.bitwise_xor((self.r[0] + self.S[11]), self.r[1])
            self.S[12] = np.bitwise_xor(np.bitwise_xor(np.bitwise_xor(self.a_mul(self.S[12]), self.S[9]), self.ainv_mul(self.S[7])), outfrom_fsm)
            # print('S[12] in loop a_mul', self.S[12])
            # print('r1 and S[9]', self.r[1], self.S[9])
            fsmtmp = self.r[1] + self.S[9]
            self.r[1] = self.T(self.r[0])
            self.r[0] = fsmtmp

            outfrom_fsm = np.bitwise_xor((self.r[0] + self.S[12]), self.r[1])
            self.S[13] = np.bitwise_xor(np.bitwise_xor(np.bitwise_xor(self.a_mul(self.S[13]), self.S[10]), self.ainv_mul(self.S[8])), outfrom_fsm)
            # print('S[13] in loop a_mul', self.S[13])
            # print('r1 and S[10]', self.r[1], self.S[10])
            fsmtmp = self.r[1] + self.S[10]
            self.r[1] = self.T(self.r[0])
            self.r[0] = fsmtmp

            outfrom_fsm = np.bitwise_xor((self.r[0] + self.S[13]), self.r[1])
            self.S[14] = np.bitwise_xor(np.bitwise_xor(np.bitwise_xor(self.a_mul(self.S[14]), self.S[11]), self.ainv_mul(self.S[9])), outfrom_fsm)
            # print('S[14] in loop a_mul', self.S[14])
            # print('r1 and S[11]', self.r[1], self.S[11])
            fsmtmp = self.r[1] + self.S[11]
            self.r[1] = self.T(self.r[0])
            self.r[0] = fsmtmp

            outfrom_fsm = np.bitwise_xor((self.r[0] + self.S[14]), self.r[1])
            self.S[15] = np.bitwise_xor(np.bitwise_xor(np.bitwise_xor(self.a_mul(self.S[15]), self.S[12]), self.ainv_mul(self.S[10])), outfrom_fsm)
            # print('S[15] in loop a_mul', self.S[15])
            # print('r1 and S[12]', self.r[1], self.S[12])
            fsmtmp = self.r[1] + self.S[12]
            self.r[1] = self.T(self.r[0])
            self.r[0] = fsmtmp
            
        print('Init ok!')
        
        
    def __repr__(self):
        return 'dstu8848_strumok'
            
        
    def byte(self, n, w):
        # return (((w)>>(n*8)) & 0xff)
        return np.bitwise_and(np.right_shift(w, np.uint64(n * 8)),
                              np.uint64(0xff))
        
        
    def ainv_mul(self, w):
        return np.bitwise_xor(np.right_shift(w, np.uint64(8)),
                              self.strumok_alphainv_mul[np.bitwise_and(w, np.uint64(0xff))])
        
        
    def a_mul(self, w):
        # print(w)
        return np.bitwise_xor(np.left_shift(w, np.uint64(8)),
                              self.strumok_alpha_mul[np.right_shift(w, np.uint64(56))])
        
        
    def T(self, w):
        return np.bitwise_xor(
                np.bitwise_xor(
                    np.bitwise_xor(
                        np.bitwise_xor(
                            np.bitwise_xor(
                                np.bitwise_xor(
                                    np.bitwise_xor(
                                        self.T0[self.byte(0, (w))], self.T1[self.byte(1,(w))]
                                    ), self.T2[self.byte(2,(w))]
                                ), self.T3[self.byte(3,(w))]
                            ), self.T4[self.byte(4,(w))]
                        ), self.T5[self.byte(5,(w))]
                    ), self.T6[self.byte(6,(w))]
                ), self.T7[self.byte(7,(w))]
            )


if __name__ == '__main__':
    key = np.zeros(8, dtype = np.uint64)
    iv = np.zeros(4, dtype = np.uint64)
    
    key[7] = 0x8000000000000000
    key[6] = 0x0000000000000000
    key[5] = 0x0000000000000000
    key[4] = 0x0000000000000000
    key[3] = 0x0000000000000000
    key[2] = 0x0000000000000000
    key[1] = 0x0000000000000000
    key[0] = 0x0000000000000000
    
    iv[0] = 1
    iv[1] = 2
    iv[2] = 3
    iv[3] = 4
    # print(type(key[0]))
    test = dstu8848(key, iv)
    print(test.S)