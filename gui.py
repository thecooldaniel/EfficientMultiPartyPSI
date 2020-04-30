import protocol
import helpers
import hashes as h
import bloom_filter as bf
import garbled_bloom_filter as gbf
import PySimpleGUI as sg

# Turn all debug prints to print in a window
# print = sg.Print

sg.change_look_and_feel('DarkBlue2') 

NumPlayers = 3 
PlayerInputSize = 30 # 10
SecParam = 40
bitLength = 128

# These parameters are meant for illustration and fast execution
# they are not considered secure or optimal
Nmaxones = 80 # 40
p = 0.3 # 0.25 # Fraction of messages to use for Cut and Choose
a = 0.27 # 0.25 # Probability a 1 is chosen by a player

perform_protocol = sg.ReadButton('Start Simulation', font=('Segoe UI', 12), key='-RUN-')
stepTracker = 0
Protocol = None

layout = [ 
            [sg.Text('Efficient Multi-Party PSI', size=(50,1), justification='left', font=('Segoe UI', 30))],
            [sg.Text('By Malia Kency and John Owens', font=('Segoe UI', 13))],
            [sg.Text('These parameters are meant for illustration and fast execution, they are not considered secure or optimal', font=('Segoe UI', 12, 'italic'))],
            [ 
                sg.Text('Number of players:', font=('Segoe UI', 12)), 
                sg.Input('3', key='-NUMPLAYERS-', font=('Segoe UI', 12))
            ],
            # [
            #     sg.Text('Player input size:', font=('Segoe UI', 12)),
            #     sg.Slider(range=(30,120), default_value=80, orientation='h', key='-INPUTSIZE-')
            # ],
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
            [sg.Multiline(key='-OUTPUT-', size=(300, 25), font=('Consolas', 10), autoscroll=True)],
            [sg.Button('Clear', font=('Segoe UI', 12)), perform_protocol, sg.Button('Exit', font=('Segoe UI', 12))],
         ]

window = sg.Window('Private Set Intersection', layout, default_element_size=(50,1))

while True:
    # Read the event that happened and the values dictionary
    event, values = window.read()
    # print(event, values)
    if event in (None, 'Exit'): 
        break
    if event == 'Clear':
        window['-OUTPUT-'].Update('')
        stepTracker = 0
    if event == '-RUN-':

        wOut = window['-OUTPUT-']
        # wOut.update('')
        
        if stepTracker == 0:
            window['-OUTPUT-'].update('')
        stepTracker += 1

        if stepTracker == 1:
            # Initialize the protocol by calculating parameters,
            # creating the players, and generating random inputs
            # Note: at least 1 shared value is guaranteed
            NumPlayers = int(values['-NUMPLAYERS-'], 10)
            # PlayerInputSize = int(values['-INPUTSIZE-'])

            Protocol = protocol.new(NumPlayers, Nmaxones, PlayerInputSize, SecParam, bitLength, p, a)
            wOut.print("\nStarting protocol...")
            wOut.print("k = {}".format(Protocol.params.k))
            wOut.print("Not = {}".format(Protocol.params.Not))
            wOut.print("gamma = {}".format(Protocol.params.gamma))
            wOut.print("gammaStar = {} \n".format(Protocol.params.gammaStar))

            wOut.print("\nSimulating players joining protocol. Total: {}\n".format(Protocol.params.NumPlayers))

            wOut.print("-------------------------------------------------------------------------------------------------------------------------------------------------------------------",
                background_color='black')

            perform_protocol.Update("Step {}: Perform Random Oblivious Transfers".format(stepTracker))
        
        if stepTracker == 2:
            
           # Perform the random oblivious transfer simulation for P0...Pt
            wOut.print("\nPerforming Random Oblivious Transfer simulation. {} transfers in total:".format(Protocol.params.Not))
            Protocol.perform_RandomOT()
            output = Protocol.print_PlayerROTTable()
            wOut.print(output)
            wOut.print("\nCounting each player's \"1s\":")
            output = Protocol.print_PlayerMessageStats()
            wOut.print(output + "\n")
            wOut.print("-------------------------------------------------------------------------------------------------------------------------------------------------------------------",
                background_color='black')
            perform_protocol.Update("Step {}: Perform Cut-and-Choose".format(stepTracker))

        elif stepTracker == 3:
            # Perform cut-and-choose simulation for P0...Pt
            wOut.print("\nPerforming Cut and Choose simulation. Size of c: {}. Size of j: {}\n".format(Protocol.params.C, Protocol.params.Not - Protocol.params.C))
            Protocol.perform_CutandChoose()

            wOut.print("-------------------------------------------------------------------------------------------------------------------------------------------------------------------",
                background_color='black')

            perform_protocol.Update("Step {}: Create Bloom Filters".format(stepTracker))

        elif stepTracker == 4:
            # Create bloom filters for P1...Pt
            wOut.print("\nCreating Bloom Filters. BF length: {} \n".format(Protocol.params.Nbf))
            Protocol.create_BloomFilters()

            wOut.print("-------------------------------------------------------------------------------------------------------------------------------------------------------------------",
                background_color='black')

            perform_protocol.Update("Step {}: Create Injective functions".format(stepTracker))

        elif stepTracker == 5:
            # Create P1...Pt's injective functions
            wOut.print("\nCreating injective functions for every Pi:")
            output = Protocol.create_InjectiveFunctions()
            wOut.print(output + "\n")

            wOut.print("-------------------------------------------------------------------------------------------------------------------------------------------------------------------",
                background_color='black')

            perform_protocol.Update("Step {}: Perform XOR sums and RGBF".format(stepTracker))
        
        elif stepTracker == 6:
            # Instantiate P0's and P1's rGBF objects
            wOut.print("\nCreating randomized GBF for every Pi \n")
            Protocol.create_RandomizedGBFs()

            # P0 performs XOR summation on its own j_messages[injective_func] where bit=1
            # P1 performs XOR summation on all P1...Pt's j_messages[injective_func] where bit = P1...Pt's choice
            Protocol.perform_XORsummation()

            # P0 calculates summary values for all elements of its input set
            # P1 calculates summary values for all elements of its input set (Every P1...Pt input values)
            Protocol.perform_SummaryValues()

            wOut.print("-------------------------------------------------------------------------------------------------------------------------------------------------------------------",
                background_color='black')

            perform_protocol.Update("Step {}: Finish protocol".format(stepTracker))
        
        elif stepTracker == 7:
            # P1 receives P0s summary values, compares them to its own
            # Intersections are recorded and output
            output = Protocol.perform_Output()
            wOut.print(output + "\n")

            wOut.print("-------------------------------------------------------------------------------------------------------------------------------------------------------------------",
                background_color='black')

            perform_protocol.Update("Restart Simulation")
            stepTracker = 0
       
window.close()