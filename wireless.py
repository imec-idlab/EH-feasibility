import numpy as np

class wireless_tech:
    def __init__(self):
        self.name = ""
        self.e_peak = 0
        self.p_idle = 0
        self.t_peak = 0

    def get_energy(self, storage_tech):
        self.e_peak = self.e_peak
        self.p_idle = self.p_idle
        self.t_peak = self.t_peak

    def get_latency(self, payload, datarate):
        return 8.0*payload/datarate
    
    def get_min_interval(self, storage_tech):
        if(storage_tech.t_charge > 0):
            return storage_tech.t_charge + self.t_peak
        else:
            return -1
    
class lora_class_a(wireless_tech):
    """
    LoRaWAN Class A wireless technology.
    """
    def __init__(self, name, pream, bw, sf, maxpl, cr, ih, de, p_tx, e_rx, t_rx, e_stup, t_stup, p_idle):
        """
        :param name:    name of device
        :param pream:   preamble
        :param bw:      bandwidth [Hz]
        :param sf:      spreading Factor
        :param maxpl:   max payload [B]
        :param cr:      coding Rate
        :param ih:      explicit header disabled?
        :param de:      low data rate optimization enabled?
        :param p_tx:    TX power [W]
        :param e_rx:    energy consumption during 2 (idle) RX listening periods [J]
        :param t_rx:    2 (idle) RX listening periods duration [s]
        :param e_stup:  start-up energy consumption [J]
        :param t_stup:  start-up duration [s]
        :param p_idle:  idle power consumption [W]
        """
        self.name = name
        self.pream = pream
        self.bw = bw    
        self.sf = sf
        self.maxpl = maxpl
        self.cr = cr
        self.ih = ih
        self.de = de
        self.p_tx = p_tx
        self.e_rx = e_rx
        self.t_rx = t_rx
        self.e_stup = e_stup
        self.t_stup = t_stup
        self.p_idle = p_idle

    def get_transmission_time(self, payload):
        """
        Get arrary of transmission times. Multiple transmissions may be required, depending on payload.

        :param payload: payload [B]
        :return:        array of TX times [s]
        """
        t_txs = []
        N_f = int(np.floor(payload/self.maxpl))
        for n in range(0,N_f):
            s_tx = self.pream+4.25+8+np.max(np.ceil((8*51-4*self.sf+44-20*self.ih)/(4*(self.sf-2*self.de)))*(self.cr+4),0)
            t_tx = s_tx*pow(2,self.sf)/self.bw
            t_txs.append(t_tx)
        s_tx = self.pream+4.25+8+np.max(np.ceil((8*(payload-self.maxpl*N_f)-4*self.sf+44-20*self.ih)/(4*(self.sf-2*self.de)))*(self.cr+4),0)
        t_tx = s_tx*pow(2,self.sf)/self.bw
        t_txs.append(t_tx)
        return t_txs

    def get_energy(self, storage_tech, payload, e_sense, t_sense):
        """
        Get peak energy parameters.

        :param storage_tech:    storage technology
        :param payload:         payload [B]
        :param e_sense:         sensing energy [J]
        :param t_sense:         sensing duration [s]
        """
        t_txs = self.get_transmission_time(payload)
        self.e_peak = (e_sense + self.e_stup + len(t_txs)*self.e_rx + np.sum(t_txs)*self.p_tx)*storage_tech.pmu_l
        self.t_peak = self.t_stup + len(t_txs)*self.t_rx + np.sum(t_txs) + t_sense

    def get_latency(self, payload):
        """
        Get latency.

        :param payload: payload [B]
        """
        t_txs = self.get_transmission_time(payload)
        return self.t_stup + (len(t_txs)-1)*self.t_rx + np.sum(t_txs)
    
class ble_lpn(wireless_tech):
    """
    BLE Low-Power Node (LPN) wireless technology
    """
    def __init__(self, name, t_rw, t_pi, t_rd, dr, hops, p_tx, p_rx, p_rd, e_doh, e_poh, p_idle):
        """
        :param name:    name of device
        :param t_rw:    receive Window [s]
        :param t_pi:    polling Interval [s]
        :param t_rd:    receive Delay [s]
        :param dr:      data rate [b/s]
        :param hops:    #hops
        :param p_tx:    TX power [W]
        :param p_rx:    RX power [W]
        :param p_rd:    power during RD [mW]
        :param e_doh:   energy overhead during data TX [J]
        :param e_poh:   energy overhead during poll TX [J]
        :param p_idle:  idle power consumption [W]
        """
        self.name = name
        self.rw = t_rw
        self.pi = t_pi
        self.rd = t_rd
        self.dr = dr
        self.hops = hops
        self.p_tx = p_tx
        self.p_rx = p_rx
        self.p_rd = p_rd
        self.e_doh = e_doh
        self.e_poh = e_poh
        self.p_idle = p_idle

    def get_transmission_time(self, payload):
        """
        Get transmission time.

        :param payload: payload [B]
        :return:        TX time [s]
        """
        return (8.0*(payload+18))/self.dr

    def get_energy(self, storage_tech, payload, e_sense, t_sense):
        """
        Get peak energy parameters.

        :param storage_tech:    storage technology
        :param payload:         payload [B]
        :param e_sense:         sensing energy [J]
        :param t_sense:         sensing duration [s]
        """
        t_txd = self.get_transmission_time(payload)
        t_txp = self.get_transmission_time(19)
    
        self.e_peak = (e_sense+self.e_doh+self.p_tx*3*t_txd+self.e_poh+self.p_tx*3*t_txp+self.p_rd*self.rd+self.p_rx*self.rw)*storage_tech.pmu_l
        self.t_peak = t_sense + 0.050039 + t_txd*3 + t_txp*3 + self.rd + self.rw
        
    def get_latency(self, payload):
        """
        Get latency.

        :param payload: payload [B]
        """
        t_tx = self.get_transmission_time(payload)
        return (0.00294+3*t_tx+2*0.000029*2)+(self.hops-1)*(0.024272+t_tx*3)

class sixtisch_leaf(wireless_tech):
    """
    6TiSCH leaf node wireless technology
    """
    def __init__(self, name, nbs, hops, t_ts, dao_pl, eb_pl, p_tx, e_tsoh, e_poh, p_idle):
        """
        :param name:    name of device
        :param nbs:     #neighbours
        :param hops:    #hops
        :param t_ts:    TSCH timeslot duration [s]
        :param dao_pl:  DAO size [B]
        :param eb_pl:   EB size [B]
        :param p_tx:    TX power [W]        
        :param e_tsoh:  fixed energy in timeslot [J]
        :param e_poh:   fixed energy in peak sequence [J]
        :param p_idle:  idle power consumption [W]
        """
        self.name = name
        self.nbs = nbs
        self.hops = hops
        self.dao_pl = dao_pl
        self.eb_pl = eb_pl
        self.p_tx = p_tx
        self.t_ts = t_ts
        self.e_tsoh = e_tsoh
        self.e_poh = e_poh
        self.p_idle = p_idle

    def get_energy(self, storage_tech, payload, e_sense, t_sense):
        """
        Get peak energy parameters.

        :param storage_tech:    storage technology
        :param payload:         payload [B]
        :param e_sense:         sensing energy [J]
        :param t_sense:         sensing duration [s]
        """
        overhead = 38 if (self.hops==1) else 48
        e_data = e_sense + self.e_tsoh + self.p_tx*(payload+overhead)
        e_dao = self.e_tsoh + self.p_tx*self.p_tx
        self.e_peak = (self.e_poh + max(e_data,e_dao))*storage_tech.pmu_l
        self.t_peak = 5*self.t_ts + (t_sense if (e_data>e_dao) else 0)

    def get_latency(self, storage_tech, payload, e_sense, t_sense, p_h):
        """
        Get latency.

        :param storage_tech:    storage technology
        :param payload:         payload [B]
        :param e_sense:         sensing energy [J]
        :param t_sense:         sensing duration [s]
        """
        self.get_energy(storage_tech, payload, e_sense, t_sense)
        storage_tech.get_capacitance(self.e_peak, self.t_peak)
        storage_tech.get_charge_time(p_h, self.p_idle)
        if(storage_tech.t_charge > 0):
            t_peak_slots = np.ceil(self.t_peak/self.t_ts)
            t_charge_slots = np.ceil(storage_tech.t_charge/self.t_ts)
            t_rbus_slots = t_peak_slots + t_charge_slots
            t_rbus = t_rbus_slots*self.t_ts
            t_lat = t_rbus + self.t_ts+(self.hops-1)*t_rbus
            if(((self.hops > 1) and (payload > 127-46)) or (payload > 127-38)):
                t_lat += t_rbus*(self.hops)
                temp = (payload-89) if (self.hops > 1) else (payload-81)
                if(((self.hops > 1) and (temp > 127-46)) or (temp > 127-38)):
                    t_lat += t_rbus*(self.hops)
            return t_lat
        else:
            return -1