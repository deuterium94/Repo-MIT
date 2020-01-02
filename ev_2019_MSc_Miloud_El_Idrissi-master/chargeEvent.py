# a chargingEvent is the basic object used for logging what's going on with each chargePort
# We will be using an array that's the same length of chargePorts
# each index will contain an array of chargingEvents
# the first index of this array will be the chargePort's log of the first vehicle that it dealth with
# the last index of these arrays will log the most recent chargingEvent for that specific chargePort

# to create, pass in the vehicle and currentTime
# when a vehicle is done charging, it will need the updated version of the same vehicle and again the currentTime

# readouts of -1 for endTime, endVehicle, and timeCharging will denote that it's either still listening or something went very wrong

#import electric_vehicle as vehicle1

class ChargeEvent:
    numEvents = 0

    def __init__( self, vehicle, startTime ):

        # parameters for each vehicle, not all are used for each algorithm implementation
        self.id                 =     ChargeEvent.numEvents 
        self.startTime          =     startTime                 # the time that this vehicle began charging
        self.initialVehicle     =     vehicle                   # we wil have all the stats of our vehicle object when it entered
        self.endTime            =     -1                        # update to endTime
        self.endVehicle         =     -1                        # will write its properties when it exits
        self.timeCharging       =     -1
        self.currentCharge      =      vehicle.currentCharge

        # keep tabs of the number of vehicles that have entered the model
        ChargeEvent.numEvents += 1

    # when the vehicle is done charging, we'll gather its stats
    def terminateCharge( self, vehicle, currentTime ):
        self.endTime        =   currentTime
        self.endVehicle     =   vehicle
        self.timeCharging   =   currentTime - self.startTime

    # probably useful to have
    def toString( self ):

        body = ''

        # ID
        #body += 'ID: ' , self.id , ' '
        
        # Start time
        body += 'Start time ' + str(self.startTime)+"  "

        # End time ( will be -1 if there's an issue )
        body += 'End time: ' + str(self.endTime)+"  "
        # Initial Charge
        body += 'Initial charge: ' + str(self.currentCharge)+"  "

        # Time charging ( will be -1 if there's an issue )
        body += 'Time charging: ' + str(self.timeCharging)+"  "

        # Charge Needed
        body += 'Charge needed: ' + str(self.initialVehicle.chargeNeeded)+"  "

        # Initial Vehicle ID
        #body += 'Vehicle ID: '+ str(self.initialVehicle.id)

        # check if it exists to avoid an error
        if self.endVehicle != -1:

            # End Vehicle ID ( parity check )
            body += 'End Vehicle ID: ' + str(self.endVehicle.id)

            # Final Charge
            body += 'Final charge: '+str(self.endVehicle.currentCharge)

        else:
            body += 'Unable to locate end vehicle'
            
        return body