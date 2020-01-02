import sys
import update_vars
import fcfs
import poissonGen
import gc



if len( sys.argv ) != 2:
    print ('Wrong Number of Arguments you sent'+ str(sys.argv)+ " .. just interval" )
    sys.exit()  

interval = int( sys.argv[ 1 ] )
update_vars.setInterval(interval)


# ------------------ real simulations -------------------------

# do tons and tons of simulations
arrivalRate =  1
numIterations = 1
arrivalStep = 1
numRunsPerIteration = 5
simulationProfitData = [ ]
simulationSuccessData = [ ]
simulationSuccessDataWithDeclined = [ ]
simulationElapsedTimeData = [ ]

for i in range( numIterations ):

    averageRates = [ 0 ] * 1    # a spot for every algo
    averageRatesWithDeclined = [ 0 ] * 1
    averageProfits = [ 0 ] * 1
    averageElapsedTimes = [ 0 ] *1
    averageChargingTime=[0]*1

    for k in range( numRunsPerIteration ):

        gc.collect()
        #print"--------------------------"

        poissonGen.setArrivalRate(arrivalRate)
        simulationInterval = poissonGen.simulateInterval()
        # don't want a simulation with no cars
        while update_vars.numberOfVehiclesInSimulation == 0:
            simulationInterval = poissonGen.simulateInterval()

        # common.vehicleIdsIn2DList( simulationInterval )

        #----------------fcfs----------------
        fcfsData = fcfs.simulate( simulationInterval )

#        fcfsACData = fcfs_AC.simulate( simulationInterval )
#
#        #----------------edf----------------
#        edfData = edf.simulate( simulationInterval )
#
#        edfACBasicData = edf_AC_Basic.simulate( simulationInterval )
#
#        edfACProData = edf_AC_Pro.simulate( simulationInterval )
#
#        #----------------llfSimple----------------
#        llfSimpleData = llfSimple.simulate( simulationInterval )
#
#        llfSimpleACBasicData = llfSimple_AC_Basic.simulate( simulationInterval )
#
#        llfSimpleACProData = llfSimple_AC_Pro.simulate( simulationInterval )
#
#        #----------------llfSmart----------------
#        llfSmartData = llfSmart.simulate( simulationInterval )
#
#        llfSmartACBasicData = llfSmart_AC_Basic.simulate( simulationInterval )
#
#        #----------------dsac----------------
#        dsacData = dsac.simulate( simulationInterval )

        # common.vehicleIdsIn2DList( simulationInterval )

        runData = [ fcfsData  ]

        runProfits = [ 0 ] * 1
        runSuccessRates = [ 0 ] * 1
        runElapsedTimes = [ 0 ] * 1
        runSuccessRatesWithDeclined = [ 0 ] * 1
        runaverageChargingTime=[ 0 ] * 1
        
        for index , algoData in enumerate( runData ):
            runProfits[ index ] = algoData[ 0 ]
            runSuccessRates[ index ] = ( 1.0 * algoData[ 1 ] ) / ( algoData[ 1 ] + algoData[ 2 ] ) 
            runSuccessRatesWithDeclined[ index ] = ( 1.0 * algoData[ 1 ] ) / algoData[ 4 ]
            runElapsedTimes[ index ] = algoData[ 5 ] 
        for index, rate in enumerate( runSuccessRates ):
            averageRates[ index ] += rate

        for index, rate in enumerate( runSuccessRatesWithDeclined ):
            averageRatesWithDeclined[ index ] += rate

        for index, profit in enumerate( runProfits ):
            averageProfits[ index ] += profit

        for index, time in enumerate( runElapsedTimes ):
            averageElapsedTimes[ index ] += time
    
    for n in range( len( averageRates ) ):
        averageRates[ n ] /= ( numRunsPerIteration * 1.0 )

    for n in range( len( averageRatesWithDeclined ) ):
        averageRatesWithDeclined[ n ] /= ( numRunsPerIteration * 1.0 )

    for n in range( len( averageProfits ) ):
        averageProfits[ n ] /= ( numRunsPerIteration * 1.0 )

    for n in range( len( averageElapsedTimes ) ):
        averageElapsedTimes[ n ] /= ( numRunsPerIteration * 1.0 )

    simulationSuccessData.append( [ arrivalRate ] + averageRates )
    simulationSuccessDataWithDeclined.append( [ arrivalRate ] + averageRatesWithDeclined )
    simulationProfitData.append( [ arrivalRate ] + averageProfits )
    simulationElapsedTimeData.append( [ arrivalRate ] + averageElapsedTimes )

    arrivalRate += arrivalStep
    
    if i % 10 == 0:
        print("------------------------summary --------------------------------------------------")
        print ("iteration: " +str(i)+ " arrival rate: "+str(arrivalRate))
        print ("averageRates: "+str( averageRates))
        print ("averageRatesWithDeclined"+str(averageRatesWithDeclined))
        print ("averageProfits: "+str(averageProfits))
        #print("Number of successfully charged EVs in simulation:\n"+str(len(simulationSuccessData)))
        print("Average Charging Time " +str(averageElapsedTimes))
        print("------------------------summary --------------------------------------------------")

#csvGen.exportSimulationDataToCSV( simulationSuccessData , "Success" )
#csvGen.exportSimulationDataToCSV( simulationSuccessDataWithDeclined , "Success With Declines" )
#csvGen.exportSimulationDataToCSV( simulationProfitData , "Profits" )
#csvGen.exportSimulationDataToCSV( simulationElapsedTimeData , "Elapsed Time" )
