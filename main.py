import math
#GT3NATurboDataGenerator - Made by Misuka.
#Also applicable to GT4
#var init
Base_BoostGaugeLimit = 13
Base_Boost1 = 13
Base_PeakRPM1 = 25
Base_SpoolRate1 = 120
Base_Boost2 = 17
Base_PeakRPM2 = 35
Base_SpoolRate2 = 110
#stage modifiers
#torque1 is lowrpm, 2 highrpm
Turbo_Stage1_single_torque1 = 1.45
Turbo_Stage1_single_torque2 = 1.08
Turbo_Stage2_single_torque1 = 1.22
Turbo_Stage2_single_torque2 = 1.24
Turbo_Stage3_single_torque1 = 0.81
Turbo_Stage3_single_torque2 = 1.58
Turbo_Stage4_single_torque1 = 0.07
Turbo_Stage4_single_torque2 = 2.45
Turbo_Stage5_single_torque1 = 0.47
Turbo_Stage5_single_torque2 = 1.71
Turbo_Stage1_twin_torque1 = 1.32
Turbo_Stage1_twin_torque2 = 1.10
Turbo_Stage2_twin_torque1 = 1.23
Turbo_Stage2_twin_torque2 = 1.23
Turbo_Stage3_twin_torque1 = 1.07
Turbo_Stage3_twin_torque2 = 1.65
Turbo_Stage4_twin_torque1 = 0.72
Turbo_Stage4_twin_torque2 = 1.85
Turbo_Stage5_twin_torque1 = 0.95
Turbo_Stage5_twin_torque2 = 1.61
NA_Stage1_base_torque1 = 1.14
NA_Stage1_base_torque2 = 1.15
NA_Stage2_base_torque1 = 1.20
NA_Stage2_base_torque2 = 1.26
NA_Stage3_base_torque1 = 1.23
NA_Stage3_base_torque2 = 1.39
NA_Stage3_sc_base_torque1 = 1.41
NA_Stage3_sc_base_torque2 = 1.45
#engine modifiers
ENGINE_OPTIONS = {
    "L1": 1,
    "L2": 1.0125,
    "L3": 1.021,
    "L4": 1.0275,
    "L5": 1.0325,
    "L6": 1.0365,
    "V6": 1.0355,
    "V8": 1.0395,
    "V10": 1.042,
    "V12": 1.044,
    "V16": 1.0455,
    "VR6": 1.036,
    "BOXER2": 1.0135,
    "BOXER4": 1.029,
    "BOXER6": 1.0367,
    "W12": 1.0447,
    "ROTOR2": 1.005,
    "ROTOR3": 1.0085,
    "ROTOR4": 1.013
}
#valvetrain modifiers
VALVETRAIN_OPTIONS = {
    "SOHC": 1.045,
    "DOHC": 1.065,
    "QOHC": 1.03,
    "OHC": 1.02,
    "OHV": 1,
    "ROTARY": 1.015
}

#chatgpt formula for displacement
def transform_value(x):
    # Normalize the input range 350 to 8300
    x_min = 350
    x_max = 8300
    x_normalized = (x - x_min) / (x_max - x_min)
    
    # Apply a logarithmic transformation
    k = 1  # 10 orig - You can adjust this value to fine-tune the curve
    x_transformed = math.log1p(k * x_normalized)  # log1p(x) is log(1 + x)
    
    # Scale and shift to the range a to b
    y_min = 1.05
    y_max = 0.90
    y = y_min + (y_max - y_min) * x_transformed / math.log1p(k)
    
    return y
#end

#chatgpt formula for engine tuning factor
def engine_tuning_factor(power, displacement):
    # Calculate the expected power based on displacement
    expected_power = displacement / 10

    # Calculate the ratio of actual power to expected power
    power_ratio = power / expected_power

    # Define the sensitivity factor
    sensitivity = 0.35  # orig 0.1 - Adjust this to control how quickly the tuning factor changes

    # Calculate the tuning factor using a logarithmic approach for smoother scaling
    if power_ratio >= 1:
        tuning_factor = 1 - sensitivity * math.log(power_ratio)
    else:
        tuning_factor = 1 + sensitivity * math.log(1 / power_ratio)

    # Ensuring the tuning factor remains within a reasonable range
    tuning_factor = max(0.70, min(tuning_factor, 1.025))
    
    return tuning_factor
#end

#start
print("GT3NATurboDataGenerator - Made by Misuka.")
#loop-start
while True:
    print()
    
        #data name input
    while True:
        try:
            label = str(input("Data Label Name: "))
            break
        except:
            print("Something went wrong.")
            continue
    
    #engine input handling
    while True:
        try:
            engine = input("Engine: ").upper()
            if engine in ENGINE_OPTIONS:
                engine_selected = ENGINE_OPTIONS[engine]
            else:
                print("Invalid engine input.")
                continue
            break
        except ValueError:
            print("Invalid engine input.")
            continue
        
    #valvetrain input handling
    while True:
        try:
            valvetrain = input("Valvetrain: ").upper()
            if engine not in ["ROTOR2", "ROTOR3", "ROTOR4"]:
                if valvetrain == "ROTARY":
                    print("Invalid valvetrain input.")
                    continue
            if engine in ["ROTOR2", "ROTOR3", "ROTOR4"]:
                if valvetrain != "ROTARY":
                    print("Invalid valvetrain input.")
                    continue
            if valvetrain in VALVETRAIN_OPTIONS:
                valvetrain_selected = VALVETRAIN_OPTIONS[valvetrain]
            else:
                print("Invalid valvetrain input.")
                continue
            break
        except ValueError:
            print("Invalid valvetrain input.")
            continue
    
    #power input handling
    while True:
        try:
            power = float(input("Peak power: "))
            if power <= 0 or power > 1500:
                print("Invalid power figure.")
                continue
            if power == 69 or power == 699:
                print("Nice.")
            break
        except ValueError:
            print("Invalid power figure.")
            continue
         
    #rpm input handling
    while True:
        try:
            maxrpm = int(input("Peak RPM: "))
            if maxrpm <= 0 or maxrpm > 180:
                print("Invalid RPM figure.")
                continue
            break
        except ValueError:
            print("Invalid RPM figure.")
            continue
        
    #disp. input handling
    while True:
        try:
            displacement = float(input("Displacement: (350-8300) "))
            if displacement < 350 or displacement > 8300:
                print("Disp. figure out of bounds.")
                continue
            else:
                displacement_mu = transform_value(displacement)
            if valvetrain == "ROTARY":
                displacement *= 2
            if displacement == 699 or displacement == 6999 or displacement == 6969:
                print("Nice.")
            break
        except ValueError:
            print("Invalid disp. figure. (Hint: Don't include 'cc')")
            continue
            
    
    #aspiration input handling. na engines get an additional 2.5% boost, to compensate for them not having default turbos that boost values, intended to level out na/turbo engines.
    while True:
        try:
            default_aspiration = input("Default Aspiration: (NA/TURBO/SC) ")
            if default_aspiration.lower() == "na":
                aspiration_multiplier = 1.025
            elif default_aspiration.lower() == "turbo" or default_aspiration.lower() == "sc":
                aspiration_multiplier = 1
            else:
                print("Invalid aspiration input.")
                continue
            break
        except ValueError:
            print("Invalid aspiration input.")
            continue
        
    #tuning factor application
    tuning_factor = engine_tuning_factor(power, displacement)
    print(f"Engine tuning factor: {tuning_factor:.2f}")
    
    #perf figure generator, disp. mu display
    #prev base_performance_figure = (((engine_selected * valvetrain_selected) * displacement_mu) * tuning_factor) * aspiration_multiplier
    base_performance_figure = (((engine_selected * valvetrain_selected) * aspiration_multiplier) * displacement_mu) * tuning_factor
    print(f"Displacement multiplier: {displacement_mu}")
    print(f"Perf figure: {base_performance_figure}")
    print()

    #power figures
    #turbo/na converted values here
    BoostGaugeLimit = round(Base_BoostGaugeLimit * base_performance_figure)
    Boost1 = round(Base_Boost1 * base_performance_figure)
    Boost2 = BoostGaugeLimit
    PeakRPM1 = round(Base_PeakRPM1 * base_performance_figure)
    PeakRPM2 = round(Base_PeakRPM2 * base_performance_figure)
    SpoolRate1 = round(Base_SpoolRate1 / base_performance_figure) #If base_performance_figure is sub-1 like 0.9, etc, will become bigger, is okay?
    SpoolRate2 = round(Base_SpoolRate2 / base_performance_figure)
    Boost2_Stage1 = BoostGaugeLimit - round(Boost1 * 0.35)
    Boost2_Stage2 = round((BoostGaugeLimit * 2) / 1.4) - round(((Boost1 * 2) / 2) * 0.55)
    Boost2_Stage3 = round((BoostGaugeLimit * 3) / 1.4) - round(((Boost1 * 3) / 2.5) * 0.65)
    Boost2_Stage4 = round(BoostGaugeLimit * 4) - round((Boost1 * 4) * 0.35)
    Boost2_Stage5 = round((BoostGaugeLimit * 4) / 1.1) - round((Boost1 * 4) * 0.3)
    TorqueModifier = int(100)
    TorqueModifier2 = int(100)
    
    #file write list var init
    output = []
    #outputs
    output.append("")
    output.append(f"{'-'*25} {label} Data Sheet {'-' * 25}")
    output.append("")
    output.append(f"Turbo 1: (SINGLE)")
    output.append(f"{'BoostGaugeLimit':<15} {'Boost1':<6} {'PeakRPM1':<8} {'SpoolRate1':<10} {'Torque1':<7} {'Torque2':<7}")
    output.append(f"{BoostGaugeLimit:<15} {Boost1:<6} {round(maxrpm / 2.7):<8} {SpoolRate1:<10} {round((TorqueModifier * Turbo_Stage1_single_torque1) * base_performance_figure):<7} {round((TorqueModifier2 * Turbo_Stage1_single_torque2) * base_performance_figure):<7}")
    output.append("")
    output.append(f"Turbo 2: (SINGLE)")
    output.append(f"{'BoostGaugeLimit':<15} {'Boost1':<6} {'PeakRPM1':<8} {'SpoolRate1':<10} {'Torque1':<7} {'Torque2':<7}")
    output.append(f"{round((BoostGaugeLimit * 2) / 1.4):<15} {round((Boost1 * 2) / 1.4):<6} {round(maxrpm / 2.2):<8} {round(SpoolRate1 / 1.1):<10} {round((TorqueModifier * Turbo_Stage2_single_torque1) * base_performance_figure):<7} {round((TorqueModifier2 * Turbo_Stage2_single_torque2) * base_performance_figure):<7}")
    output.append("")
    output.append(f"Turbo 3: (SINGLE)")
    output.append(f"{'BoostGaugeLimit':<15} {'Boost1':<6} {'PeakRPM1':<8} {'SpoolRate1':<10} {'Torque1':<7} {'Torque2':<7}")
    output.append(f"{round((BoostGaugeLimit * 3) / 1.4):<15} {round((Boost1 * 3) / 1.4):<6} {round(maxrpm / 1.5):<8} {round(SpoolRate1 / 1.65):<10} {round((TorqueModifier * Turbo_Stage3_single_torque1) * base_performance_figure):<7} {round((TorqueModifier2 * Turbo_Stage3_single_torque2) * base_performance_figure):<7}")
    output.append("")
    output.append(f"Turbo 4: (SINGLE)")
    output.append(f"{'BoostGaugeLimit':<15} {'Boost1':<6} {'PeakRPM1':<8} {'SpoolRate1':<10} {'Torque1':<7} {'Torque2':<7}")
    output.append(f"{round(BoostGaugeLimit * 4):<15} {round(Boost1 * 4):<6} {maxrpm - 5:<8} {round(SpoolRate1 / 5.6):<10} {round((TorqueModifier * Turbo_Stage4_single_torque1) * base_performance_figure):<7} {round((TorqueModifier2 * Turbo_Stage4_single_torque2) * base_performance_figure):<7}")
    output.append("")
    output.append(f"Turbo 5: (Original, SINGLE)")
    output.append(f"{'BoostGaugeLimit':<15} {'Boost1':<6} {'PeakRPM1':<8} {'SpoolRate1':<10} {'Torque1':<7} {'Torque2':<7}")
    output.append(f"{round((BoostGaugeLimit * 4) / 1.1):<15} {round((Boost1 * 4) / 1.1):<6} {maxrpm:<8} {round(SpoolRate1 / 4.3):<10} {round((TorqueModifier * Turbo_Stage5_single_torque1) * base_performance_figure):<7} {round((TorqueModifier2 * Turbo_Stage5_single_torque2) * base_performance_figure):<7}")
    output.append("")
    output.append(f"Turbo 1: (TWIN)")
    output.append(f"{'BoostGaugeLimit':<15} {'Boost1':<6} {'PeakRPM1':<8} {'SpoolRate1':<10} {'Boost2':<6} {'PeakRPM2':<8} {'SpoolRate2':<10} {'Torque1':<7} {'Torque2':<7}")
    output.append(f"{BoostGaugeLimit:<15} {round(Boost1 * 0.35):<6} {round(maxrpm / 4.5):<8} {round(SpoolRate1 * 1.1):<10} {Boost2_Stage1:<6} {round(maxrpm / 2.7):<8} {SpoolRate2:<10} {round((TorqueModifier * Turbo_Stage1_twin_torque1) * base_performance_figure):<7} {round((TorqueModifier2 * Turbo_Stage1_twin_torque2) * base_performance_figure):<7}")
    output.append("")
    output.append(f"Turbo 2: (TWIN)")
    output.append(f"{'BoostGaugeLimit':<15} {'Boost1':<6} {'PeakRPM1':<8} {'SpoolRate1':<10} {'Boost2':<6} {'PeakRPM2':<8} {'SpoolRate2':<10} {'Torque1':<7} {'Torque2':<7}")
    output.append(f"{round((BoostGaugeLimit * 2) / 1.4):<15} {round(((Boost1 * 2) / 2) * 0.55):<6} {round(maxrpm / 3.7):<8} {round((SpoolRate1 / 1.1) * 1.1):<10} {Boost2_Stage2:<6} {round(maxrpm / 2.1):<8} {round(SpoolRate2 / 1.1):<10} {round((TorqueModifier * Turbo_Stage2_twin_torque1) * base_performance_figure):<7} {round((TorqueModifier2 * Turbo_Stage2_twin_torque2) * base_performance_figure):<7}")
    output.append("")
    output.append(f"Turbo 3: (TWIN)")
    output.append(f"{'BoostGaugeLimit':<15} {'Boost1':<6} {'PeakRPM1':<8} {'SpoolRate1':<10} {'Boost2':<6} {'PeakRPM2':<8} {'SpoolRate2':<10} {'Torque1':<7} {'Torque2':<7}")
    output.append(f"{round((BoostGaugeLimit * 3) / 1.4):<15} {round(((Boost1 * 3) / 2.5) * 0.65):<6} {round(maxrpm / 2.7):<8} {round((SpoolRate1 / 1.65) * 1.1):<10} {Boost2_Stage3:<6} {round(maxrpm / 1.4):<8} {round(SpoolRate2 / 1.65):<10} {round((TorqueModifier * Turbo_Stage3_twin_torque1) * base_performance_figure):<7} {round((TorqueModifier2 * Turbo_Stage3_twin_torque2) * base_performance_figure):<7}")
    output.append("")
    output.append(f"Turbo 4: (TWIN)")
    output.append(f"{'BoostGaugeLimit':<15} {'Boost1':<6} {'PeakRPM1':<8} {'SpoolRate1':<10} {'Boost2':<6} {'PeakRPM2':<8} {'SpoolRate2':<10} {'Torque1':<7} {'Torque2':<7}")
    output.append(f"{round(BoostGaugeLimit * 4):<15} {round((Boost1 * 4) * 0.35):<6} {round(maxrpm / 2.25):<8} {round((SpoolRate1 / 3.5) * 1.1):<10} {Boost2_Stage4:<6} {round(maxrpm / 1.21):<8} {round(SpoolRate2 / 4):<10} {round((TorqueModifier * Turbo_Stage4_twin_torque1) * base_performance_figure):<7} {round((TorqueModifier2 * Turbo_Stage4_twin_torque2) * base_performance_figure):<7}")
    output.append("")
    output.append(f"Turbo 5: (Original, TWIN)")
    output.append(f"{'BoostGaugeLimit':<15} {'Boost1':<6} {'PeakRPM1':<8} {'SpoolRate1':<10} {'Boost2':<6} {'PeakRPM2':<8} {'SpoolRate2':<10} {'Torque1':<7} {'Torque2':<7}")
    output.append(f"{round((BoostGaugeLimit * 4) / 1.1):<15} {round((Boost1 * 4) * 0.3):<6} {round(maxrpm / 2.30):<8} {round((SpoolRate1 / 2.6) * 1.1):<10} {Boost2_Stage5:<6} {round(maxrpm / 1.27):<8} {round(SpoolRate2 / 3):<10} {round((TorqueModifier * Turbo_Stage5_twin_torque1) * base_performance_figure):<7} {round((TorqueModifier2 * Turbo_Stage5_twin_torque2) * base_performance_figure):<7}")
    output.append("")
    if default_aspiration.lower() == "turbo":
        output.append("NA-Tune data is only outputted for NA/SC cars.")
        output.append("")
        output.append(f"{'-'*25} Finished {label} {'-' * 25}")
        output.append("")
    else:
        output.append(f"NA-Tune 1: ")   
        output.append(f"{'Torque1':<7} {'Torque2':<7}")
        output.append(f"{round((TorqueModifier * NA_Stage1_base_torque1) * base_performance_figure):<7} {round((TorqueModifier2 * NA_Stage1_base_torque2) * base_performance_figure):<7} ")
        output.append("")
        output.append(f"NA-Tune 2: ")
        output.append(f"{'Torque':<7} {'Torque2':<7}")
        output.append(f"{round((TorqueModifier * NA_Stage2_base_torque1) * base_performance_figure):<7} {round((TorqueModifier2 * NA_Stage2_base_torque2) * base_performance_figure):<7} ")
        output.append("")
        output.append(f"NA-Tune 3: ")
        output.append(f"{'Torque':<7} {'Torque2':<7}")
        output.append(f"{round((TorqueModifier * NA_Stage3_base_torque1) * base_performance_figure):<7} {round((TorqueModifier2 * NA_Stage3_base_torque2) * base_performance_figure):<7} ")
        output.append("")
        output.append(f"NA-Tune 3: (SUPERCHARGER) ")
        output.append(f"{'Torque':<7} {'Torque2':<7}")
        output.append(f"{round((TorqueModifier * NA_Stage3_sc_base_torque1) * base_performance_figure):<7} {round((TorqueModifier2 * NA_Stage3_sc_base_torque2) * base_performance_figure):<7} ")
        output.append("")
        output.append(f"{'-'*25} Finished {label} {'-' * 25}")
        output.append("")
        
    #join output
    output_string = "\n".join(output)
    #print output to console
    print(output_string)
    #write to file
    with open("output.txt", "a") as f:
        f.write(output_string)
    
    #debug list
    #print(f"Debug; Stage4T power: {power * round((TorqueModifier2 * Turbo_Stage4_single_torque2) * base_performance_figure) / 100}")
    #print(f"Debug; Stage3NA_SC power: {power * round((TorqueModifier2 * NA_Stage3_sc_base_torque2) * base_performance_figure) / 100}")
    #print(f"Debug; Stage3T_TWIN power: {power * round((TorqueModifier2 * Turbo_Stage3_twin_torque2) * base_performance_figure) / 100}")
    #print(f"Perf1: eng-valve                    {(engine_selected * valvetrain_selected)}")
    #print(f"Perf2: eng-valve-asp                {(engine_selected * valvetrain_selected) *  aspiration_multiplier}")
    #print(f"Perf3: eng-valve-asp-disp           {((engine_selected * valvetrain_selected) *  aspiration_multiplier) * displacement_mu}")
    #print(f"Perf4: eng-valve-asp-disp-factor    {(((engine_selected * valvetrain_selected) * aspiration_multiplier) * displacement_mu) * tuning_factor}")
    #print(f"Debug; disp. {displacement}")
    #print(f'Debug; def_aspiration "{default_aspiration}"')
    #print(f'Debug; aspiration mu "{aspiration_multiplier}"')
    #print(f'Debug; engine mu "{engine_selected}"')
    #print(f'Debug; valve mu "{valvetrain_selected}"')
    #print(f'Debug; engine type "{engine}"')
    #print(f'Debug; valve type "{valvetrain}"')
    redo = input("Generate another? y/n ")
    if redo.lower() == "n":
        ask_clear = input("Empty output.txt? y/n ")
        if ask_clear.lower() == "y":
            confirm = input("Are you sure? y/n ")
            if confirm.lower() == "y":
                open("output.txt", "w").close()
                break
            else:
                break
        else:
            break
