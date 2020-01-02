import random
import electric_vehicle
import update_vars
# ----------- Globals & Constants -------------

# --- poissonStuff ---
avgArrivalRate = 10.0 # cars per minute

# sets the arrival rate to a specificed value. Used for mass simulation
def setArrivalRate( newArrivalRate ):
    global avgArrivalRate
    avgArrivalRate = newArrivalRate

# --- charging stuff ---
# chargeRateMu
# chargeRateSigma

# chargeNeeded - the charge needed at the end 
chargeNeededMu = .9 #kwh in $
chargeNeededSigma = .1 #kwh in %

currentChargeMu = .4 #kwh in %
currentChargeSigma = .15 #kwh in %

uniformMaxCapacity = 100 #kwh
uniformChargeRate = 20 #kw

# just some values of common cars.. Volt: 16, Leaf: 24, Model S: 60 in kw
# more of some vs others to reprsent realistic distribution
batteryCapacities = [ 16, 16, 16, 16, 24, 24, 24, 24, 24, 16, 16, 16, 16, 16, 16, 24, 60 ]

# ------------ Poisson Generator ------------

# the main function for generating an interval on which to run an algorithmn
# will create a 2-level array, the top level being the length of the interval
# level 2 contains an array of the vehicle objects that will arrive during that minute

def vehicleGen( arrayOfArrivalsPerMin ):
    vehicles = []

    for minute, arrivalesDuringMin in enumerate( arrayOfArrivalsPerMin ):
        if arrivalesDuringMin != 0 :
            vehiclesDuringMin = []

            for i in range( 0, arrivalesDuringMin ):
                depart = minute + random.randint( 60 , 180 )
                batteryCapacity = random.choice( batteryCapacities )
                chargeNeeded = random.gauss( ( chargeNeededMu * batteryCapacity ) , ( chargeNeededSigma * batteryCapacity ) )
                currentCharge = random.gauss( ( currentChargeMu * batteryCapacity ) , ( currentChargeSigma * batteryCapacity ) )
                chargeRate = uniformChargeRate
                vehiclesDuringMin.append(electric_vehicle.EV( minute, depart, chargeNeeded, currentCharge, chargeRate, batteryCapacity ) )
            
            vehicles.append( vehiclesDuringMin )

        else:
            vehicles.append( [] )

    return vehicles
    #small test

################
def simulateInterval():

    arrivalTimes = []
    prevArrival = 0

    while True:
        nextArrival = vehicleArrives( prevArrival ) # prev had math.floor here
        if nextArrival >= update_vars.interval:
            break
        arrivalTimes.append( nextArrival )
        prevArrival = nextArrival

    arrivalsPerMin = [ 0 ] * update_vars.interval

    for arrivalTime in arrivalTimes:
        arrivalsPerMin[ int( arrivalTime ) ] += 1
    
    # print "total number of vehicles:  " , len( arrivalTimes )

    update_vars.numberOfVehiclesInSimulation = len( arrivalTimes )
    
    vehicles = vehicleGen( arrivalsPerMin )
    return vehicles

def vehicleArrives( prevArrival ):
    return prevArrival + random.expovariate( avgArrivalRate )