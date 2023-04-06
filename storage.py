import numpy as np

class storage_tech:
    '''
    Storage and PMU technology.
    '''
    def __init__(self, c, v_min, v_max, pmu_l, pmu_h, p_leak):
        '''
        :param c:        capacitance [F]
        :param v_min:    minimal PMU voltage [V]
        :param v_max:    maximal PMU voltage [V]
        :param pmu_l:    PMU <-> load efficiency [^-1]
        :param pmu_h:    PMU <-> harvester efficiency 
        :param p_leak:   leakage power [W]
        '''
        self.c = c
        self.v_min = v_min
        self.v_max = v_max
        self.pmu_l = pmu_l
        self.pmu_h = pmu_h
        self.p_leak = p_leak
        self.t_charge = -1

    def get_capacitance(self, e_peak, t_peak):
        '''
        Get minimal capacitance.
        
        :param e_peak:  peak energy sequence [J]
        :param t_peak:  peak sequence duration [s]
        '''
        self.c = 2*(e_peak+self.p_leak*t_peak)/(pow(self.v_max,2)-pow(self.v_min,2))

    def get_charge_time(self, p_h, p_c):
        '''
        Calculate recharge time of capacitor.

        :param p_h: harvested power [W]
        :param p_c: consumed power [W]
        '''
        p_h = p_h*self.pmu_h
        p_c = p_c*self.pmu_l
        if((self.v_min-(p_h*self.v_max/p_c) != 0) and ((self.v_max-(p_h*self.v_max/p_c))/(self.v_min-(p_h*self.v_max/p_c)) > 0)):
            self.t_charge = -((self.c*pow(self.v_max,2))/p_c)*np.log((self.v_max-(p_h*self.v_max/p_c))/(self.v_min-(p_h*self.v_max/p_c)))
        else:
            self.t_charge = -1