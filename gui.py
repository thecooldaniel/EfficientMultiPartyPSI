import protocol
import helpers
import hashes as h
import bloom_filter as bf
import garbled_bloom_filter as gbf
import PySimpleGUI as sg

sg.change_look_and_feel('DarkBlue2') 

perform_protocol = sg.ReadButton('Start Simulation', font=('Segoe UI', 12), key='-RUN-')
stepTracker = 0
Protocol = None
disableChecks = False

layout = [ 
            [sg.Text('Efficient Multi-Party PSI', size=(50,1), justification='left', font=('Segoe UI', 30))],
            [sg.Text('By Malia Kency and John Owens', font=('Segoe UI', 13))],
            [sg.Text('These parameters are meant for illustration and fast execution, they are not considered secure or optimal', font=('Segoe UI', 12, 'italic'))],
            [
                sg.Frame('', [
                    [
                        sg.Checkbox('Let me break stuff', font=('Segoe UI', 10), key='-DISABLECHECKS-', enable_events=True)
                    ],
                    [
                        sg.Text('Number of players:    ', font=('Segoe UI', 10)), 
                        sg.Input('3', key='-NUMPLAYERS-', font=('Segoe UI', 10), disabled=True), 
                        sg.Text('        Player input size:', font=('Segoe UI', 10)), 
                        sg.Input('20', key='-INPUTSIZE-', font=('Segoe UI', 10), disabled=True)],
                    [
                        sg.Text('Weight of chosen 1s:  ', font=('Segoe UI', 10)), 
                        sg.Input('0.27', key='-A-', font=('Segoe UI', 10), disabled=True), 
                        sg.Text('Cut-and-Choose Prob:', font=('Segoe UI', 10)), 
                        sg.Input('0.3', key='-C-', font=('Segoe UI', 10), disabled=True)],
                    [
                        sg.Text('Number of max ones: ', font=('Segoe UI', 10)), 
                        sg.Input('80', key='-NMAXONES-', font=('Segoe UI', 10), disabled=True)
                    ],
                ]),
            ],
            [ 
                sg.Text('Constant protocol parameters that will be used:', font=('Segoe UI', 12), size=(72,1),),
                sg.Text('Parameters that will be calculated:', font=('Segoe UI', 12)),
            ],
           
            [ sg.Listbox(
                    values = [
                        'NumPlayers       = Total number of players, P\N{LATIN SUBSCRIPT SMALL LETTER I}',
                        'PlayerInputSize  = Size of the players input sets',
                        'SecParam (kappa) = 40  = Security Parameter',
                        'bitLength        = 128 = length of random generated strings',
                        'Nmaxones         = Max number of ones a player is allowed after cut-and-choose',
                        'p = 0.3          = Percentage of total messages to be used for cut-and-choose',
                        'a = 0.27         = Sampling weight of 1s vs. 0s for every P\N{LATIN SUBSCRIPT SMALL LETTER I}'],
                    size=(85,8), font=('Consolas', 10)),
                sg.Listbox(
                    values = [
                        'Not       = Total number of Random Oblivious Transfer',
                        'Nbf       = Size of the player\'s bloom_filter. Calculated on initalization',
                        'k         = Number of hash functions to use. Calculated on initalization',
                        'm\N{LATIN SUBSCRIPT SMALL LETTER h}        = The number of 1s a player chooses',
                        'gamma     = Verifies the correct relationship between p, k, m\N{LATIN SUBSCRIPT SMALL LETTER h}',
                        'gammaStar = Verifies the correct relationship between p, k, Not'],
                        size=(85,8), font=('Consolas', 10))
            ],
            [sg.Multiline(key='-OUTPUT-', size=(200, 20), font=('Consolas', 10), autoscroll=True, text_color='white')],
            [sg.Button('Reset', font=('Segoe UI', 12)), perform_protocol, sg.Button('Exit', font=('Segoe UI', 12))],
         ]

window = sg.Window('Private Set Intersection', layout, location=(100,40), resizable=True)

while True:
    # Read the event that happened and the values dictionary
    event, values = window.read()
    # print(event, values)
    if event in (None, 'Exit'): 
        break
    if event == 'Reset':
        window['-OUTPUT-'].Update('')
        perform_protocol.Update("Start Simulation")
        stepTracker = 0
    if event == '-DISABLECHECKS-':
        if values['-DISABLECHECKS-']:
            window['-NUMPLAYERS-'].update(disabled=False)
            window['-INPUTSIZE-'].update(disabled=False)
            window['-A-'].update(disabled=False)
            window['-C-'].update(disabled=False)
            window['-NMAXONES-'].update(disabled=False)
            disableChecks = True
        else:
            window['-NUMPLAYERS-'].update(disabled=True)
            window['-INPUTSIZE-'].update(disabled=True)
            window['-A-'].update(disabled=True)
            window['-C-'].update(disabled=True)
            window['-NMAXONES-'].update(disabled=True)
            disableChecks = False

    if event == '-RUN-':
        NumPlayers = 3 
        PlayerInputSize = 30 # 10
        SecParam = 40
        bitLength = 128
        Nmaxones = 80 # 40
        p = 0.3
        a = 0.27

        if disableChecks:
            PlayerInputSize = int(values['-INPUTSIZE-'])
            NumPlayers = int(values['-NUMPLAYERS-'])
            Nmaxones = int(values['-NMAXONES-'])
            p = float(values['-C-'])
            a = float(values['-A-'])

        wOut = window['-OUTPUT-']
        
        if stepTracker == 0:
            window['-OUTPUT-'].update('')
        stepTracker += 1

        if stepTracker == 1:

            # Initialize the protocol by calculating parameters,
            # creating the players, and generating random inputs
            # Note: at least 1 shared value is guaranteed
            # PlayerInputSize = int(values['-INPUTSIZE-'])

            Protocol = protocol.new(NumPlayers, Nmaxones, PlayerInputSize, SecParam, bitLength, p, a, disableChecks)
            wOut.print("\nStarting protocol...")
            wOut.print("k = {}".format(Protocol.params.k))
            wOut.print("Not = {}".format(Protocol.params.Not))
            wOut.print("gamma = {}".format(Protocol.params.gamma))
            wOut.print("gammaStar = {} \n".format(Protocol.params.gammaStar))

            wOut.print("\nSimulating players joining protocol. Total: {}".format(Protocol.params.NumPlayers), background_color='#284050', text_color='white')
            wOut.print("At least one intersection will occur at the value: {}".format(Protocol.params.shared_random), background_color="red", text_color="white")
            wOut.print("\nStep " + str(stepTracker-1) +" finished\n", background_color='#284050', text_color='white')
            perform_protocol.Update("Step {}: Perform Random Oblivious Transfers".format(stepTracker))

        if stepTracker == 2:
            
           # Perform the random oblivious transfer simulation for P0...Pt
            wOut.print("\nPerforming Random Oblivious Transfer simulation. {} transfers in total:".format(Protocol.params.Not))
            Protocol.perform_RandomOT()
            output = Protocol.print_PlayerROTTable()
            wOut.print(output)
            wOut.print("\nCounting each player's \"1s\":")
            output = Protocol.print_PlayerMessageStats()
            wOut.print(output + "\n\nStep " + str(stepTracker-1) +" finished\n")
            perform_protocol.Update("Step {}: Perform Cut-and-Choose".format(stepTracker))

        elif stepTracker == 3:
            # Perform cut-and-choose simulation for P0...Pt
            wOut.print("\nPerforming Cut and Choose simulation. Size of c: {}. Size of j: {}".format(Protocol.params.C, Protocol.params.Not - Protocol.params.C), background_color='#284050', text_color='white')
            wOut.print("\nStep " + str(stepTracker-1) +" finished\n", background_color='#284050', text_color='white')
            Protocol.perform_CutandChoose()
            perform_protocol.Update("Step {}: Create Bloom Filters".format(stepTracker))

        elif stepTracker == 4:
            # Create bloom filters using j messages for P1...Pt
            wOut.print("\nCreating Bloom Filters. BF length: {}".format(Protocol.params.Nbf))
            output = Protocol.create_BloomFilters()
            wOut.print(output)
            wOut.print("\nStep " + str(stepTracker-1) +" finished\n")
            perform_protocol.Update("Step {}: Create Injective functions".format(stepTracker))

        elif stepTracker == 5:
            # Create P1...Pt's injective functions
            wOut.print("\nCreating injective functions for every Pi:", background_color='#284050', text_color='white')
            output = Protocol.create_InjectiveFunctions()
            wOut.print(output, background_color='#284050', text_color='white')
            wOut.print("\nStep " + str(stepTracker-1) +" finished\n", background_color='#284050', text_color='white')  
            perform_protocol.Update("Step {}: Perform XOR sums and RGBF".format(stepTracker))
        
        elif stepTracker == 6:
            # Instantiate P0's and P1's rGBF objects
            wOut.print("\nCreating randomized GBF for every Pi")
            Protocol.create_RandomizedGBFs()

            # P0 performs XOR summation on its own j_messages[injective_func] where bit=1
            # P1 performs XOR summation on all P1...Pt's j_messages[injective_func] where bit = P1...Pt's choice
            output = Protocol.perform_XORsummation()
            wOut(output)
            
            # P0 calculates summary values for all elements of its input set
            # P1 calculates summary values for all elements of its input set (Every P1...Pt input values)
            Protocol.perform_SummaryValues()
            wOut.print("\nStep " + str(stepTracker-1) +" finished\n")
            perform_protocol.Update("Step {}: Finish protocol".format(stepTracker))

        elif stepTracker == 7:
            # P1 receives P0s summary values, compares them to its own
            # Intersections are recorded and output
            output, intersections = Protocol.perform_Output()
            wOut.print(output, background_color='#284050', text_color='white')
            wOut.print(intersections, background_color="red", text_color="white")
            wOut.print("\nStep " + str(stepTracker-1) +" finished\n", background_color='#284050', text_color='white')
            perform_protocol.Update("Restart Simulation")
            stepTracker = 0
       
window.close()