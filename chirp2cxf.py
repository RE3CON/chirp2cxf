import csv
import sys




#chirpcsvfile = sys.argv[1]

#ctcss data
ctcss_tones = [
    67.0, 69.3, 71.9, 74.4, 77.0, 79.7, 82.5, 85.4, 88.5, 91.5,
    94.8, 97.4, 100.0, 103.5, 107.2, 110.9, 114.8, 118.8, 123.0, 127.3,
    131.8, 136.5, 141.3, 146.2, 151.4, 156.7, 159.8, 162.2, 165.5, 167.9,
    171.3, 173.8, 177.3, 179.9, 183.5, 186.2, 189.9, 192.8, 196.6, 199.5,
    203.5, 206.5, 210.7, 218.1, 225.7, 229.1, 233.6, 241.8, 250.3
    ]

#set these varibles if the CtCss is not in the table
AnaTxCTCIndex=0
AnaRxCTCIndex=0

# Open the CSV file
with open('chirp.csv', mode='r') as csv_file:
    
    # Create a CSV reader object
    csv_reader = csv.DictReader(csv_file)
    
    # Iterate over each row in the CSV file
    for row in csv_reader:
        
        # Put each value into a separate variable
        Location = row['Location']
        Name = row['Name']
        Frequency = row['Frequency']
        Duplex = row['Duplex']
        Offset = row['Offset']
        Tone = row['Tone']
        rToneFreq = row['rToneFreq'] #ctcss tone frequency
        cToneFreq = row['cToneFreq']
        DtcsCode = row['DtcsCode']
        DtcsPolarity = row['DtcsPolarity']
        RxDtcsCode = row['RxDtcsCode']
        CrossMode = row['CrossMode']
        TStep = row['TStep']
        Skip = row['Skip']
        Power = row['Power']
        Mode = row['Mode']
        
        #Start field translation  
        
        #Check location is ok (<200)
        if float(Location)>200:
            break
        chanIndex=Location


        #Name goes into <Name>
        Name = Name[:10]


        #Tidy up for <Rxfreq>
        RxFreq = float(Frequency)
        RxFreq = round(RxFreq,6)


        #Calculate Transmit <Txfreq> from Recieve and Offset Xml variable <Txfreq>
        TxFreq = float(Frequency) + float(Offset) #CHIRP sets Offset to 0 if not used
        if Duplex == "-":
            TxFreq = float(Frequency) - float(Offset)
        TxFreq = round(TxFreq,6)

        

        #calculate ctcss tone index position for rx and tx tones
        if float(rToneFreq) in ctcss_tones:
            AnaTxCTCIndex = ctcss_tones.index(float(rToneFreq))
        if float(cToneFreq) in ctcss_tones:
            AnaRxCTCIndex = ctcss_tones.index(float(cToneFreq))


        #Calculate values for <AnaTxCTCFlag> <AnaRxCTCFlag>
        if Tone == "":
            AnaTxCTCFlag = 0
            AnaRxCTCFlag = 0
        if Tone == "Tone":
            AnaTxCTCFlag = 1
            AnaRxCTCFlag = 0
        if Tone == "TSQL":
            AnaTxCTCFlag = 1
            AnaRxCTCFlag = 1
        if Tone == "Cross":
            if CrossMode == "->Tone":            
                AnaTxCTCFlag = 0
                AnaRxCTCFlag = 1
        if Tone == "Cross":
            if CrossMode == "Tone->Tone":            
                AnaTxCTCFlag = 1
                AnaRxCTCFlag = 1

        #Calculate <TxPowerLevel>
        TxPowerLevel = 2 #default to high
        if Power == "4.0W": #Chirp config for a BF=8HP uses these values
            TxPowerLevel = 1
        if Power == "1.0W":
            TxPowerLevel = 0

        #calculate the <BandWidth>
        Bandwidth = 0 #default to 25khz
        if Mode == "NFM":
            Bandwidth = 1
        
        
        # Do something with the variables
        #print(Location, " ", Name, " ", Rxfreq," ", Duplex, " ",Offset, " ",Txfreq, "rToneFreq =", AnaTxCTCIndex)

        #Lets print the XML
        
        print ('    <Channel Name=\"'+Name+'\" chanIndex=\"'+str(chanIndex)+'\">')
        print ('      <BandWidth>'+str(Bandwidth)+'</BandWidth>')
        print ('      <TxFreq>'+str(TxFreq)+'</TxFreq>')
        print ('      <RxFreq>'+str(RxFreq)+'</RxFreq>')
        print ('      <TxPowerLevel>'+str(TxPowerLevel)+'</TxPowerLevel>')
        print ('      <AnaTxCTCFlag>'+str(AnaTxCTCFlag)+'</AnaTxCTCFlag>')
        print ('      <AnaRxCTCFlag>'+str(AnaRxCTCFlag)+'</AnaRxCTCFlag>')
        print ('      <AnaTxCTCIndex>'+str(AnaTxCTCIndex)+'</AnaTxCTCIndex>')
        print ('      <AnaRxCTCIndex>'+str(AnaRxCTCIndex)+'</AnaRxCTCIndex>')
        print ('      <FreqStep>2</FreqStep>')
        print ('      <FreqReverseFlag>0</FreqReverseFlag>')
        print ('      <EncryptFlag>0</EncryptFlag>')
        print ('      <BusyNoTx>0</BusyNoTx>')
        print ('      <PTTIdFlag>0</PTTIdFlag>')
        print ('      <DTMFDecode>0</DTMFDecode>')
        print ('      <AMChanFlag>0</AMChanFlag>')
        print ('    </Channel>')
        
