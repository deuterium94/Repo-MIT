try:
    import queue
except ImportError:
    import Queue as queue
import chargePorts
import chargeEvent
import update_vars

#fcfs
q1=queue.Queue(0)

# ------ FCFS ------

# the main implementation of the First Come First Serve algorithm
# takes in an array of arrays of vehicle minutes ( 2-level )
def simulate( arrayOfVehicleArrivals ):
    
    # reset global variables such as time, done/failed lots
    update_vars.updateGlobals( arrayOfVehicleArrivals )
    global currentTime

    # initialize a CSV document for storing all data

    # iterate through each vehicle in each minute
    for minute, numVehiclesPerMin in enumerate( arrayOfVehicleArrivals ):
        for vehicle in numVehiclesPerMin:       
            port = chargePorts.openChargePort()
            
            if vehicle.currentCharge > vehicle.chargeNeeded:
                #csvGen.exportVehicleToCSV( vehicle, "Charge Not Needed" )
                update_vars.cantChargeLot.append( vehicle )
                continue

            # a port is open so start charging the vehicle
            if port is not None:

                # add to chargePort
                chargePorts.chargePorts[ port ] = vehicle
            
                # initialize a listener object for its charging activity
                chargePorts.chargePortListeners[ port ].insert( 0 , chargeEvent.ChargeEvent( vehicle, update_vars.currentTime ) )
                print("vehicle "+str(vehicle)+"charged at "+str(update_vars.currentTime ))
            # no ports are available so put the vehicle in the q1
            else:
                q1.put( vehicle )
                print("vehicle not charged  : "+str(vehicle)+" at "+str(update_vars.currentTime) +"min")
    


        updateVehiclesFCFS()
        update_vars.currentTime += 1
        update_vars.lenEVs=len(arrayOfVehicleArrivals)


    # print "status:  " , openChargePort() , "  " , q1.empty()
    
    # run the clock until all vehicles have ran through the simulation
    while chargePorts.chargePortsEmpty() == False or not q1.empty():
        updateVehiclesFCFS()
        update_vars.currentTime += 1
    # print "FCFS: total number of cars: ", update_vars.numberOfVehiclesInSimulation , \
    #     "  elapsed time: " , update_vars.currentTime , \
    #     "  done charging lot: " , len( update_vars.doneChargingLot ) , \
    #     "  failed charging lot: " , len( update_vars.failedLot ) , \
    #     "  cant charge lot: " , len( update_vars.cantChargeLot ) , \
    #     "  fcfsQueue size:  " , q1.qsize() , \
    #     "  chargePort " , chargePorts.toString()

    # write a CSV for all the chargePort logs
    #csvGen.exportChargePortsToCSV( "fcfs" )
    
    output = [update_vars.calcProfit(), len(update_vars.doneChargingLot), len(update_vars.failedLot), len(update_vars.declinedLot), update_vars.numberOfVehiclesInSimulation, update_vars.currentTime]
    return output

# called to update the vehicles for each minute of simulation
def updateVehiclesFCFS():

    # check each chargePort
    for index, vehicle in enumerate( chargePorts.chargePorts ):        

        # add 1 minute of charge
        if vehicle is not None:
            vehicle.currentCharge +=  ( vehicle.chargeRate ) / 60.0
            removed = False;

            # check if done charging
            if vehicle.currentCharge >= vehicle.chargeNeeded:

                # this vehicle is on the out, so wrap up its listener
                chargePorts.chargePortListeners[ index ][ 0 ].terminateCharge( vehicle , update_vars.currentTime )

                # remove finished vehicle from grid and document it
                #csvGen.exportVehicleToCSV( vehicle, "SUCCESS" )
                update_vars.doneChargingLot.append( vehicle )
                
                # the next vehicle
                if not q1.empty():

                    nextVehicle = q1.get()
                    chargePorts.chargePorts[ index ] = nextVehicle

                    # and then make a new listener
                    chargePorts.chargePortListeners[ index ].insert( 0 , chargeEvent.ChargeEvent( nextVehicle , update_vars.currentTime ) )

                else:
                    chargePorts.chargePorts[ index ] = None
                removed = True;


            # check if deadline reached            
            if update_vars.currentTime >= vehicle.depTime and not removed:

                # this vehicle is on the out, so wrap up its listener
                chargePorts.chargePortListeners[ index ][ 0 ].terminateCharge( vehicle , update_vars.currentTime )
                
                # remove finished vehicle from grid and document it
                #csvGen.exportVehicleToCSV( vehicle, "FAILURE" )               
                update_vars.failedLot.append( vehicle )
                
                # the next vehicle
                if not q1.empty():

                    nextVehicle = q1.get()
                    chargePorts.chargePorts[ index ] = nextVehicle

                    # and then make a new listener
                    chargePorts.chargePortListeners[ index ].insert( 0 , chargeEvent.ChargeEvent( nextVehicle , update_vars.currentTime ) )

                else:
                    chargePorts.chargePorts[ index ] = None
