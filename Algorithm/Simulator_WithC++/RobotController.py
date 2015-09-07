import copy
import time
import subprocess

__author__ = 'ECAND_000'

class RobotController:
    def __init__(self, completeMap, robot, algorithm, wifiComm, ui):
        # Needed for sensor reading
        self.completeMap = completeMap

        # Other objects needed for reading and sending data and determining the next action
        self.robot = robot
        self.algorithm = algorithm
        self.wifiComm = wifiComm
        self.ui = ui

    def explore(self):
        start = time.time()

        # Probably before going into the loop, tell the robot to do self adjustment
        while True:
            # Data sent --> (x, y, orientation, mapKnowledge)
            actions = subprocess.Popen(["algorithm", str(self.robot.x), str(self.robot.y), str(self.robot.orientation.value), self.robot.mapKnowledge.translate()], stdout=subprocess.PIPE).communicate()[0]

            # actions --> String from CPP
            # Format:
            # 'F', 'L', 'R'
            for action in actions:
                # Read sensors reading from Arduino
                sensorReading = self.wifiComm.read()
                for reading in sensorReading:
                    # DO SOMETHING WITH THE READING
                    # WHAT TO DO DEPENDS ON HOW THE READING IS COMMUNICATED
                    # UPDATE THE ROBOT'S MAP KNOWLEDGE USING THOSE READINGS
                    # UPDATE THE UI USING THOSE READINGS
                    pass

                r = self.robot.do(action)
                if r == False:
                    break

                # Send the action to the Arduino --> since if there is a break, that action is then not transferred
                # Basically each action is tested using the simulator's robot first and the actual robot sensor readings
                self.wifiComm.write(r)
                self.ui.drawRobot()

        end = time.time()
        print("RUNNING TIME:", end - start)
        print("Robot exploration done!")
        print("Going back to start zone...")

        # RUN FASTEST PATH ALGORITHM HERE TO GO BACK TO (1,1) --> ROBOT'S CENTRAL POSITION


        # PROBABLY USE A BLOCKING WI-FI READING SINCE THERE IS NO POINT IN CONTINUING THE WHILE LOOP IF THERE IS NO INCOMING DATA!!
        #
        # while self.robot.wifiComm.read() != "S":
        #   time.sleep(0.1)
        #
        # while True:
        #   Use ALGORITHM to determine the next move (probably the ALGORITHM will return a bunch of moves) --> at this point in time, assume that there is NO OBSTACLE at all
        #   For each move:
        #       Read sensors (using the robot's readSensors() method) --> inside here, there should be a MAP UPDATE (based on the sensor reading, like the simulation right now)
        #       Update the ROBOT GRIDMAP
        #       Do the move!! (send to Arduino + simulator) --> at this point
        #           --> there should be a logic which check whether it is possible to do THIS MOVE before sending message!! --> probably the logic can be put inside the self.robot --> inside the moveForward() method, return FALSE if not possible
        #           --> if not, BREAK, then go to the next loop of the WHILE LOOP (search for bunch of moves based on the sensor readings just now)
        #
        #       Remove the move!! (by list.pop(0))


    def fastestPathRun(self):
        print("Running fastest path algorithm...")

        # Probably before going into the loop, tell the robot to do self adjustment
        # The algorithm runs once and only once
        # The algorithm must return a bunch of actions from the Start zone to the End Zone all at once
        return