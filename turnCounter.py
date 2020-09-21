class TurnCounter():
    currentEffects = {}
    effectCounts = {}
    roundCounter = 1
    killList = []

    def pprint(self):
        if len(self.currentEffects) == 0:
            print("No effect to count")
            return
         # Counts the turns left and prints information to user
        for effectName in self.currentEffects:
            if self.currentEffects[effectName] == 1:
                print("Last round of {}".format(effectName))
            else:
                print("{} has {} rounds left".format(effectName, self.currentEffects[effectName]))

    def next_turn(self):
        self.roundCounter += 1
        for effectName in self.currentEffects:
            self.currentEffects[effectName] -= 1
            if(self.currentEffects[effectName] == 0):
                self.killList.append(effectName)

    def run(self):
        run = True
        while run:
            # Interprets input and puts info into both dictionaries
            cmd = input("\n\n\nTurn {}; What happens? ".format(self.roundCounter)).split(":")
            while len(cmd) > 1:
                inName, inRounds = cmd[0], cmd[-1]
                if inName in self.effectCounts:
                    self.currentEffects[inName + "1"] = self.currentEffects[inName]
                    del self.currentEffects[inName]
                    self.effectCounts[inName] += 1
                    self.currentEffects[inName + str(self.effectCounts[inName])] = int(inRounds)
                else:
                    self.currentEffects[inName] = int(inRounds)
                    self.effectCounts[inName] = 1

                cmd = input("Anything else? ").split(":")
            if(cmd[0].lower() == 'q'):
                run = False
                
            self.pprint()
            self.next_turn()
                # KILLS THE UNWANTED. fr tho removes finished sequences from dictionaries
            for effectName in self.killList:
                del self.currentEffects[effectName]
                trueEffect = "".join(i for i in effectName if not i.isdigit())
                self.effectCounts[trueEffect] -= 1
                if self.effectCounts[trueEffect] == 0:
                    del self.effectCounts[trueEffect]
            self.killList.clear()

if __name__ == "__main__":
    tc = TurnCounter()
    print("""Turn counter for spells and effects!
    Usage: Input two arguments; name of effects and turns to last.
           If you put in nothing, a turn advances and counters count
    Example: Greater Flaming Sphere: 7
    (input argument is split at ':' )""")

    tc.run()
