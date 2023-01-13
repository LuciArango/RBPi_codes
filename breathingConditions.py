import numpy as np
import skfuzzy as fuzz
import skfuzzy as control
#import RPi.GPIO as GPIO
import time
#import board
#import busio
#import adafruit_sgp30
#import matplotlib.pyplot as plt

    
def BCidentification (CO2_level, O2_level):    
    ###Generar variables del universo
    #Rango de CO2 y O2 para la altitud de Bogotá (mínimo y máximo posible)
    #input
    start = time.time()
    patient_CO2    = np.arange(0, 200, 1)
    patient_O2   = np.arange(0, 100, 1)
    #output
    capnia   = np.arange(0, 100, 1)
    oxia   = np.arange(0, 100, 1)

    output_list = [capnia, oxia]
    output_name = ['Capnography state', 'Oxigenation state']

    #Bogotá giving a minute ventilation VE of (10.2 L SD 2.6), PaCo2 (range 28.5 to 38.9 mmHg), and SaO2 (range 88.4 to 96.0)

    ###Generamos las funciones fuzzy de membresia triangulares (trimf)
    #Inputs
    patient_CO2_verylo     = fuzz.trimf(patient_CO2,   [0, 21, 26])
    patient_CO2_lo     = fuzz.trimf(patient_CO2,   [25, 27, 29])
    patient_CO2_md     = fuzz.trimf(patient_CO2,   [28, 35, 38])
    patient_CO2_hi     = fuzz.trimf(patient_CO2,   [37, 41, 43])
    patient_CO2_veryhi     = fuzz.trimf(patient_CO2,   [42, 48, 200])

    patient_O2_verylo     = fuzz.trimf(patient_O2,   [0, 60, 80])
    patient_O2_lo     = fuzz.trimf(patient_O2,   [79, 85, 89])
    patient_O2_md     = fuzz.trimf(patient_O2,   [88, 90, 92])
    patient_O2_hi     = fuzz.trimf(patient_O2,   [91, 94, 97])
    patient_O2_veryhi     = fuzz.trimf(patient_O2,   [96, 100, 100])

    #Outputs
    severehipo_capnia     = fuzz.trimf(capnia,   [0, 10, 21])
    mildhipo_capnia     = fuzz.trimf(capnia,   [20, 30, 41])
    normo_capnia     = fuzz.trimf(capnia,   [40, 50, 60])
    mildhiper_capnia     = fuzz.trimf(capnia,   [59, 60, 80])
    severehiper_capnia     = fuzz.trimf(capnia,   [79, 80, 200])

    severehipo_oxia    = fuzz.trimf(oxia,   [79, 80, 100])#escala invertida, los niveles más bajos de hipoxia tienen el mayor puntaje
    mildhipo_oxia     = fuzz.trimf(oxia,   [59, 60, 80])
    normo_oxia     = fuzz.trimf(oxia,   [40, 50, 60])
    mildhiper_oxemia     = fuzz.trimf(oxia,   [20, 30, 41])
    severehiper_oxemia     = fuzz.trimf(oxia,   [0, 10, 21])


    ###Definition of rules (25 rules)
    # If - Then rules combining the inputs to modulate the outputs
    # rule 1:  
    #if CO2_level is very low and O2_level is very low then command is Severe Hypocapnia and Severe Hypoxia
    rule1_patient_CO2= fuzz.interp_membership(patient_CO2, patient_CO2_verylo, CO2_level)
    rule1_patient_O2= fuzz.interp_membership(patient_O2, patient_O2_verylo, O2_level)
    active_rule1 = min(rule1_patient_CO2, rule1_patient_O2)

    rule_1_clip = []
    rule_1_clip.append(np.fmin(active_rule1, severehipo_capnia))
    rule_1_clip.append(np.fmin(active_rule1, severehipo_oxia))
    #Nota: No sé si está condición se puede presentar

    # rule 2: 
    #if CO2_level is low and O2_level is low then command is Mild Hypocapnia and Mild Hypoxia
    rule2_patient_CO2= fuzz.interp_membership(patient_CO2, patient_CO2_lo, CO2_level)
    rule2_patient_O2= fuzz.interp_membership(patient_O2, patient_O2_lo, O2_level)
    active_rule2 = min(rule2_patient_CO2, rule2_patient_O2)

    rule_2_clip = []
    rule_2_clip.append(np.fmin(active_rule2, mildhipo_capnia))
    rule_2_clip.append(np.fmin(active_rule2, mildhipo_oxia))

    # rule 3: 
    #if CO2_level is very low and O2_level is low then command is Severe Hypocapnia and Mild Hypoxia
    rule3_patient_CO2= fuzz.interp_membership(patient_CO2, patient_CO2_verylo, CO2_level)
    rule3_patient_O2= fuzz.interp_membership(patient_O2, patient_O2_lo, O2_level)
    active_rule3 = min(rule3_patient_CO2, rule3_patient_O2)

    rule_3_clip = []
    rule_3_clip.append(np.fmin(active_rule3, severehipo_capnia))
    rule_3_clip.append(np.fmin(active_rule3, mildhipo_oxia))

    # rule 4: 
    #if CO2_level is very low and O2_level is normal then command is Severe Hypocapnia and normooxia
    rule4_patient_CO2= fuzz.interp_membership(patient_CO2, patient_CO2_verylo, CO2_level)
    rule4_patient_O2= fuzz.interp_membership(patient_O2, patient_O2_md, O2_level)
    active_rule4 = min(rule4_patient_CO2, rule4_patient_O2)

    rule_4_clip = []
    rule_4_clip.append(np.fmin(active_rule4, severehipo_capnia))
    rule_4_clip.append(np.fmin(active_rule4, normo_oxia))

    # rule 5: 
    #if CO2_level is very low and O2_level is high then command is Severe Hypocapnia and Mild Hyperoxemia
    rule5_patient_CO2= fuzz.interp_membership(patient_CO2, patient_CO2_verylo, CO2_level)
    rule5_patient_O2= fuzz.interp_membership(patient_O2, patient_O2_hi, O2_level)
    active_rule5 = min(rule5_patient_CO2, rule5_patient_O2)

    rule_5_clip = []
    rule_5_clip.append(np.fmin(active_rule5, severehipo_capnia))
    rule_5_clip.append(np.fmin(active_rule5, mildhiper_oxemia))

    # rule 6: 
    #if CO2_level is low and O2_level is very low then command is Mild Hypercapnia and Severe Hypoxia
    rule6_patient_CO2= fuzz.interp_membership(patient_CO2, patient_CO2_lo, CO2_level)
    rule6_patient_O2= fuzz.interp_membership(patient_O2, patient_O2_verylo, O2_level)
    active_rule6 = min(rule6_patient_CO2, rule6_patient_O2)

    rule_6_clip = []
    rule_6_clip.append(np.fmin(active_rule6, mildhipo_capnia))
    rule_6_clip.append(np.fmin(active_rule6, severehipo_oxia))

    # rule 7: 
    #if CO2_level is low and O2_level is normal then command is Mild Hypercapnia and normo-oxia
    rule7_patient_CO2= fuzz.interp_membership(patient_CO2, patient_CO2_lo, CO2_level)
    rule7_patient_O2= fuzz.interp_membership(patient_O2, patient_O2_md, O2_level)
    active_rule7 = min(rule7_patient_CO2, rule7_patient_O2)

    rule_7_clip = []
    rule_7_clip.append(np.fmin(active_rule7, mildhipo_capnia))
    rule_7_clip.append(np.fmin(active_rule7, normo_oxia))

    # rule 8: 
    #if CO2_level is low and O2_level is high then command is Mild Hypercapnia and MildHiperoxemia
    rule8_patient_CO2= fuzz.interp_membership(patient_CO2, patient_CO2_lo, CO2_level)
    rule8_patient_O2= fuzz.interp_membership(patient_O2, patient_O2_hi, O2_level)
    active_rule8 = min(rule8_patient_CO2, rule8_patient_O2)

    rule_8_clip = []
    rule_8_clip.append(np.fmin(active_rule8, mildhipo_capnia))
    rule_8_clip.append(np.fmin(active_rule8, mildhiper_oxemia))

    # rule 9: 
    #if CO2_level is normal and O2_level is very low then command is normo capnia and Severe Hipoxia
    rule9_patient_CO2= fuzz.interp_membership(patient_CO2, patient_CO2_md, CO2_level)
    rule9_patient_O2= fuzz.interp_membership(patient_O2, patient_O2_verylo, O2_level)
    active_rule9 = min(rule9_patient_CO2, rule9_patient_O2)

    rule_9_clip = []
    rule_9_clip.append(np.fmin(active_rule9, normo_capnia))
    rule_9_clip.append(np.fmin(active_rule9, severehipo_oxia))

    # rule 10: 
    #if CO2_level is normal and O2_level is low then command is normo capnia and Mild Hipoxia
    rule10_patient_CO2= fuzz.interp_membership(patient_CO2, patient_CO2_md, CO2_level)
    rule10_patient_O2= fuzz.interp_membership(patient_O2, patient_O2_lo, O2_level)
    active_rule10 = min(rule10_patient_CO2, rule10_patient_O2)

    rule_10_clip = []
    rule_10_clip.append(np.fmin(active_rule10, normo_capnia))
    rule_10_clip.append(np.fmin(active_rule10, mildhipo_oxia))

    ### rule 11: 
    ###if CO2_level is normal and O2_level is normal then command is normo capnia and normo-oxia
    rule11_patient_CO2= fuzz.interp_membership(patient_CO2, patient_CO2_md, CO2_level)
    rule11_patient_O2= fuzz.interp_membership(patient_O2, patient_O2_md, O2_level)
    active_rule11 = min(rule11_patient_CO2, rule11_patient_O2)

    rule_11_clip = []
    rule_11_clip.append(np.fmin(active_rule11, normo_capnia))
    rule_11_clip.append(np.fmin(active_rule11, normo_oxia))

    # rule 12: 
    #if CO2_level is normal and O2_level is high then command is normo capnia and Mild Hiperoxemia
    rule12_patient_CO2= fuzz.interp_membership(patient_CO2, patient_CO2_md, CO2_level)
    rule12_patient_O2= fuzz.interp_membership(patient_O2, patient_O2_hi, O2_level)
    active_rule12 = min(rule12_patient_CO2, rule12_patient_O2)

    rule_12_clip = []
    rule_12_clip.append(np.fmin(active_rule12, normo_capnia))
    rule_12_clip.append(np.fmin(active_rule12, mildhiper_oxemia))

    # rule 13: 
    #if CO2_level is high and O2_level is very low then command is Mild Hypercapnia and Severe Hipoxia
    rule13_patient_CO2= fuzz.interp_membership(patient_CO2, patient_CO2_hi, CO2_level)
    rule13_patient_O2= fuzz.interp_membership(patient_O2, patient_O2_verylo, O2_level)
    active_rule13 = min(rule13_patient_CO2, rule13_patient_O2)

    rule_13_clip = []
    rule_13_clip.append(np.fmin(active_rule13, mildhiper_capnia))
    rule_13_clip.append(np.fmin(active_rule13, severehipo_oxia))

    # rule 14: 
    #if CO2_level is high and O2_level is low then command is Mild Hypercapnia and Mild Hipoxia
    rule14_patient_CO2= fuzz.interp_membership(patient_CO2, patient_CO2_hi, CO2_level)
    rule14_patient_O2= fuzz.interp_membership(patient_O2, patient_O2_lo, O2_level)
    active_rule14 = min(rule14_patient_CO2, rule14_patient_O2)

    rule_14_clip = []
    rule_14_clip.append(np.fmin(active_rule14, mildhiper_capnia))
    rule_14_clip.append(np.fmin(active_rule14, mildhipo_oxia))

    # rule 15: 
    #if CO2_level is high and O2_level is normal then command is Mild Hypercapnia and normo-oxia
    rule15_patient_CO2= fuzz.interp_membership(patient_CO2, patient_CO2_hi, CO2_level)
    rule15_patient_O2= fuzz.interp_membership(patient_O2, patient_O2_md, O2_level)
    active_rule15 = min(rule15_patient_CO2, rule15_patient_O2)

    rule_15_clip = []
    rule_15_clip.append(np.fmin(active_rule15, mildhiper_capnia))
    rule_15_clip.append(np.fmin(active_rule15, normo_oxia))

    # rule 16: 
    #if CO2_level is high and O2_level is high then command is Mild Hypercapnia and Mild Hiperoxemia
    rule16_patient_CO2= fuzz.interp_membership(patient_CO2, patient_CO2_hi, CO2_level)
    rule16_patient_O2= fuzz.interp_membership(patient_O2, patient_O2_hi, O2_level)
    active_rule16 = min(rule16_patient_CO2, rule16_patient_O2)

    rule_16_clip = []
    rule_16_clip.append(np.fmin(active_rule16, mildhiper_capnia))
    rule_16_clip.append(np.fmin(active_rule16, mildhiper_oxemia))

    # rule 17: 
    #if CO2_level is very high and O2_level is very low then command is Severe Hypercapnia and Severe Hypoxia
    rule17_patient_CO2= fuzz.interp_membership(patient_CO2, patient_CO2_veryhi, CO2_level)
    rule17_patient_O2= fuzz.interp_membership(patient_O2, patient_O2_verylo, O2_level)
    active_rule17 = min(rule17_patient_CO2, rule17_patient_O2)

    rule_17_clip = []
    rule_17_clip.append(np.fmin(active_rule17, severehiper_capnia))
    rule_17_clip.append(np.fmin(active_rule17, severehipo_oxia))

    # rule 18: 
    #if CO2_level is very high and O2_level is low then command is Severe Hypercapnia and Mild Hypoxia
    rule18_patient_CO2= fuzz.interp_membership(patient_CO2, patient_CO2_veryhi, CO2_level)
    rule18_patient_O2= fuzz.interp_membership(patient_O2, patient_O2_lo, O2_level)
    active_rule18 = min(rule18_patient_CO2, rule18_patient_O2)

    rule_18_clip = []
    rule_18_clip.append(np.fmin(active_rule18, severehiper_capnia))
    rule_18_clip.append(np.fmin(active_rule18, mildhipo_oxia))

    # rule 19: 
    #if CO2_level is very high and O2_level is normal then command is Severe Hypercapnia and normo-oxia
    rule19_patient_CO2= fuzz.interp_membership(patient_CO2, patient_CO2_veryhi, CO2_level)
    rule19_patient_O2= fuzz.interp_membership(patient_O2, patient_O2_md, O2_level)
    active_rule19 = min(rule19_patient_CO2, rule19_patient_O2)

    rule_19_clip = []
    rule_19_clip.append(np.fmin(active_rule19, severehiper_capnia))
    rule_19_clip.append(np.fmin(active_rule19, normo_oxia))

    # rule 20: 
    #if CO2_level is very high and O2_level is high then command is Severe Hypercapnia and Hiperoxemia
    rule20_patient_CO2= fuzz.interp_membership(patient_CO2, patient_CO2_veryhi, CO2_level)
    rule20_patient_O2= fuzz.interp_membership(patient_O2, patient_O2_hi, O2_level)
    active_rule20 = min(rule20_patient_CO2, rule20_patient_O2)

    rule_20_clip = []
    rule_20_clip.append(np.fmin(active_rule20, severehipo_capnia))
    rule_20_clip.append(np.fmin(active_rule20, mildhiper_oxemia))

    # rule 21: 
    #if CO2_level is very low and O2_level is very high then command is Severe Hypocapnia and Severe Hiperoxemia
    rule21_patient_CO2= fuzz.interp_membership(patient_CO2, patient_CO2_verylo, CO2_level)
    rule21_patient_O2= fuzz.interp_membership(patient_O2, patient_O2_veryhi, O2_level)
    active_rule21 = min(rule21_patient_CO2, rule21_patient_O2)

    rule_21_clip = []
    rule_21_clip.append(np.fmin(active_rule21, severehipo_capnia))
    rule_21_clip.append(np.fmin(active_rule21, severehiper_oxemia))

    # rule 22: 
    #if CO2_level is low and O2_level is very high then command is Mild Hypocapnia and Severe Hiperoxemia
    rule22_patient_CO2= fuzz.interp_membership(patient_CO2, patient_CO2_lo, CO2_level)
    rule22_patient_O2= fuzz.interp_membership(patient_O2, patient_O2_veryhi, O2_level)
    active_rule22 = min(rule22_patient_CO2, rule22_patient_O2)

    rule_22_clip = []
    rule_22_clip.append(np.fmin(active_rule22, mildhipo_capnia))
    rule_22_clip.append(np.fmin(active_rule22, severehiper_oxemia))

    # rule 23: 
    #if CO2_level is normal and O2_level is very high then command is normo capnia and Severe Hiperoxemia
    rule23_patient_CO2= fuzz.interp_membership(patient_CO2, patient_CO2_md, CO2_level)
    rule23_patient_O2= fuzz.interp_membership(patient_O2, patient_O2_veryhi, O2_level)
    active_rule23 = min(rule23_patient_CO2, rule23_patient_O2)

    rule_23_clip = []
    rule_23_clip.append(np.fmin(active_rule23, normo_capnia))
    rule_23_clip.append(np.fmin(active_rule23, severehiper_oxemia))

    # rule 24: 
    #if CO2_level is high and O2_level is very high then command is Mild Hypercapnia and Severe Hiperoxemia
    rule24_patient_CO2= fuzz.interp_membership(patient_CO2, patient_CO2_hi, CO2_level)
    rule24_patient_O2= fuzz.interp_membership(patient_O2, patient_O2_veryhi, O2_level)
    active_rule24 = min(rule24_patient_CO2, rule24_patient_O2)

    rule_24_clip = []
    rule_24_clip.append(np.fmin(active_rule24, mildhiper_capnia))
    rule_24_clip.append(np.fmin(active_rule24, severehiper_oxemia))

    # rule 25: 
    #if CO2_level is very high and O2_level is very high then command is Severe Hypercapnia and Severe Hiperoxemia
    rule25_patient_CO2= fuzz.interp_membership(patient_CO2, patient_CO2_veryhi, CO2_level)
    rule25_patient_O2= fuzz.interp_membership(patient_O2, patient_O2_veryhi, O2_level)
    active_rule25 = min(rule25_patient_CO2, rule25_patient_O2)

    rule_25_clip = []
    rule_25_clip.append(np.fmin(active_rule25, severehiper_capnia))
    rule_25_clip.append(np.fmin(active_rule25, severehiper_oxemia))

    #Combine all rules into a list
    rule_list = [rule_1_clip, rule_2_clip, rule_3_clip, rule_4_clip, rule_5_clip, rule_6_clip, rule_7_clip, rule_8_clip, rule_9_clip,
                 rule_10_clip, rule_11_clip, rule_12_clip, rule_13_clip, rule_14_clip, rule_15_clip, rule_16_clip, rule_17_clip, rule_18_clip,
                 rule_19_clip, rule_20_clip, rule_21_clip, rule_22_clip, rule_23_clip, rule_24_clip, rule_25_clip]

    ###Agregation and defuzzification process
    # Step 3
    for i,output in enumerate(output_list):
      a = np.fmax(rule_1_clip[i], rule_2_clip[i])#no entiendo esto
      a = np.fmax(a, rule_3_clip[i])
      a = np.fmax(a, rule_4_clip[i])
      a = np.fmax(a, rule_5_clip[i])
      a = np.fmax(a, rule_6_clip[i])
      a = np.fmax(a, rule_7_clip[i])
      a = np.fmax(a, rule_8_clip[i])
      a = np.fmax(a, rule_9_clip[i])
      a = np.fmax(a, rule_11_clip[i])
      a = np.fmax(a, rule_12_clip[i])
      a = np.fmax(a, rule_13_clip[i])
      a = np.fmax(a, rule_14_clip[i])
      a = np.fmax(a, rule_15_clip[i])
      a = np.fmax(a, rule_16_clip[i])
      a = np.fmax(a, rule_17_clip[i])
      a = np.fmax(a, rule_18_clip[i])
      a = np.fmax(a, rule_19_clip[i])
      a = np.fmax(a, rule_20_clip[i])
      a = np.fmax(a, rule_21_clip[i])
      a = np.fmax(a, rule_22_clip[i])
      a = np.fmax(a, rule_23_clip[i])
      a = np.fmax(a, rule_24_clip[i])
      a = np.fmax(a, rule_25_clip[i])
      
      print(output_name[i], ": ", fuzz.defuzz(output, a, 'centroid'))

    aggregated_list = []
    defuzz_list, patient_state = [],[]
    defuz_activation_list = []
    for output_idx,output in enumerate(output_list):
      x = rule_list[0]
      for rule_idx in range(1, len(rule_list)):
        if rule_idx==1:
          x = x[output_idx]
        y = rule_list[rule_idx]
        x = np.fmax(x,y[output_idx])
      aggregated_list.append(x)

      real_ans = fuzz.defuzz(output, x, 'centroid')
      ans = round(real_ans,2)
      defuzz_list.append(real_ans)#porcentaje de pertenencia
      patient_state.append(ans)
      defuz_activation_list.append(fuzz.interp_membership(output, x, real_ans))

      
      
      print(output_name[output_idx], ": ",ans)
      print(defuzz_list)
      
    capnia_value = patient_state[0]
    oxia_value = patient_state[1]
    full_time= time.time() - start
    return capnia_value, oxia_value, full_time

    ###Aggregated rules and defuzzified membership function for each output
    """
    fig, (ax2, ax3) = plt.subplots(nrows=2, figsize=(10, 20))

    cp0 = np.zeros_like(capnia)
    ax2.plot(capnia, severehipo_capnia, 'b', linewidth=1.5, linestyle='--', label='Severe hypocapnia')
    ax2.plot(capnia, mildhipo_capnia, 'g', linewidth=1.5, linestyle='--', label='Mild hypocapnia')
    ax2.plot(capnia, normo_capnia, 'r', linewidth=1.5, linestyle='--', label='Normal levels')
    ax2.plot(capnia, mildhiper_capnia, 'c', linewidth=1.5, linestyle='--', label='Mild hypercapnia')
    ax2.plot(capnia, severehiper_capnia, 'y', linewidth=1.5, linestyle='--', label='Severe hypercapnia')
    ax2.fill_between(capnia, cp0, aggregated_list[0], facecolor='Orange', alpha=0.7)
    ax2.plot([defuzz_list[0], defuzz_list[0]], [0, defuz_activation_list[0]], 'k', linewidth=1.5, alpha=0.9)
    ax2.set_title('State of acidity')
    ax2.legend()

    ox0 = np.zeros_like(oxia)
    ax3.plot(oxia, severehipo_oxia, 'b', linewidth=1.5, linestyle='--', label='Severe Hypoxia')
    ax3.plot(oxia, mildhipo_oxia, 'g', linewidth=1.5, linestyle='--', label='Mild Hypoxia')
    ax3.plot(oxia, normo_oxia, 'r', linewidth=1.5, linestyle='--', label='Normal levels')
    ax3.plot(oxia, mildhiper_oxemia, 'c', linewidth=1.5, linestyle='--', label='Mild Hiperoxemia')
    ax3.plot(oxia, severehiper_oxemia, 'y', linewidth=1.5, linestyle='--', label='Severe Hiperoxemia')
    ax3.fill_between(capnia, ox0, aggregated_list[1], facecolor='Orange', alpha=0.7)
    ax3.plot([defuzz_list[1], defuzz_list[1]], [0, defuz_activation_list[1]], 'k', linewidth=1.5, alpha=0.9)
    ax3.set_title('State of basicity')
    ax3.legend()

    for ax in (ax2, ax3):
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.get_xaxis().tick_bottom()
        ax.get_yaxis().tick_left()

    plt.tight_layout()
    """

    """
    print (control_value)
        if control_value > 24 and control_value <= 30: # no change
            GPIO.output(17, GPIO.HIGH)
            time.sleep(5)
            GPIO.output(17, GPIO.LOW)
        elif control_value > 30 and control_value <= 40: # heat
            GPIO.output(27, GPIO.HIGH)
            time.sleep(5)
            GPIO.output(27, GPIO.LOW)
        elif control_value > 10 and control_value <= 24: # cool
            GPIO.output(22, GPIO.HIGH)
            time.sleep(5)
            GPIO.output(22, GPIO.LOW)
        else:
            print ('Valor calculado')
                                
        # Used in the debugging phase
        print ('La temperatura ha sido modificada')"""
