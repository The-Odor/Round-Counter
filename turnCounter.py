print("""Turn counter for spells and effects!
Usage: Input two arguments; name of effects and turns to last.
       If you put in nothing, a turn advances and counters count
Example: Greater Flaming Sphere: 7
(input argument is split at ':' )""")

# Uses one dicitionary to keep track of effects and another dictionary
# to enable tracking of duplicate effects (and enumerates them as such)

currentEffects = {}
effectCounts = {}
roundCounter = 0
while True:
    roundCounter += 1

    # Inerprets input and puts info into both dictionaries
    cmd = input("\n\n\nTurn {}; What happens? ".format(roundCounter)).split(":")
    while len(cmd) > 1:
        inName, inRounds = cmd[0], cmd[-1]
        if inName in effectCounts:
            if inName in currentEffects:
                currentEffects[inName + "1"] = currentEffects[inName]
                del currentEffects[inName]
            effectCounts[inName] += 1
            currentEffects[inName + str(effectCounts[inName])] = int(inRounds)

        else:
            currentEffects[inName] = int(inRounds)
            effectCounts[inName] = 1

        cmd = input("Anything else? ").split(":")

    killList = []

    # Counts the turns left and prints information to user
    for effectName in currentEffects:
        currentEffects[effectName] -= 1
        if currentEffects[effectName] == 0:
            killList.append(effectName)
            print("  {} is running out!!!".format(effectName))
        else:
            print("{} has {} rounds left".format(effectName, currentEffects[effectName]))

    # KILLS THE UNWANTED. fr tho removes finished sequenses from dictionaries
    for effectName in killList:
        del currentEffects[effectName]
        trueEffect = "".join(i for i in effectName if not i.isdigit())
        effectCounts[trueEffect] -= 1
        if effectCounts[trueEffect] == 0:
            del effectCounts[trueEffect]
