import numpy as np
import matplotlib.pyplot as plt
from time import gmtime, strftime

def print_time(time):
    t = gmtime(time)
    if(t.tm_hour>0):
        return strftime("%Hh %Mmin %Ss",gmtime(time))
    elif(t.tm_min>0):
        return strftime("%Mmin %Ss",gmtime(time))
    else:
        return str(round(time,3))+"s"

def print_power(power):
    if(power>1000):
        return str(round((power/1000.0),3))+"mW"
    else:
        return str(power)+"uW"

def plot_interval_vs_pharv(p_min, p_max, wireless_tech, storage_tech, payload, e_sense, t_sense):
    ''' 
    Plot minimal achievable transmission interval vs harvested power.

    :param p_min:           minimal harvested power [uW]
    :param p_max:           maximal harvested power [uW]
    :param wireless_tech:   wireless technology
    :param storage_tech:    storage/PMU technology
    :param payload:         payload [B]
    :param e_sense:         sensing energy [J]
    :param t_sense:         sensing time [s]
    '''
    first = 0
    min_ints = []
    for ph in range(p_min, p_max):
        p = ph/1000000.0
        wireless_tech.get_energy(storage_tech, payload, e_sense, t_sense)
        storage_tech.get_capacitance(wireless_tech.e_peak, wireless_tech.t_peak)
        storage_tech.get_charge_time(p, wireless_tech.p_idle)
        min_int = wireless_tech.get_min_interval(storage_tech)
        if(min_int > 0):
            min_ints.append(min_int)
            if(first == 0):
                first = ph
    fig1 = plt.figure(wireless_tech.name)
    plt.xlabel("Harvested power [uW]")
    plt.ylabel("Min. transmission interval [s]")
    plt.yscale("log")
    plt.xscale("log")
    plt.vlines(first,0,min_ints[0], color="grey", linewidth=0.5, linestyle="--")
    plt.hlines(min_ints[0],0,first, color="grey", linewidth=0.5, linestyle="--")
    plt.vlines(p_max,0,min_ints[-1], color="grey", linewidth=0.5, linestyle="--")
    plt.hlines(min_ints[-1],0,p_max, color="grey", linewidth=0.5, linestyle="--")
    plt.plot(range(first,p_max),min_ints, label=wireless_tech.name, linewidth='3')
    plt.autoscale()
    plt.text(first,min_ints[0]," ["+print_power(first)+", "+print_time(min_ints[0])+"]", horizontalalignment='left',verticalalignment='bottom')
    plt.text(p_max,min_ints[-1]," ["+print_power(p_max)+", "+print_time(min_ints[-1])+"]", horizontalalignment='right',verticalalignment='bottom')
    plt.grid(which='major')
    plt.show()

def plot_latency_vs_pl(pl_min, pl_max, wireless_tech):
    ''' 
    Plot minimal achievable latency vs data size (not for 6TiSCH).

    :param pl_min:          minimal data size [B]
    :param pl_max:          maximal data size [B]
    :param wireless_tech:   wireless technology
    '''
    min_lats = []
    for pl in range(pl_min, pl_max):
        lat = wireless_tech.get_latency(pl)
        min_lats.append(lat)
    fig1 = plt.figure(wireless_tech.name)
    plt.xlabel("Data size [B]")
    plt.ylabel("Min. latency [s]")
    plt.vlines(pl_min,0,min_lats[0], color="grey", linewidth=0.5, linestyle="--")
    plt.hlines(min_lats[0],0,pl_min, color="grey", linewidth=0.5, linestyle="--")
    plt.vlines(pl_max,0,min_lats[-1], color="grey", linewidth=0.5, linestyle="--")
    plt.hlines(min_lats[-1],0,pl_max, color="grey", linewidth=0.5, linestyle="--")
    plt.plot(range(pl_min,pl_max),min_lats)
    plt.autoscale()
    plt.text(pl_min,min_lats[0]," ["+str(pl_min)+" B"+", "+print_time(min_lats[0])+"]", horizontalalignment='left',verticalalignment='bottom')
    plt.text(pl_max,min_lats[-1]," ["+str(pl_max)+" B"+", "+print_time(min_lats[-1])+"]", horizontalalignment='right',verticalalignment='bottom')
    plt.grid(which='major')
    plt.show()

def plot_latency_vs_pharv(p_min, p_max, wireless_tech, storage_tech, payload, e_sense, t_sense):
    ''' 
    Plot minimal achievable latency vs harvested power (for 6TiSCH only).

    :param p_min:           minimal harvested power [uW]
    :param p_max:           maximal harvested power [uW]
    :param wireless_tech:   wireless technology technology
    :param storage_tech:    storage/PMU technology
    :param payload:         data size [B]
    :param e_sense:         sensing energy [J]
    :param t_sense:         sensing time [s]
    '''
    first = 0
    lats = []
    for ph in range(p_min, p_max):
        p = ph/1000000.0
        lat = wireless_tech.get_latency(storage_tech, payload, e_sense, t_sense, p)
        if(lat > 0):
            lats.append(lat)
            if(first == 0):
                first = ph
    fig1 = plt.figure(wireless_tech.name)
    plt.xlabel("Harvested power [uW]")
    plt.ylabel("Latency [s]")
    plt.yscale("log")
    plt.xscale("log")
    plt.grid(which='major')
    plt.vlines(first,0,lats[0], color="grey", linewidth=0.5, linestyle="--")
    plt.hlines(lats[0],0,first, color="grey", linewidth=0.5, linestyle="--")
    plt.vlines(p_max,0,lats[-1], color="grey", linewidth=0.5, linestyle="--")
    plt.hlines(lats[-1],0,p_max, color="grey", linewidth=0.5, linestyle="--")
    plt.plot(range(first,p_max),lats)
    plt.autoscale()
    plt.text(first,lats[0]," ["+print_power(first)+", "+print_time(lats[0])+"]")
    plt.text(p_max,lats[-1]," ["+print_power(p_max)+", "+print_time(lats[-1])+"]")
    plt.show()